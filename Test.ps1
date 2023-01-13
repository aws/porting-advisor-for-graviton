<#
.Synopsis
Builds project, runs unit tests, runs integration tests
#>

Write-Host "Building project"
.\Build.ps1
if($LASTEXITCODE -ne 0) {
    throw "**ERROR**: failed to build project"
}

Write-Host "Running unit tests"
.\Unit-Test.ps1
if($LASTEXITCODE -ne 0) {
    throw "*ERROR**: unit tests failed"
}

Write-Host "Running integration tests"
.\Integration-Test.ps1
if($LASTEXITCODE -ne 0) {
    throw "*ERROR**: integration tests failed"
}
