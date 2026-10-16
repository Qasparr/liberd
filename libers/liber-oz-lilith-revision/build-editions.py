#!/usr/bin/env python3
"""Build HTML + PDF twins for the two Teacher's Editions and the gematria catalog.
MECHANISM: reuses the compendium builder's tokenizer and renderers — one
pipeline, three documents. DOCTRINE: same ivory/blood/gold dress, same fonts."""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("comp_builder", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "build-compendium.py"))
comp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(comp)

DOCS = [
    ("teachers-edition-witness-a.md", "Liber Oz — Teacher's Edition (Witness A)"),
    ("teachers-edition-witness-b.md", "Liber Oz — Teacher's Edition (Witness B)"),
    ("gematria-catalog.md", "Liber Oz — Gematria Catalog"),
]

d = os.path.dirname(os.path.abspath(__file__))
for md_name, title in DOCS:
    src = os.path.join(d, md_name)
    with open(src, encoding="utf-8") as f:
        toks = comp.tokenize(f.read().split("\n"))
    html = comp.render_html(toks, title)
    with open(src.replace(".md", ".html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", src.replace(".md", ".html"))
    comp.render_pdf(toks, src.replace(".md", ".pdf"))
    print("wrote", src.replace(".md", ".pdf"))
