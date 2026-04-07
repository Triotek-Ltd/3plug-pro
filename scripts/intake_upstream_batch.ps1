param(
    [Parameter(Mandatory = $true)]
    [string]$ConfigPath,

    [Parameter(Mandatory = $false)]
    [string]$Org = "Triotek-Ltd",

    [Parameter(Mandatory = $false)]
    [string]$LocalBase = "C:\Users\Administrator\isaac\erp\rnd\3plug-pro-root\3plug\repos",

    [Parameter(Mandatory = $false)]
    [switch]$ForcePush
)

$ErrorActionPreference = "Stop"

function Add-SafeDirectory {
    param(
        [Parameter(Mandatory = $true)]
        [string]$PathValue
    )

    if (-not (Test-Path $PathValue)) {
        return
    }

    $resolved = (Resolve-Path $PathValue).Path -replace "\\", "/"
    git config --global --add safe.directory $resolved | Out-Null
    git config --global --add safe.directory $PathValue | Out-Null
}

function Test-GitHubRepoExists {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepoName
    )

    $command = "gh api repos/$RepoName 1>nul 2>nul"
    cmd /c $command | Out-Null
    return ($LASTEXITCODE -eq 0)
}

if (-not (Test-Path $ConfigPath)) {
    throw "Config path does not exist: $ConfigPath"
}

if (-not (Test-Path $LocalBase)) {
    New-Item -ItemType Directory -Path $LocalBase | Out-Null
}

$validGroups = @("platform", "apps-core", "apps-vertical", "stacks", "docs")
$entries = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$scriptPath = Join-Path $PSScriptRoot "intake_upstream_repo.ps1"

foreach ($entry in $entries) {
    $repoName = $entry.name
    $upstreamUrl = $entry.upstream_url
    $branchCandidates = @($entry.branch_candidates)
    $repoGroup = $entry.repo_group
    if (-not $repoGroup) {
        $repoGroup = "apps-core"
    }
    if ($repoGroup -notin $validGroups) {
        throw "Invalid repo group '$repoGroup' for $repoName"
    }

    $groupPath = Join-Path $LocalBase $repoGroup
    if (-not (Test-Path $groupPath)) {
        New-Item -ItemType Directory -Path $groupPath | Out-Null
    }

    $localPath = Join-Path $groupPath $repoName
    $orgRepo = "$Org/$repoName"
    $orgRemoteUrl = "https://github.com/$orgRepo.git"

    Write-Output ""
    Write-Output "=== $repoName ==="

    if (-not (Test-GitHubRepoExists -RepoName $orgRepo)) {
        Write-Output "Creating private repo $orgRepo"
        gh repo create $orgRepo --private --disable-issues --disable-wiki | Out-Host
        if ($LASTEXITCODE -ne 0) {
            throw "Failed creating GitHub repo: $orgRepo"
        }
    }

    $intakeParams = @{
        RepoPath = $localPath
        OrgRemoteUrl = $orgRemoteUrl
        UpstreamUrl = $upstreamUrl
        BranchCandidates = $branchCandidates
    }

    if ($ForcePush) {
        $intakeParams["ForcePush"] = $true
    }

    & $scriptPath @intakeParams

    Add-SafeDirectory -PathValue $localPath

    gh repo edit $orgRepo --default-branch main | Out-Host
    if ($LASTEXITCODE -ne 0) {
        throw "Failed setting default branch for $orgRepo"
    }

    Write-Output "Working tree: $localPath"
}

Write-Output ""
Write-Output "Batch intake complete."
