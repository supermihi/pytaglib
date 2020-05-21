$ver = $args[0]
$myargs = "-$ver", '-m', 'venv', '--upgrade', "venv-$ver"
iex "& py $myargs"
iex "& venv-$ver/Scripts/Python.exe -m pip install -r build_win_requirements.txt"
iex "& venv-$ver/Scripts/Python.exe build_win.py"
