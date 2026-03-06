# Task completion checklist

- After Python edits, run `uv run python -m py_compile` on each touched Python file at minimum.
- If docs or README files change, verify formatting/rendering:
  - for Markdown: check headings, links, image paths, and fenced code blocks
  - for Sphinx docs: build the relevant target when practical (`en`, `zh_CN`, or gettext/html as needed)
- If runtime/UI logic changes and the environment supports it, do a smoke run with `uv run python main.py`.
- No clear repo-wide lint or automated unit-test setup is present, so do not claim lint/test coverage that does not exist.
- Report any verification you could not run.
