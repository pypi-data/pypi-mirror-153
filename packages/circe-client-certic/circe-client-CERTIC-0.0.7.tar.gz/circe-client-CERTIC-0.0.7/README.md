# Circe Python Client Library

This is a client library for the [Circe server](https://git.unicaen.fr/pdn-certic/circe).

## Requirements

The Circe Python client library has been tested with Python versions 3.6 and above.

## Quickstart

### Install

Within a virtual environment:

    pip install circe-client-CERTIC

### Configuration

You may provide the configuration as constructor arguments for the client class as well as 
environment variables:

- CIRCE_ENDPOINT: URL of Circe server
- CIRCE_SECRET: secret key provided by the server
- CIRCE_APP_UUID: id of current client app

### Basic usage

    from circe_client import Client
    
    client = Client(api_endpoint="http://localhost:8000/", secret_key="test", application_uuid="test")
    job = client.new_job()
    job.add_file("mydocument.docx")
    job.add_transformation("mytransformation_id")
    client.send(job, wait=True)
    for file_name, file_pointer in job.result.files:
        pass  # do something with result files
