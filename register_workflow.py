import boto3
from botocore.exceptions import ClientError
from config import SWFConfig

swf = boto3.client('swf')

# Register a workflow
try:
	swf.register_workflow_type(
		domain = SWFConfig.DOMAIN,
		name = SWFConfig.WORKFLOW,
		version = SWFConfig.WORKFLOW_VERSION,
		description = 'Pour tester la création de workflow depuis python',
		defaultTaskStartToCloseTimeout=str(3600),
		defaultExecutionStartToCloseTimeout=str(24*3600),
		defaultChildPolicy = "TERMINATE",
		defaultTaskList={
					'name': SWFConfig.TASK_LIST_NAME
			},
	)
	print(f"{SWFConfig.WORKFLOW} created !")
except ClientError as e:
	print('Error workflow registration: ', e.response.get('Error', {}).get('Code'))

# Register an activity type
try:
	for activity_type in SWFConfig.ACTIVITY_LIST:
		swf.register_activity_type(
			domain=SWFConfig.DOMAIN,
			name=activity_type,
			version=SWFConfig.WORKFLOW_VERSION,
			description=f"Activity type {activity_type}",
			defaultTaskHeartbeatTimeout="900",
			defaultTaskScheduleToStartTimeout="120",
			defaultTaskScheduleToCloseTimeout="3800",
			defaultTaskStartToCloseTimeout="3600",
				defaultTaskList={"name": SWFConfig.TASK_LIST_NAME }
		)
		print("Worker created")
except ClientError as e:
	print('Error in registering activity: ', e.response.get('Error', {}).get('Code'))
