<#
.Synopsis
Converts the porting-advisor python module into a Windows executable.
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

$Filename = .\Get-Binary-Name.ps1
Write-Host "*** Will use $Filename as name ***"

if (!(Test-Path -Path .venv)) {
    Write-Host "Creating Python virtual environment"
    python -m venv .venv
    if($LASTEXITCODE -ne 0) {
        throw "**ERROR**: could not create Python Virtual Environment."
    }
}

Write-Host "Making sure Python Virtual Environment is active"
.\.venv\Scripts\Activate.ps1
if($LASTEXITCODE -ne 0) {
    throw "**ERROR**: could not activate Python Virtual Environment."
}

Write-Host "Installing requirements"
pip install -r requirements-build.txt
if($LASTEXITCODE -ne 0) {
    throw "**ERROR**: error installing required packages"
}

try {
    mvn package --file .\src\advisor\tools\graviton-ready-java\pom.xml
} catch {
    Write-Host "Could not find Maven. Skipping jar generation for Graviton Ready Java tool."
}

Write-Host "Generating executable"
pyinstaller --clean porting-advisor-win-x64.spec --noconfirm
if($LASTEXITCODE -ne 0) {
    throw "**ERROR**: pyinstaller failed, binary was not created"
}

Remove-Item .\dist\$Filename\pyinstaller-5.0.1.dist-info -Recurse
Write-Output "*** Success: Executable saved at dist\$Filename ***"