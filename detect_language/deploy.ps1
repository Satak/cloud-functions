$token = Get-Childitem env:TOKEN | Select-Object -ExpandProperty Value
$project = Get-Childitem env:PROJECT | Select-Object -ExpandProperty Value
gcloud beta functions deploy detect-language --entry-point main --runtime python37 --trigger-http --project "$project" --region europe-west1 --set-env-vars TOKEN=$token --source ./src