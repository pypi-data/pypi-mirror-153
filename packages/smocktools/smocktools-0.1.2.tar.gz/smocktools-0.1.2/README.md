# Tools Package

This is a package. You can use

[Github-flavored Markdown](https://github.com/smockgithub/smocktools)

MysqlRepository 是mysql工具类，为了特殊情况下的稳定性要求，进行了链接丢失的重新链接补偿。

使用方法：
```
pip install smocktools
```

```
from smocktools import MysqlRepository

r = MysqlRepository("localhost","root","123456","test")
```