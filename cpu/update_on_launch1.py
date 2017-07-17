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
name = "no name"
ops_name = "no name"
def lambda_handler(event, context):
  filters = [
      {
        'Name': 'instance-id',
        'Values': [event['detail']['instance-id']]
      }
  ]
	ec2 = boto3.resource('ec2')
	ops = boto3.client('opsworks')
	stack_list = ops.describe_stacks()
	opswork_id = {"no name": "null","Docker Registry": "Docker Registry"}
	for i in stack_list['Stacks']:
		opswork_id[i['Name']] = i['StackId']
	item_count = 0
	account_id = context.invoked_function_arn.split(':')[4]
	ins = ec2.instances.filter(Filters=filters)
	with conn.cursor() as cur:
		for i in ins:
			if i.tags is not None:
				for t in i.tags:
					if(t['Key'] == 'opsworks:stack'):
						ops_name = t['Value']
					if(t['Key'] == 'Name'):
						name = t['Value']
			else:
				print "tags is none"
			print i.id
			time = (i.launch_time).strftime('%y-%m-%d %H:%M:%S')
			try:
				cur.execute("""INSERT INTO instances (aws_account_id,name,opswork_id,instance_id,instance_type,start_time,days_elapsed,acknowledgement)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (account_id,name,opswork_id[ops_name],i.id,i.instance_type,time,-1,0))
			except IntegrityError as e:
				cur.execute("SELECT start_time,stop_time FROM instances where instance_id='i-a6a64f3f'")
			result_set = cur.fetchall()
			print result_set
		conn.commit()