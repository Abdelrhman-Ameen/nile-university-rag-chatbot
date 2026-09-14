$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$projectPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $projectPython)) {
    throw 'Run .\setup.ps1 first.'
}
$settings = (& $projectPython -c "import json; from nu_chat.config import OLLAMA_MODEL,OLLAMA_URL; print(json.dumps({'model':OLLAMA_MODEL,'url':OLLAMA_URL}))") | ConvertFrom-Json
New-Item -ItemType Directory -Force -Path '.runtime' | Out-Null
$ollamaReady = $false
try { $null = Invoke-RestMethod -Uri "$($settings.url)/api/tags" -TimeoutSec 3; $ollamaReady = $true } catch {}
if (-not $ollamaReady) {
    if ($settings.url -notin @('http://127.0.0.1:11434', 'http://localhost:11434')) {
        throw "Start the configured Ollama server at $($settings.url)."
    }
    $portableOllama = Join-Path $PSScriptRoot '.runtime\ollama\ollama.exe'
    if (Test-Path -LiteralPath $portableOllama) {
        $ollamaExecutable = $portableOllama
        $env:OLLAMA_MODELS = Join-Path $PSScriptRoot '.runtime\models'
    } else {
        $installedOllama = Get-Command ollama -ErrorAction SilentlyContinue
        if (-not $installedOllama) { throw 'Install Ollama from https://ollama.com/download/windows, then run this script again.' }
        $ollamaExecutable = $installedOllama.Source
    }
    $env:OLLAMA_HOST = '127.0.0.1:11434'
    $env:OLLAMA_NO_CLOUD = '1'
    Start-Process -FilePath $ollamaExecutable -ArgumentList 'serve' -WindowStyle Hidden -RedirectStandardOutput '.runtime\ollama.out.log' -RedirectStandardError '.runtime\ollama.err.log'
    for ($attempt = 0; $attempt -lt 20; $attempt++) {
        try { $null = Invoke-RestMethod -Uri "$($settings.url)/api/tags" -TimeoutSec 2; $ollamaReady = $true; break } catch { Start-Sleep -Seconds 1 }
    }
    if (-not $ollamaReady) { throw 'Ollama did not start. Check .runtime\ollama.err.log.' }
}
$models = Invoke-RestMethod -Uri "$($settings.url)/api/tags" -TimeoutSec 5
if ($settings.model -notin $models.models.name) {
    Write-Host "Downloading $($settings.model). This happens once."
    $body = @{model=$settings.model; stream=$false} | ConvertTo-Json
    $result = Invoke-RestMethod -Method Post -Uri "$($settings.url)/api/pull" -ContentType 'application/json' -Body $body -TimeoutSec 3600
    if ($result.status -ne 'success') { throw 'Model download failed. Try running the script again.' }
}
Write-Host "Loading $($settings.model)..."
$warmupBody = @{model=$settings.model; stream=$false; keep_alive='30m'; options=@{num_ctx=8192}} | ConvertTo-Json -Depth 3
$null = Invoke-RestMethod -Method Post -Uri "$($settings.url)/api/generate" -ContentType 'application/json' -Body $warmupBody -TimeoutSec 180
Write-Host 'Open http://127.0.0.1:8000'
& $projectPython -X utf8 -m nu_chat serve
if ($LASTEXITCODE -ne 0) { throw 'The chat server exited with an error.' }
