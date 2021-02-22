git clone https://github.com/TES286/TMCL.git TMCL && cd TMCL
python3.8 -m pip install pyinstaller
pyinstaller -F run.py
cp dist/run /usr/bin/tmcl

echo "You can use command \"TMCL\" to run TMCL"
