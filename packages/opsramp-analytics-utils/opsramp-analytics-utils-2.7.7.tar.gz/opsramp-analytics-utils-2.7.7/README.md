## OpsRamp Analytics Utilities

This is the SDK for writing OpsRamp analytics apps. It is based on [dash](https://plotly.com/dash/), and it has a number of utility functions.

It contains [analysis wrapper project](https://github.com/opsramp/analysis-wrapper).

It is published on [Pypi](https://pypi.org/project/opsramp-analytics-utils/)

#### How to publish on Pypi

After make updates on SDK, modify the version in _setup.py_.

```
python setup.py sdist bdist_wheel
python -m twine upload dist/*

Note: if above command not works, then use below command
python -m twine upload --skip-existing dist/*
```

- To upgrade the sdk for your app
```
pip install --no-cache-dir --upgrade opsramp-analytics-utils
```
