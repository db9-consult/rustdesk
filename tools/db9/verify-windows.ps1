param([Parameter(Mandatory = $true)][string]$PackageDirectory)
$ErrorActionPreference = 'Stop'
$packageRoot = (Resolve-Path -LiteralPath $PackageDirectory).Path
$exe = Join-Path $packageRoot 'rustdesk-db9-1.5.0-x86_64.exe'
$msi = Join-Path $packageRoot 'rustdesk-db9-1.5.0-x86_64.msi'
foreach ($file in @($exe, $msi)) {
    if (-not (Test-Path -LiteralPath $file)) { throw "Missing package: $file" }
}
$report = @()
$renamed = Join-Path $packageRoot 'renamed-client.exe'
Copy-Item -LiteralPath $exe -Destination $renamed
try {
    $process = Start-Process -FilePath $renamed -ArgumentList '--version' -WindowStyle Hidden -PassThru -Wait -RedirectStandardOutput (Join-Path $packageRoot 'version.txt')
    if ($process.ExitCode -ne 0) { throw "Renamed EXE exited $($process.ExitCode)" }
    $version = (Get-Content -LiteralPath (Join-Path $packageRoot 'version.txt') -Raw).Trim()
    if ($version -notmatch '1\.5\.0') { throw "Unexpected EXE version: $version" }
    $report += 'PASS: renamed self-extracting EXE executes and reports version 1.5.0.'
} finally {
    Remove-Item -LiteralPath $renamed -Force
    Remove-Item -LiteralPath (Join-Path $packageRoot 'version.txt') -Force -ErrorAction SilentlyContinue
}
foreach ($operation in @('install', 'repair', 'uninstall')) {
    $args = switch ($operation) {
        'install' { @('/i', "`"$msi`"", '/qn', 'LAUNCH_TRAY_APP=N', 'REBOOT=ReallySuppress') }
        'repair' { @('/fa', "`"$msi`"", '/qn', 'LAUNCH_TRAY_APP=N', 'REBOOT=ReallySuppress') }
        'uninstall' { @('/x', "`"$msi`"", '/qn', 'REBOOT=ReallySuppress') }
    }
    $log = Join-Path $packageRoot "msi-$operation.log"
    $args += @('/l*v', "`"$log`"")
    $process = Start-Process -FilePath 'msiexec.exe' -ArgumentList $args -WindowStyle Hidden -PassThru -Wait
    if ($process.ExitCode -notin @(0, 3010)) { throw "MSI $operation failed: $($process.ExitCode); see $log" }
    $report += "PASS: MSI $operation (exit $($process.ExitCode))."
}
$report += 'NOT TESTED: interactive remote-control session and relay between two authorized devices.'
$report | Set-Content -LiteralPath (Join-Path $packageRoot 'db9-windows-validation.txt') -Encoding utf8
