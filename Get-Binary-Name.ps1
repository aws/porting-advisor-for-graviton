<#
.Synopsis
Get the name for the binary to generate.
#>
$ProcessorSuffix = (Get-CimInstance Win32_OperatingSystem).OSArchitecture | Select-Object -first 1
if ($ProcessorSuffix = '64-bit') {
    $ProcessorSuffix = 'x64'
} else {
    $ProcessorSuffix = 'other'
}
Write-Output "porting-advisor-win-$ProcessorSuffix"