# Detect language cloud function

This is a simplified Flask app ment to run in GCP as a cloud function. It takes `POST` request and analyze and detects the language in `text` field with Google Translate API.

## Example POST request payload

```json
{
    "text": "This is a sample text"
}
```

## Local testing

This is a bit tricky to test locally since you need to enable the translate API in google GCP and authenticate it.

Read more: <https://cloud.google.com/translate/docs/quickstart-client-libraries>

```txt
Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the file path of the JSON file that contains your service account key. This variable only applies to your current shell session, so if you open a new session, set the variable again.
```

1. Install `google-cloud-translate` python library
   1. `pip install google-cloud-translate`
   2. Documentation: <https://googleapis.github.io/google-cloud-python/latest/translate/usage.html>
2. Enable Translate API in GCP
3. Authenticate to GCP by setting up the `GOOGLE_APPLICATION_CREDENTIALS` env var
4. Start Flask test server

```bash
python run.py detect_language.src.main
```

2. Send POST request with requests library

```python
import requests

url = 'http://localhost:5000/'
body = {'text': 'This is a sample text'}
requests.post(url, json=body).json()
```

3. Result

```python
{'confidence': 1, 'language': 'en'}
```

The confidence value is an optional floating point value between `0` and `1`. The closer this value is to `1`, the higher the confidence level for the language detection.

**NOTE**

Gibberish text is often detected as some obscure language. To get the best and most reliable results is to expect that the text that's been evaluated is in english with large sample set!

## GCP Cloud Function deployment

Install `gcloud`, authenticate to GCP and deploy cloud function to GCP cloud with the `gcloud` cmd tool.

### Example

`gcloud functions deploy detect-language --entry-point main --runtime python37 --trigger-http --project <GCP Project ID> --region europe-west1`

### Official documentation

<https://cloud.google.com/functions/docs/deploying/filesystem>