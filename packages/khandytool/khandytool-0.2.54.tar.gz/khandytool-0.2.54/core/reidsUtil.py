import redis
class RedisOper:
    def __init__(self, host, password, port,db):
        # 连接redis
        self.__redis = redis.StrictRedis(host=host, password=password, port=port,db=db)
    # 设置key-value
    def setKey(self, key, value):
        self.__redis.set(key, value)
    # 获取key-value
    def getKey(self, key):
        return self.__redis.get(key).decode()
    # 判断key是否存在
    def is_existsKey(self,key):
        # 返回1存在，0不存在
        return self.__redis.exists(key)
    # 添加集合操作
    def add_setKey(self,key,value):
        # 集合中存在该元素则返回0,不存在则添加进集合中，并返回1
        # 如果key不存在，则创建key集合，并添加元素进去,返回1
        return self.__redis.sadd(key,value)
    # 判断value是否在key集合中
    def is_Inset(self,key,value):
        '''判断value是否在key集合中，返回布尔值'''
        return self.__redis.sismember(key,value)
    # 关闭连接
    def close(self):
        self.__redis.close()