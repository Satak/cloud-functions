param (
    [Parameter(Mandatory)]
    [string]$Project
)

$token = Get-Childitem env:TOKEN | Select-Object -ExpandProperty Value
if(!$token) {
    Write-Error "Token environment variable missing!"
} else {
    Write-Output "Deploying cloud function to GCP project: $Project"
    gcloud beta functions deploy snapshot --entry-point main --runtime python37 --trigger-http --project "$Project" --region europe-west1 --set-env-vars TOKEN="$token" --source ./src
}
