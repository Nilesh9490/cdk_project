from aws_cdk import (
    core
)
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
import aws_cdk.aws_rds as rds
import aws_cdk.aws_secretsmanager as secrets



class RDSStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str,vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
      
        cluster = rds.DatabaseCluster(self, "Database",
                                        engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_10_11),
#                                        credentials=rds.Credentials.from_generated_secret("syscdk"), # Optional - will default to 'admin' username and generated password
                                        instance_props={
        # optional , defaults to t3.medium
                                        "instance_type": ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM),
                                        "vpc_subnets": {
                                        "subnet_type": ec2.SubnetType.PRIVATE
                                                },
                                        "vpc": vpc
                                             }
                                            )
                                        


                                    

