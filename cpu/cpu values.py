import boto3
import logging


#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)
opswork_id = {}
filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
def lambda_handler(event, context): 
  account_id = context.invoked_function_arn.split(':')[4] 
  #generating list for opswork stack and corresponding id
  ops = boto3.client('opsworks')
  stack_list = ops.describe_stacks()
  opswork_id = {"no name": "null","Docker Registry": "null"}
  for i in stack_list['Stacks']:
    opswork_id[i['Name']] = i['StackId'] 
  ec2_client = boto3.resource('ec2')
  instances = ec2_client.instances.filter(Filters=filters)
  for i in instances:
    name = "no name"
    ops_name = "no name"
    if i.tags is not None:
      for t in i.tags:
        if(t['Key'] == 'opsworks:stack'):
          ops_name = t['Value']
        else:
          print "do nothing"
        if(t['Key'] == 'Name'):
          name = t['Value']
        else:
          print "do nothing"
    else:
        print "tags is none"
    print account_id  
    print name 
    print ops_name
    print i.id 
    print i.instance_type 
    print (i.launch_time).strftime('%Y-%m-%d %H:%M:%S')
    try:
      print opswork_id[ops_name]
    except:
      print "not found"