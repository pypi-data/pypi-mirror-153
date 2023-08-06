# ossctl

OSS command line controller

# 打包上传
```bash

python3 -m pip install --upgrade setuptools wheel twine build

python3 -m build

python3 -m twine upload dist/*
```
# 下载使用
```bash
pip install ossctl
```
```python
python -m ossctl -h
```