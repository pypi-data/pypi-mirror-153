import json
from copy import deepcopy
from typing import Dict, Any, Union, List

from pydantic import BaseModel


class Base(BaseModel):
    def to_dict(self):
        self_dict = self.dict()
        name = self_dict.pop('Name')
        if not self_dict.get('DependsOn'):
            self_dict.pop('DependsOn', None)
        if not self_dict.get('DeletionPolicy'):
            self_dict.pop('DeletionPolicy', None)
        return {name: self_dict}


class Resource(Base):
    Name: str
    Type: str
    Properties: Dict[str, Any]
    DependsOn: List[str] = []
    DeletionPolicy: Union[str, None] = None

    def __add__(self, v: Union[dict, 'Resource']):
        if isinstance(v, Resource):
            v = deepcopy(v.to_dict())
        v.update(self.to_dict())
        return v

    def __str__(self):
        return self.Name


class Parameter(Base):
    Name: str
    Type: str
    Description: str = ""
    Default: str = ""

    def __add__(self, v: Union[dict, 'Parameter']):
        if isinstance(v, Parameter):
            v = deepcopy(v.to_dict())
        v.update(self.to_dict())
        return v

    def __str__(self):
        return self.Name


class Template(BaseModel):
    AWSTemplateFormatVersion: str = "2010-09-09"
    Description: str = ""
    Parameters: List[Parameter]
    Resources: List[Resource]

    def to_dict(self, *args, **kwargs) -> 'DictStrAny':
        resources_result = {}
        parameters_result = {}
        for parameter in self.Parameters:
            parameters_result = parameter + parameters_result
        for resource in self.Resources:
            resources_result = resource + resources_result
        self_dict = self.dict(*args, **kwargs)
        if not self.Parameters:
            self_dict.pop('Parameters')

        self_dict['Resources'] = resources_result
        self_dict['Parameters'] = parameters_result
        return self_dict


def build_bucket_artifact_name(project_name):
    """

    """
    try:
        import boto3
    except ImportError:
        return None

    try:
        sts = boto3.client("sts")
        account_id = sts.get_caller_identity()["Account"]
    except Exception as e:
        print(f"Failed to get account id: {e}")
        return None
    else:
        return account_id + "-" + project_name + "-artifacts"


def get_basic_template(*, project_name: str, artifacts_bucket: str):
    resources = [Resource(Name='LmdRole',
                          Type='AWS::IAM::Role',
                          Properties={
                              'AssumeRolePolicyDocument': {'Version': '2012-10-17',
                                                           'Statement': [
                                                               {'Effect': 'Allow',
                                                                'Principal': {
                                                                    'Service': 'lambda.amazonaws.com'},
                                                                'Action': 'sts:AssumeRole'}]},
                              'Path': '/',
                              'Policies': [
                                  {'PolicyDocument': {
                                      'Version': '2012-10-17', 'Statement': [
                                          {'Effect': 'Allow',
                                           'Action': ['logs:CreateLogGroup', 'logs:CreateLogStream',
                                                      'logs:PutLogEvents'],
                                           'Resource': '*'}]},
                                      'PolicyName': f'{project_name}-LambdaLogPermission'
                                  },
                                  {'PolicyDocument': {'Version': '2012-10-17',
                                                      'Statement': [
                                                          {'Effect': 'Allow',
                                                           'Action': [
                                                               'ec2:DescribeNetworkInterfaces',
                                                               'ec2:CreateNetworkInterface',
                                                               'ec2:DeleteNetworkInterface',
                                                               'ec2:DescribeInstances',
                                                               'ec2:AttachNetworkInterface'],
                                                           'Resource': '*'}]},
                                   'PolicyName': f'{project_name}-LambdaVpcPermission'
                                   }
                              ]
                          }),

                 Resource(Name='ApiRole',
                          Type='AWS::IAM::Role',
                          Properties={
                              'AssumeRolePolicyDocument': {'Version': '2012-10-17',
                                                           'Statement': [
                                                               {'Effect': 'Allow',
                                                                'Principal': {
                                                                    'Service': 'apigateway.amazonaws.com'},
                                                                'Action': 'sts:AssumeRole'}]},
                              'Path': '/',
                              'Policies': [
                                  {'PolicyDocument': {
                                      'Version': '2012-10-17',
                                      'Statement': [
                                          {'Effect': 'Allow',
                                           'Action': 'lambda:InvokeFunction',
                                           'Resource': '*'}
                                      ]
                                  },
                                      'PolicyName': f'{project_name}-ApiInvokeLambdaPermission'
                                  },
                                  {'PolicyDocument': {
                                      'Version': '2012-10-17',
                                      'Statement': [
                                          {'Effect': 'Allow',
                                           'Action': [
                                               'logs:CreateLogGroup',
                                               'logs:CreateLogStream',
                                               'logs:DescribeLogGroups',
                                               'logs:DescribeLogStreams',
                                               'logs:PutLogEvents',
                                               'logs:GetLogEvents',
                                               'logs:FilterLogEvents'],
                                           'Resource': '*'}]},
                                      'PolicyName': f'{project_name}-ApiLogPermission'}]}),

                 Resource(Name='Api',
                          Type='AWS::ApiGateway::RestApi',
                          Properties={
                              'Body': {'Fn::Transform': {'Name': 'AWS::Include',
                                                         'Parameters': {'Location': {
                                                             'Fn::Sub': f's3://${artifacts_bucket}/api.json'}}}},
                              'Name': {'Fn::Sub': '${Environment}-' + project_name},
                              'Parameters': {
                                  'endpointConfigurationTypes': 'REGIONAL'}}),

                 Resource(Name='DeployApi',
                          Type='AWS::ApiGateway::Deployment',
                          Properties={
                              'RestApiId': {'Ref': 'Api'}},
                          DeletionPolicy="Retain"),

                 Resource(Name='ApiStage',
                          Type='AWS::ApiGateway::Stage',
                          Properties={
                              'RestApiId': {'Ref': 'Api'},
                              'DeploymentId': {'Ref': 'DeployApi'},
                              'StageName': {'Ref': 'Environment'}}),

                 Resource(Name='usagePlan',
                          Type='AWS::ApiGateway::UsagePlan',
                          Properties={
                              'ApiStages': [{'ApiId': {'Ref': 'Api'}, 'Stage': {'Ref': 'ApiStage'}}],
                              'Description': f'Custom {project_name} usage plan',
                              'Quota': {'Limit': 5000, 'Period': 'MONTH'},
                              'Throttle': {'BurstLimit': 200, 'RateLimit': 100},
                              'UsagePlanName': {'Fn::Sub': '${Environment}-' + f'{project_name}-Plan'}}),

                 Resource(Name='ApiKey',
                          Type='AWS::ApiGateway::ApiKey',
                          Properties={
                              'Name': {'Fn::Sub': '${Environment}-' + f'{project_name}-ApiKey'},
                              'Description': 'CloudFormation API Key V1',
                              'Enabled': True, 'StageKeys': [
                                  {'RestApiId': {'Ref': 'Api'}, 'StageName': {'Ref': 'ApiStage'}}]},
                          DependsOn=[
                              "DeployApi",
                              "Api"
                          ]),

                 Resource(Name='usagePlanKey',
                          Type='AWS::ApiGateway::UsagePlanKey',
                          Properties={
                              'KeyId': {'Ref': 'ApiKey'}, 'KeyType': 'API_KEY',
                              'UsagePlanId': {'Ref': 'UsagePlan'}}),

                 Resource(Name='LayerCore',
                          Type='AWS::Lambda::LayerVersion',
                          Properties={
                              'CompatibleRuntimes': ['python3.9'], 'Content': 'src/layers/core',
                              'LayerName': {'Fn::Sub': '${Environment}-core'}})
                 ]
    parameters = [
        Parameter(Name='Environment', Type='String',
                  Description='Environment Name.'),
        Parameter(Name='NetworkStackParameter', Type='String',
                  Description='The stack name for get all network configuration.'),
        Parameter(Name='ArtifactsBucket', Type='String',
                  Description='The bucket name where all artifacts will be stored.',
                  Default=build_bucket_artifact_name(project_name) or artifacts_bucket),
        Parameter(Name='projectName', Type='String',
                  Description='The project name for the project.',
                  Default=project_name),
    ]

    template_cfn = Template(Resources=resources, Parameters=parameters)

    return json.dumps(template_cfn.to_dict(), indent=2)


def get_pipeline_template(project_name: str, repository_name: str):
    parameters = [
        Parameter(Name="Environment", Type="String", Description="Environment name."),
        Parameter(Name="AppName", Type="String", Description="The project name.", Default=project_name),
        Parameter(Name="Branch", Type="String", Description="Branch name for deploy de project.", Default='dev'),
        Parameter(Name="Repository", Type="String", Description="Repository name.", Default=repository_name),
        Parameter(Name="PrincipalTemplate", Type="String", Description="Name of the main template in the project.",
                  Default="projectTemplate.json"),
        Parameter(Name="ParametersTemplate", Type="String",
                  Description="One json string with the all parameter use in the PrincipalTemplate.",
                  Default="{}"
                  ),

    ]
    resources = [
        Resource(Name="AppPipeline",
                 Type="AWS::CodePipeline::Pipeline",
                 Properties={'Name': {'Fn::Sub': '${Environment}-{AppName}-pipeline'},
                             'RoleArn': {'Fn::GetAtt': ['RoleCodePipeline', 'Arn']},
                             'Stages': [{'Name': 'Source',
                                         'Actions': [{
                                             'Name': {'Fn::Sub': 'Source${AppName}'},
                                             'ActionTypeId': {
                                                 'Category': 'Source',
                                                 'Owner': 'AWS',
                                                 'Version': 1,
                                                 'Provider': 'CodeCommit'},
                                             'OutputArtifacts': [
                                                 {
                                                     'Name': 'SourceOutput'}],
                                             'Configuration': {
                                                 'BranchName': {
                                                     'Ref': 'Branch'},
                                                 'RepositoryName': {
                                                     'Ref': 'Repository'},
                                                 'PollForSourceChanges': False},
                                             'RunOrder': 1}]},
                                        {'Name': 'Build',
                                         'Actions': [{'Name': {
                                             'Fn::Sub': 'Build${AppName}'},
                                             'InputArtifacts': [
                                                 {
                                                     'Name': 'SourceOutput'}],
                                             'ActionTypeId': {
                                                 'Category': 'Build',
                                                 'Owner': 'AWS',
                                                 'Version': 1,
                                                 'Provider': 'CodeBuild'},
                                             'Configuration': {
                                                 'ProjectName': {
                                                     'Ref': 'CodeBuildProject'},
                                                 'EnvironmentVariables': {
                                                     'Fn::Sub': [
                                                         '[{"name":"BUCKETTEMPLATES","value":"${bucket}","type":"PLAINTEXT"}]',
                                                         {
                                                             'bucket': {
                                                                 'Ref': 'BucketCodePipelineArtifactStore'}}]}},
                                             'RunOrder': 1,
                                             'OutputArtifacts': [
                                                 {
                                                     'Name': 'projectsBuilded'}]}]},
                                        {'Name': 'Deploy',
                                         'Actions': [{
                                             'Name': 'CreateChangeSet',
                                             'ActionTypeId': {
                                                 'Category': 'Deploy',
                                                 'Owner': 'AWS',
                                                 'Version': 1,
                                                 'Provider': 'CloudFormation'},
                                             'Configuration': {
                                                 'ActionMode': 'CHANGE_SET_REPLACE',
                                                 'ChangeSetName': {
                                                     'Fn::Join': [
                                                         '-',
                                                         [
                                                             {
                                                                 'Ref': 'Environment'},
                                                             {
                                                                 'Ref': 'AppName'},
                                                             'changeSet']]},
                                                 'StackName': {
                                                     'Fn::Join': [
                                                         '-',
                                                         [
                                                             {
                                                                 'Ref': 'Environment'},
                                                             {
                                                                 'Ref': 'AppName'},
                                                             'stack']]},
                                                 'Capabilities': 'CAPABILITY_IAM,CAPABILITY_NAMED_IAM,CAPABILITY_AUTO_EXPAND',
                                                 'TemplatePath': {
                                                     'Fn::Join': [
                                                         '::',
                                                         [
                                                             'projectsBuilded',
                                                             {
                                                                 'Ref': 'PrincipalTemplate'}]]},
                                                 'RoleArn': {
                                                     'Fn::GetAtt': [
                                                         'RoleCloudFormation',
                                                         'Arn']},
                                                 'ParameterOverrides': {
                                                     'Ref': 'ParametersTemplate'}},
                                             'RunOrder': 1,
                                             'InputArtifacts': [
                                                 {
                                                     'Name': 'projectsBuilded'}]},
                                             {
                                                 'Name': 'ChangesetExcecute',
                                                 'ActionTypeId': {
                                                     'Category': 'Deploy',
                                                     'Owner': 'AWS',
                                                     'Version': 1,
                                                     'Provider': 'CloudFormation'},
                                                 'Configuration': {
                                                     'ActionMode': 'CHANGE_SET_EXECUTE',
                                                     'ChangeSetName': {
                                                         'Fn::Join': [
                                                             '-',
                                                             [
                                                                 {
                                                                     'Ref': 'Environment'},
                                                                 {
                                                                     'Ref': 'AppName'},
                                                                 'changeSet']]},
                                                     'StackName': {
                                                         'Fn::Join': [
                                                             '-',
                                                             [
                                                                 {
                                                                     'Ref': 'Environment'},
                                                                 {
                                                                     'Ref': 'AppName'},
                                                                 'stack']]}},
                                                 'RunOrder': 2,
                                                 'InputArtifacts': [
                                                     {
                                                         'Name': 'projectsBuilded'}]}]}],
                             'ArtifactStore': {'Type': 'S3', 'Location': {'Ref': 'BucketCodePipelineArtifactStore'}}}),

        Resource(Name="RoleAmazonCloudWatchEvent",
                 Type="AWS::IAM::Role",
                 Properties={
                     'AssumeRolePolicyDocument': {'Version': '2012-10-17', 'Statement': [
                         {'Effect': 'Allow', 'Principal': {'Service': ['events.amazonaws.com']},
                          'Action': 'sts:AssumeRole'}]},
                     'Path': '/', 'Policies': [
                         {'PolicyName': {
                             'Fn::Join': ['-', [{'Ref': 'Environment'}, {'Ref': 'AppName'}, 'pipeline-execution']]},
                             'PolicyDocument': {'Version': '2012-10-17', 'Statement': [
                                 {'Effect': 'Allow', 'Action': 'codepipeline:StartPipelineExecution',
                                  'Resource': {'Fn::Join': ['',
                                                            [
                                                                'arn:aws:codepipeline:',
                                                                {
                                                                    'Ref': 'AWS::Region'},
                                                                ':',
                                                                {
                                                                    'Ref': 'AWS::AccountId'},
                                                                ':',
                                                                {
                                                                    'Ref': 'AppPipeline'}]]}}]}}]}),

        Resource(Name="RuleAmazonCloudWatchEvent",
                 Type="AWS::Events::Rule",
                 Properties={
                     'EventPattern': {'source': ['aws.codecommit'],
                                      'detail-type': ['CodeCommit Repository State Change'],
                                      'resources': [
                                          {'Fn::Join': ['', ['arn:aws:codecommit:', {'Ref': 'AWS::Region'}, ':',
                                                             {'Ref': 'AWS::AccountId'}, ':', {'Ref': 'Repository'}]]}],
                                      'detail': {'event': ['referenceCreated', 'referenceUpdated'],
                                                 'referenceType': ['branch'],
                                                 'referenceName': [{'Ref': 'Branch'}]}},
                     'Targets': [{'Arn': {'Fn::Join': ['', [
                         'arn:aws:codepipeline:', {'Ref': 'AWS::Region'}, ':', {'Ref': 'AWS::AccountId'}, ':',
                         {'Ref': 'AppPipeline'}]]}, 'RoleArn': {'Fn::GetAtt': ['RoleAmazonCloudWatchEvent', 'Arn']},
                                  'Id': {
                                      'Fn::Join': ['-', [{'Ref': 'Environment'}, {'Ref': 'AppName'},
                                                         'codepipeline-AppPipeline']]}}]}),

        Resource(Name="RoleCodePipeline",
                 Type="AWS::IAM::Role",
                 Properties={
                     'AssumeRolePolicyDocument': {'Version': '2012-10-17', 'Statement': [
                         {'Effect': 'Allow', 'Principal': {'Service': ['codepipeline.amazonaws.com']},
                          'Action': 'sts:AssumeRole'}]}, 'Path': '/', 'Policies': [{'PolicyName': {
                         'Fn::Join': ['-', [{'Ref': 'Environment'}, {'Ref': 'AppName'}, 'CodePipeline-Service-Role']]},
                         'PolicyDocument': {'Version': '2012-10-17',
                                            'Statement': [
                                                {'Effect': 'Allow',
                                                 'Action': [
                                                     'codecommit:CancelUploadArchive',
                                                     'codecommit:GetBranch',
                                                     'codecommit:GetCommit',
                                                     'codecommit:GetUploadArchiveStatus',
                                                     'codecommit:UploadArchive'],
                                                 'Resource': '*'},
                                                {'Effect': 'Allow',
                                                 'Action': [
                                                     'codedeploy:CreateDeployment',
                                                     'codedeploy:GetApplicationRevision',
                                                     'codedeploy:GetDeployment',
                                                     'codedeploy:GetDeploymentConfig',
                                                     'codedeploy:RegisterApplicationRevision'],
                                                 'Resource': '*'},
                                                {'Effect': 'Allow',
                                                 'Action': [
                                                     'codebuild:BatchGetBuilds',
                                                     'codebuild:StartBuild'],
                                                 'Resource': '*'},
                                                {'Effect': 'Allow',
                                                 'Action': [
                                                     'devicefarm:ListProjects',
                                                     'devicefarm:ListDevicePools',
                                                     'devicefarm:GetRun',
                                                     'devicefarm:GetUpload',
                                                     'devicefarm:CreateUpload',
                                                     'devicefarm:ScheduleRun'],
                                                 'Resource': '*'},
                                                {'Effect': 'Allow',
                                                 'Action': [
                                                     'lambda:InvokeFunction',
                                                     'lambda:ListFunctions'],
                                                 'Resource': '*'},
                                                {'Effect': 'Allow',
                                                 'Action': [
                                                     'iam:PassRole'],
                                                 'Resource': '*'},
                                                {'Effect': 'Allow',
                                                 'Action': [
                                                     'elasticbeanstalk:*',
                                                     'ec2:*',
                                                     'elasticloadbalancing:*',
                                                     'autoscaling:*',
                                                     'cloudwatch:*',
                                                     's3:*', 'sns:*',
                                                     'cloudformation:*',
                                                     'rds:*', 'sqs:*',
                                                     'ecs:*'],
                                                 'Resource': '*'}]}}]}),

        Resource(Name="BucketCodePipelineArtifactStore",
                 Type="AWS::S3::Bucket",
                 Properties={'BucketName': {
                     'Fn::Join': ['-', [{'Ref': 'Environment'}, {'Ref': 'AppName'}, 'artifacts',
                                        {'Ref': 'AWS::AccountId'}]]}}),

        Resource(Name="RoleCodeBuildProject",
                 Type="AWS::IAM::Role",
                 Properties={'RoleName': {'Fn::Sub': '${Environment}-${AppName}-CodeBuild-Role'},
                             'AssumeRolePolicyDocument': {'Version': '2012-10-17', 'Statement': [
                                 {'Effect': 'Allow', 'Principal': {'Service': ['codebuild.amazonaws.com']},
                                  'Action': 'sts:AssumeRole'}]}, 'Path': '/service-role/', 'Policies': [
                         {'PolicyName': {'Fn::Sub': '${Environment}-${AppName}-CodeBuild-Policy'},
                          'PolicyDocument': {'Version': '2012-10-17', 'Statement': [
                              {'Effect': 'Allow', 'Resource': 'arn:aws:logs:us-east-1:*:log-group:/aws/codebuild/*:*',
                               'Action': ['logs:CreateLogGroup', 'logs:CreateLogStream', 'logs:PutLogEvents']},
                              {'Effect': 'Allow', 'Resource': ['arn:aws:s3:::codepipeline-us-east-1-*'],
                               'Action': ['s3:PutObject', 's3:GetObject', 's3:GetObjectVersion', 's3:ListBucket',
                                          's3:GetBucketAcl', 's3:PutObjectAcl', 's3:GetBucketLocation']},
                              {'Effect': 'Allow', 'Action': ['codebuild:CreateReportGroup', 'codebuild:CreateReport',
                                                             'codebuild:UpdateReport', 'codebuild:BatchPutTestCases'],
                               'Resource': 'arn:aws:codebuild:us-east-1:*:report-group/*-*'},
                              {'Effect': 'Allow', 'Action': 's3:*', 'Resource': '*'}]}}]}),

        Resource(Name="CodeBuildProject",
                 Type="AWS::CodeBuild::Project",
                 Properties={'Name': {'Fn::Join': ['-', [{'Ref': 'Environment'}, {'Ref': 'AppName'}, 'Compile']]},
                             'ServiceRole': {'Fn::GetAtt': ['RoleCodeBuildProject', 'Arn']},
                             'Artifacts': {'Type': 'CODEPIPELINE'},
                             'Environment': {'Type': 'LINUX_CONTAINER', 'ComputeType': 'BUILD_GENERAL1_SMALL',
                                             'Image': 'aws/codebuild/standard:5.0', 'EnvironmentVariables': [
                                     {'Name': 'ENVIRONMENT', 'Value': {'Ref': 'Environment'}},
                                     {'Name': 'BUCKET', 'Value': {'Ref': 'BucketCodePipelineArtifactStore'}}]},
                             'Source': {'Type': 'CODEPIPELINE'}, 'TimeoutInMinutes': 60,
                             'Tags': [{'Key': 'Product', 'Value': {'Ref': 'AppName'}}]}),

        Resource(Name="RoleCloudFormation",
                 Type="AWS::IAM::Role",
                 Properties={
                     'RoleName': {
                         'Fn::Join': ['-', [{'Ref': 'Environment'}, {'Ref': 'AppName'}, 'CloudFormation-Role']]},
                     'AssumeRolePolicyDocument': {'Version': '2012-10-17', 'Statement': [
                         {'Effect': 'Allow', 'Principal': {'Service': ['cloudformation.amazonaws.com']},
                          'Action': 'sts:AssumeRole'}]}, 'Path': '/', 'Policies': [{'PolicyName': {
                         'Fn::Join': ['-', [{'Ref': 'Environment'}, {'Ref': 'AppName'}, 'CloudFormation-Policy']]},
                         'PolicyDocument': {'Statement': [
                             {'Sid': 'VisualEditor0',
                              'Effect': 'Allow', 'Action': [
                                 'organizations:ListPoliciesForTarget',
                                 'organizations:ListRoots',
                                 'organizations:ListTargetsForPolicy',
                                 'apigateway:*',
                                 'organizations:DescribeAccount',
                                 'cloudformation:CreateChangeSet',
                                 's3:GetBucketVersioning',
                                 'organizations:DescribePolicy',
                                 'organizations:ListChildren',
                                 'organizations:ListPolicies',
                                 'iam:*', 's3:GetObject',
                                 'organizations:DescribeOrganization',
                                 'codedeploy:*', 'lambda:*',
                                 'organizations:DescribeOrganizationalUnit',
                                 'organizations:ListParents',
                                 's3:GetObjectVersion',
                                 'logs:CreateLogGroup',
                                 'logs:CreateLogStream',
                                 'logs:PutLogEvents',
                                 'ec2:AcceptVpcPeeringConnection',
                                 'ec2:AcceptVpcEndpointConnections',
                                 'ec2:AllocateAddress',
                                 'ec2:AssignIpv6Addresses',
                                 'ec2:AssignPrivateIpAddresses',
                                 'ec2:AssociateAddress',
                                 'ec2:AssociateDhcpOptions',
                                 'ec2:AssociateRouteTable',
                                 'ec2:AssociateSubnetCidrBlock',
                                 'ec2:AssociateVpcCidrBlock',
                                 'ec2:AttachClassicLinkVpc',
                                 'ec2:AttachInternetGateway',
                                 'ec2:AttachNetworkInterface',
                                 'ec2:AttachVpnGateway',
                                 'ec2:AuthorizeSecurityGroupEgress',
                                 'ec2:AuthorizeSecurityGroupIngress',
                                 'ec2:CreateCustomerGateway',
                                 'ec2:CreateDefaultSubnet',
                                 'ec2:CreateDefaultVpc',
                                 'ec2:CreateDhcpOptions',
                                 'ec2:CreateEgressOnlyInternetGateway',
                                 'ec2:CreateFlowLogs',
                                 'ec2:CreateInternetGateway',
                                 'ec2:CreateNatGateway',
                                 'ec2:CreateNetworkAcl',
                                 'ec2:CreateNetworkAcl',
                                 'ec2:CreateNetworkAclEntry',
                                 'ec2:CreateNetworkInterface',
                                 'ec2:CreateNetworkInterfacePermission',
                                 'ec2:CreateRoute',
                                 'ec2:CreateRouteTable',
                                 'ec2:CreateSecurityGroup',
                                 'ec2:CreateSubnet', 'ec2:CreateTags',
                                 'ec2:CreateVpc',
                                 'ec2:CreateVpcEndpoint',
                                 'ec2:CreateVpcEndpointConnectionNotification',
                                 'ec2:CreateVpcEndpointServiceConfiguration',
                                 'ec2:CreateVpcPeeringConnection',
                                 'ec2:CreateVpnConnection',
                                 'ec2:CreateVpnConnectionRoute',
                                 'ec2:CreateVpnGateway',
                                 'ec2:DeleteCustomerGateway',
                                 'ec2:DeleteDhcpOptions',
                                 'ec2:DeleteEgressOnlyInternetGateway',
                                 'ec2:DeleteFlowLogs',
                                 'ec2:DeleteInternetGateway',
                                 'ec2:DeleteNatGateway',
                                 'ec2:DeleteNetworkAcl',
                                 'ec2:DeleteNetworkAclEntry',
                                 'ec2:DeleteNetworkInterface',
                                 'ec2:DeleteNetworkInterfacePermission',
                                 'ec2:DeleteRoute',
                                 'ec2:DeleteRouteTable',
                                 'ec2:DeleteSecurityGroup',
                                 'ec2:DeleteSubnet', 'ec2:DeleteTags',
                                 'ec2:DeleteVpc',
                                 'ec2:DeleteVpcEndpoints',
                                 'ec2:DeleteVpcEndpointConnectionNotifications',
                                 'ec2:DeleteVpcEndpointServiceConfigurations',
                                 'ec2:DeleteVpcPeeringConnection',
                                 'ec2:DeleteVpnConnection',
                                 'ec2:DeleteVpnConnectionRoute',
                                 'ec2:DeleteVpnGateway',
                                 'ec2:DescribeAccountAttributes',
                                 'ec2:DescribeAddresses',
                                 'ec2:DescribeAvailabilityZones',
                                 'ec2:DescribeClassicLinkInstances',
                                 'ec2:DescribeCustomerGateways',
                                 'ec2:DescribeDhcpOptions',
                                 'ec2:DescribeEgressOnlyInternetGateways',
                                 'ec2:DescribeFlowLogs',
                                 'ec2:DescribeInstances',
                                 'ec2:DescribeInternetGateways',
                                 'ec2:DescribeKeyPairs',
                                 'ec2:DescribeMovingAddresses',
                                 'ec2:DescribeNatGateways',
                                 'ec2:DescribeNetworkAcls',
                                 'ec2:DescribeNetworkInterfaceAttribute',
                                 'ec2:DescribeNetworkInterfacePermissions',
                                 'ec2:DescribeNetworkInterfaces',
                                 'ec2:DescribePrefixLists',
                                 'ec2:DescribeRouteTables',
                                 'ec2:DescribeSecurityGroupReferences',
                                 'ec2:DescribeSecurityGroups',
                                 'ec2:DescribeStaleSecurityGroups',
                                 'ec2:DescribeSubnets',
                                 'ec2:DescribeTags',
                                 'ec2:DescribeVpcAttribute',
                                 'ec2:DescribeVpcClassicLink',
                                 'ec2:DescribeVpcClassicLinkDnsSupport',
                                 'ec2:DescribeVpcEndpointConnectionNotifications',
                                 'ec2:DescribeVpcEndpointConnections',
                                 'ec2:DescribeVpcEndpoints',
                                 'ec2:DescribeVpcEndpointServiceConfigurations',
                                 'ec2:DescribeVpcEndpointServicePermissions',
                                 'ec2:DescribeVpcEndpointServices',
                                 'ec2:DescribeVpcPeeringConnections',
                                 'ec2:DescribeVpcs',
                                 'ec2:DescribeVpnConnections',
                                 'ec2:DescribeVpnGateways',
                                 'ec2:DetachClassicLinkVpc',
                                 'ec2:DetachInternetGateway',
                                 'ec2:DetachNetworkInterface',
                                 'ec2:DetachVpnGateway',
                                 'ec2:DisableVgwRoutePropagation',
                                 'ec2:DisableVpcClassicLink',
                                 'ec2:DisableVpcClassicLinkDnsSupport',
                                 'ec2:DisassociateAddress',
                                 'ec2:DisassociateRouteTable',
                                 'ec2:DisassociateSubnetCidrBlock',
                                 'ec2:DisassociateVpcCidrBlock',
                                 'ec2:EnableVgwRoutePropagation',
                                 'ec2:EnableVpcClassicLink',
                                 'ec2:EnableVpcClassicLinkDnsSupport',
                                 'ec2:ModifyNetworkInterfaceAttribute',
                                 'ec2:ModifySubnetAttribute',
                                 'ec2:ModifyVpcAttribute',
                                 'ec2:ModifyVpcEndpoint',
                                 'ec2:ModifyVpcEndpointConnectionNotification',
                                 'ec2:ModifyVpcEndpointServiceConfiguration',
                                 'ec2:ModifyVpcEndpointServicePermissions',
                                 'ec2:ModifyVpcPeeringConnectionOptions',
                                 'ec2:ModifyVpcTenancy',
                                 'ec2:MoveAddressToVpc',
                                 'ec2:RejectVpcEndpointConnections',
                                 'ec2:RejectVpcPeeringConnection',
                                 'ec2:ReleaseAddress',
                                 'ec2:ReplaceNetworkAclAssociation',
                                 'ec2:ReplaceNetworkAclEntry',
                                 'ec2:ReplaceRoute',
                                 'ec2:ReplaceRouteTableAssociation',
                                 'ec2:ResetNetworkInterfaceAttribute',
                                 'ec2:RestoreAddressToClassic',
                                 'ec2:RevokeSecurityGroupEgress',
                                 'ec2:RevokeSecurityGroupIngress',
                                 'ec2:UnassignIpv6Addresses',
                                 'ec2:UnassignPrivateIpAddresses',
                                 'ec2:UpdateSecurityGroupRuleDescriptionsEgress',
                                 'ec2:UpdateSecurityGroupRuleDescriptionsIngress'],
                              'Resource': '*'}],
                             'Version': '2012-10-17'}}]}),

    ]
