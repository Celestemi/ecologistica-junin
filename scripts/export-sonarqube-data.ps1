[CmdletBinding()]
param(
    [string]$SonarUrl = "http://localhost:9001",
    [string]$OutputDirectory = ".sonarqube-temp"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Read-SonarProjectHint {
    $propertiesPath = Join-Path $script:ProjectRoot "sonar-project.properties"
    if (-not (Test-Path -LiteralPath $propertiesPath)) {
        return $null
    }

    $keyLine = Get-Content -LiteralPath $propertiesPath |
        Where-Object { $_ -match '^\s*sonar\.projectKey\s*=' } |
        Select-Object -First 1

    if ($null -eq $keyLine) {
        return $null
    }

    return (($keyLine -split '=', 2)[1]).Trim()
}

function ConvertTo-QueryString {
    param([hashtable]$Parameters)

    return (($Parameters.GetEnumerator() | ForEach-Object {
        $name = [Uri]::EscapeDataString([string]$_.Key)
        $value = [Uri]::EscapeDataString([string]$_.Value)
        "$name=$value"
    }) -join '&')
}

function Invoke-SonarApi {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [hashtable]$Parameters = @{}
    )

    $uri = "$script:BaseUrl/$($Path.TrimStart('/'))"
    if ($Parameters.Count -gt 0) {
        $uri = "$uri`?$(ConvertTo-QueryString -Parameters $Parameters)"
    }

    try {
        return Invoke-RestMethod -Method Get -Uri $uri -Headers $script:AuthHeaders
    }
    catch {
        $status = $null
        if ($_.Exception.Response) {
            $status = [int]$_.Exception.Response.StatusCode
        }
        $suffix = if ($null -ne $status) { " (HTTP $status)" } else { "" }
        throw "Falló la consulta a $Path$suffix. Verifica la URL, el token y sus permisos."
    }
}

function Get-AllPages {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$CollectionProperty,
        [hashtable]$Parameters = @{},
        [int]$PageSize = 500
    )

    $items = [System.Collections.Generic.List[object]]::new()
    $page = 1

    do {
        $pageParameters = @{}
        foreach ($entry in $Parameters.GetEnumerator()) {
            $pageParameters[$entry.Key] = $entry.Value
        }
        $pageParameters['p'] = $page
        $pageParameters['ps'] = $PageSize

        $response = Invoke-SonarApi -Path $Path -Parameters $pageParameters
        $pageItems = @($response.$CollectionProperty)
        foreach ($item in $pageItems) {
            $items.Add($item)
        }

        if ($null -ne $response.paging) {
            $total = [int]$response.paging.total
        }
        else {
            $total = $items.Count
        }
        $page++
    } while ($items.Count -lt $total -and $pageItems.Count -gt 0)

    return @($items)
}

function Remove-SensitiveProperties {
    param([AllowNull()]$Value)

    if ($null -eq $Value) { return $null }

    if ($Value -is [System.Collections.IDictionary]) {
        $clean = [ordered]@{}
        foreach ($key in $Value.Keys) {
            if ([string]$key -notmatch '(?i)token|authorization|credential|password|secret|header') {
                $clean[$key] = Remove-SensitiveProperties -Value $Value[$key]
            }
        }
        return $clean
    }

    if ($Value -is [System.Collections.IEnumerable] -and $Value -isnot [string]) {
        return @($Value | ForEach-Object { Remove-SensitiveProperties -Value $_ })
    }

    if ($Value -is [pscustomobject]) {
        $clean = [ordered]@{}
        foreach ($property in $Value.PSObject.Properties) {
            if ($property.Name -notmatch '(?i)token|authorization|credential|password|secret|header') {
                $clean[$property.Name] = Remove-SensitiveProperties -Value $property.Value
            }
        }
        return [pscustomobject]$clean
    }

    return $Value
}

function Write-SafeJson {
    param(
        [Parameter(Mandatory = $true)][string]$FileName,
        [Parameter(Mandatory = $true)]$Data
    )

    $path = Join-Path $script:OutputPath $FileName
    $safeData = Remove-SensitiveProperties -Value $Data
    $safeData | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $path -Encoding UTF8
    Write-Host "Generado: $path"
}

$script:ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$script:BaseUrl = $SonarUrl.TrimEnd('/')
$script:OutputPath = [IO.Path]::GetFullPath((Join-Path $script:ProjectRoot $OutputDirectory))

$tokenSecure = Read-Host "Token de SonarQube (no se mostrará ni se guardará)" -AsSecureString
$tokenPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($tokenSecure)
try {
    $tokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($tokenPointer)
    if ([string]::IsNullOrWhiteSpace($tokenPlain)) {
        throw "El token no puede estar vacío."
    }
    $basicValue = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${tokenPlain}:"))
    $script:AuthHeaders = @{ Authorization = "Basic $basicValue" }
}
finally {
    if ($tokenPointer -ne [IntPtr]::Zero) {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($tokenPointer)
    }
    $tokenPlain = $null
    $tokenSecure.Dispose()
}

try {
    $systemStatus = Invoke-SonarApi -Path 'api/system/status'
    $projectHint = Read-SonarProjectHint
    $projects = Get-AllPages -Path 'api/projects/search' -CollectionProperty 'components'

    $project = $null
    if ($projectHint) {
        $project = @($projects | Where-Object { $_.key -eq $projectHint }) | Select-Object -First 1
    }
    if ($null -eq $project -and $projects.Count -eq 1) {
        $project = $projects[0]
    }
    if ($null -eq $project) {
        $available = ($projects | ForEach-Object { "'$($_.key)' ($($_.name))" }) -join ', '
        throw "No se pudo identificar de forma inequívoca el proyecto analizado. Clave configurada: '$projectHint'. Proyectos visibles: $available"
    }

    New-Item -ItemType Directory -Path $script:OutputPath -Force | Out-Null

    $metricDefinitions = Get-AllPages -Path 'api/metrics/search' -CollectionProperty 'metrics'
    $metricKeys = @($metricDefinitions | ForEach-Object { $_.key } | Sort-Object -Unique)
    $componentMeasures = [System.Collections.Generic.List[object]]::new()
    $chunkSize = 40
    for ($offset = 0; $offset -lt $metricKeys.Count; $offset += $chunkSize) {
        $last = [Math]::Min($offset + $chunkSize - 1, $metricKeys.Count - 1)
        $chunk = $metricKeys[$offset..$last] -join ','
        $measureResponse = Invoke-SonarApi -Path 'api/measures/component' -Parameters @{
            component = $project.key
            metricKeys = $chunk
            additionalFields = 'metrics,periods'
        }
        foreach ($measure in @($measureResponse.component.measures)) {
            $componentMeasures.Add($measure)
        }
    }

    $qualityGate = Invoke-SonarApi -Path 'api/qualitygates/project_status' -Parameters @{
        projectKey = $project.key
    }
    $issues = Get-AllPages -Path 'api/issues/search' -CollectionProperty 'issues' -Parameters @{
        componentKeys = $project.key
        additionalFields = '_all'
    }
    $hotspots = Get-AllPages -Path 'api/hotspots/search' -CollectionProperty 'hotspots' -Parameters @{
        projectKey = $project.key
    }

    Write-SafeJson -FileName 'project.json' -Data ([ordered]@{
        exportedAt = (Get-Date).ToUniversalTime().ToString('o')
        sonarUrl = $script:BaseUrl
        serverStatus = $systemStatus.status
        configuredProjectKeyHint = $projectHint
        project = $project
    })
    Write-SafeJson -FileName 'metric-definitions.json' -Data ([ordered]@{
        total = $metricDefinitions.Count
        metrics = $metricDefinitions
    })
    Write-SafeJson -FileName 'measures.json' -Data ([ordered]@{
        projectKey = $project.key
        total = $componentMeasures.Count
        measures = @($componentMeasures)
    })
    Write-SafeJson -FileName 'quality-gate.json' -Data $qualityGate
    Write-SafeJson -FileName 'issues.json' -Data ([ordered]@{
        projectKey = $project.key
        total = $issues.Count
        issues = $issues
    })
    Write-SafeJson -FileName 'security-hotspots.json' -Data ([ordered]@{
        projectKey = $project.key
        total = $hotspots.Count
        hotspots = $hotspots
    })

    Write-Host ""
    Write-Host "Exportación completada para '$($project.key)' ($($project.name))."
    Write-Host "Los JSON no contienen el token ni cabeceras de autenticación."
}
finally {
    $script:AuthHeaders = $null
    $basicValue = $null
}
