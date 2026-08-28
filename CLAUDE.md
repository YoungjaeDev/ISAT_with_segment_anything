# CLAUDE.md

## Project Overview

- `isat-sam` 패키지명으로 배포되는 PyQt5 기반 이미지 분할 주석 도구
- Meta의 Segment Anything 계열(SAM/SAM2/SAM3/HQ-SAM/Mobile-SAM/Edge-SAM/Med2D-SAM)을 연동한다
- 핵심 목표: 기존 동작을 깨지 않으면서 문서, 번역, 버그 수정, 유지보수를 안정적으로 진행

## Commands

```bash
# 가상환경 생성 및 활성화
uv venv
.\.venv\Scripts\activate

# editable 설치
uv pip install -e .

# 의존성 설치
uv pip install -r requirements.txt

# 문서 의존성
uv pip install -r docs/requirements.txt

# 앱 실행
uv run python main.py
uv run isat-sam

# torch CUDA 설치 (RTX 3090, CUDA 12.4)
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124

# SAM3 체크포인트 다운로드 (facebook/sam3 는 gated 저장소)
# 1) https://huggingface.co/facebook/sam3 에서 라이선스 동의
# 2) hf auth login  (또는 HF_TOKEN 환경변수)
uv run hf download facebook/sam3 sam3.pt --local-dir ISAT/checkpoints

# 아이콘 리소스 컴파일 (아이콘 추가/변경 시)
uv run python -m PyQt5.pyrcc_main ISAT/icons.qrc -o ISAT/icons_rc.py

# 소스 배포본 빌드
uv run python setup.py sdist

# Windows EXE 빌드 (PyInstaller)
./build_exe.bat
```

## Architecture

### Entry point & startup sequence

`main.py` → `ISAT/main.py:main()` → `ISAT/widgets/mainwindow.py:MainWindow`

`MainWindow.__init__()` runs: `setupUi()` (Qt Designer UI) → `init_ui()` (docks/dialogs) → `reload_cfg()` (YAML configs) → `init_connect()` (signal wiring) → `InitSegAnyThread` (async SAM model load) → `CheckLatestVersionThread`.

### ui/ vs widgets/ split

- **`ISAT/ui/`** — auto-generated from Qt Designer `.ui` files. Pure layout classes (`Ui_MainWindow`, `Ui_SettingDialog`, etc.). Never hand-edit the `.py` files; edit the `.ui` files in Qt Designer.
- **`ISAT/widgets/`** — hand-written logic classes. Pattern: `class SomeWidget(QDialog, Ui_SomeWidget)` inherits layout and adds behavior.

### Two-layer data model

- **`ISAT/annotation.py`** — disk representation. `Object` (category, group, segmentation vertices, area, bbox, layer, iscrowd, note) and `Annotation` (image metadata + list of Objects, load/save as JSON).
- **`ISAT/widgets/polygon.py`** — visual representation. `BaseShape` holds the shared point/vertex logic; `Polygon` and `OBB` are `QGraphicsPolygonItem` subclasses that mix it in, with `BaseVertex` subclasses (`PolygonVertex`, `OBBVertex`, `LineVertex`) as children. Conversion: `to_object()` for save, `load_object()` for display.

### Annotation data flow

**Create:** user draws or SAM predicts mask → `cv2.findContours` → `Polygon` on scene → `mainwindow.polygons` list → on save: `polygon.to_object()` → `Annotation.objects` → `Annotation.save_annotation()`

**Load:** `MainWindow.show_image()` → `Annotation(image_path, label_path)` → `annotation.load_annotation()` → for each Object, create `Polygon` with `load_object()` → add to scene + `mainwindow.polygons`

### Canvas interaction

`ISAT/widgets/canvas.py` has two classes:
- **`AnnotationScene`** (`QGraphicsScene`) — mouse/key event handling. Mode machine: `STATUSMode` (VIEW/CREATE/EDIT/REPAINT) × `DRAWMode` (POLYGON/SEGMENTANYTHING_POINT/SEGMENTANYTHING_BOX/SEGMENTANYTHING_VISUAL/OBB).
- **`AnnotationView`** (`QGraphicsView`) — zoom, pan, fit-to-window.

### SAM model integration

`ISAT/segment_any/segment_any.py` is the **facade**: `SegAny` for images, `SegAnyVideo` for video (SAM2/SAM2.1/SAM3). It auto-detects model type from the checkpoint filename string (e.g., `"mobile_sam"`, `"sam2"`, `"sam3"`, `"edge_sam"`) and dispatches to the correct sub-package predictor. All 8 SAM variants are **vendored directly** in the source tree under `ISAT/segment_any/` — they are not pip dependencies.

`ISAT/segment_any/model_zoo.py` — registry of 20 model entries with download URLs (HuggingFace + ModelScope mirrors), memory/param counts, and image/video capability flags.

### Config files

- **`ISAT/software.yaml`** — software settings (mask_alpha, language, contour_mode, auto_save, bfloat16), keyboard shortcuts, and category labels with colors.
- **`ISAT/isat.yaml`** — category labels only (name + hex color).
- **`ISAT/configs.py`** — `ISAT_ROOT`, `CHECKPOINT_PATH`, enums (`STATUSMode`, `DRAWMode`, `MAPMode`, `CONTOURMode`, `CONTOURMethod`), YAML load/save helpers.
- SAM2/SAM2.1 model architectures are defined as Hydra `@package _global_` YAML configs in `ISAT/segment_any/sam2/configs/`.

Note: `*.yaml` is in `.gitignore`, so config changes are not tracked by default.

### Concurrency model

All heavy work runs on `QThread` subclasses communicating via `pyqtSignal`:
- `InitSegAnyThread` — SAM model loading (several GB)
- `SegAnyThread` — image encoder, caches features for ±1 adjacent images
- `SegAnyVideoThread` — video frame-by-frame propagation
- `DownloadThread` — checkpoint download with HTTP range resume
- `GPUResource_Thread` — polls `nvidia-smi` for status bar display
- `CheckLatestVersionThread` — PyPI version check
- `AutoSegmentThread` — batch auto-segmentation

### Format converters

`ISAT/formats/` — all inherit from base `ISAT` class in `formats/isat.py`: `COCO`, `YOLO`, `LABELME`, `VOC`, `VOCDetect`. The `Converter` class in `widgets/converter_dialog.py` orchestrates them.

### Plugin system

Plugins are discovered via `entry_points` group `isat.plugins`, must subclass `ISAT/plugin_base.py:PluginBase`. `MainWindow` fires lifecycle hooks: `trigger_application_start/shutdown`, `trigger_before/after_image_open`, `trigger_before_annotations_save`, `trigger_after_annotation_changed`, `trigger_after_sam_encode_finished`.

### Key dependencies

`torch>=2.3.0`, `pyqt5`, `opencv_python_headless`, `shapely`, `pycocotools`, `hydra-core`, `timm`, `einops`, `pydicom`, `fuzzywuzzy`, `imgviz`, `orjson`

## Codebase Structure

- `main.py` -- 루트 실행 진입점
- `ISAT/main.py` -- 앱 실행 함수
- `ISAT/widgets/` -- 메인 애플리케이션 로직
- `ISAT/ui/` -- Qt Designer `.ui` 파일과 생성된 UI 코드
- `ISAT/segment_any/` -- SAM 계열 모델 연동
- `ISAT/annotation.py` -- 주석 데이터 모델과 JSON 저장/로드
- `ISAT/configs.py` -- YAML 설정, 경로, enum
- `ISAT/checkpoints/` -- 모델 체크포인트 저장 위치 (git 추적 제외, `CHECKPOINT_PATH`)
- `icons/` -- SVG 아이콘 (중국어_영어 명명 규칙, 예: `保存_save.svg`)
- `ISAT/icons.qrc` -- Qt 리소스 파일, `ISAT/icons_rc.py` -- 컴파일된 리소스
- `tools/` -- 본체와 분리된 보조 도구 (SAM3 텍스트 프롬프트 기반 자동 예비 라벨링 등, Dockerfile로 별도 실행)
- `docs/source/` -- Sphinx 원문 문서
- `docs/source/locales/zh_CN/`, `docs/source/locales/ko_KR/` -- 번역 카탈로그
- `README.md`, `README-cn.md`, `README-ko.md` -- 루트 README

## Work Scope

- 요청받은 범위만 수정한다
- 관련 없는 리팩터링, 스타일 정리, 파일 이동은 하지 않는다
- 설정 파일, 빌드 흐름, 배포 방식 변경은 사용자 확인 없이 진행하지 않는다
- 새 의존성 추가나 버전 변경은 사용자 확인 없이 진행하지 않는다

## Python Rules

- 가상환경은 `uv` 기준으로 사용한다
- 생성된 UI 코드보다 `ISAT/widgets/` 쪽 동작 로직을 우선해서 읽고 수정한다
- 주석이 꼭 필요할 때만 짧게 추가한다
- 새 docstring은 영어로 작성한다
- 새 코드 주석은 한국어로 작성한다

## Documentation and Translation

- README 계열과 Sphinx 문서는 별개로 관리한다
- README 번역은 별도 파일로 관리한다 (예: `README-ko.md`)
- Sphinx 문서는 gettext locale 구조를 따른다
- 기술 용어, 명령어, 코드 블록, 링크, 파일 경로, 모델명은 함부로 의역하지 않는다
- 자연스러운 한국어를 우선하되, 의미가 바뀌는 직역 또는 과한 의역은 피한다
- 번역투 표현보다 실제 문서 작성자가 쓴 듯한 간결한 문장을 우선한다
- 문장 단위로 매끄럽게 다듬되, 원문의 정보량은 유지한다
- `SAM`, `SAM2`, `SAM3`, `MobileSAM`, `EdgeSAM`, `MedSAM`, `plugin`, `checkpoint` 같은 이름은 문맥상 필요한 경우 원문 표기를 유지한다
- Markdown과 reStructuredText 문법은 수정 의도가 없는 한 보존한다
- 이미지 경로, 앵커, 배지, 표, 코드 블록 언어 태그는 깨지지 않게 유지한다

## Verification

작업 후 가능한 범위에서 아래를 우선 검토한다.

```bash
# Python 파일 수정 시
uv run python -m py_compile <file>

# 앱 실행 확인
uv run python main.py

# 문서 빌드
uv run sphinx-build -b html -D language=en docs/source docs/build/html/en
uv run sphinx-build -b html -D language=zh_CN docs/source docs/build/html/zh_CN
uv run sphinx-build -b html -D language=ko_KR docs/source docs/build/html/ko_KR

# gettext 갱신
uv run sphinx-build -b gettext docs/source docs/build/gettext
uv run sphinx-intl update -p docs/build/gettext -l zh_CN -l ko_KR -d docs/source/locales
```

자동화된 테스트나 린트 설정은 저장소에 잡혀 있지 않다. `test/` 디렉터리에는 단발성 스크립트 두 개(`coco_display.py`, `f32_vs_bf16.py`)만 있고, 실제 검증은 GUI 앱을 직접 실행해서 한다. 없는 검증을 했다고 보고하지 않는다.

## Pre-commit Checklist

- 변경이 요청 범위를 벗어나지 않았는지 확인
- 번역 변경이면 문체와 용어가 문서 전체에서 일관적인지 확인
- 링크, 제목 레벨, 목록, 코드 블록이 깨지지 않았는지 확인
- 검증하지 못한 항목이 있으면 그대로 명시
