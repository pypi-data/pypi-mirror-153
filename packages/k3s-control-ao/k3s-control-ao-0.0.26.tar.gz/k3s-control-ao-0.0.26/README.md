# k3s-control-ao

定义访问k3s-control服务的接口

# 打包上传
```bash
rm -r dist

rm -r src/ddd_objects.egg-info

python3 -m pip install --upgrade setuptools wheel twine build

python3 -m build

python3 -m twine upload dist/*
```
# 下载使用
```bash
pip install k3s-control-ao
```
```python
import k3s_control_ao
```