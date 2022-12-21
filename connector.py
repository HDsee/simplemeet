import mysql.connector.pooling
import mysql.connector
# 讀取.env的隱藏資料
from dotenv import load_dotenv
import os

rdsHost = os.getenv("rdsHost")
rdsDatabease = os.getenv("rdsDatabase")
rdsUser = os.getenv("rdsUser")
rdsPassword = os.getenv("rdsPassword")
s3ID = os.getenv("s3ID")
s3Key = os.getenv("s3Key")


connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="db",
                                                   pool_size=3,
                                                   host=rdsHost,
                                                   user=rdsUser,
                                                   password=rdsPassword,
                                                   database=rdsDatabease,
                                                   port=3306)

