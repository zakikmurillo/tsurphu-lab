Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Section([string]$title) {
  Write-Host ""
  Write-Host "=== $title ==="
}

function Try-Run([string[]]$cmd, [string]$label) {
  Write-Host ">> $label"
  Write-Host ("   " + ($cmd -join " "))
  & $cmd[0] @($cmd[1..($cmd.Length-1)])
  if ($LASTEXITCODE -ne 0) {
    throw "Command failed ($LASTEXITCODE): $label"
  }
}

function Show-Path([string]$label, [string]$path) {
  if (Test-Path $path) {
    Write-Host ("{0}: {1}" -f $label, $path)
  } else {
    Write-Host ("{0}: MISSING ({1})" -f $label, $path)
  }
}

# Repo root = parent of tools/
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RepoRoot

Write-Section "TSURPHU DEV (one-command bootstrap + tests)"
Write-Host "Repo: $RepoRoot"

# Prefer py launcher if available
$pyCmd = Get-Command py -ErrorAction SilentlyContinue
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if (-not $pyCmd -and -not $pythonCmd) {
  throw "Neither 'py' nor 'python' found in PATH. Install Python, or enable the Windows Python Launcher."
}

# Choose interpreter (prefer 3.12 then 3.13, else fallback)
$Py = @()
if ($pyCmd) {
  foreach ($ver in @("3.12","3.13","3.11","3.10")) {
    try {
      & py "-$ver" -c "import sys; print(sys.version)" *> $null
      if ($LASTEXITCODE -eq 0) {
        $Py = @("py", "-$ver")
        break
      }
    } catch {}
  }
  if ($Py.Count -eq 0) { $Py = @("py") }
} else {
  $Py = @("python")
}

Write-Section "Python selected"
Try-Run @($Py + @("-c","import sys; print(sys.executable); print(sys.version)")) "Show python"

# Create venv
Write-Section "Create/Reuse venv (.venv)"
$VenvDir = Join-Path $RepoRoot ".venv"
$VenvPy  = Join-Path $VenvDir "Scripts\python.exe"

if (-not (Test-Path $VenvPy)) {
  Try-Run @($Py + @("-m","venv",".venv")) "Create venv"
} else {
  Write-Host ">> venv already exists: $VenvDir"
}

if (-not (Test-Path $VenvPy)) {
  throw "Venv python not found at: $VenvPy"
}

# Upgrade pip
Write-Section "Upgrade pip"
Try-Run @($VenvPy, "-m","pip","install","-U","pip","wheel","setuptools") "pip upgrade"

# Install project (try editable + dev extras; fallback to editable only; ensure pytest)
Write-Section "Install project"
$Installed = $false
try {
  Try-Run @($VenvPy, "-m","pip","install","-e",".[dev]") "pip install -e .[dev]"
  $Installed = $true
} catch {
  Write-Host "!! .[dev] extras not available (or failed). Falling back to -e ."
}

if (-not $Installed) {
  Try-Run @($VenvPy, "-m","pip","install","-e",".") "pip install -e ."
}

Try-Run @($VenvPy, "-m","pip","install","-U","pytest") "Ensure pytest"

# Run bootstrap
Write-Section "Bootstrap/Validate (auto-detect)"
if (-not (Test-Path ".\tools\tsurphu.py")) {
  throw "Missing CLI: tools/tsurphu.py"
}

$helpText = & $VenvPy ".\tools\tsurphu.py" "-h" 2>&1 | Out-String

$cmd = ""
if ($helpText -match '\bbootstrap\b') {
  $cmd = "bootstrap"
} elseif ($helpText -match '\bvalidate\b') {
  $cmd = "validate"
} else {
  throw "No known command found in tsurphu CLI help. Expected bootstrap or validate."
}

Try-Run @($VenvPy, ".\tools\tsurphu.py", $cmd) "tsurphu $cmd"

# Run tests
Write-Section "Tests (pytest -q)"
Try-Run @($VenvPy, "-m","pytest","-q") "pytest -q"

Write-Section "Key files"
Show-Path "Documento Maestro" (Join-Path $RepoRoot "docs\master.md")
Show-Path "ChangeSetPacket-1" (Join-Path $RepoRoot "docs\changesetpacket-1.md")
Show-Path "Object Ledger" (Join-Path $RepoRoot "docs\object-ledger.csv")

Write-Section "DONE ✅"
