# ROT cloud function

This is a simplified Flask app ment to run in GCP as a cloud function. It takes `POST` request and transfers the message with ROT defined in the payload.

## Example POST request payload

```json
{
    "message": "This is a sample text",
    "rot": 13
}
```

## Local testing

1. Start Flask test server

```bash
python run.py rot.src.main
```

2. Send POST request with requests library

```python
import requests

url = 'http://localhost:5000/'
body = {'message': 'This is a sample text', 'rot': 13}
requests.post(url, json=body).json()
```

3. Result

```python
{'data': 'Guvf vf n fnzcyr grkg'}
```

## GCP Cloud Function deployment

Install `gcloud`, authenticate to GCP and deploy cloud function to GCP cloud with the `gcloud` cmd tool.

### Example

`gcloud functions deploy rot --entry-point main --runtime python37 --trigger-http --project <GCP Project ID> --region europe-west1`

### Official documentation

<https://cloud.google.com/functions/docs/deploying/filesystem>