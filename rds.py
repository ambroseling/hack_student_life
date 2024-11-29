import boto3

# Specify the AWS region
ec2 = boto3.client('ec2', 
    region_name='us-east-1',
    aws_access_key_id='AKIAX3DNHCQLIDK3642P',
    aws_secret_access_key='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'
)

response = ec2.authorize_security_group_ingress(
    GroupId='sg-027a7473b05e8969d',
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 5432,
            'ToPort': 5432,
            'IpRanges': [
                {
                    'CidrIp': '174.89.161.177/32',
                    'Description': 'Local development access'
                },
            ],
        },
    ],
)