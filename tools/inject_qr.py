# -*- coding: utf-8 -*-
"""Inject the verified QR SVG into slides.html (responsive: viewBox only)."""
import re

SLIDES = r"C:\Users\tomha\claude code\beit-berl-samr-journey\slides.html"
QR = r"C:\Users\tomha\AppData\Local\Temp\claude\C--Users-tomha-claude-code-workshops\a906e0e1-c13a-44fd-931b-86a084bbb6c6\scratchpad\qr_samr.svg"

svg = open(QR, encoding="utf-8").read().strip()
# drop the fixed mm size so CSS controls it; keep viewBox
svg = re.sub(r'\swidth="[^"]*"\s+height="[^"]*"', '', svg, count=1)
# decorative for AT (the container has role=img + aria-label)
svg = svg.replace('<svg ', '<svg aria-hidden="true" focusable="false" ', 1)

html = open(SLIDES, encoding="utf-8").read()
assert "<!--QR_SVG-->" in html, "placeholder missing!"
html = html.replace("<!--QR_SVG-->", svg)
open(SLIDES, "w", encoding="utf-8", newline="\n").write(html)
print("QR injected. placeholder remaining:", "<!--QR_SVG-->" in html)
