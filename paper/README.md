# Paper Build

This directory uses the official ICLR 2026 style files downloaded from the ICLR/Master-Template archive at runtime.

Build sequence from this directory:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The final orchestration target is `C:/Users/wangz/Downloads/29.pdf`.
