# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glcm_cupy', 'glcm_cupy.cross', 'glcm_cupy.glcm']

package_data = \
{'': ['*']}

install_requires = \
['scikit-image>=0.18.3,<0.19.0', 'tqdm>=4.63.0,<4.64.0']

setup_kwargs = {
    'name': 'glcm-cupy',
    'version': '0.1.9',
    'description': 'Binned GLCM 5 Features implemented in CuPy',
    'long_description': '# 📖[Wiki](https://eve-ning.github.io/glcm-cupy/)\n\n# GLCM Bin 5 on CuPy\n\nThis is a CuPy reimplementation of my `glcmbin5` [**on my other repository**](https://github.com/Eve-ning/glcmbin5).\n\nThis directly utilizes CUDA to speed up the processing of GLCM.\n\n# Installation\n\n**Python >= 3.7**\n\nFirst, you need to install this\n\n```shell\npip install glcm-cupy\n```\n\nThen, you need **CuPy**.\nYou need to [install CuPy manually](https://docs.cupy.dev/en/stable/install.html), \nas it\'s dependent on the version of CUDA you have.\n\nI recommend using `conda-forge` as it worked for me :)\n\nFor CUDA `11.6`, we use\n```shell\nconda install -c conda-forge cupy cudatoolkit=11.6\n```\n\nReplace the version you have on the arg.\n\n```shell\nconda install -c conda-forge cupy cudatoolkit=__._\n```\n\n# Usage\n\nThe usage is simple:\n\n```pycon\n>>> from glcm_cupy import GLCM\n>>> import numpy as np\n>>> from PIL import Image\n>>> ar = np.asarray(Image.open("image.jpg"))\n>>> ar.shape\n(1080, 1920, 3)\n>>> g = GLCM(...).run(ar)\n>>> g.shape\n(1074, 1914, 3, 8)\n```\n\nThe last dimension of `g` is the GLCM Features.\n\nTo retrieve a specific GLCM Feature:\n\n```pycon\n>>> from glcm_cupy import CONTRAST\n>>> g[..., CONTRAST].shape\n(1074, 1914, 3)\n```\n\nYou may also consider simply `glcm` if you\'re not reusing `GLCM()`\n```pycon\n>>> from glcm_cupy import glcm\n>>> g = glcm(ar, ...)\n```\n\n## **[Example: Processing an Image](examples/process_an_image/main.py)**\n\n## Features\n\nThese are the features implemented.\n\n- `HOMOGENEITY = 0`\n- `CONTRAST = 1`\n- `ASM = 2`\n- `MEAN = 3`\n- `VAR = 4`\n- `CORRELATION = 5`\n\nDon\'t see one you need? Raise an issue, I\'ll (hopefully) add it.\n\n## Radius & Step Size\n\n- The radius defines the window radius for each GLCM window.\n- The step size defines the distance between each window.\n  - If it\'s diagonal, it treats a diagonal step as 1. It\'s not the euclidean distance.\n\n## Binning\n\nTo reduce GLCM processing time, you can specify `bin_from` & `bin_to`.\n\nThis will bin the image from a range to another.\n\nI highly recommend using this to reduce time taken before raising it.\n\nE.g.\n\n> I have an RGB image with a max value of 255.\n> \n> I limit the max value to 31. This reduces the processing time.\n> \n> `GLCM(..., bin_from=256, bin_to=32).run(ar)`\n\nThe lower the max value, the smaller the GLCM required. Thus allowing for\nmore GLCMs to run concurrently.\n\n## Direction\n\nBy default we have the following directions to run GLCM on.\n\n- East: `Direction.EAST`\n- South East: `Direction.SOUTH_EAST`\n- South: `Direction.SOUTH`\n- South West: `Direction.SOUTH_WEST`\n\nFor each direction, the GLCM will be bi-directional.\n\nWe can specify only certain directions here.\n\n```pycon\n>>> from glcm_cupy import GLCM\n>>> GLCM()\n>>> g = GLCM(directions=(Direction.SOUTH_WEST, Direction.SOUTH))\n```\n\nThe result of these directions will be averaged together.\n\n# Notes\n\n> Q: Why did my image shrink?\n> \n> The image shrunk due to `step_size` & `radius`.\n> \n> The amount of shrink per XY Dimension is\n> `size - 2 * step_size - 2 * radius`\n\n> Q: What\'s the difference between this and `glcmbin5`?\n> \n> This is the faster one, and easier to use.\n> I highly recommend avoiding `glcmbin5` as it has C++, which means you need to compile manually.\n> \n> It\'s the first version of GLCM I made.\n\n## CUDA Notes\n\n### Why is the kernel split into 4?\n\nThe kernel is split into 4 sections\n\n1) GLCM Creation\n2) Features (ASM, Contrast, Homogeneity, GLCM Mean I, GLCM Mean J)\n3) Features (GLCM Variance I, GLCM Variance J)\n4) Features (GLCM Correlation)\n\nThe reason why it\'s split is due to (2) being reliant on (1), and (3) on (2), ... .\n\nThere are some other solutions tried\n\n1) `__syncthreads()` will not work as we require to sync all blocks.\n    1) We can\'t put all calculations in a block due to the thread limit of 512, 1024, 2048.\n    2) We require 256 * 256 threads minimum to support a GLCM of max value 255.\n2) **Cooperative Groups** imposes a 24 block limit.\n\nThus, the best solution is to split the kernel.\n\n### Atomic Add\n\nThreads cannot write to a single pointer in parallel, information will be overwritten and lost. This is the **Race\nCondition**.\n\nIn order to avoid this, we use [**Atomic\nFunctions**](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#atomic-functions).\n\n> ... it is guaranteed to be performed without interference from other threads\n\n### Custom Atomic Add\n\n`Deprecated >=1.7`\n\nCurrently `atomicAdd()` doesn\'t have the signature to support `uint8` or `unsigned char`. We get this implementation\nfrom this [**StackOverflow\nAnswer**](https://stackoverflow.com/questions/5447570/cuda-atomic-operations-on-unsigned-chars)\n\n# Change Log\n\n## 1.6\n\nDropped dependency on J variables as I & J are always the same\n\n## 1.7\n\nFix issue with GLCM overflowing by making it `float32`\n\n## 1.8\n\nImplement Cross GLCM\n',
    'author': 'Evening',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Eve-ning/glcmbin5_cupy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
