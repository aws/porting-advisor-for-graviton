<#
.Synopsis
Sets up Python Virtual Environment.
#>

try {
    Get-Command python | ForEach-Object {
        $PYTHON_VERSION_MAJOR = [int]($_.FileVersionInfo.ProductVersion -split '\.')[0]
        $PYTHON_VERSION_MINOR = [int]($_.FileVersionInfo.ProductVersion -split '\.')[1]

        if ($PYTHON_VERSION_MAJOR -ge 3 -and $PYTHON_VERSION_MINOR -ge 10) {
            $PYTHON3 = $_.Name
        }
    }
    $p = & $PYTHON3 "--version"
} catch {
    throw '**ERROR**: python3.10+ is missing, please install it before running this build script'
}

try {
    $p = pip --version
} catch {
    throw '**ERROR**: pip is missing, please install it before running this build script'
}

if (!(Test-Path -Path .venv)) {
    Write-Host "💻 Creating Python virtual environment"
    & $PYTHON3 "-m" "venv" ".venv"
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

