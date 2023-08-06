https://pypi.org/project/knifes/

## 包升级
1. 修改版本号
2. rm -r dist && python -m build && python -m twine upload dist/*

## 项目更新包
pip install knifes --index-url https://pypi.python.org/simple -U

## 额外需要安装三方包

### ase
- cryptography
- pycrypto

### sms
- tencentcloud-sdk-python==3.0.600
