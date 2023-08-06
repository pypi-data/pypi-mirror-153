# -*- coding: UTF-8 -*-

# CommonUtils

1. 修改setup中的版本

2. python setup.py sdist build

3. twine upload --skip-existing dist/*


### 项目Python版本

pip的一些操作

# 升级依赖包
pip install --upgrade BeanCommonUtils

# 安装依赖包
pip install -r requirements.txt

# 更改依赖包文件
pip freeze > requirements.txt


### Version 0.3
修改日志工具

### Version 1.0.1
date_utils add compute_special_time_timestamp 按指定格式的时间的字符串入参, 返回它的时间戳(精度毫秒)