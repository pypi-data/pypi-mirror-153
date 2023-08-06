# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toeplitzlda',
 'toeplitzlda.benchmark',
 'toeplitzlda.classification',
 'toeplitzlda.usup_replay']

package_data = \
{'': ['*']}

install_requires = \
['blockmatrix>=0.2.0,<0.3.0', 'numpy>=1.22.1,<2.0.0', 'scikit-learn>=1.0,<2.0']

extras_require = \
{'neuro': ['pandas>=1.4.0,<2.0.0',
           'mne>=0.24.1,<0.25.0',
           'moabb>=0.4.4,<0.5.0',
           'seaborn>=0.11.2,<0.12.0'],
 'solver': ['toeplitz==0.3.2']}

setup_kwargs = {
    'name': 'toeplitzlda',
    'version': '0.2.6',
    'description': 'Implementation of LDA using a block-Toeplitz structured covariance matrix for stationary spatiotemporal data.',
    'long_description': '# ToeplitzLDA\n\nCode for the ToeplitzLDA classifier proposed in [here](https://arxiv.org/abs/2202.02001).\nThe classifier conforms sklearn and can be used as a drop-in replacement for other LDA\nclassifiers. For in-depth usage refer to the learning from label proportions (LLP) example\nor the example script.\n\nNote we used Ubuntu 20.04 with python 3.8.10 to generate our results.\n\n## Getting Started / User Setup\n\nIf you only want to use this library, you can use the following setup. Note that this\nsetup is based on a fresh Ubuntu 20.04 installation.\n\n### Getting fresh ubuntu ready\n\n```bash\napt install python3-pip python3-venv\n```\n\n### Python package installation\n\nIn this setup, we assume you want to run the examples that actually make use of real EEG\ndata or the actual unsupervised speller replay. If you only want to employ `ToeplitzLDA`\nin your own spatiotemporal data / without `mne` and `moabb` then you can remove the\npackage extra `neuro`, i.e. `pip install toeplitzlda` or `pip install toeplitzlda[solver]`\n\n0. (Optional) Install fortran Compiler. On ubuntu: `apt install gfortran`\n1. Create virtual environment: `python3 -m venv toeplitzlda_venv`\n2. Activate virtual environment: `source toeplitzlda_venv/bin/activate`\n3. Install toeplitzlda: `pip install toeplitzlda[neuro,solver]`, if you dont have a\n   fortran compiler: `pip install toeplitzlda[neuro]`\n\n### Check if everything works\n\nEither clone this repo or just download the `scripts/example_toeplitz_lda_bci_data.py`\nfile and run it: `python example_toeplitz_lda_bci_data.py`. Note that this will\nautomatically download EEG data with a size of around 650MB.\n\nAlternatively, you can use the `scripts/example_toeplitz_lda_generated_data.py` where\nartificial data is generated. Note however, that only stationary background noise is\nmodeled and no interfering artifacts as is the case in, e.g., real EEG data. As a result,\nthe _overfitting_ effect of traditional slda on these artifacts is reduced.\n\n## Using ToeplitzLDA in place of traditional shrinkage LDA from sklearn\n\nIf you have already your own pipeline, you can simply add `toeplitzlda` as a dependency in\nyour project and then replace sklearns LDA, i.e., instead of:\n\n```python\nfrom sklearn.discriminant_analysis import LinearDiscriminantAnalysis\nclf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto")  # or eigen solver\n```\n\nuse\n\n```python\nfrom toeplitzlda.classification import ToeplitzLDA\nclf = ToeplitzLDA(n_channels=your_n_channels)\n```\n\nwhere `your_n_channels` is the number of channels of your signal and needs to be provided\nfor this method to work.\n\nIf you prefer using sklearn, you can only replace the covariance estimation part, note\nhowever, that this in practice (on our data) yields worse performance, as sklearn\nestimates the class-wise covariance matrices and averages them afterwards, whereas we\nremove the class-wise means and the estimate one covariance matrix from the pooled data.\n\nSo instead of:\n\n```python\nfrom sklearn.discriminant_analysis import LinearDiscriminantAnalysis\nclf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto")  # or eigen solver\n```\n\nyou would use\n\n```python\nfrom sklearn.discriminant_analysis import LinearDiscriminantAnalysis\nfrom toeplitzlda.classification.covariance import ToepTapLW\ntoep_cov = ToepTapLW(n_channels=your_n_channels)\nclf = LinearDiscriminantAnalysis(solver="lsqr", covariance_estimator=toep_cov)  # or eigen solver\n```\n\n## Development Setup\n\nWe use a fortran compiler to provide speedups for solving block-Toeplitz linear equation\nsystems. If you are on ubuntu you can install `gfortran`.\n\nWe use `poetry` for dependency management. If you have it installed you can simply use\n`poetry install` to set up the virtual environment with all dependencies. All extra\nfeatures can be installed with `poetry install -E solver -E neuro`.\n\nIf setup does not work for you, please open an issue. We cannot provide in-depth support\nfor many different platforms, but could provide a\n[singularity](https://sylabs.io/guides/3.5/user-guide/introduction.html) image.\n\n## Learning from label proportions\n\nUse the `run_llp.py` script to apply ToeplitzLDA in the LLP scenario and create the\nresults file for the different preprocessing parameters. These can then be visualized\nusing `visualize_llp.py` to create the plots shown in our publication. Note that running\nLLP takes a while and the two datasets will be downloaded automatically and are\napproximately 16GB in size. Alternatively, you can use the results provided by us that are\nstored in `scripts/usup_replay/provided_results` by moving/copying them to the location\nthat `visualize_llp.py` looks for.\n\n## ERP benchmark\n\nThis is not yet available.\n\nNote this benchmark will take quite a long time if you do not have access to a computing\ncluster. The public datasets (including the LLP datasets) total a size of approximately\n120GB.\n\nBLOCKING TODO: How should we handle the private datasets?\n\n- [ ] Split benchmark into public and private/closed classes\n- [ ] Can we provide the code for private datasets without the data? Or is that too\n      sensitive?\n\n## FAQ\n\n### Why is my classification performance for my stationary spatiotemporal data really bad?\n\nCheck if your data is in _channel-prime_ order, i.e., in the flattened feature vector, you\nfirst enumerate over all channels (or some other spatially distributed sensors) for the\nfirst time point and then for the second time point and so on. If this is not the case,\ntell the classifier: e.g. `ToeplitzLDA(n_channels=16, data_is_channel_prime=False)`\n\n### I dont know if my data is stationary. How can I find out?\n\nWe do not provide any statistical testing or other facilities to check for stationarity.\nHowever, we use the `blockmatrix` package (disclaimer: also provided by us), which can\nvisualize your covariance matrix in a way that you can see if stationarity is a reasonable\nassumption or not. Note however, sometimes your data will look non-stationary due to,\ne.g., artifacts, even though your underlying process is stationary. This often happens if\nthe number of data samples to estimate the covariance is small. However, in our data it\nthen is often better to enforce stationarity anyhow, as you can avoid overfitting on the\n_presumably_ non-stationary observed data.\n\n## Further Work / Todos\n\n- [ ] Example how to check data for stationarity. Maybe better in `blockmatrix` package.\n',
    'author': 'Jan Sosulski',
    'author_email': 'mail@jan-sosulski.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jsosulski/toeplitzlda',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
