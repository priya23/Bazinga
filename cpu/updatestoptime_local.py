import boto3
import logging
import sys
import datetime
import rds_config
import pymysql
rds_host  = "127.0.0.1"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
port = 3306
server_address = (rds_host, port)
conn = pymysql.connect(rds_host, user='root', db='ops', connect_timeout=5)
current_time =datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
with conn.cursor() as cur:
	cur.execute("""UPDATE instances SET  stop_time=%s WHERE instance_id=%s """, (current_time,'i-a6a64f3f'))
	cur.commit()