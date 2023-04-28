<#
.Synopsis
Sets up Python Virtual Environment.
#>

try {
    $p = python --version
} catch {
    throw '**ERROR**: python is missing, please install it before running this build script'
}

try {
    $p = pip --version
} catch {
    throw '**ERROR**: pip is missing, please install it before running this build script'
}

if (!(Test-Path -Path .venv)) {
    Write-Host "💻 Creating Python virtual environment"
    python -m venv .venv
    if($LASTEXITCODE -ne 0) {
        throw "**ERROR**: could not create Python Virtual Environment."
    }
}

Write-Host "💡 Making sure Python Virtual Environment is active"
.\.venv\Scripts\Activate.ps1
if($LASTEXITCODE -ne 0) {
    throw "**ERROR**: could not activate Python Virtual Environment."
}

Write-Host "☁️ Installing requirements"
pip install -r requirements-build.txt
if($LASTEXITCODE -ne 0) {
    throw "**ERROR**: error installing required packages"
}