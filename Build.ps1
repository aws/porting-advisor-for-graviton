<#
.Synopsis
Converts the porting-advisor python module into a Windows executable.
#>

if (!(Test-Path -Path .venv)) {
    .\Setup-Environment.ps1
}

$Filename = .\Get-Binary-Name.ps1
Write-Host "*** Will use $Filename as name ***"

try {
    mvn package --file .\src\advisor\tools\graviton-ready-java\pom.xml
} catch {
    Write-Host "Could not find Maven. Skipping jar generation for Graviton Ready Java tool."
}

Write-Host "🏗️ Generating executable"
pyinstaller --clean porting-advisor-win-x64.spec --noconfirm
if($LASTEXITCODE -ne 0) {
    throw "**ERROR**: pyinstaller failed, binary was not created"
}

Write-Output "🎉 *** Success: Executable saved at dist\$Filename ***"
