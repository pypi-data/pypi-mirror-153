
import sys,os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)

import time
from smocktools_pkg.mysqlRepository import MysqlRepository

r = MysqlRepository("localhost","root","123456","test")

res = r.get_one("select * from test_table1")

for i in range(1,3):
    res = r.get_one("select * from test_table1")
    print("成功"+str(i))
    time.sleep(1)

print(1)