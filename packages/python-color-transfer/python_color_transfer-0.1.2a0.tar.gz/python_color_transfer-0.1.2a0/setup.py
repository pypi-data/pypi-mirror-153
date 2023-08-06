# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_color_transfer']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19,<2.0', 'opencv-python>=4.2,<5.0']

setup_kwargs = {
    'name': 'python-color-transfer',
    'version': '0.1.2a0',
    'description': 'Three methods of color transfer implemented in python.',
    'long_description': '# Color Transfer in Python\n\nThree methods of color transfer implemented in Python.\n\n\n## Output Examples\n\n| Input image  | Reference image  | Mean std transfer | Lab mean transfer | Pdf transfer + Regrain |\n|--------------|------------|-------------------|-------------------|------------------------|\n| ![example1_input](https://i.imgur.com/slFs7uz.jpeg) | ![example1_ref](https://i.imgur.com/CbcmZcW.png) | ![example1_mt](https://i.imgur.com/6NW8cgf.jpeg)         | ![example1_lt](https://i.imgur.com/M9iBNdJ.jpeg)         | ![example1_pdf-reg](https://i.imgur.com/4RUpleJ.jpeg)             |\n| ![example2_input](https://i.imgur.com/3f92VzO.jpeg) | ![example2_ref](https://i.imgur.com/FE6fSiG.jpeg) | ![example2_mt](https://i.imgur.com/ssmM63F.jpeg)         | ![example2_lt](https://i.imgur.com/KXrFWbh.jpeg)         | ![example2_pdf-reg](https://i.imgur.com/MrslCTI.jpeg)             |\n| ![example1_input](https://i.imgur.com/PHtfrPk.png) | ![example1_ref](https://i.imgur.com/LULa5k0.png) | ![example1_mt](https://i.imgur.com/RAYarUL.jpeg)         | ![example1_lt](https://i.imgur.com/ueoePsi.jpeg)         | ![example1_pdf-reg](https://i.imgur.com/rYHJW47.jpeg)             |\n| ![example1_input](https://i.imgur.com/xCFLWda.png) | ![example1_ref](https://i.imgur.com/HZsiqyQ.jpeg) | ![example1_mt](https://i.imgur.com/jxeidOD.jpeg)         | ![example1_lt](https://i.imgur.com/GIUz83F.jpeg)         | ![example1_pdf-reg](https://i.imgur.com/faqeIdT.jpeg)             |\n\n## Methods\n\nLet input image be $I$, reference image be $R$ and output image be $O$.\nLet $f{I}(r, g, b)$, $f{R}(r, g, b)$ be probability density functions of $I$ and $R$\'s rgb values. \n\n- **Mean std transfer**\n\n    $$O = (I - mean(I)) / std(I) \\* std(R) + mean(R).$$\n\n- **Lab mean transfer**[^1]\n\n    $$I\' = rgb2lab(I)$$\n    $$R\' = rgb2lab(R)$$\n    $$O\' = (I\' - mean(I\')) / std(I\') \\* std(R\') + mean(R\')$$\n    $$O = lab2rgb(O\')$$\n\n- **Pdf transfer**[^2]\n\n    $O = t(I)$, where $t: R^3-> R^3$ is a continous mapping so that $f{t(I)}(r, g, b) = f{R}(r, g, b)$. \n\n\n## Requirements\n- 🐍 [python>=3.6](https://www.python.org/downloads/)\n\n\n## Installation\n\n### From PyPi\n\n```bash\npip install python-color-transfer\n```\n\n### From source\n\n```bash\ngit clone https://github.com/pengbo-learn/python-color-transfer.git\ncd python-color-transfer\n\npip install -r requirements.txt\n```\n\n## Demo\n\n- To replicate the results in [Output Examples](<#output-examples> "Output Examples"), run:\n\n```bash\npython demo.py \n```\n\n<details>\n  <summary>Output</summary>\n\n```\ndemo_images/house.jpeg: 512x768x3\ndemo_images/hats.png: 512x768x3\nPdf transfer time: 1.47s\nRegrain time: 1.16s\nMean std transfer time: 0.09s\nLab Mean std transfer time: 0.09s\nSaved to demo_images/house_display.png\n\ndemo_images/fallingwater.png: 727x483x3\ndemo_images/autumn.jpg: 727x1000x3\nPdf transfer time: 1.87s\nRegrain time: 0.87s\nMean std transfer time: 0.12s\nLab Mean std transfer time: 0.11s\nSaved to demo_images/fallingwater_display.png\n\ndemo_images/tower.jpeg: 743x1280x3\ndemo_images/sunset.jpg: 743x1114x3\nPdf transfer time: 2.95s\nRegrain time: 2.83s\nMean std transfer time: 0.23s\nLab Mean std transfer time: 0.21s\nSaved to demo_images/tower_display.png\n  \ndemo_images/scotland_house.png: 361x481x3\ndemo_images/scotland_plain.png: 361x481x3\nPdf transfer time: 0.67s\nRegrain time: 0.49s\nMean std transfer time: 0.04s\nLab Mean std transfer time: 0.22s\nSaved to demo_images/scotland_display.png\n```\n\n</details>\n\n\n## Usage\n\n```python\nfrom pathlib import Path\n\nimport cv2\nfrom python_color_transfer.color_transfer import ColorTransfer\n\n# Using demo images\ninput_image = \'demo_images/house.jpeg\'\nref_image = \'demo_images/hats.png\'\n\n# input image and reference image\nimg_arr_in = cv2.imread(input_image)\nimg_arr_ref = cv2.imread(ref_image)\n\n# Initialize the class\nPT = ColorTransfer()\n\n# Pdf transfer\nimg_arr_pdf_reg = PT.pdf_tranfer(img_arr_in=img_arr_in,\n                             img_arr_ref=img_arr_ref,\n                             regrain=True)\n# Mean std transfer\nimg_arr_mt = PT.mean_std_transfer(img_arr_in=img_arr_in,\n                                  img_arr_ref=img_arr_ref)\n# Lab mean transfer\nimg_arr_lt = PT.lab_transfer(img_arr_in=img_arr_in, img_arr_ref=img_arr_ref)\n\n# Save the example results\nimg_name = Path(input_image).stem\nfor method, img in [(\'pdf-reg\', img_arr_pdf_reg), (\'mt\', img_arr_mt),\n                   (\'lt\', img_arr_lt)]:\n    cv2.imwrite(f\'{img_name}_{method}.jpg\', img)\n```\n\n\n[^1]: Lab mean transfer: [Color Transfer between Images](https://www.cs.tau.ac.il/~turkel/imagepapers/ColorTransfer.pdf) by Erik Reinhard, Michael Ashikhmin, Bruce Gooch and Peter Shirley.\\\n    [Open source\'s python implementation](https://github.com/chia56028/Color-Transfer-between-Images)\n\n[^2]: Pdf transfer: [Automated colour grading using colour distribution transfer](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.458.7694&rep=rep1&type=pdf) by F. Pitie , A. Kokaram and R. Dahyot.\\\n    [Author\'s matlab implementation](https://github.com/frcs/colour-transfer)\n',
    'author': 'pengbo-learn',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
