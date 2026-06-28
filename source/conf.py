# Configuration file for the Sphinx documentation builder.

import os
import sys
# Dodanie ścieżki do katalogu nadrzędnego, gdzie leży biblioteka_zapytania.py
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = 'Sprawozdanie-z-laboratoriów'
copyright = '2026, Michał Bednarczyk'
author = 'Michał Bednarczyk'

# -- General configuration ---------------------------------------------------
# Dodanie rozszerzenia autodoc
extensions = [
    'sphinx.ext.autodoc'
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']

# -- Options for LaTeX output ------------------------------------------------
# Optymalizacja generowania PDF - eliminacja pustych stron między rozdziałami
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'fncychap': '\\usepackage[Bjarne]{fncychap}',
    'extraclassoptions': 'openany,oneside',
    'printindex': '',
    'preamble': r'''
\usepackage{babel}
\usepackage{graphicx}
\usepackage{hyperref}
\setcounter{tocdepth}{2}
\raggedbottom

% TWARDY RESET INDEKSU - zmusza LaTeXa do zignorowania komendy generującej spis
\renewcommand{\printindex}{}

% Zmniejszenie przestrzeni przed nagłówkami
\setlength{\parskip}{0pt plus 1pt}
\setlength{\parindent}{0pt}

% Zwiększenie wysokości headera
\setlength{\headheight}{14.49998pt}
''',
    'sphinxsetup': 'hmargin={0.7in,0.7in}, vmargin={0.7in,0.7in}, verbatimwithframe=false',
}
latex_documents = [
    (
        'index', 
        'sprawozdanie-z-laboratoriow.tex', 
        'Sprawozdanie z Laboratorium: Bazy Danych',
        'Michał Bednarczyk, Jan Balázs de Borbátviz,Norbert Antonovitch',  # Combined authors into one string
        'manual'                         # This is now correctly the documentclass
    ),
]

latex_show_urls = 'footnote'
latex_show_pagerefs = False
latex_max_embed_pages = 0

# KLUCZOWE: Wyłącza generowanie bzdurnego "Python Module Index" w PDF i spisie treści
latex_domain_indices = False
