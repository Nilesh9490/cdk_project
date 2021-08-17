from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as _apigateway,
    core
)

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
import aws_cdk.aws_eks as eks
import aws_cdk.aws_ecr as ecr
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.aws_apigatewayv2 as apigt2
import requests
import yaml
#import js_yaml as yaml
#import sync_request as request

class EKSStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str,vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        eks_role = iam.Role(self, "eksadmin", assumed_by=iam.ServicePrincipal(service='eks.amazonaws.com'),
                            role_name='eks-cluster-role', managed_policies=
                            [iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AmazonEKSClusterPolicy')])
        nodegroup_role = iam.Role(self, "eksnode", assumed_by=iam.ServicePrincipal(service='ec2.amazonaws.com'),
                            role_name='eks-node-role', managed_policies=
                            [iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name="AdministratorAccess")])

        eks_instance_profile = iam.CfnInstanceProfile(self, 'instanceprofile',
                                                      roles=[eks_role.role_name],
                                                      instance_profile_name='eks-cluster-role')

        cluster = eks.Cluster(self, "Dev-RCM-EKS-CLUSTER", cluster_name="Cluster",
                              version=eks.KubernetesVersion.V1_20,
                              vpc=vpc,
                              default_capacity_instance=ec2.InstanceType("t2.micro"),
                              default_capacity=0,
                              #masters_role=eks_role
                              )



        nodegroup = cluster.add_nodegroup_capacity('Dev-RCM-EKS-CLUSTER-NodeGroup',
                                                   instance_type=ec2.InstanceType("t2.micro"),
                                                   disk_size=50,
                                                   min_size=1,
                                                   nodegroup_name="Dev-RCM-EKS-CLUSTER-NodeGroup",
                                                   #node_role=nodegroup_role
                                                   )

        asg = cluster.add_auto_scaling_group_capacity("DEV-RCM-EKS-AUTO",
    				instance_type=ec2.InstanceType("t2.micro"),
    				min_capacity=1,
    				max_capacity=1,
    				desired_capacity=1
                                )

        tml1 = yaml.load_all(open("/home/techment/Desktop/nilesh/kipu/cdk_kipu/cdkbasics_ingress/ingress/servicedeployment.yaml"), Loader=yaml.Loader)
        servicedeployment = ["deployment", "service","ingressservice"]
        for temp3,temp4 in zip(tml1,servicedeployment) :
            cluster.add_manifest(temp4,  temp3)


        tml = yaml.load_all(open("/home/techment/Desktop/nilesh/kipu/cdk_kipu/cdkbasics_ingress/ingress/ingress.yaml"), Loader=yaml.Loader)
        ingress = ["ing1","ing2","ing3","ing4","ing5","ing6","ing7","ing8","ing9","ing10","ing11","ing12","ing13","ing14","ing15","ing16","ing                  17","ing18"]
        for temp1,temp2 in zip(tml,ingress) :
            cluster.add_manifest( temp2,  temp1)

        
        my_lambda= _lambda.Function(self,id='lambdafunction',runtime=_lambda.Runtime.PYTHON_3_8,
                    handler='authorizer.lambda_handler',
                    code= _lambda.Code.asset('lambdacode'),
                    environment = {
                               # 'x-api-key': 'staging',
                                'cognito_api': 'https://api-users-cognito.kipu.dev'
        }
        ) 
                    
        api_with_method = _apigateway.LambdaRestApi(self,id='restapi',rest_api_name='cdkrestapi_authorizer',handler=my_lambda)
        authorizer = api_with_method.root.add_resource('authorizer')
        authorizer.add_method('GET')
        authorizer.add_method("DELETE", _apigateway.HttpIntegration("http://aws.amazon.com"))
