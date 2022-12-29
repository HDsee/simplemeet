import mysql.connector.pooling
import mysql.connector
# 讀取.env的隱藏資料
from dotenv import load_dotenv
import os
import redis
import logging

logging.basicConfig(level=logging.INFO)

rdsHost = os.getenv("rdsHost")
rdsDatabease = os.getenv("rdsDatabase")
rdsUser = os.getenv("rdsUser")
rdsPassword = os.getenv("rdsPassword")
s3ID = os.getenv("s3ID")
s3Key = os.getenv("s3Key")
redisHost = os.getenv("redisHost")


connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="db",
                                                   pool_size=3,
                                                   host=rdsHost,
                                                   user=rdsUser,
                                                   password=rdsPassword,
                                                   database=rdsDatabease,
                                                   port=3306)


redisDb = redis.Redis(host=redisHost, port=6379)
# redisDb = redis.Redis(host="localhost", port=6379)