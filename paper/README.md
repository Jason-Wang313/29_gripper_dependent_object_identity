# Paper Build

This directory uses the official ICLR 2026 style files downloaded from the ICLR/Master-Template archive at runtime.

Build sequence from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```

The final orchestration target is `C:/Users/wangz/Downloads/29.pdf`; the script
removes transient `paper/main.pdf` after copying.
