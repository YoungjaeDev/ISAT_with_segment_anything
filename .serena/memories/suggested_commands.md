# Suggested commands for ISAT_with_segment_anything

## Environment
- `uv venv`
- `.\\.venv\\Scripts\\activate`
- `uv pip install -e .`
- `uv pip install -r requirements.txt`
- `uv pip install -r docs/requirements.txt`

## Run the app
- `uv run python main.py`
- `uv run isat-sam`  (after editable/package install)

## Docs
- `uv run sphinx-apidoc -o docs/source/_api ISAT ISAT/segment_any/edge_sam/* ISAT/segment_any/mobile_sam/* ISAT/segment_any/sam2/* ISAT/segment_any/sam3/* ISAT/segment_any/segment_anything/* ISAT/segment_any/segment_anything_hq/* ISAT/segment_any/segment_anything_fast/* ISAT/segment_any/segment_anything_med2d/* ISAT/ui/* ISAT/icons_rc.py -f`
- `uv run sphinx-build -b gettext docs/source docs/build/gettext`
- `uv run sphinx-intl update -p docs/build/gettext -l zh_CN -d docs/source/locales`
- `uv run sphinx-build -b html -D language=en docs/source docs/build/html/en`
- `uv run sphinx-build -b html -D language=zh_CN docs/source docs/build/html/zh_CN`

## Verification helpers
- `uv run python -m py_compile main.py`
- `uv run python -m py_compile ISAT/main.py`
- `uv run python -m py_compile ISAT/annotation.py`
- `uv run python -m py_compile ISAT/configs.py`
- `git status --short`
- `rg "pattern"`

## Packaging / release-oriented scripts
- `build_exe.bat`
- `python setup.py sdist`
