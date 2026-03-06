<h1 align='center'>ISAT_with_segment_anything [isat-sam]</h1>
<h2 align='center'>一款基于SAM的交互式半自动图像分割标注工具</h2>
<p align='center'>
    <a href='https://github.com/yatengLG/ISAT_with_segment_anything/stargazers' target="_blank"><img alt="GitHub forks" src="https://img.shields.io/github/stars/yatengLG/ISAT_with_segment_anything?style=social"></a>
    <a href='https://github.com/yatengLG/ISAT_with_segment_anything/forks' target="_blank"><img alt="GitHub forks" src="https://img.shields.io/github/forks/yatengLG/ISAT_with_segment_anything"></a>
    <a href='https://pypi.org/project/isat-sam/' target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/isat-sam?style=social&logo=pypi"></a>
    <a href='https://pypi.org/project/isat-sam/' target="_blank"><img alt="Pepy Total Downlods" src="https://img.shields.io/pepy/dt/isat-sam?style=social&logo=pypi"></a>
</p>
<p align='center'>
<b>如果这个项目对你有帮助，欢迎点个 Star 支持一下。</b>
</p>
<p align='center'>
    <a href='README-ko.md'><b>[한국어]</b></a>
    <a href='README.md'><b>[English]</b></a>
    <a href='README-cn.md'><b>[中文]</b></a>
</p>
<p align='center'><img src="./display/software.gif" alt="software.gif"></p>

ISAT 专注于图像分割，目标是提供更顺手、更实用的标注工作流。

最新文档请参考 [Documentation in English](https://isat-sam.readthedocs.io/en/latest/#) 或 [中文文档](https://isat-sam.readthedocs.io/zh-cn/latest/)。

---

# 更新
- **从 1.5.2 版本开始，ISAT 支持基于 SAM3 的 visual prompt。**
    <details>
        <summary>视觉提示</summary>
            <p align='center'><img src="./display/visual_prompt.gif" alt="visual_prompt.gif"></p>
    </details>

- **从 1.5.0 版本开始，ISAT 支持 SAM3 和 text prompt。**

    <details>
        <summary>文本提示</summary>
            <h3>单类别</h3>
                <p align='center'><img src="./display/text_prompt1.gif" alt="text_prompt1.gif"></p>
            <h3>多类别</h3>
                <p align='center'><img src="./display/text_prompt2.gif" alt="text_prompt2.gif"></p>
    </details>

- **从 1.4.0 版本开始，ISAT 提供 plugin system。** 只需少量代码就可以扩展 ISAT 的功能。
  
    官方插件示例:
  - [ISAT_plugin_auto_annotate](https://github.com/yatengLG/ISAT_plugin_auto_annotate) ![PyPI - Version](https://img.shields.io/pypi/v/isat-plugin-auto-annotate?style=social&logo=pypi)
 ![Pepy Total Downloads](https://img.shields.io/pepy/dt/isat-plugin-auto-annotate?style=social) : 基于 YOLO 的自动标注功能，仅用 240 行代码实现。
  - [ISAT_plugin_mask_export](https://github.com/yatengLG/ISAT_plugin_mask_export) ![PyPI - Version](https://img.shields.io/pypi/v/isat-plugin-mask-export?style=social&logo=pypi)
![Pepy Total Downloads](https://img.shields.io/pepy/dt/isat-plugin-mask-export?style=social) : mask 导出功能，仅用 160 行代码实现。

- 其他版本和 release notes 请参考 [releases](https://github.com/yatengLG/ISAT_with_segment_anything/releases)。

# 安装

- 新建 conda 环境（推荐，可选）
    ```shell
    # 创建环境
    conda create -n isat_env python=3.8
    
    # 激活环境
    conda activate isat_env
    ```

- 安装
    ```shell
    pip install isat-sam
    ```

- 运行
    ```shell
    isat-sam
    ```

# Star History

**欢迎给项目点个 Star 支持一下。**
[![Star History Chart](https://api.star-history.com/svg?repos=yatengLG/ISAT_with_segment_anything&type=Date)](https://star-history.com/#yatengLG/ISAT_with_segment_anything&Date)


# 核心贡献者

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


# 引用
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
