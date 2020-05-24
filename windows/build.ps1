param ($pyver)
$ErrorActionPreference = "Stop"

if ($null -eq $pyver) {
    Write-Host "No python version specified. Using system default"
    $pyver = ""
}
else {
    $pyver = "-$pyver"
}

$build = "build/windows"
$venv = "$build/venv-$pyver"
$myargs = $pyver, '-m', 'venv', '--upgrade', "$venv"


iex "& py $myargs"
iex "& $venv/Scripts/Python.exe -m pip install -r windows/build_win_requirements.txt"
iex "& $venv/Scripts/Python.exe windows/build_win.py"
