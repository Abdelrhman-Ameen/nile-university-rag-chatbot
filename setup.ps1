$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        uv venv --python 3.12 .venv
    } else {
        py -3.12 -m venv .venv
    }
    if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.12 and try again.' }
}
if (Get-Command uv -ErrorAction SilentlyContinue) {
    uv pip sync requirements.txt
} else {
    & '.venv\Scripts\python.exe' -m ensurepip
    & '.venv\Scripts\python.exe' -m pip install -r requirements.txt
}
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
& '.venv\Scripts\python.exe' -X utf8 -m nu_chat ingest
if ($LASTEXITCODE -ne 0) { throw 'Source ingestion failed. Check the output above.' }
Write-Host 'Ready. Run .\run.ps1 to start the chat.'
