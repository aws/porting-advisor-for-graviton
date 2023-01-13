<#
.Synopsis
Run unit tests for project.
#>
Write-Host "*** running unit tests ***"
$Err = coverage run --source=./src -m unittest discover -s unittest -p "test_*.py" -v
if ($null -ne $Err) {
    Write-Error "Unit tests failed"
}
