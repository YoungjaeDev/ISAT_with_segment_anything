<h1 align='center'>ISAT_with_segment_anything [isat-sam]</h1>
<h2 align='center'>Segment Anything 기반 인터랙티브 반자동 이미지 분할 주석 도구</h2>
<p align='center'>
    <a href='https://github.com/yatengLG/ISAT_with_segment_anything/stargazers' target="_blank"><img alt="GitHub forks" src="https://img.shields.io/github/stars/yatengLG/ISAT_with_segment_anything?style=social"></a>
    <a href='https://github.com/yatengLG/ISAT_with_segment_anything/forks' target="_blank"><img alt="GitHub forks" src="https://img.shields.io/github/forks/yatengLG/ISAT_with_segment_anything"></a>
    <a href='https://pypi.org/project/isat-sam/' target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/isat-sam?style=social&logo=pypi"></a>
    <a href='https://pypi.org/project/isat-sam/' target="_blank"><img alt="Pepy Total Downlods" src="https://img.shields.io/pepy/dt/isat-sam?style=social&logo=pypi"></a>
</p>
<p align='center'>
<b>이 프로젝트가 도움이 됐다면 Star로 지원해 주세요.</b>
</p>
<p align='center'>
    <a href='README-ko.md'><b>[한국어]</b></a>
    <a href='README.md'><b>[English]</b></a>
    <a href='README-cn.md'><b>[中文]</b></a>
</p>
<p align='center'><img src="./display/software.gif" alt="software.gif"></p>

ISAT는 이미지 분할에 초점을 맞춘 도구로, 더 매끄럽고 실용적인 주석 작업 흐름을 제공하는 것을 목표로 합니다.

최신 공식 문서는 [Documentation in English](https://isat-sam.readthedocs.io/en/latest/#)와 [中文文档](https://isat-sam.readthedocs.io/zh-cn/latest/)에서 확인할 수 있습니다.

---

# 업데이트
- **1.5.2 버전부터 ISAT는 SAM3 기반 visual prompt를 지원합니다.**
    
    <details>
        <summary>Visual prompt</summary>
            <p align='center'><img src="./display/visual_prompt.gif" alt="visual_prompt.gif"></p>
    </details>

- **1.5.0 버전부터 ISAT는 SAM3와 text prompt를 지원합니다.**
    
    <details>
        <summary>Text prompt</summary>
            <h3>단일 카테고리</h3>
                <p align='center'><img src="./display/text_prompt1.gif" alt="text_prompt1.gif"></p>
            <h3>다중 카테고리</h3>
                <p align='center'><img src="./display/text_prompt2.gif" alt="text_prompt2.gif"></p>
    </details>

- **1.4.0 버전부터 ISAT는 플러그인 시스템을 지원합니다.** 비교적 적은 코드만으로 ISAT 기능을 확장할 수 있습니다.
  
    공식 플러그인 예시는 다음과 같습니다.
  - [ISAT_plugin_auto_annotate](https://github.com/yatengLG/ISAT_plugin_auto_annotate) ![PyPI - Version](https://img.shields.io/pypi/v/isat-plugin-auto-annotate?style=social&logo=pypi)
 ![Pepy Total Downloads](https://img.shields.io/pepy/dt/isat-plugin-auto-annotate?style=social) : YOLO 기반 자동 주석 기능으로, 약 240줄의 코드만으로 구현되어 있습니다.
  - [ISAT_plugin_mask_export](https://github.com/yatengLG/ISAT_plugin_mask_export) ![PyPI - Version](https://img.shields.io/pypi/v/isat-plugin-mask-export?style=social&logo=pypi)
![Pepy Total Downloads](https://img.shields.io/pepy/dt/isat-plugin-mask-export?style=social) : 마스크 내보내기 기능으로, 약 160줄의 코드만으로 구현되어 있습니다.

- 다른 버전과 릴리스 노트는 [releases](https://github.com/yatengLG/ISAT_with_segment_anything/releases)에서 확인할 수 있습니다.

# 설치

- conda 환경 생성(권장, 선택)
    ```shell
    # 환경 생성
    conda create -n isat_env python=3.8
    
    # 환경 활성화
    conda activate isat_env
    ```

- 설치
    ```shell
    pip install isat-sam
    ```

- 실행
    ```shell
    isat-sam
    ```

# Star History

**프로젝트가 도움이 됐다면 Star로 응원해 주세요.**
[![Star History Chart](https://api.star-history.com/svg?repos=yatengLG/ISAT_with_segment_anything&type=Date)](https://star-history.com/#yatengLG/ISAT_with_segment_anything&Date)


# Contributors

<table border="0">
<tr>
    <td><img alt="yatengLG" src="https://avatars.githubusercontent.com/u/31759824?v=4" width="60" height="60" href="">
    <td><img alt="Alias-z" src="https://avatars.githubusercontent.com/u/66273343?v=4" width="60" height="60" href="">
    <td>...
</td>
</tr>
<tr>
  <td><a href="https://github.com/yatengLG">yatengLG</a>
  <td><a href="https://github.com/Alias-z">Alias-z</a>
    <td><a href="https://github.com/yatengLG/ISAT_with_segment_anything/graphs/contributors">...</a>
</tr>
</table>


# Citation
```text
@misc{ISAT_with_segment_anything,
  title={{ISAT with Segment Anything: An Interactive Semi-Automatic Annotation Tool}},
  author={Ji, Shuwei and Zhang, Hongyuan},
  url={https://github.com/yatengLG/ISAT_with_segment_anything},
  note={Updated on 2025-02-07},
  year={2024},
  version={1.33}
}
```
