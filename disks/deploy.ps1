$token = Get-Childitem env:TOKEN | Select-Object -ExpandProperty Value
$project = Get-Childitem env:GCP_PROJECT | Select-Object -ExpandProperty Value
$zones = Get-Childitem env:GCP_ZONES | Select-Object -ExpandProperty Value
gcloud beta functions deploy disks --entry-point main --runtime python37 --trigger-http --project "$project" --region europe-west1 --set-env-vars TOKEN=$token,GCP_ZONES=$zones --source ./src