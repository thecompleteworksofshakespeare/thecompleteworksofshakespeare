#!/bin/bash

if [ "$(uname)" != "Darwin" ]; then
    exit 1
fi

echo "Checking for Pandoc"
which pandoc > /dev/null && echo "[OK]" || (echo "[Installing]" && brew install pandoc)

echo "Checking for Python Imaging Library PIL"
python -c "import PIL" > /dev/null 2>&1 && echo "[OK]" || echo "Please install PIL - pip install pillow"

echo "Checking for PDF generation tool"
which pdflatex && echo "[OK]" || echo "Please install pdflatex"

exit 0
