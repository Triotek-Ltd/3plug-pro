param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath,

    [Parameter(Mandatory = $true)]
    [string]$OrgRemoteUrl,

    [Parameter(Mandatory = $false)]
    [string]$UpstreamUrl,

    [Parameter(Mandatory = $false)]
    [string]$UpstreamBranch,

    [Parameter(Mandatory = $false)]
    [string[]]$BranchCandidates = @(
        "version-16-hotfix",
        "version-16",
        "main",
        "develop",
        "master"
    ),

    [Parameter(Mandatory = $false)]
    [switch]$ForcePush
)

$ErrorActionPreference = "Stop"

function Add-SafeDirectory {
    param(
        [Parameter(Mandatory = $true)]
        [string]$PathValue
    )

    $resolved = (Resolve-Path $PathValue).Path -replace "\\", "/"
    git config --global --add safe.directory $resolved | Out-Null
    git config --global --add safe.directory $PathValue | Out-Null
}

function Resolve-UpstreamBranch {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SourceUrl,

        [Parameter(Mandatory = $true)]
        [string[]]$Candidates
    )

    $heads = git ls-remote --heads $SourceUrl
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to inspect upstream heads for $SourceUrl"
    }

    foreach ($candidate in $Candidates) {
        if ($heads -match "refs/heads/$candidate$") {
            return $candidate
        }
    }

    throw "Could not resolve an upstream branch for $SourceUrl from candidates: $($Candidates -join ', ')"
}

if (-not (Test-Path $RepoPath)) {
    if (-not $UpstreamUrl) {
        throw "Repo path does not exist and no upstream URL was provided: $RepoPath"
    }

    $cloneBranch = $UpstreamBranch
    if (-not $cloneBranch) {
        $cloneBranch = Resolve-UpstreamBranch -SourceUrl $UpstreamUrl -Candidates $BranchCandidates
    }

    Write-Output "Cloning upstream branch $cloneBranch into $RepoPath"
    git clone --origin upstream --branch $cloneBranch --single-branch $UpstreamUrl $RepoPath | Out-Host
    if ($LASTEXITCODE -ne 0) {
        throw "Failed cloning $UpstreamUrl into $RepoPath"
    }
} elseif (-not (Test-Path (Join-Path $RepoPath ".git"))) {
    if (-not $UpstreamUrl) {
        throw "Repo path exists but is not a git repository and no upstream URL was provided: $RepoPath"
    }

    $existingItems = Get-ChildItem -Force $RepoPath
    $allowedItems = @("README.md")
    $unexpected = $existingItems | Where-Object { $_.Name -notin $allowedItems }
    if ($unexpected) {
        $names = ($unexpected | Select-Object -ExpandProperty Name) -join ", "
        throw "Repo path $RepoPath contains unexpected files for bootstrap: $names"
    }

    foreach ($item in $existingItems) {
        Remove-Item -LiteralPath $item.FullName -Force
    }

    $cloneBranch = $UpstreamBranch
    if (-not $cloneBranch) {
        $cloneBranch = Resolve-UpstreamBranch -SourceUrl $UpstreamUrl -Candidates $BranchCandidates
    }

    Write-Output "Bootstrapping existing folder $RepoPath from upstream branch $cloneBranch"
    git -C $RepoPath init | Out-Host
    git -C $RepoPath remote add upstream $UpstreamUrl
    git -C $RepoPath fetch upstream $cloneBranch | Out-Host
    git -C $RepoPath checkout -b $cloneBranch FETCH_HEAD | Out-Host
}

Add-SafeDirectory -PathValue $RepoPath

if (-not $UpstreamBranch) {
    if ($UpstreamUrl) {
        $UpstreamBranch = Resolve-UpstreamBranch -SourceUrl $UpstreamUrl -Candidates $BranchCandidates
    } else {
        $UpstreamBranch = "version-16-hotfix"
    }
}

Write-Output "Normalizing upstream-derived repo at $RepoPath using $UpstreamBranch"

if ($UpstreamUrl) {
    $hasUpstream = git -C $RepoPath remote
    if ($hasUpstream -notcontains "upstream") {
        git -C $RepoPath remote add upstream $UpstreamUrl
    } else {
        git -C $RepoPath remote set-url upstream $UpstreamUrl
    }

    git -C $RepoPath fetch upstream $UpstreamBranch | Out-Host
    if ($LASTEXITCODE -ne 0) {
        throw "Failed fetching upstream branch $UpstreamBranch from $UpstreamUrl"
    }
}

# Resolve the baseline ref from either a local branch or the fetched upstream-tracking ref.
$baselineRef = $UpstreamBranch
$localBranchRef = git -C $RepoPath for-each-ref --format='%(refname)' "refs/heads/$UpstreamBranch"
if (-not $localBranchRef) {
    $baselineRef = "upstream/$UpstreamBranch"
    $upstreamBranchRef = git -C $RepoPath for-each-ref --format='%(refname)' "refs/remotes/$baselineRef"
    if (-not $upstreamBranchRef) {
        throw "Could not resolve baseline ref for $UpstreamBranch in $RepoPath"
    }
}

$baselineCommit = (git -C $RepoPath rev-parse $baselineRef).Trim()
if (-not $baselineCommit) {
    throw "Could not resolve baseline commit for $baselineRef in $RepoPath"
}

# Create or refresh the two standard branches from the chosen upstream baseline.
$isBare = ((git -C $RepoPath rev-parse --is-bare-repository).Trim() -eq "true")
if ($isBare) {
    git -C $RepoPath update-ref refs/heads/upstream-v16 $baselineCommit | Out-Null
    git -C $RepoPath update-ref refs/heads/main $baselineCommit | Out-Null
    git -C $RepoPath symbolic-ref HEAD refs/heads/main | Out-Null
} else {
    $currentBranch = (git -C $RepoPath branch --show-current).Trim()
    if ($currentBranch -eq "main") {
        git -C $RepoPath checkout --detach $baselineCommit | Out-Host
    }

    git -C $RepoPath branch -f upstream-v16 $baselineCommit | Out-Host
    git -C $RepoPath branch -f main $baselineCommit | Out-Host
    git -C $RepoPath checkout main | Out-Host
}

# Set the Triotek org remote.
if ((git -C $RepoPath remote) -contains "origin") {
    git -C $RepoPath remote remove origin | Out-Null
}
git -C $RepoPath remote add origin $OrgRemoteUrl

Write-Output "Pushing clean branches: upstream-v16 and main"

if ($ForcePush) {
    git -C $RepoPath push --force origin upstream-v16 main | Out-Host
} else {
    git -C $RepoPath push origin upstream-v16 main | Out-Host
}

if ($LASTEXITCODE -ne 0) {
    throw "Failed pushing clean branches to $OrgRemoteUrl"
}

Write-Output "Done. Next steps:"
Write-Output "1. Set main as default branch in GitHub"
Write-Output "2. Open PRs from upstream-v16 to main when upstream changes are reviewed"
Write-Output "3. If cleaning an already-noisy repo, delete old remote branches separately after confirming main is correct"
