$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "log-prompt-history.sh"

if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $pythonScript
    exit 0
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $pythonScript
    exit 0
}

exit 0