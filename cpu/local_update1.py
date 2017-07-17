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
name = "no name"
ops_name = "no name"
filters = [
{
	'Name': 'instance-id',
	'Values': ['i-a6a64f3f']
	}
]
ec2 = boto3.resource('ec2')
ops = boto3.client('opsworks')
stack_list = ops.describe_stacks()
opswork_id = {"no name": "null","Docker Registry": "Docker Registry","Count Cluster V2 VPC": "Count Cluster V2 VPC"}
for i in stack_list['Stacks']:
	opswork_id[i['Name']] = i['StackId']
item_count = 0
account_id = '1234'
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
		except pymysql.err.IntegrityError as e:
			cur.execute("SELECT start_time,stop_time,number_of_hours FROM instances where instance_id='i-a6a64f3f'")
			result_set = cur.fetchall()
			current_time = datetime.datetime.utcnow()
			for i in result_set:
				time1, time2,old_time =i
			number_of_hours = int((abs((time1-time2).total_seconds()) / 3600) + .5)
			if old_time == None:
				old_time = 0
			print number_of_hours
			cur.execute("""UPDATE instances SET start_time=%s ,stop_time=%s ,number_of_hours=%s WHERE instance_id=%s """, (current_time,"NULL",(old_time+number_of_hours)))
		conn.commit()