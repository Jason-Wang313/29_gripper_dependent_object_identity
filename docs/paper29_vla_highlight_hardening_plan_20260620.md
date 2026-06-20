# Paper29 VLA Highlight Hardening Plan

Date: 2026-06-20

## Objective

Make `C:/Users/wangz/Downloads/29.pdf` explicitly match the visible VLA-v4 role model's PDF link-box behavior while preserving the final 25-page interface-conditioned identity paper:

- citation links use green one-point boxes;
- internal section/equation/table/figure links use red one-point boxes;
- no cyan URL boxes appear;
- the final PDF is rebuilt, rendered, inspected, copied only to Downloads, and leaves no local `paper/main.pdf`.

## Plan-Start Evidence

Baseline artifact:

- Canonical PDF: `C:/Users/wangz/Downloads/29.pdf`
- Pages: 25
- Size: 325,610 bytes
- SHA256: `E1BEFA43E4001EDAAE047DC5BAE248092A0DE758B538F23FDA91CE9FB4894BB9`
- Local `paper/main.pdf`: absent
- Repository state: clean against `origin/master`

Baseline link inventory from the current Downloads PDF:

- Link pages: `[(2, 32), (3, 23), (6, 1)]`
- Annotation colors: green = 53, red = 3, cyan = 0
- Border widths: `(0, 0, 1)` for all 56 link annotations

Source finding:

- `paper/main.tex` is the manuscript source.
- The preamble currently uses plain `\usepackage{hyperref}` with no explicit VLA-style `\hypersetup`.
- The manuscript has both citation commands and internal references, so green citation boxes and red internal boxes should remain present after hardening.

Baseline visual render:

- Rendered affected pages 2, 3, and 6 into `C:/Users/wangz/highlight_box_hardening/tmp/pdfs/paper29_before`.
- Visual samples already show role-model-like green citation boxes and red internal reference boxes. The source still needs explicit policy hardening to prevent drift.

## Role-Model Target

Install the same explicit hyperref policy as the visible VLA-v4 role model:

```tex
\usepackage{hyperref}
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 1},
  citebordercolor={0 1 0},
  linkbordercolor={1 0 0},
  urlbordercolor={0 1 0}
}
```

## Execution Plan

1. Add the role-model `\hypersetup` immediately after `\usepackage{hyperref}` in `paper/main.tex`.
2. Rebuild with `scripts/build_pdf.ps1`, including BibTeX, so the final PDF is copied to Downloads and local `paper/main.pdf` is removed.
3. Recompute page count, SHA256, annotation colors, border widths, and link pages from the rebuilt PDF.
4. Render the affected link pages from the rebuilt Downloads PDF into `tmp/pdfs/paper29_after`.
5. Visually inspect every affected page against the VLA role model:
   - green citation boxes remain crisp and aligned;
   - red internal reference boxes remain crisp and aligned;
   - no cyan boxes appear;
   - layout, figures, line numbers, headers, tables, and page count remain stable.
6. Update README/status/audit/version/validation metadata with the new hash and visual-hardening result.
7. Scan LaTeX logs for fatal errors, undefined citations/references, rerun warnings, and overfull boxes.
8. Remove Paper29 temp renders, leaving only the shared role-model render directory.
9. Stage only Paper29 source and metadata files, commit, push, and verify a clean repository.

## Non-Goals

- Do not alter experiment results, claims, figures, tables, bibliography content, or page count.
- Do not add or remove citations merely to change link counts.
- Do not leave intermediate PDFs or render folders behind.

## Final QA Result

- Final PDF: `C:/Users/wangz/Downloads/29.pdf`
- Pages: 25
- Size: 325,610 bytes
- SHA256: `9E9B16A8A9D82BC4F6ED1CFF6802454218EB9AEC44CC0158E2EBBBF46E38726D`
- Link pages: `[(2, 32), (3, 23), (6, 1)]`
- Annotation colors: green = 53, red = 3, cyan = 0
- Border widths: `(0, 0, 1)` for all 56 link annotations
- Visual QA: affected pages rendered from the rebuilt Downloads PDF and inspected. Green citation boxes and red internal reference boxes are crisp and aligned; no layout drift or cyan boxes appear.
- Local `paper/main.pdf`: absent after canonical build
