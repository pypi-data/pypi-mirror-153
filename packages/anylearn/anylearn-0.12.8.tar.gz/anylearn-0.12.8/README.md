# anylearn-sdk
为AnyLearn深度学习系统设计的SDK，用于支持基于python的代码调用方式，并在上层扩展复杂应用。

![UnitTestLinux](https://github.com/Dmagine/Anylearn-sdk/workflows/UnitTestLinux/badge.svg)
![UnitTestWindows](https://github.com/thulab/Anylearn-sdk/workflows/UnitTestWindows/badge.svg)
![Docs](https://github.com/thulab/Anylearn-sdk/workflows/Docs/badge.svg)
![DocsDev](https://github.com/thulab/Anylearn-sdk/workflows/DocsDev/badge.svg)
![Sync2thulab](https://github.com/Dmagine/Anylearn-sdk/workflows/sync2thulab/badge.svg)

### 在线用户手册
[稳定版 (`master`)](https://thulab.github.io/Anylearn-sdk/)
|
[开发版 (`dev`)](https://thulab.github.io/Anylearn-sdk/nightly/)

### Dev
Virtual env
```shell
python3 -m venv venv
source venv/bin/activate
```
Dependencies
```shell
python -m pip install -r requirements_dev.txt
python setup.py install
```

### Test
```shell
pytest
```

### Build
```shell
python setup.py sdist
python setup.py bdist_wheel
```
