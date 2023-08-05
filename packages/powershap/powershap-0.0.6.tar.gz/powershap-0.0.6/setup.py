# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['powershap', 'powershap.shap_wrappers']

package_data = \
{'': ['*']}

install_requires = \
['catboost>=1.0.5,<2.0.0',
 'numpy>=1.20,<1.21',
 'pandas>=1.3,<1.4',
 'shap>=0.40.0,<0.41.0',
 'sklearn>=0.0,<0.1',
 'statsmodels>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'powershap',
    'version': '0.0.6',
    'description': 'Feature selection using statistical significance of shap values',
    'long_description': '\t\n<p align="center">\n    <a href="#readme">\n        <img alt="PowerShap logo" src="https://raw.githubusercontent.com/predict-idlab/powershap/main/powershap_full_scaled.png" width=70%>\n    </a>\n</p>\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/powershap.svg)](https://pypi.org/project/powershap/)\n[![support-version](https://img.shields.io/pypi/pyversions/powershap)](https://img.shields.io/pypi/pyversions/powershap)\n[![codecov](https://img.shields.io/codecov/c/github/predict-idlab/powershap?logo=codecov)](https://codecov.io/gh/predict-idlab/powershap)\n[![Code quality](https://img.shields.io/lgtm/grade/python/github/predict-idlab/powershap?label=code%20quality&logo=lgtm)](https://lgtm.com/projects/g/predict-idlab/powershap/context:python)\n[![Downloads](https://pepy.tech/badge/powershap)](https://pepy.tech/project/powershap)\n[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?)](http://makeapullrequest.com)\n[![Testing](https://github.com/predict-idlab/powershap/actions/workflows/test.yml/badge.svg)](https://github.com/predict-idlab/powershap/actions/workflows/test.yml)\n[![DOI](https://zenodo.org/badge/470633431.svg)](https://zenodo.org/badge/latestdoi/470633431)\n\n> *powershap* is a **feature selection method** that uses statistical hypothesis testing and power calculations on **Shapley values**, enabling fast and intuitive wrapper-based feature selection.  \n\n## Installation ⚙️\n\n| [**pip**](https://pypi.org/project/powershap/) | `pip install powershap` | \n| ---| ----|\n\n## Usage 🛠\n\n*powershap* is built to be intuitive, it supports various models including linear, tree-based, and even deep learning models.  \n<!-- It is also implented as sklearn `Transformer` component, allowing convenient integration in `sklearn` pipelines. -->\n\n```py\nfrom powershap import PowerShap\nfrom catboost import CatBoostClassifier\n\nX, y = ...  # your classification dataset\n\nselector = PowerShap(\n    model=CatBoostClassifier(n_estimators=250, verbose=0, use_best_model=True)\n)\n\nselector.fit(X, y)  # Fit the PowerShap feature selector\nselector.transform(X)  # Reduce the dataset to the selected features\n\n```\n\n## Features ✨\n\n* default automatic mode\n* `scikit-learn` compatible\n* supports various models\n* insights into the feature selection method: call the `._processed_shaps_df` on a fitted `PowerSHAP` feature selector.\n* tested code!\n\n## Benchmarks ⏱\n\nCheck out our benchmark results [here](examples/results/).  \n\n## How does it work ⁉️\n\nPowershap is built on the core assumption that *an informative feature will have a larger impact on the prediction compared to a known random feature.*\n\n* Powershap trains multiple models with different random seeds on different subsets of the data. Each iteration it adds a random uniform feature to the dataset for training.\n* In a single iteration after training a model, powershap calculates the absolute Shapley values of all features, including the random feature. If there are multiple outputs or multiple classes, powershap uses the maximum across these multiple outputs. These values are then averaged for each feature, symbolising the impact of the feature in this iteration.\n* After performing all iterations, each feature then has an array of impacts. The impact array of each feature is then compared to the average of the random feature impact array using the percentile formula to provide a p-value. This tests whether the feature has a larger impact than the random feature and outputs a low p-value if true. \n* Powershap then outputs all features with a p-value below the provided threshold. The threshold is by default 0.01.\n\n\n### Automatic mode 🤖\n\nThe required number of iterations and the threshold values are hyperparameters of powershap. However, to *avoid manually optimizing the hyperparameters* powershap by default uses an automatic mode that automatically determines these hyperparameters. \n\n* The automatic mode first starts with executing powershap using ten iterations.\n* Then, for each feature powershap calculates the effect size and the statistical power of the test using a student-t power test. \n* Using the calculated effect size, powershap then calculates the required iterations to achieve a predefined power requirement. By default this is 0.99, which represents a false positive probability of 0.01.\n* If the required iterations are larger than the already performed iterations, powershap then further executes for the extra required iterations. \n* Afterward, powershap re-calculates the required iterations and it keeps re-executing until the required iterations are met.\n\n## Referencing our package :memo:\n\nIf you use *powershap* in a scientific publication, we would highly appreciate citing us as:\n\n```bibtex\n@software{jarne_verhaeghe_2022_6490197,\n  author       = {Jarne Verhaeghe and\n                  Jeroen Van Der Donckt and\n                  Femke Ongenae and\n                  Sofie Van Hoecke},\n  title        = {predict-idlab/powershap: powershap v0.0.5.1},\n  month        = apr,\n  year         = 2022,\n  publisher    = {Zenodo},\n  version      = {powershap-v0.0.5.1},\n  doi          = {10.5281/zenodo.6490197},\n  url          = {https://doi.org/10.5281/zenodo.6490197}\n}\n```\n\nPaper is pending.\n\n---\n\n<p align="center">\n👤 <i>Jarne Verhaeghe, Jeroen Van Der Donckt</i>\n</p>\n',
    'author': 'Jarne Verhaeghe, Jeroen Van Der Donckt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/predict-idlab/powershap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
