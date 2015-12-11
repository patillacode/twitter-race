#!/usr/bin/env python
import redis

# redis conf
REDIS_IP = 'localhost'
REDIS_DB = 1
REDIS_POOL = redis.ConnectionPool(max_connections=500,
                                  host=REDIS_IP,
                                  db=REDIS_DB,
                                  port=6379)
REDIS = redis.Redis(connection_pool=REDIS_POOL)
