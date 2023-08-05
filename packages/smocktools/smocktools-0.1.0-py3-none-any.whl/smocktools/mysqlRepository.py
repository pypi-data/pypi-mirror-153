#!/usr/bin/env python
# encoding=utf-8

import time
from sshtunnel import SSHTunnelForwarder
import pymysql
from functools import wraps
import traceback

class MysqlRepository:

    def mysql_retry_wrapper(max_retry=100, exception=(pymysql.Error,), sleep_time = 10):
        """
        max_retry : 最大重试次数
        exception : 捕获的异常类型，其他类型则直接抛出

        expm:@mysql_retry_wrapper(max_retry=100,exception=(pymysql.Error,))
        """
        def decorator(method):
            @wraps(method)
            def wrapper(self,*args, **kwargs):
                for i in range(max_retry + 1):
                    try:
                        res = method(self,*args, **kwargs)
                    except exception:
                        print(traceback.format_exc() + f"at {i + 1} time retry")
                        # log
                        
                        time.sleep(sleep_time) #n秒后重试

                        if i == max_retry: #超过最大次数还是继续抛出异常
                            raise exception

                        self.reConn(reTryTime=100,sleepTime=10) # 重新初始化conn
                    else:
                        return res
            return wrapper
        return decorator

    def __init__(self,host,user,passwd,database,isSSH=False,ssh_port=22,ssh_ip="127.0.0.1",ssh_user=None,ssh_passwd=None):
        self.host = host
        self.user = user
        self.passwd=passwd
        self.database=database
        self.isSSH=isSSH
        self.ssh_port=ssh_port
        self.ssh_ip=ssh_ip
        self.ssh_user=ssh_user
        self.ssh_passwd=ssh_passwd
        self.conn=None
        self.cursor=None
        self.server=None

        self._initConn()
        self.cursor = self.conn.cursor()

    def _initConn(self):
        """
        初始化conn
        """
        self.isSSH=self.isSSH
        if self.isSSH==False:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                database=self.database,
                charset='utf8'
                )

        else:
            self.server = SSHTunnelForwarder(
                (self.ssh_ip, 22), 
                ssh_password=self.ssh_passwd, 
                ssh_username=self.ssh_user, 
                remote_bind_address=('127.0.0.1', int(self.ssh_port))) 
            self.server.start()
            print('SSH连接成功')
            self.conn = pymysql.connect(
                host=self.host,
                port=self.server.local_bind_port,
                user=self.user,
                passwd=self.passwd,
                database=self.database,
                charset='utf8')
            print('mysql数据库连接成功')

    def reConn(self,reTryTime=3,sleepTime=10):
        """
        重新链接数据库
        当数据库丢失的时候，ping会自动重连。可以对抗mysql暂时无服务，也不需要重新获取游标。
        """
        for i in range(1,reTryTime+1):
            try:
                self.conn.ping(reconnect=True)
                self.cursor = self.conn.cursor() # 重新获取游标（可以不获取，只要conn没有被重新初始化）
            except:
                print(traceback.format_exc() + f"db reconn at {i + 1} time retry")
                # log
                time.sleep(sleepTime) #n秒后重试
            else:
                break
            

    @mysql_retry_wrapper(max_retry=10,exception=(pymysql.Error,))
    def get_one(self,sql,params=None):
        self.cursor.execute(sql,params)
        result = self.cursor.fetchone()
        return result



    def __del__(self):
        if self.isSSH:
            self.server.close()
        self.conn.close()
