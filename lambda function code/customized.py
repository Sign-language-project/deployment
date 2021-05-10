import boto3

ec2 = boto3.resource('ec2')

instance = ec2.create_instances(
    BlockDeviceMappings=[
        {
            
            'Ebs': {
                'DeleteOnTermination': True,
                'Iops': 2000,
                'SnapshotId': 'snap-06dc430e03851699a',
                'VolumeSize': 8,
                'VolumeType':'gp2',
                
                'Encrypted': False
            }
        },
    ],
    ImageId='ami-0f447354763f0eaac',
    InstanceType='t3.micro',
    
    
    KeyName='deploy',
    MaxCount=2,
    MinCount=1,
    
    Monitoring={
        'Enabled': False
    },
    Placement={
        'AvailabilityZone': 'eu-south-1a'
       
    }
    ,
    SecurityGroupIds=[
        'sg-0c4e00f01dea6a2ba',
    ],
    SecurityGroups=[
        'open test',
    ],
    SubnetId='subnet-e7977a8e',
    
    UserData= """!/bin/bash
              yum update -y
              yum install -y httpd24
              service httpd start
              chkconfig httpd on
             
              shutdown -h +5""",
    
    InstanceInitiatedShutdownBehavior= 'terminate',
    
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': True,
            'DeleteOnTermination': True 
        }
    ]
  
)