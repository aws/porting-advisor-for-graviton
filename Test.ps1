<#
.Synopsis
Builds project, runs unit tests, runs integration tests
#>

Write-Host "🐍 Setup virtual environment"
.\Setup-Environment.ps1
if($LASTEXITCODE -ne 0) {
    throw "*ERROR**: failed to initialize Python Virtual Environment"
}

Write-Host "🔬 Running unit tests"
.\Unit-Test.ps1
if($LASTEXITCODE -ne 0) {
    throw "*ERROR**: unit tests failed"
}

Write-Host "⚒️ Building project"
.\Build.ps1
if($LASTEXITCODE -ne 0) {
    throw "**ERROR**: failed to build project"
}

Write-Host "🧪 Running integration tests"
.\Integration-Test.ps1
if($LASTEXITCODE -ne 0) {
    throw "*ERROR**: integration tests failed"
}
