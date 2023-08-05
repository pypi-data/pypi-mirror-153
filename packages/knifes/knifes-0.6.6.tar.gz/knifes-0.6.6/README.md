https://pypi.org/project/knifes/

包升级：
修改版本号
rm -r dist && python -m build && python -m twine upload dist/*
rm -r dist && rm -r build && python -m build && python -m twine upload dist/*


项目更新包：
pip install knifes --index-url https://pypi.python.org/simple -U


