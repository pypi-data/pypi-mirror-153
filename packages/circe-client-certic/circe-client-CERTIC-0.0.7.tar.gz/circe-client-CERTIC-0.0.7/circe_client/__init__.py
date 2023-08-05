#!/usr/bin/env python
try:
    import sys
    import json
    import requests
    import tempfile
    import tarfile
    import os
    from typing import List, Union, Iterator, Tuple, BinaryIO
    from time import time, sleep
    from shutil import copyfileobj
    import hmac
    import hashlib
except ModuleNotFoundError:
    sys.exit("Needed modules were not found. Please refer to the documentation.")

try:
    assert sys.version_info >= (3, 6)
except AssertionError:
    sys.exit("Please update your python (>= 3.6)")


def hmac_string(payload: str, secret_key: str) -> str:
    hmac_hash = hmac.new(key=secret_key.encode("utf-8"), digestmod=hashlib.sha256)
    hmac_hash.update(payload.encode("utf-8"))
    return hmac_hash.hexdigest()


def hmac_file(file_path: str, secret_key: str) -> str:
    with open(file_path, "rb") as f:
        hmac_hash = hmac.new(key=secret_key.encode("utf-8"), digestmod=hashlib.sha256)
        for chunk in iter(lambda: f.read(8192), b""):
            hmac_hash.update(chunk)
        return hmac_hash.hexdigest()


class JobResult:
    def __init__(self, result_archive_path: str):
        self._tar = tarfile.open(result_archive_path, "r:gz")

    @property
    def files(self) -> Iterator[Tuple[str, BinaryIO]]:
        for member in self._tar.getmembers():
            if member.isfile():
                yield member.name, self._tar.extractfile(member)

    @property
    def documents(self) -> Iterator[Tuple[str, BinaryIO]]:
        for file_name, file in self.files:
            if file_name not in ["out.log", "job.json"]:
                yield file_name, file

    @property
    def log(self) -> Iterator[dict]:
        for fn, fp in self.files:
            if fn == "out.log":
                line = fp.readline().decode("utf-8").strip()
                while line:
                    yield json.loads(line)
                    line = fp.readline().decode("utf-8").strip()

    def __del__(self):
        self._tar.close()


class Job:
    def __init__(self):
        self.uuid = None
        self.files = []
        self.transformations = []
        self.notify_hook = None
        self.result_file_path = None
        self._temp_archive_path = None

    def add_file(self, file_path: str, local_name: str = None) -> "Job":
        if not local_name:
            local_name = os.path.basename(file_path)
        self.files.append(
            (
                file_path,
                local_name,
            )
        )
        return self

    def add_transformation(self, transformation: str, options: dict = None) -> "Job":
        if options is None:
            options = {}
        self.transformations.append({"name": transformation, "options": options})
        return self

    def set_notify_hook(self, notify_hook: str) -> "Job":
        self.notify_hook = notify_hook
        return self

    def make_archive(self) -> str:
        _, temp_json_path = tempfile.mkstemp()
        with open(temp_json_path, "w") as f:
            json.dump(
                {
                    "transformations": self.transformations,
                    "notify_hook": self.notify_hook,
                },
                f,
                indent=4,
            )

        _, temp_zip_path = tempfile.mkstemp(suffix=".tar.gz")

        with tarfile.open(temp_zip_path, "w:gz") as tar:
            tar.add(temp_json_path, "job.json")
            for file_path, local_name in self.files:
                tar.add(file_path, local_name)
        try:
            os.remove(temp_json_path)
        except PermissionError:
            pass
        self._temp_archive_path = temp_zip_path
        return temp_zip_path

    @property
    def result(self) -> Union[JobResult, None]:
        if self.result_file_path:
            return JobResult(self.result_file_path)

    def __del__(self):
        if self.result_file_path and os.path.isfile(self.result_file_path):
            try:
                os.remove(self.result_file_path)
            except PermissionError:
                pass
        if self._temp_archive_path and os.path.isfile(self._temp_archive_path):
            try:
                os.remove(self._temp_archive_path)
            except PermissionError:
                pass


class ClientException(Exception):
    pass


class TimeoutException(ClientException):
    pass


class AccessDenied(ClientException):
    pass


class Client:
    """
    Client will use the following env vars by default:

    CIRCE_ENDPOINT: address of Circe server
    CIRCE_SECRET: secret key
    CIRCE_APP_UUID: id of current client app
    """

    def __init__(
        self,
        api_endpoint: str = None,
        secret_key: str = None,
        application_uuid: str = None,
        credentials_file_path: str = None,
    ):
        if credentials_file_path:
            with open(credentials_file_path, "r") as credentials_file:
                credentials: dict = json.load(credentials_file)
                self.endpoint = credentials.get("endpoint")
                self.secret_key = credentials.get("secret")
                self.application_uuid = credentials.get("uuid")
        else:
            self.endpoint = api_endpoint or os.getenv("CIRCE_ENDPOINT")
            self.secret_key = secret_key or os.getenv("CIRCE_SECRET")
            self.application_uuid = application_uuid or os.getenv("CIRCE_APP_UUID")
        if not self.endpoint or not self.secret_key or not self.application_uuid:
            raise ClientException("Missing parameters")

    @staticmethod
    def new_job() -> Job:
        return Job()

    def available_transformations(self) -> List[str]:
        r = requests.get("{}transformations/".format(self.endpoint))
        if r.status_code == 200:
            return r.json()

    def send(self, job: Job, wait: bool = False, destination_file: str = None):
        job_archive_path = job.make_archive()
        job_hash = hmac_file(job_archive_path, self.secret_key)
        with open(job_archive_path, "rb") as f:
            if wait:
                r = requests.post(
                    "{}job/?block=1".format(self.endpoint),
                    data=f,
                    stream=True,
                    headers={
                        "Authorization": "{} {}".format(self.application_uuid, job_hash)
                    },
                )
                if r.status_code == 200:
                    if not destination_file:
                        _, destination_file = tempfile.mkstemp(suffix=".tar.gz")
                    with open(destination_file, "wb") as dest_fp:
                        # r.raw not working with post requests, so no copyfileobj :(
                        dest_fp.write(r.content)
                        job.result_file_path = destination_file
                        return
                if r.status_code == 403:
                    raise AccessDenied()
            else:
                r = requests.post(
                    "{}job/".format(self.endpoint),
                    data=f,
                    headers={
                        "Authorization": "{} {}".format(self.application_uuid, job_hash)
                    },
                )
                if r.status_code == 200:
                    job.uuid = r.text
                elif r.status_code == 403:
                    raise AccessDenied()
                else:
                    raise ClientException(
                        "Unsupported server status: {}".format(r.status_code)
                    )

        os.remove(job_archive_path)

    def poll(
        self,
        job: Job,
        destination_file: str = None,
        timeout: int = 30,
        poll_interval: int = 1,
    ):
        if not job.uuid:
            self.send(job)
        then = time()
        while True:
            r = requests.get(
                "{}job/{}".format(self.endpoint, job.uuid),
                stream=True,
                headers={
                    "Authorization": "{} {}".format(
                        self.application_uuid, hmac_string(job.uuid, self.secret_key)
                    )
                },
            )
            if r.status_code == 200:  # work is done
                if not destination_file:
                    _, destination_file = tempfile.mkstemp(suffix=".tar.gz")
                with open(destination_file, "wb") as f:
                    copyfileobj(r.raw, f)
                    job.result_file_path = destination_file
                    return
            else:  # should probably test for 202 code here ?
                now = time()
                if int(now - then) > timeout:  # time's up
                    raise TimeoutException()
                else:
                    sleep(poll_interval)  # give more time to server


if __name__ == "__main__":
    try:
        import argh
    except ImportError:
        sys.exit("Argh module is needed.")

    def send_job(
        files: str,
        transformations: str,
        app_uid: str = None,
        app_secret: str = None,
        endpoint: str = None,
    ) -> str:
        files = files.split(",")
        transformations = transformations.split(",")
        client = Client(endpoint, app_secret, app_uid)
        job = client.new_job()
        for f_path in files:
            job.add_file(f_path)
        for trs in transformations:
            job.add_transformation(trs)
        client.send(job, wait=True)
        for log_entry in job.result.log:
            print(log_entry["message"])

    parser = argh.ArghParser()
    parser.add_commands([send_job])
    parser.dispatch()
