param([switch]$Gpu)

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
if ($Gpu) {
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        uv pip install --python '.venv\Scripts\python.exe' --no-deps 'torch==2.14.0+cu130' --index-url 'https://download.pytorch.org/whl/cu130'
    } else {
        & '.venv\Scripts\python.exe' -m pip install --no-deps 'torch==2.14.0+cu130' --index-url 'https://download.pytorch.org/whl/cu130'
    }
    if ($LASTEXITCODE -ne 0) { throw 'CUDA PyTorch installation failed.' }
    & '.venv\Scripts\python.exe' -c "import torch; assert torch.cuda.is_available(), 'CUDA GPU is unavailable'; print(torch.ones(1, device='cuda').sum().item())"
    if ($LASTEXITCODE -ne 0) { throw 'CUDA verification failed. Check the NVIDIA driver.' }
    $env:EMBEDDING_DEVICE = 'cuda'
}
& '.venv\Scripts\python.exe' -X utf8 -m nu_chat ingest
if ($LASTEXITCODE -ne 0) { throw 'Source ingestion failed. Check the output above.' }
Write-Host 'Ready. Run .\run.ps1 to start the chat.'
