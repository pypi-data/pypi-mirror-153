#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import showlog
import redis
import time


class Basics:
    def __init__(
            self,
            con_info: dict = None,  # 连结信息，如果设置，将优先使用
            db: int = None,  # 需要连接的数据库，以数字为序号的，从0开始
            host=None,  # 连接的域名
            port=None,  # 连接的端口
            password=None,  # 连接的密码,
            max_connections=None
    ):
        # 初始化所有参数
        if con_info is not None:
            self.con_db = con_info.get('db', 0)
            self.host = con_info.get('host')
            self.port = con_info.get('port')
            self.pwd = con_info.get('password')
            self.max_connections = con_info.get('max_connections')
        else:
            if db is None:
                self.con_db = 0
            else:
                self.con_db = db
            self.host = host
            self.port = port
            self.pwd = password
            self.max_connections = max_connections
        self.pool = self.make_connect_pool()
        self.conn = self.connect()

    def make_connect_pool(
            self
    ):
        # 使用连接池连接，节省每次连接用的时间
        pool = redis.ConnectionPool(
            host=self.host,
            port=self.port,
            password=self.pwd,
            db=self.con_db,
            max_connections=self.max_connections
        )
        return pool

    def connect(
            self
    ):
        # 从连接池中拿出一个连接
        connection = redis.Redis(
            connection_pool=self.pool
        )
        return connection

    def delete_key(
            self,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        删除 key
        存在key且删除成功返回1，不存在key且删除失败返回0
        """
        while True:
            try:
                return self.conn.delete(key)  # 删除key
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def get_db_key_list(
            self,
            decode: bool = True,  # 返回内容解码
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        读取 库中键列表
        若有key，则返回key列表；若无key，则返回空列表
        """
        while True:
            try:
                inner_keys = list(self.conn.keys())
                if decode is False:
                    return inner_keys
                else:
                    key_list = list()
                    for key in inner_keys:
                        key_list.append(key.decode())
                    return key_list
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def get_list_key_values_count(
            self,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        获取 列表的 键的值元素数量
        """
        while True:
            try:
                return self.conn.llen(key)  # 获取列表的元素个数
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def read_list_key_values_all(
            self,
            key,
            decode: bool = True,  # 返回内容解码
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        读取 列表的 键的所有值列表
        """
        while True:
            try:
                if decode is False:
                    return self.conn.lrange(name=key, start=0, end=-1)
                else:
                    values_source = self.conn.lrange(name=key, start=0, end=-1)
                    values = list()
                    for each_value in values_source:
                        if each_value is not None:
                            values.append(each_value.decode())
                        else:
                            values.append(each_value)
                    return values
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def read_list_first_value(
            self,
            key,
            decode: bool = True,  # 返回内容解码
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        读取 列表的 第一个元素
        """
        while True:
            try:
                if decode is False:
                    return self.conn.lindex(key, 0)
                else:
                    source_value = self.conn.lindex(key, 0)
                    if source_value is None:
                        return source_value
                    else:
                        return source_value.decode()
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def read_list_last_value(
            self,
            key,
            decode: bool = True,  # 返回内容解码
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        """
        获取 列表的 最后一个元素
        """
        while True:
            try:
                if decode is False:
                    return self.conn.lindex(key, -1)
                else:
                    source_value = self.conn.lindex(key, -1)
                    if source_value is None:
                        return source_value
                    else:
                        return source_value.decode()
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def list_add_l(
            self,
            key,
            value,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 在list左侧添加值
        while True:
            try:
                return self.conn.lpush(key, value)
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def list_add_r(
            self,
            key,
            value,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 在list右侧添加值，作为队列使用时，一般在右侧添加
        while True:
            try:
                return self.conn.rpush(key, value)
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def list_pop_l(
            self,
            key,
            decode: bool = True,  # 返回内容解码
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 从左侧出队列，作为队列时，经常使用此方法
        while True:
            try:
                key_type = self.conn.type(key).decode()
                if key_type == 'list':
                    if decode is False:
                        return self.conn.lpop(key)
                    else:
                        return self.conn.lpop(key).decode()
                else:
                    return f'key type is not list, type is {key_type}'
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def list_pop_r(
            self,
            key,
            decode: bool = True,  # 返回内容解码
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 从右侧侧出队列
        while True:
            try:
                if decode is False:
                    return self.conn.rpop(key)
                else:
                    return self.conn.rpop(key).decode()
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def set_string(
            self,
            name,
            value,
            ex=None,
            px=None,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 设置键值，ex过期时间（秒），px过期时间（毫秒）
        while True:
            try:
                return self.conn.set(
                    name,
                    value,
                    ex=ex,
                    px=px,
                    nx=False,
                    xx=False
                )
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def get_string(
            self,
            name,
            decode: bool = True,  # 返回内容解码
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 获取键值
        while True:
            try:
                if decode is False:
                    return self.conn.get(name)
                else:
                    return self.conn.get(name).decode()
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def count_set(
            self,
            key,
            value,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 键 计数 设定值
        while True:
            try:
                return self.conn.set(name=key, value=value)
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def count_add(
            self,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 键 计数 增加1
        while True:
            try:
                return self.conn.incr(key)
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def count_reduce(
            self,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 键 计数 减少1
        while True:
            try:
                return self.conn.decr(key)
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def count_get(
            self,
            key,
            decode: bool = True,  # 返回内容解码
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 键 计数 获取值
        while True:
            try:
                if decode is False:
                    return self.conn.get(key)
                else:
                    count_value = self.conn.get(key)
                    if count_value is None:
                        return count_value
                    else:
                        return count_value.decode()
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    # -------------------- hash --------------------

    def hash_set(
            self,
            name,
            key,
            value,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 单个增加--修改(单个取出)--没有就新增，有的话就修改
        while True:
            try:
                return self.conn.hset(
                    name=name,
                    key=key,
                    value=value
                )
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def hash_delete(
            self,
            name,
            key,
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 单个增加--修改(单个取出)--没有就新增，有的话就修改
        while True:
            try:
                return self.conn.hdel(
                    name,
                    key
                )
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def hash_keys(
            self,
            name,
            decode: bool = True,  # 返回内容解码
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 取hash中所有的key
        while True:
            try:

                if decode is None:
                    return self.conn.hkeys(name=name)
                else:
                    res = self.conn.hkeys(
                        name=name
                    )
                    hkeys_list = list()
                    for each in res:
                        if each is not None:
                            hkeys_list.append(each.decode())
                        else:
                            hkeys_list.append(each)
                    return hkeys_list
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def hash_get(
            self,
            name,
            key,
            decode: bool = True,  # 返回内容解码
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 单个取hash的key对应的值
        while True:
            try:
                if decode is False:
                    return self.conn.hget(name=name, key=key)
                else:
                    data_source = self.conn.hget(
                        name=name,
                        key=key
                    )
                    if data_source is None:
                        return data_source
                    else:
                        return data_source.decode()
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def hash_get_many(
            self,
            name,
            key_list: list,
            decode: bool = True,  # 返回内容解码
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 多个取hash的key对应的值
        while True:
            try:
                if decode is False:
                    return self.conn.hmget(name=name, keys=key_list)
                else:
                    res_list = list()
                    data_source = self.conn.hmget(
                        name=name,
                        keys=key_list
                    )
                    for each in data_source:
                        if each is None:
                            res_list.append(each)
                        else:
                            res_list.append(each.decode())
                    return res_list
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e

    def hash_get_all(
            self,
            name,
            decode: bool = True,  # 返回内容解码
            auto_reconnect: bool = True,  # 自动重连
            reconnect_delay: int = 1  # 重连延时，单位为秒
    ):
        # 取出所有键值对
        res_list = dict()
        while True:
            try:
                key_type = self.conn.type(name=name)
                if key_type is None:
                    return
                elif 'hash' not in key_type.decode():
                    return
                else:
                    if decode is False:
                        return self.conn.hgetall(name=name)
                    else:
                        data_source = self.conn.hgetall(
                            name=name
                        )
                        if data_source is None:
                            return res_list
                        else:
                            for each_key, each_value in data_source.items():
                                res_list[each_key.decode()] = each_value.decode()
                            return res_list
            except redis.exceptions.ConnectionError as e:
                if auto_reconnect is True:
                    showlog.warning(f'连接失败，将在{reconnect_delay}秒后重连...')
                    time.sleep(1)
                    self.conn = self.connect()
                else:
                    return e
