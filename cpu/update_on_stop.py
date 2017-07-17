import boto3
import logging
import sys
import datetime
import rds_config
import pymysql
rds_host  = "fdstage-shard7-vpc.cwcfhlpilw8g.us-east-1.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
port = 3306
#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)
server_address = (rds_host, port)
try:
  conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
  logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
  sys.exit()
logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

current_time =datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
def lambda_handler(event, context):
	with conn.cursor() as cur:
		try:
			cur.execute("""UPDATE instances SET  stop_time=%s WHERE instance_id=%s """, (current_time,event['detail']['instance-id']))
		except Exception as e:
			print str(e)
		conn.commit()