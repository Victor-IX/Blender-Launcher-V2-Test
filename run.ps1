& ./.venv/Scripts/python.exe ./build_style.py
if ($args -contains "-debug") {
    & ./.venv/Scripts/python.exe ./source/main.py -debug
} 
elseif ($args -contains "-rc") {
    & ./.venv/Scripts/python.exe ./source/main.py --build-cache
}
else {
    & ./.venv/Scripts/python.exe ./source/main.py
}