#!/usr/bin/env python3
from aws_cdk import core

from stacks.vpc_stack import VPCStack
from stacks.rds_stack import RDSStack
from stacks.eks_stack import EKSStack
#from stacks.lambda_stack import Lambda_stack
app = core.App()
vpc_stack = VPCStack(app, 'DEV-RCM-VPC')
eks_stack = EKSStack(app,'DEV-RCM-EKS', vpc=vpc_stack.vpc)
rds_stack = RDSStack(app,'DEV-RCM-RDS', vpc=vpc_stack.vpc)
app.synth()
