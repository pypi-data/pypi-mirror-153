# upswing-utility-package

## installing from github
```
pip install git+https://github.com/Upswing-cognitive-hospitality-solution/upswing-utility-package#egg=upswingutil
```

## For deployment on PyPI
### build package
```python setup.py sdist bdist_wheel```

### upload package
```twine upload dist/*```
##### dependency: ```pip install twine```

### classifiers
https://pypi.org/classifiers/


#### install from local
```
pip install upswingutil --no-index --find-links /Users/harsh/upswing/github/upswing-utility-package/dist
pip install upswingutil --no-index --find-links C:\Upswing\Projects\Code\upswing-utility-package\dist   

```