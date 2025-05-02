$ErrorActionPreference = "Stop"

$requiredPythonVersion = [Version]"3.11"
$cliName = "a-toad-emo"
$pypiPackage = "a-toad-emo"

function Check-Python {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Python 3 is not installed." -ForegroundColor Red
        Write-Host "➡️  Please install it from https://www.python.org/downloads/"
        exit 1
    }

    $version = python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))"
    if ([Version]$version -lt $requiredPythonVersion) {
        Write-Host "❌ Python $requiredPythonVersion or higher is required (found: $version)" -ForegroundColor Red
        exit 1
    }

    Write-Host "✅ Python $version detected." -ForegroundColor Green
}

function Check-Pipx {
    if (-not (Get-Command pipx -ErrorAction SilentlyContinue)) {
        Write-Host "ℹ️ pipx not found. Installing pipx..." -ForegroundColor Yellow
        python -m pip install --user pipx
        python -m pipx ensurepath
        Write-Host "✅ pipx installed. You may need to restart your terminal." -ForegroundColor Green
    }
}

function Install-CLI {
    $pipxList = pipx list
    if ($pipxList -like "*${cliName}*") {
        Write-Host "🔄 Updating $cliName via pipx..." -ForegroundColor Cyan
        pipx upgrade $pypiPackage
    }
    else {
        Write-Host "⬇️ Installing $cliName via pipx..." -ForegroundColor Cyan
        pipx install $pypiPackage
    }

    Write-Host "🎉 Installation complete. Run with: $cliName --help" -ForegroundColor Green
}

# Execute install steps
Check-Python
Check-Pipx
Install-CLI