<#
.Synopsis
Run unit tests for project.
#>
Write-Host "*** running unit tests ***"
$Err = python -m unittest discover -s unittest -p "test_*.py" -v
if ($null -ne $Err) {
    Write-Error "Unit tests failed"
}
