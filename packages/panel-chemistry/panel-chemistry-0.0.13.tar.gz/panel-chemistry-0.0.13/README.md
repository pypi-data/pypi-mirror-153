# 🧪 Panel-Chemistry

👨‍🔬📈🛠️🐍❤️

![Python Versions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue) ![Style Black](https://warehouse-camo.ingress.cmh1.psfhosted.org/fbfdc7754183ecf079bc71ddeabaf88f6cbc5c00/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f64652532307374796c652d626c61636b2d3030303030302e737667) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) ![Test Results](https://github.com/MarcSkovMadsen/panel-chemistry/actions/workflows/tests.yaml/badge.svg?branch=main) [![Follow on Twitter](https://img.shields.io/twitter/follow/MarcSkovMadsen.svg?style=social)](https://twitter.com/MarcSkovMadsen)

The purpose of the `panel-chemistry` project is to make it really easy for you  to do **exploratory data analysis** and **build powerful data and viz tools** within the domain of **Chemistry** using [Python](https://www.python.org/) and [HoloViz Panel](https://panel.holoviz.org/).

![Panel Chemistry Teaser](https://raw.githubusercontent.com/MarcSkovMadsen/panel-chemistry/main/assets/panel-chemistry-teaser.gif)

Check out the `panel-chemistry` examples on **Binder**

| Jupyter Notebook | Jupyter Labs | Panel Apps |
| - | - | - |
| [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?filepath=examples) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?urlpath=lab/tree/examples) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?urlpath=panel) |

## 🏁 Background

This project was started by the discussion [How to display JSME molecular editor with Panel?](https://discourse.holoviz.org/t/how-to-display-jsme-molecular-editor-with-panel/2306/12) in the [Panel Community Forum](https://discourse.holoviz.org/)

## 🏃 Getting Started

```bash
pip install panel-chemistry
```

or with `conda`

```bash
conda install -c conda-forge panel-chemistry
```

Run the below in a Notebook or using `panel serve NAME_OF_SCRIPT.py`.

```python
import panel as pn
from panel_chemistry.widgets import JSMEEditor

pn.extension("jsme", sizing_mode="stretch_width")
```

```python
smiles="N[C@@H](CCC(=O)N[C@@H](CS)C(=O)NCC(=O)O)C(=O)O"
editor = JSMEEditor(value=smiles, height=500, format="smiles")

editor.servable()
```

![JSME Editor](https://raw.githubusercontent.com/MarcSkovMadsen/panel-chemistry/main/assets/panel-chemistry-example.png)

## 👩‍🏫 Examples

Check out the `panel-chemistry` **reference guides** on **Binder**

| Guide | NB Viewer | Github Notebook | Jupyter Notebook | Jupyter Labs | Panel Apps |
| - | - | - | - | - | - |
| JSME Editor | [View](https://nbviewer.org/github/MarcSkovMadsen/panel-chemistry/blob/main/examples/reference/JSMEEditor.ipynb) | [View](https://github.com/MarcSkovMadsen/panel-chemistry/blob/main/examples/reference/JSMEEditor.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?filepath=examples/reference/JSMEEditor.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?urlpath=lab/tree/examples/reference/JSMEEditor.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?urlpath=panel/JSMEEditor) |
| NGL Viewer | [View](https://nbviewer.org/github/MarcSkovMadsen/panel-chemistry/blob/main/examples/reference/NGLViewer.ipynb) | [View](https://github.com/MarcSkovMadsen/panel-chemistry/blob/main/examples/reference/NGLViewer.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?filepath=examples/reference/NGLViewer.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?urlpath=lab/tree/examples/reference/NGLViewer.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?urlpath=panel/NGLViewer) |
| PDBe_MolStar | [View](https://nbviewer.org/github/MarcSkovMadsen/panel-chemistry/blob/main/examples/reference/PDBe_MolStar.ipynb) | [View](https://github.com/MarcSkovMadsen/panel-chemistry/blob/main/examples/reference/PDBe_MolStar.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?filepath=examples/reference/PDBe_MolStar.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?urlpath=lab/tree/examples/reference/PDBe_MolStar.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?urlpath=panel/PDBe_MolStar) |
| Py3DMol Pane | [View](https://nbviewer.org/github/MarcSkovMadsen/panel-chemistry/blob/main/examples/reference/Py3DMol.ipynb) | [View](https://github.com/MarcSkovMadsen/panel-chemistry/blob/main/examples/reference/Py3DMol.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?filepath=examples/reference/Py3DMol.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?urlpath=lab/tree/examples/reference/Py3DMol.ipynb) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/marcskovmadsen/panel-chemistry/HEAD?urlpath=panel/Py3DMol) |

## 💡 Inspiration

- [Awesome Python Chemistry](https://github.com/lmmentel/awesome-python-chemistry)
- [Dash Bio](https://dash.plotly.com/dash-bio)
- [JSME Editor](https://jsme-editor.github.io) and [Test Page](https://jsme-editor.github.io/dist/JSME_test.html)
- [3DMol.js](https://3dmol.csb.pitt.edu/) and [py3Dmol](https://colab.research.google.com/drive/1T2zR59TXyWRcNxRgOAiqVPJWhep83NV_?usp=sharing)
- [RDKit](http://www.rdkit.org/)
- [RDKit IPython Tools](https://github.com/apahl/rdkit_ipynb_tools)

## 🎁 Contributing

If you want to contribute reach out via [Github Issues](https://github.com/MarcSkovMadsen/panel-chemistry/issues) or in the Contributor Community Forum on Gitter: https://gitter.im/panel-chemistry/community#

For more details see the [Developer Guide](DEVELOPER_GUIDE.md)

## FAQ

## 📰 Change Log

- 0.0.12: Add PDBeMolstar component and py.typed file
- 0.0.11: Add LICENSE and VERSION files to package. Now available on conda-forge
- 0.0.10: Update to Panel 0.12.6.
- 0.0.9: Add Py3DMol pane. Update to Panel 0.12.4.
