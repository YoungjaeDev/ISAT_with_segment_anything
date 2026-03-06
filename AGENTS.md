# AGENTS.md

이 저장소에서 작업할 때 지켜야 할 기본 규칙이다.

## 목적

- 이 프로젝트는 `isat-sam` 패키지명으로 배포되는 PyQt5 기반 이미지 분할 주석 도구다.
- 핵심 목표는 기능 추가보다 기존 동작을 깨지 않으면서 문서, 번역, 버그 수정, 유지보수를 안정적으로 진행하는 것이다.

## 작업 범위

- 요청받은 범위만 수정한다.
- 관련 없는 리팩터링, 스타일 정리, 파일 이동은 하지 않는다.
- 설정 파일, 빌드 흐름, 배포 방식 변경은 사용자 확인 없이 진행하지 않는다.

## 코드베이스 구조

- `main.py`: 루트 실행 진입점
- `ISAT/main.py`: 앱 실행 함수
- `ISAT/widgets/`: 메인 애플리케이션 로직
- `ISAT/ui/`: Qt Designer `.ui` 파일과 생성된 UI 코드
- `ISAT/segment_any/`: SAM 계열 모델 연동
- `ISAT/annotation.py`: 주석 데이터 모델과 JSON 저장/로드
- `ISAT/configs.py`: YAML 설정, 경로, enum
- `docs/source/`: Sphinx 원문 문서
- `docs/source/locales/zh_CN/`: 기존 중국어 번역 카탈로그
- `README.md`, `README-cn.md`: 루트 README

## 문서와 번역 작업 규칙

- README 계열과 Sphinx 문서는 별개로 관리한다.
- README 번역은 별도 파일로 관리한다.
- Sphinx 문서는 gettext locale 구조를 따른다.
- 기술 용어, 명령어, 코드 블록, 링크, 파일 경로, 모델명은 함부로 의역하지 않는다.
- 자연스러운 한국어를 우선하되, 의미가 바뀌는 직역 또는 과한 의역은 피한다.
- 번역투 표현보다 실제 문서 작성자가 쓴 듯한 간결한 문장을 우선한다.
- 문장 단위로 매끄럽게 다듬되, 원문의 정보량은 유지한다.
- `SAM`, `SAM2`, `SAM3`, `MobileSAM`, `EdgeSAM`, `MedSAM`, `plugin`, `checkpoint` 같은 이름은 문맥상 필요한 경우 원문 표기를 유지한다.
- Markdown과 reStructuredText 문법은 수정 의도가 없는 한 보존한다.
- 이미지 경로, 앵커, 배지, 표, 코드 블록 언어 태그는 깨지지 않게 유지한다.

## Python 작업 규칙

- 가상환경은 `uv` 기준으로 사용한다.
- 새 의존성 추가나 버전 변경은 사용자 확인 없이 진행하지 않는다.
- 작은 수정이라도 수정한 Python 파일은 최소 `py_compile`로 검증한다.
- 생성된 UI 코드보다 `ISAT/widgets/` 쪽 동작 로직을 우선해서 읽고 수정한다.
- 주석이 꼭 필요할 때만 짧게 추가한다.
- 새 docstring은 영어로 작성한다.
- 새 코드 주석은 한국어로 작성한다.

## 검증

작업 후 가능한 범위에서 아래를 우선 검토한다.

- Python 파일 수정 시
  - `uv run python -m py_compile <파일>`
- 앱 실행 확인이 필요할 때
  - `uv run python main.py`
- 문서 빌드 확인이 필요할 때
  - `uv run sphinx-build -b html -D language=en docs/source docs/build/html/en`
  - `uv run sphinx-build -b html -D language=zh_CN docs/source docs/build/html/zh_CN`
- gettext 갱신이 필요할 때
  - `uv run sphinx-build -b gettext docs/source docs/build/gettext`
  - `uv run sphinx-intl update -p docs/build/gettext -l zh_CN -d docs/source/locales`

자동화된 전체 테스트/린트 설정은 저장소에 분명하게 잡혀 있지 않다. 없는 검증을 했다고 보고하지 않는다.

## 실행과 개발 명령

- 가상환경 생성
  - `uv venv`
- 가상환경 활성화
  - `.\\.venv\\Scripts\\activate`
- editable 설치
  - `uv pip install -e .`
- 의존성 설치
  - `uv pip install -r requirements.txt`
- 문서 의존성 설치
  - `uv pip install -r docs/requirements.txt`
- 앱 실행
  - `uv run python main.py`
  - `uv run isat-sam`

## 커밋 전 체크

- 변경이 요청 범위를 벗어나지 않았는지 확인한다.
- 번역 변경이면 문체와 용어가 문서 전체에서 일관적인지 확인한다.
- 링크, 제목 레벨, 목록, 코드 블록이 깨지지 않았는지 확인한다.
- 검증하지 못한 항목이 있으면 그대로 명시한다.

