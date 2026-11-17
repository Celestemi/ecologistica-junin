param(
    [Parameter(Mandatory=$true)][string]$Phase,
    [string[]]$TestPaths = @(),
    [switch]$Frontend,
    [switch]$Coverage
)
$ErrorActionPreference = 'Stop'
$repoPath = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoPath
$containerName = 'ecologistica-post-audit-20261117'
$details = docker inspect $containerName | ConvertFrom-Json
$bindings = @($details.NetworkSettings.Ports.'5432/tcp')
if ($LASTEXITCODE -ne 0 -or $details.Config.Labels.'ecologistica.purpose' -ne 'post-audit-disposable' -or
    -not $details.State.Running -or $bindings.Count -ne 1 -or
    $bindings[0].HostIp -ne '127.0.0.1' -or $bindings[0].HostPort -ne '25436' -or
    $details.Mounts.Where({$_.Type -ne 'tmpfs'}).Count -gt 0 -or
    $details.HostConfig.Tmpfs.'/var/lib/postgresql/data' -ne 'rw') {
    throw 'Abortado: no se verifico PostGIS exclusivamente descartable y sin volumen persistente.'
}
$outputPath = Join-Path $repoPath "AUDITORIA/CORRECCIONES_EVIDENCIAS/$Phase"
$runtimePath = Join-Path $repoPath "AUDITORIA/CORRECCIONES_EVIDENCIAS/runtime/$Phase"
New-Item -ItemType Directory -Force -Path $outputPath,$runtimePath | Out-Null
$env:DATABASE_URL = 'postgresql+asyncpg://ecologistica:post-audit-disposable@127.0.0.1:25436/ecologistica_test'
$env:APP_ENVIRONMENT = 'demo'
$env:ALLOW_DEMO_ACCOUNTS = 'true'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:EN001_WRITE = '0'
$env:ECOLOGISTICA_TEST_DISPOSABLE = '1'
$env:SECRET_KEY = 'post-audit-only-disposable-signing-key-not-for-production'
$env:OSRM_BASE_URL = ''
$env:COVERAGE_FILE = Join-Path $runtimePath '.coverage'
# Native stderr may contain harmless test warnings; preserve it and use exit code.
$ErrorActionPreference = 'Continue'
if ($Frontend) {
    $frontArgs = @('node_modules/vitest/vitest.mjs','run','--reporter=default','--reporter=json',"--outputFile.json=$outputPath/frontend-results.json")
    if ($Coverage) { $frontArgs += @('--coverage.enabled=true',"--coverage.reportsDirectory=$runtimePath/frontend-coverage") }
    & node @frontArgs 2>&1 |
        Tee-Object -FilePath (Join-Path $outputPath 'frontend.log')
} else {
    $testArgs = @('-B','-m','pytest','-o','addopts=','-o','junit_family=xunit1','-o',"cache_dir=$runtimePath/cache",'-q','-ra','--tb=short',
        "--basetemp=$runtimePath/tmp", "--junitxml=$outputPath/backend-junit.xml")
    if ($Coverage) {
        $testArgs += @('--cov=app',"--cov-report=json:$outputPath/backend-coverage.json",'--cov-report=term','--cov-fail-under=80')
    }
    & ./.venv/Scripts/python.exe @testArgs @TestPaths 2>&1 | Tee-Object -FilePath (Join-Path $outputPath 'backend.log')
}
$testExit = $LASTEXITCODE
Write-Output "POST_AUDIT_EXIT=$testExit"
exit $testExit
