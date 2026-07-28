# Suspense in Shorts

**Theory-pluralist annotation and evaluation of suspense in short fiction.**

This repository documents the annotation data, corpus preparation, and evaluation
pipeline for the URAP project *Measuring Suspense in Fiction* at UC Berkeley
(summer term 2026). It is the companion data-and-analysis repository to
[**SuspenseLens**](https://github.com/SvenjaGuhr/SuspenseLens), the browser-based
annotation tool.

---

## Overview

Suspense is one of the most contested concepts in literary theory: competing accounts
disagree not only on how to measure it but on what has to be true for it to occur at
all. Rather than choosing one account, this project operationalizes several
*incompatible* theories of suspense in parallel and annotates the same short stories
under each, so that agreement and disagreement can be measured **within** and
**across** theoretical frames.

Because suspense has no ground truth to validate against, agreement among annotators
working from a shared operationalization is the only available standard, and
disagreement across operationalizations is treated as an object of study rather than
as noise to be removed. This repository holds the manual annotations produced under
that design and the code that evaluates them.

Two research questions organize the work:

1. **Reliability.** When annotators follow the guidelines for a single theory, how
   consistently do they rate sentences, and does that consistency break down when
   annotations from different theories are compared?
2. **Theory vs. intrinsic concept (companion work).** Can a language model be prompted
   to follow a specified theory of suspense, or does it fall back on its own
   pretrained, everyday notion? That comparison is carried out with
   [SuspenseLens](https://github.com/SvenjaGuhr/SuspenseLens).

---

## Annotation scheme

Each text is annotated sentence by sentence under **four conditions**:

1. **T1 — Uncertainty-based suspense** (suspense depends on uncertainty about an
   anticipated, high-stakes outcome)
2. **T2 — Desire-frustration** (suspense without uncertainty: a strong desire to affect
   an imminent outcome combined with an inability to act)
3. **T3 — Partial uncertainty / anomalous suspense** (suspense that survives partial or
   retained knowledge of the outcome)
4. **T4 — Casual reader** (an atheoretical baseline: surface-level judgments of tension
   with no theoretical guidance)

Every sentence carries **two independent 0–5 ratings**:

- `reader_suspense_level` — suspense experienced by the reader
- `character_anxiety_level` — anxiety experienced by a character in the story world

`0` is the default, and long stretches of a text are expected to remain at `0`.
Annotations also record the suspense-experiencing entity (character or narrator) and
the suspense-evoking element, following a shared *constitutional* prompt held constant
across all four conditions.

Annotations are organized by **annotator group** (`a`, `b`, `o`). One worksheet
corresponds to one *(theory, group)* pair and is named `T<theory><group>_<Text>`
(for example, `T1a_Doyle_How_It_Happened` is group A working under theory 1). We refer
to each such series as an annotation **unit**.

---

## Repository structure

```
Suspense_in_Shorts/
├── 20260720_IAA_Evaluation/                 # manual annotations, one folder per text
│   ├── Anderson_Hippogriff/                 #   each folder holds Group_A/B/O .xlsx files
│   ├── Doyle_How_It_Happened/
│   ├── Gaskell_Old_Nurses_Story/
│   ├── Hemingway_The_Killers/
│   ├── London_The_Heathen/
│   ├── Marks_Wedding_Day/
│   ├── Munro_Defensive_Diamond/
│   ├── Nesbit_The_Semi-detached/
│   ├── Wharton_Miss_Mary/
│   └── Wilde_Model_Millionaire/
│
├── 202607_annotator_evaluation_combined.ipynb   # main evaluation notebook (interactive)
├── 20260430_IAA_Suspense.ipynb                  # earlier IAA notebook (superseded)
│
├── Gutenberg_text_filter_corpus_preparation.ipynb   # corpus scraping and filtering
├── sentence_splitting_for_suspense_annotion.py      # one-sentence-per-line splitting
│
├── evaluation_outputs/                      # generated results
│   └── run_20260728_094740/                 #   figures/, results.xlsx, run_log.txt
│
├── Flowchart_Suspense_Annotation.png        # workflow diagram
├── LICENSE
└── README.md
```

Each text folder under `20260720_IAA_Evaluation/` contains the three
`Group_*.xlsx` files for that story; coverage is not uniform, since not every group
annotated every condition on every text.

---

## The evaluation pipeline

The main notebook, `202607_annotator_evaluation_combined.ipynb`, walks from *who
annotated what* to *how reliable the annotations are* to *whether sharing a theory
makes annotators agree more*, and exports the results. It answers the two questions
above with tools chosen for the data, which is ordinal (0–5) and heavily
zero-inflated.

**1. Reliability (within a theory).**
Inter-annotator agreement is reported per text, per condition, and overall using:

- **Krippendorff's α (ordinal)** — the headline coefficient; handles two or more
  raters, missing data, and the ordinal scale;
- **Weighted Cohen's κ (quadratic)** — a pairwise, ordinal companion;
- **Percent agreement (raw)** — not chance-corrected, but defined even when a unit used
  a single value throughout, which the chance-corrected coefficients are not.

Units that did not complete a text, or whose ratings carry no variance, are excluded
and reported, since a chance-corrected coefficient is undefined for a constant series.
This matters most on `character_anxiety_level`, where several units rate every sentence
`0`.

**2. Coherence (within vs. across theory).**
To test whether the operationalizations produce distinguishable behavior, every pair of
annotation units within a text is labelled **intra**-theory (same condition) or
**inter**-theory (different condition), and the **Spearman rank correlation** between
the two units is computed over the sentences they share. The test statistic is
`mean(intra) − mean(inter)`, and its significance is assessed with a **permutation
test** (labels shuffled, N = 10,000, one-tailed). Spearman is used because it asks only
whether annotators *order* sentences similarly and is invariant to how each annotator
uses the 0–5 range.

**Outputs.** Results are written to a timestamped folder under `evaluation_outputs/`:
heatmaps (unit × unit, theory × theory, group × group) as PNGs, a single
`results.xlsx` workbook (completeness, per-text agreement matrices, an IAA summary, and
the coherence tables), and a `run_log.txt` of the console output.

---

## Running the evaluation

Requirements (Python 3.10+):

```bash
pip install pandas numpy scipy matplotlib seaborn openpyxl ipywidgets
```

Then open `202607_annotator_evaluation_combined.ipynb` in Jupyter, JupyterLab, or
PyCharm and:

1. Set `ROOT` in the configuration cell to the `20260720_IAA_Evaluation` folder.
2. Run all cells. The notebook auto-discovers the text folders.
3. Use the interactive explorer to switch text, target column, metric, and the groups
   and theories being compared; heatmaps and summaries update on demand.
4. Run the export cell to write figures and `results.xlsx` to `evaluation_outputs/`.

To evaluate the character-anxiety scale instead of reader suspense, set
`DEFAULT_TARGET = "character_anxiety_level"` and re-run.

---

## Corpus preparation

`Gutenberg_text_filter_corpus_preparation.ipynb` documents how the short-fiction corpus
was scraped from Project Gutenberg and filtered, following the cleaning procedures
established for the *d-Prose (1870–1920)* collection. `sentence_splitting_for_suspense_annotion.py`
splits each story into one sentence per line, the format the annotation workbooks
expect.

---

## Companion tool: SuspenseLens

[**SuspenseLens**](https://github.com/SvenjaGuhr/SuspenseLens) is a browser-based tool
that loads a short story sentence by sentence, runs it through a locally hosted
language model (default: Qwen3-4B), and returns sentence-level suspense annotations
under the same four theoretical perspectives used here. Results are shown as a
color-coded heatmap with theory-specific underlines and can be evaluated against the
human gold-standard annotations in this repository.

<img width="1229" alt="SuspenseLens annotating 'Oh Rats!'" src="https://github.com/user-attachments/assets/cf8677e9-6588-4386-8103-0c8d5c4fd483" />

---

## How to cite

> Guhr, Svenja. 2026. *Suspense in Shorts.* GitHub repository.
> https://github.com/SvenjaGuhr/Suspense_in_Shorts

> Guhr, Svenja. 2026. *SuspenseLens.* GitHub repository.
> https://github.com/SvenjaGuhr/SuspenseLens

---

## References

- Carroll, Noël. 1997. "The Paradox of Suspense." In *Suspense: Conceptualizations,
  Theoretical Analyses, and Empirical Explorations.* LEA's Communication Series.
- De Ford, Miriam Allen. 1961. "Oh Rats!" *Galaxy Magazine*, December 1961.
  https://www.gutenberg.org/ebooks/51751
- Gerrig, Richard. 1989. "Suspense in the Absence of Uncertainty." *Journal of Memory
  and Language* 28 (6): 633–48. https://doi.org/10.1016/0749-596X(89)90001-6
- Halterman, Andrew, and Katherine A. Keith. 2026. "Codebook LLMs: Evaluating LLMs as
  Measurement Tools for Political Science Concepts." *Political Analysis* 34 (2):
  188–204. https://doi.org/10.1017/pan.2025.10017
- Iwata, Yumiko. 2009. "Creating Suspense and Surprise in Short Literary Fiction: A
  Stylistic and Narratological Approach." Doctoral thesis, University of Birmingham.
  https://etheses.bham.ac.uk/id/eprint/284/
- Smuts, Aaron. 2008. "The Desire-Frustration Theory of Suspense." *Journal of
  Aesthetics and Art Criticism* 66 (3): 281–90.
  https://doi.org/10.1111/j.1540-6245.2008.00309.x
- Tseng, Yu-Min, et al. 2024. "Two Tales of Persona in LLMs: A Survey of Role-Playing
  and Personalization." *Findings of the ACL: EMNLP 2024*, 16612–31.
  https://doi.org/10.18653/v1/2024.findings-emnlp.969

---

## License

Released under the terms of the [LICENSE](LICENSE) file in this repository.

*Part of the URAP project "Measuring Suspense in Fiction," UC Berkeley, summer 2026.*
