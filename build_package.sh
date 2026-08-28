#!/bin/sh

set -eu
rm -rf _deps _dist
mkdir -p _deps
cd _deps
wget https://www.python.org/ftp/python/3.13.15/python-3.13.15-embed-win32.zip -O python.zip
wget https://gnuwin32.sourceforge.net/downlinks/make-bin-zip.php -O make-bin.zip
wget https://gnuwin32.sourceforge.net/downlinks/make-dep-zip.php -O make-dep.zip
wget https://github.com/gbdev/rgbds/releases/download/v1.0.3/rgbds-win32.zip
wget https://bootstrap.pypa.io/get-pip.py
wget https://github.com/daid/LADX-Disassembly/archive/refs/heads/HackBase.zip -O disasm.zip
unzip make-bin.zip
unzip make-dep.zip
unzip rgbds-win32.zip
unzip disasm.zip
mv `ls | grep LADX-Disassembly-*` LADX-Disassembly
cd bin
unzip ../python.zip
chmod +x python.exe
echo "import site" >> `ls *._pth`
# Ensure that files can import other local files, for some reason this is not the default with a ._pth file
cat > sitecustomize.py <<EOF
import os
import sys

if len(sys.argv) > 0 and sys.argv[0] and sys.argv[0] not in ('-c', '-m'):
    path = [os.path.dirname(os.path.abspath(sys.argv[0]))]
    norm_script_dir = os.path.normcase(path[0])
    for p in sys.path:
        if os.path.normcase(p) != norm_script_dir:
            path.append(p)
    sys.path[:] = path

EOF
./python.exe ../get-pip.py
./python.exe -m pip install -r ../../requirements.txt
cd ..
cd ..
mkdir -p _dist/support _dist/src
cd _dist
cp -a ../_deps/bin ./support/
cp -a ../_deps/bin ./support/
cp -a ../_deps/LADX-Disassembly ./src/LADX-Origonal
cp -a ../_deps/LADX-Disassembly ./src/LADX-Hack
cp -a ../scripts_win32/* ./
cp -a ../lab KoholintLab
