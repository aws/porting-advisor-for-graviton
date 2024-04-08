function Test-Line {
    param([string]$ReportType, [string]$Result, [string]$Pattern)

    if(-Not ($Result | Select-String -Quiet -Pattern $Pattern))
    {
        throw "**FAILED**: $ReportType report is missing: $Pattern"
    }
    else
    {
        Write-Host "**PASS** $ReportType report has: $Pattern"
    }
}

function Test-Report {
    param([string]$ReportType, [string]$Result, [string[]]$Patterns)

    ForEach($Pattern in $Patterns)
    {
        Test-Line $ReportType $Result $Pattern
    }
}

$Filename = .\Get-Binary-Name.ps1

$Lines_To_Find = @(
    "detected java code. we recommend using Corretto"
    "detected python code. min version 3.7.5 is required"
    "detected python code. if you need pip, version 19.3 or above is recommended"
    "dependency library numpy is present. min version 1.19.0 is required"
    "detected java code. min version 8 is required. version 11 or above is recommended"
    "using dependency library snappy-java version 1.1.3. upgrade to at least version 1.1.4"
    "using dependency library hadoop-lzo. this library requires a manual build"
    "dependency library: leveldbjni-all is not supported on Graviton"
    "detected go code. min version 1.16 is required. version 1.18 or above is recommended"
    "using dependency library github.com/golang/snappy version 0.0.1. upgrade to at least version 0.0.2"
)

Write-Host "Running samples to console"
$ResultConsole = Invoke-Expression ".\dist\$Filename\$Filename.exe .\sample-projects"
Test-Report "Console" $ResultConsole $Lines_To_Find

Write-Host "Running samples to HTML report"
Invoke-Expression ".\dist\$Filename\$Filename.exe .\sample-projects --output test.html"
$ResultHtml = Get-Content -Path test.html
Test-Report "HTML" $ResultHtml $Lines_To_Find
Remove-Item -Path test.html

Write-Host "Running samples to Dependency Report"
$Dependencies = @(
    "<si><t>component</t></si><si><t>version</t></si><si><t>origin</t></si><si><t>filename</t></si>"
    "<si><t>junit</t></si><si><t>4.8.2</t></si>"
    "<si><t>zstd-jni</t></si><si><t>1.1.0</t></si>"
    "<si><t>snappy-java</t></si><si><t>1.1.3</t></si>"
    "<si><t>lz4-java</t></si><si><t>1.4.0</t></si>"
    "<si><t>hadoop-lzo</t></si><si><t>0.4.17</t></si>"
    "<si><t>leveldbjni-all</t></si><si><t>1.8</t></si>"
    "<si><t>CommandLineParser</t></si><si><t>2.8.0</t></si>"
    "<si><t>Microsoft.Build.Utilities.Core</t></si><si><t>17.1.0</t></si>"
    "<si><t>Microsoft.Extensions.Logging.Console</t></si><si><t>6.0.0</t></si>"
    "<si><t>Microsoft.NET.Test.Sdk</t></si><si><t>16.5.0</t></si>"
    "<si><t>Microsoft.VisualStudio.Setup.Configuration.Interop</t></si><si><t>3.1.2196</t></si>"
    "<si><t>System.Linq.Async</t></si><si><t>6.0.1</t></si>"
    "<si><t>xunit</t></si><si><t>2.4.1</t></si>"
    "<si><t>coverlet.collector</t></si><si><t>1.2.0</t></si>"
    "<si><t>SciPy</t></si>"
    "<si><t>NumPy</t></si>"
    "<si><t>cors</t></si><si><t>2.8.5</t></si>"
    "<si><t>express</t></si><si><t>4.18.1</t></si>"
    "<si><t>rxjs</t></si><si><t>7.5.6</t></si>"
    "<si><t>socket.io</t></si><si><t>4.5.1</t></si>"
    "<si><t>@codechecks/client</t></si><si><t>0.1.12</t></si>"
    "<si><t>@commitlint/cli</t></si><si><t>17.0.3</t></si>"
    "<si><t>eslint</t></si><si><t>7.32.0</t></si>"
    "<si><t>typescript</t></si><si><t>4.7.4</t></si>"
    "<si><t>github.com/aws/aws-sdk-go</t></si>"
    "<si><t>github.com/golang/snappy</t></si>"
    "<si><t>rails</t></si><si><t>6.1.6.1</t></si>"
    "<si><t>rake</t></si><si><t>11.1</t></si>"
    "<si><t>actionpack</t></si>"
    "<si><t>bcrypt</t></si><si><t>3.1</t></si>"
    "<si><t>cucumber</t></si><si><t>4.1</t></si>"
    "<si><t>gc_tracer</t></si>"
    "<si><t>gssapi</t></si>"
    "<si><t>mail</t></si>"
    "<si><t>turbo-rails</t></si>"
    "<si><t>httpclient</t></si>"
    "<si><t>jruby-openssl</t></si>"
)
Invoke-Expression ".\dist\$Filename\$Filename.exe .\sample-projects --output test.xlsx --output-format dependencies"
# xlsx files are compressed files, so we need to unzip them and then compare them
Expand-Archive test.xlsx -DestinationPath temp
$ResultXlsx = Get-Content ".\temp\xl\sharedStrings.xml"
Test-Report "Dependencies" $ResultXlsx $Dependencies
Remove-Item -Path test.xlsx
Remove-Item -LiteralPath ".\temp" -Force -Recurse


Write-Host "--- Running negative tests ---"

Write-Host "Running missing arguments test"
$MissingArgumentError = $( $Result = & Invoke-Expression ".\dist\$Filename\$Filename.exe" ) 2>&1
if(-Not ($MissingArgumentError | Select-String -Quiet -Pattern "porting-advisor: error: the following arguments are required: DIRECTORY"))
{
    throw "**FAILED**: missing arguments test"
}
else
{
    Write-Host "**PASSED** missing arguments test"
}


Write-Host "Running directory not found test"
$DirectoryNotFoundError = $( $Result = & Invoke-Expression ".\dist\$Filename\$Filename.exe unexisting_directory" ) 2>&1
if(-Not ($DirectoryNotFoundError | Select-String -Quiet -Pattern "unexisting_directory: directory not found."))
{
    throw "**FAILED**: directory not found test"
}
else
{
    Write-Host "**PASSED** directory not found test"
}

exit 0