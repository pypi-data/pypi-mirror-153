"""
Type annotations for amplify service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_amplify/type_defs/)

Usage::

    ```python
    from mypy_boto3_amplify.type_defs import AutoBranchCreationConfigTypeDef

    data: AutoBranchCreationConfigTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    DomainStatusType,
    JobStatusType,
    JobTypeType,
    PlatformType,
    RepositoryCloneMethodType,
    StageType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AutoBranchCreationConfigTypeDef",
    "CustomRuleTypeDef",
    "ProductionBranchTypeDef",
    "ArtifactTypeDef",
    "BackendEnvironmentTypeDef",
    "BranchTypeDef",
    "ResponseMetadataTypeDef",
    "CreateBackendEnvironmentRequestRequestTypeDef",
    "CreateBranchRequestRequestTypeDef",
    "CreateDeploymentRequestRequestTypeDef",
    "SubDomainSettingTypeDef",
    "CreateWebhookRequestRequestTypeDef",
    "WebhookTypeDef",
    "DeleteAppRequestRequestTypeDef",
    "DeleteBackendEnvironmentRequestRequestTypeDef",
    "DeleteBranchRequestRequestTypeDef",
    "DeleteDomainAssociationRequestRequestTypeDef",
    "DeleteJobRequestRequestTypeDef",
    "JobSummaryTypeDef",
    "DeleteWebhookRequestRequestTypeDef",
    "GenerateAccessLogsRequestRequestTypeDef",
    "GetAppRequestRequestTypeDef",
    "GetArtifactUrlRequestRequestTypeDef",
    "GetBackendEnvironmentRequestRequestTypeDef",
    "GetBranchRequestRequestTypeDef",
    "GetDomainAssociationRequestRequestTypeDef",
    "GetJobRequestRequestTypeDef",
    "GetWebhookRequestRequestTypeDef",
    "StepTypeDef",
    "PaginatorConfigTypeDef",
    "ListAppsRequestRequestTypeDef",
    "ListArtifactsRequestRequestTypeDef",
    "ListBackendEnvironmentsRequestRequestTypeDef",
    "ListBranchesRequestRequestTypeDef",
    "ListDomainAssociationsRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWebhooksRequestRequestTypeDef",
    "StartDeploymentRequestRequestTypeDef",
    "StartJobRequestRequestTypeDef",
    "StopJobRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBranchRequestRequestTypeDef",
    "UpdateWebhookRequestRequestTypeDef",
    "CreateAppRequestRequestTypeDef",
    "UpdateAppRequestRequestTypeDef",
    "AppTypeDef",
    "CreateBackendEnvironmentResultTypeDef",
    "CreateBranchResultTypeDef",
    "CreateDeploymentResultTypeDef",
    "DeleteBackendEnvironmentResultTypeDef",
    "DeleteBranchResultTypeDef",
    "GenerateAccessLogsResultTypeDef",
    "GetArtifactUrlResultTypeDef",
    "GetBackendEnvironmentResultTypeDef",
    "GetBranchResultTypeDef",
    "ListArtifactsResultTypeDef",
    "ListBackendEnvironmentsResultTypeDef",
    "ListBranchesResultTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateBranchResultTypeDef",
    "CreateDomainAssociationRequestRequestTypeDef",
    "SubDomainTypeDef",
    "UpdateDomainAssociationRequestRequestTypeDef",
    "CreateWebhookResultTypeDef",
    "DeleteWebhookResultTypeDef",
    "GetWebhookResultTypeDef",
    "ListWebhooksResultTypeDef",
    "UpdateWebhookResultTypeDef",
    "DeleteJobResultTypeDef",
    "ListJobsResultTypeDef",
    "StartDeploymentResultTypeDef",
    "StartJobResultTypeDef",
    "StopJobResultTypeDef",
    "JobTypeDef",
    "ListAppsRequestListAppsPaginateTypeDef",
    "ListBranchesRequestListBranchesPaginateTypeDef",
    "ListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef",
    "ListJobsRequestListJobsPaginateTypeDef",
    "CreateAppResultTypeDef",
    "DeleteAppResultTypeDef",
    "GetAppResultTypeDef",
    "ListAppsResultTypeDef",
    "UpdateAppResultTypeDef",
    "DomainAssociationTypeDef",
    "GetJobResultTypeDef",
    "CreateDomainAssociationResultTypeDef",
    "DeleteDomainAssociationResultTypeDef",
    "GetDomainAssociationResultTypeDef",
    "ListDomainAssociationsResultTypeDef",
    "UpdateDomainAssociationResultTypeDef",
)

AutoBranchCreationConfigTypeDef = TypedDict(
    "AutoBranchCreationConfigTypeDef",
    {
        "stage": StageType,
        "framework": str,
        "enableAutoBuild": bool,
        "environmentVariables": Mapping[str, str],
        "basicAuthCredentials": str,
        "enableBasicAuth": bool,
        "enablePerformanceMode": bool,
        "buildSpec": str,
        "enablePullRequestPreview": bool,
        "pullRequestEnvironmentName": str,
    },
    total=False,
)

_RequiredCustomRuleTypeDef = TypedDict(
    "_RequiredCustomRuleTypeDef",
    {
        "source": str,
        "target": str,
    },
)
_OptionalCustomRuleTypeDef = TypedDict(
    "_OptionalCustomRuleTypeDef",
    {
        "status": str,
        "condition": str,
    },
    total=False,
)


class CustomRuleTypeDef(_RequiredCustomRuleTypeDef, _OptionalCustomRuleTypeDef):
    pass


ProductionBranchTypeDef = TypedDict(
    "ProductionBranchTypeDef",
    {
        "lastDeployTime": datetime,
        "status": str,
        "thumbnailUrl": str,
        "branchName": str,
    },
    total=False,
)

ArtifactTypeDef = TypedDict(
    "ArtifactTypeDef",
    {
        "artifactFileName": str,
        "artifactId": str,
    },
)

_RequiredBackendEnvironmentTypeDef = TypedDict(
    "_RequiredBackendEnvironmentTypeDef",
    {
        "backendEnvironmentArn": str,
        "environmentName": str,
        "createTime": datetime,
        "updateTime": datetime,
    },
)
_OptionalBackendEnvironmentTypeDef = TypedDict(
    "_OptionalBackendEnvironmentTypeDef",
    {
        "stackName": str,
        "deploymentArtifacts": str,
    },
    total=False,
)


class BackendEnvironmentTypeDef(
    _RequiredBackendEnvironmentTypeDef, _OptionalBackendEnvironmentTypeDef
):
    pass


_RequiredBranchTypeDef = TypedDict(
    "_RequiredBranchTypeDef",
    {
        "branchArn": str,
        "branchName": str,
        "description": str,
        "stage": StageType,
        "displayName": str,
        "enableNotification": bool,
        "createTime": datetime,
        "updateTime": datetime,
        "environmentVariables": Dict[str, str],
        "enableAutoBuild": bool,
        "customDomains": List[str],
        "framework": str,
        "activeJobId": str,
        "totalNumberOfJobs": str,
        "enableBasicAuth": bool,
        "ttl": str,
        "enablePullRequestPreview": bool,
    },
)
_OptionalBranchTypeDef = TypedDict(
    "_OptionalBranchTypeDef",
    {
        "tags": Dict[str, str],
        "enablePerformanceMode": bool,
        "thumbnailUrl": str,
        "basicAuthCredentials": str,
        "buildSpec": str,
        "associatedResources": List[str],
        "pullRequestEnvironmentName": str,
        "destinationBranch": str,
        "sourceBranch": str,
        "backendEnvironmentArn": str,
    },
    total=False,
)


class BranchTypeDef(_RequiredBranchTypeDef, _OptionalBranchTypeDef):
    pass


ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredCreateBackendEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBackendEnvironmentRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
    },
)
_OptionalCreateBackendEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBackendEnvironmentRequestRequestTypeDef",
    {
        "stackName": str,
        "deploymentArtifacts": str,
    },
    total=False,
)


class CreateBackendEnvironmentRequestRequestTypeDef(
    _RequiredCreateBackendEnvironmentRequestRequestTypeDef,
    _OptionalCreateBackendEnvironmentRequestRequestTypeDef,
):
    pass


_RequiredCreateBranchRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBranchRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
    },
)
_OptionalCreateBranchRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBranchRequestRequestTypeDef",
    {
        "description": str,
        "stage": StageType,
        "framework": str,
        "enableNotification": bool,
        "enableAutoBuild": bool,
        "environmentVariables": Mapping[str, str],
        "basicAuthCredentials": str,
        "enableBasicAuth": bool,
        "enablePerformanceMode": bool,
        "tags": Mapping[str, str],
        "buildSpec": str,
        "ttl": str,
        "displayName": str,
        "enablePullRequestPreview": bool,
        "pullRequestEnvironmentName": str,
        "backendEnvironmentArn": str,
    },
    total=False,
)


class CreateBranchRequestRequestTypeDef(
    _RequiredCreateBranchRequestRequestTypeDef, _OptionalCreateBranchRequestRequestTypeDef
):
    pass


_RequiredCreateDeploymentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDeploymentRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
    },
)
_OptionalCreateDeploymentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDeploymentRequestRequestTypeDef",
    {
        "fileMap": Mapping[str, str],
    },
    total=False,
)


class CreateDeploymentRequestRequestTypeDef(
    _RequiredCreateDeploymentRequestRequestTypeDef, _OptionalCreateDeploymentRequestRequestTypeDef
):
    pass


SubDomainSettingTypeDef = TypedDict(
    "SubDomainSettingTypeDef",
    {
        "prefix": str,
        "branchName": str,
    },
)

_RequiredCreateWebhookRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWebhookRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
    },
)
_OptionalCreateWebhookRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWebhookRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)


class CreateWebhookRequestRequestTypeDef(
    _RequiredCreateWebhookRequestRequestTypeDef, _OptionalCreateWebhookRequestRequestTypeDef
):
    pass


WebhookTypeDef = TypedDict(
    "WebhookTypeDef",
    {
        "webhookArn": str,
        "webhookId": str,
        "webhookUrl": str,
        "branchName": str,
        "description": str,
        "createTime": datetime,
        "updateTime": datetime,
    },
)

DeleteAppRequestRequestTypeDef = TypedDict(
    "DeleteAppRequestRequestTypeDef",
    {
        "appId": str,
    },
)

DeleteBackendEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteBackendEnvironmentRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
    },
)

DeleteBranchRequestRequestTypeDef = TypedDict(
    "DeleteBranchRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
    },
)

DeleteDomainAssociationRequestRequestTypeDef = TypedDict(
    "DeleteDomainAssociationRequestRequestTypeDef",
    {
        "appId": str,
        "domainName": str,
    },
)

DeleteJobRequestRequestTypeDef = TypedDict(
    "DeleteJobRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "jobId": str,
    },
)

_RequiredJobSummaryTypeDef = TypedDict(
    "_RequiredJobSummaryTypeDef",
    {
        "jobArn": str,
        "jobId": str,
        "commitId": str,
        "commitMessage": str,
        "commitTime": datetime,
        "startTime": datetime,
        "status": JobStatusType,
        "jobType": JobTypeType,
    },
)
_OptionalJobSummaryTypeDef = TypedDict(
    "_OptionalJobSummaryTypeDef",
    {
        "endTime": datetime,
    },
    total=False,
)


class JobSummaryTypeDef(_RequiredJobSummaryTypeDef, _OptionalJobSummaryTypeDef):
    pass


DeleteWebhookRequestRequestTypeDef = TypedDict(
    "DeleteWebhookRequestRequestTypeDef",
    {
        "webhookId": str,
    },
)

_RequiredGenerateAccessLogsRequestRequestTypeDef = TypedDict(
    "_RequiredGenerateAccessLogsRequestRequestTypeDef",
    {
        "domainName": str,
        "appId": str,
    },
)
_OptionalGenerateAccessLogsRequestRequestTypeDef = TypedDict(
    "_OptionalGenerateAccessLogsRequestRequestTypeDef",
    {
        "startTime": Union[datetime, str],
        "endTime": Union[datetime, str],
    },
    total=False,
)


class GenerateAccessLogsRequestRequestTypeDef(
    _RequiredGenerateAccessLogsRequestRequestTypeDef,
    _OptionalGenerateAccessLogsRequestRequestTypeDef,
):
    pass


GetAppRequestRequestTypeDef = TypedDict(
    "GetAppRequestRequestTypeDef",
    {
        "appId": str,
    },
)

GetArtifactUrlRequestRequestTypeDef = TypedDict(
    "GetArtifactUrlRequestRequestTypeDef",
    {
        "artifactId": str,
    },
)

GetBackendEnvironmentRequestRequestTypeDef = TypedDict(
    "GetBackendEnvironmentRequestRequestTypeDef",
    {
        "appId": str,
        "environmentName": str,
    },
)

GetBranchRequestRequestTypeDef = TypedDict(
    "GetBranchRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
    },
)

GetDomainAssociationRequestRequestTypeDef = TypedDict(
    "GetDomainAssociationRequestRequestTypeDef",
    {
        "appId": str,
        "domainName": str,
    },
)

GetJobRequestRequestTypeDef = TypedDict(
    "GetJobRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "jobId": str,
    },
)

GetWebhookRequestRequestTypeDef = TypedDict(
    "GetWebhookRequestRequestTypeDef",
    {
        "webhookId": str,
    },
)

_RequiredStepTypeDef = TypedDict(
    "_RequiredStepTypeDef",
    {
        "stepName": str,
        "startTime": datetime,
        "status": JobStatusType,
        "endTime": datetime,
    },
)
_OptionalStepTypeDef = TypedDict(
    "_OptionalStepTypeDef",
    {
        "logUrl": str,
        "artifactsUrl": str,
        "testArtifactsUrl": str,
        "testConfigUrl": str,
        "screenshots": Dict[str, str],
        "statusReason": str,
        "context": str,
    },
    total=False,
)


class StepTypeDef(_RequiredStepTypeDef, _OptionalStepTypeDef):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListAppsRequestRequestTypeDef = TypedDict(
    "ListAppsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListArtifactsRequestRequestTypeDef = TypedDict(
    "_RequiredListArtifactsRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "jobId": str,
    },
)
_OptionalListArtifactsRequestRequestTypeDef = TypedDict(
    "_OptionalListArtifactsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListArtifactsRequestRequestTypeDef(
    _RequiredListArtifactsRequestRequestTypeDef, _OptionalListArtifactsRequestRequestTypeDef
):
    pass


_RequiredListBackendEnvironmentsRequestRequestTypeDef = TypedDict(
    "_RequiredListBackendEnvironmentsRequestRequestTypeDef",
    {
        "appId": str,
    },
)
_OptionalListBackendEnvironmentsRequestRequestTypeDef = TypedDict(
    "_OptionalListBackendEnvironmentsRequestRequestTypeDef",
    {
        "environmentName": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListBackendEnvironmentsRequestRequestTypeDef(
    _RequiredListBackendEnvironmentsRequestRequestTypeDef,
    _OptionalListBackendEnvironmentsRequestRequestTypeDef,
):
    pass


_RequiredListBranchesRequestRequestTypeDef = TypedDict(
    "_RequiredListBranchesRequestRequestTypeDef",
    {
        "appId": str,
    },
)
_OptionalListBranchesRequestRequestTypeDef = TypedDict(
    "_OptionalListBranchesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListBranchesRequestRequestTypeDef(
    _RequiredListBranchesRequestRequestTypeDef, _OptionalListBranchesRequestRequestTypeDef
):
    pass


_RequiredListDomainAssociationsRequestRequestTypeDef = TypedDict(
    "_RequiredListDomainAssociationsRequestRequestTypeDef",
    {
        "appId": str,
    },
)
_OptionalListDomainAssociationsRequestRequestTypeDef = TypedDict(
    "_OptionalListDomainAssociationsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListDomainAssociationsRequestRequestTypeDef(
    _RequiredListDomainAssociationsRequestRequestTypeDef,
    _OptionalListDomainAssociationsRequestRequestTypeDef,
):
    pass


_RequiredListJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListJobsRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
    },
)
_OptionalListJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListJobsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListJobsRequestRequestTypeDef(
    _RequiredListJobsRequestRequestTypeDef, _OptionalListJobsRequestRequestTypeDef
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

_RequiredListWebhooksRequestRequestTypeDef = TypedDict(
    "_RequiredListWebhooksRequestRequestTypeDef",
    {
        "appId": str,
    },
)
_OptionalListWebhooksRequestRequestTypeDef = TypedDict(
    "_OptionalListWebhooksRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListWebhooksRequestRequestTypeDef(
    _RequiredListWebhooksRequestRequestTypeDef, _OptionalListWebhooksRequestRequestTypeDef
):
    pass


_RequiredStartDeploymentRequestRequestTypeDef = TypedDict(
    "_RequiredStartDeploymentRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
    },
)
_OptionalStartDeploymentRequestRequestTypeDef = TypedDict(
    "_OptionalStartDeploymentRequestRequestTypeDef",
    {
        "jobId": str,
        "sourceUrl": str,
    },
    total=False,
)


class StartDeploymentRequestRequestTypeDef(
    _RequiredStartDeploymentRequestRequestTypeDef, _OptionalStartDeploymentRequestRequestTypeDef
):
    pass


_RequiredStartJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartJobRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "jobType": JobTypeType,
    },
)
_OptionalStartJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartJobRequestRequestTypeDef",
    {
        "jobId": str,
        "jobReason": str,
        "commitId": str,
        "commitMessage": str,
        "commitTime": Union[datetime, str],
    },
    total=False,
)


class StartJobRequestRequestTypeDef(
    _RequiredStartJobRequestRequestTypeDef, _OptionalStartJobRequestRequestTypeDef
):
    pass


StopJobRequestRequestTypeDef = TypedDict(
    "StopJobRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
        "jobId": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateBranchRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBranchRequestRequestTypeDef",
    {
        "appId": str,
        "branchName": str,
    },
)
_OptionalUpdateBranchRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBranchRequestRequestTypeDef",
    {
        "description": str,
        "framework": str,
        "stage": StageType,
        "enableNotification": bool,
        "enableAutoBuild": bool,
        "environmentVariables": Mapping[str, str],
        "basicAuthCredentials": str,
        "enableBasicAuth": bool,
        "enablePerformanceMode": bool,
        "buildSpec": str,
        "ttl": str,
        "displayName": str,
        "enablePullRequestPreview": bool,
        "pullRequestEnvironmentName": str,
        "backendEnvironmentArn": str,
    },
    total=False,
)


class UpdateBranchRequestRequestTypeDef(
    _RequiredUpdateBranchRequestRequestTypeDef, _OptionalUpdateBranchRequestRequestTypeDef
):
    pass


_RequiredUpdateWebhookRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWebhookRequestRequestTypeDef",
    {
        "webhookId": str,
    },
)
_OptionalUpdateWebhookRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWebhookRequestRequestTypeDef",
    {
        "branchName": str,
        "description": str,
    },
    total=False,
)


class UpdateWebhookRequestRequestTypeDef(
    _RequiredUpdateWebhookRequestRequestTypeDef, _OptionalUpdateWebhookRequestRequestTypeDef
):
    pass


_RequiredCreateAppRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAppRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateAppRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAppRequestRequestTypeDef",
    {
        "description": str,
        "repository": str,
        "platform": PlatformType,
        "iamServiceRoleArn": str,
        "oauthToken": str,
        "accessToken": str,
        "environmentVariables": Mapping[str, str],
        "enableBranchAutoBuild": bool,
        "enableBranchAutoDeletion": bool,
        "enableBasicAuth": bool,
        "basicAuthCredentials": str,
        "customRules": Sequence[CustomRuleTypeDef],
        "tags": Mapping[str, str],
        "buildSpec": str,
        "customHeaders": str,
        "enableAutoBranchCreation": bool,
        "autoBranchCreationPatterns": Sequence[str],
        "autoBranchCreationConfig": AutoBranchCreationConfigTypeDef,
    },
    total=False,
)


class CreateAppRequestRequestTypeDef(
    _RequiredCreateAppRequestRequestTypeDef, _OptionalCreateAppRequestRequestTypeDef
):
    pass


_RequiredUpdateAppRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAppRequestRequestTypeDef",
    {
        "appId": str,
    },
)
_OptionalUpdateAppRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAppRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
        "platform": PlatformType,
        "iamServiceRoleArn": str,
        "environmentVariables": Mapping[str, str],
        "enableBranchAutoBuild": bool,
        "enableBranchAutoDeletion": bool,
        "enableBasicAuth": bool,
        "basicAuthCredentials": str,
        "customRules": Sequence[CustomRuleTypeDef],
        "buildSpec": str,
        "customHeaders": str,
        "enableAutoBranchCreation": bool,
        "autoBranchCreationPatterns": Sequence[str],
        "autoBranchCreationConfig": AutoBranchCreationConfigTypeDef,
        "repository": str,
        "oauthToken": str,
        "accessToken": str,
    },
    total=False,
)


class UpdateAppRequestRequestTypeDef(
    _RequiredUpdateAppRequestRequestTypeDef, _OptionalUpdateAppRequestRequestTypeDef
):
    pass


_RequiredAppTypeDef = TypedDict(
    "_RequiredAppTypeDef",
    {
        "appId": str,
        "appArn": str,
        "name": str,
        "description": str,
        "repository": str,
        "platform": PlatformType,
        "createTime": datetime,
        "updateTime": datetime,
        "environmentVariables": Dict[str, str],
        "defaultDomain": str,
        "enableBranchAutoBuild": bool,
        "enableBasicAuth": bool,
    },
)
_OptionalAppTypeDef = TypedDict(
    "_OptionalAppTypeDef",
    {
        "tags": Dict[str, str],
        "iamServiceRoleArn": str,
        "enableBranchAutoDeletion": bool,
        "basicAuthCredentials": str,
        "customRules": List[CustomRuleTypeDef],
        "productionBranch": ProductionBranchTypeDef,
        "buildSpec": str,
        "customHeaders": str,
        "enableAutoBranchCreation": bool,
        "autoBranchCreationPatterns": List[str],
        "autoBranchCreationConfig": AutoBranchCreationConfigTypeDef,
        "repositoryCloneMethod": RepositoryCloneMethodType,
    },
    total=False,
)


class AppTypeDef(_RequiredAppTypeDef, _OptionalAppTypeDef):
    pass


CreateBackendEnvironmentResultTypeDef = TypedDict(
    "CreateBackendEnvironmentResultTypeDef",
    {
        "backendEnvironment": BackendEnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBranchResultTypeDef = TypedDict(
    "CreateBranchResultTypeDef",
    {
        "branch": BranchTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDeploymentResultTypeDef = TypedDict(
    "CreateDeploymentResultTypeDef",
    {
        "jobId": str,
        "fileUploadUrls": Dict[str, str],
        "zipUploadUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBackendEnvironmentResultTypeDef = TypedDict(
    "DeleteBackendEnvironmentResultTypeDef",
    {
        "backendEnvironment": BackendEnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBranchResultTypeDef = TypedDict(
    "DeleteBranchResultTypeDef",
    {
        "branch": BranchTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateAccessLogsResultTypeDef = TypedDict(
    "GenerateAccessLogsResultTypeDef",
    {
        "logUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetArtifactUrlResultTypeDef = TypedDict(
    "GetArtifactUrlResultTypeDef",
    {
        "artifactId": str,
        "artifactUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBackendEnvironmentResultTypeDef = TypedDict(
    "GetBackendEnvironmentResultTypeDef",
    {
        "backendEnvironment": BackendEnvironmentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBranchResultTypeDef = TypedDict(
    "GetBranchResultTypeDef",
    {
        "branch": BranchTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListArtifactsResultTypeDef = TypedDict(
    "ListArtifactsResultTypeDef",
    {
        "artifacts": List[ArtifactTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBackendEnvironmentsResultTypeDef = TypedDict(
    "ListBackendEnvironmentsResultTypeDef",
    {
        "backendEnvironments": List[BackendEnvironmentTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBranchesResultTypeDef = TypedDict(
    "ListBranchesResultTypeDef",
    {
        "branches": List[BranchTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBranchResultTypeDef = TypedDict(
    "UpdateBranchResultTypeDef",
    {
        "branch": BranchTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDomainAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDomainAssociationRequestRequestTypeDef",
    {
        "appId": str,
        "domainName": str,
        "subDomainSettings": Sequence[SubDomainSettingTypeDef],
    },
)
_OptionalCreateDomainAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDomainAssociationRequestRequestTypeDef",
    {
        "enableAutoSubDomain": bool,
        "autoSubDomainCreationPatterns": Sequence[str],
        "autoSubDomainIAMRole": str,
    },
    total=False,
)


class CreateDomainAssociationRequestRequestTypeDef(
    _RequiredCreateDomainAssociationRequestRequestTypeDef,
    _OptionalCreateDomainAssociationRequestRequestTypeDef,
):
    pass


SubDomainTypeDef = TypedDict(
    "SubDomainTypeDef",
    {
        "subDomainSetting": SubDomainSettingTypeDef,
        "verified": bool,
        "dnsRecord": str,
    },
)

_RequiredUpdateDomainAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDomainAssociationRequestRequestTypeDef",
    {
        "appId": str,
        "domainName": str,
    },
)
_OptionalUpdateDomainAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDomainAssociationRequestRequestTypeDef",
    {
        "enableAutoSubDomain": bool,
        "subDomainSettings": Sequence[SubDomainSettingTypeDef],
        "autoSubDomainCreationPatterns": Sequence[str],
        "autoSubDomainIAMRole": str,
    },
    total=False,
)


class UpdateDomainAssociationRequestRequestTypeDef(
    _RequiredUpdateDomainAssociationRequestRequestTypeDef,
    _OptionalUpdateDomainAssociationRequestRequestTypeDef,
):
    pass


CreateWebhookResultTypeDef = TypedDict(
    "CreateWebhookResultTypeDef",
    {
        "webhook": WebhookTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteWebhookResultTypeDef = TypedDict(
    "DeleteWebhookResultTypeDef",
    {
        "webhook": WebhookTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWebhookResultTypeDef = TypedDict(
    "GetWebhookResultTypeDef",
    {
        "webhook": WebhookTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWebhooksResultTypeDef = TypedDict(
    "ListWebhooksResultTypeDef",
    {
        "webhooks": List[WebhookTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateWebhookResultTypeDef = TypedDict(
    "UpdateWebhookResultTypeDef",
    {
        "webhook": WebhookTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteJobResultTypeDef = TypedDict(
    "DeleteJobResultTypeDef",
    {
        "jobSummary": JobSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListJobsResultTypeDef = TypedDict(
    "ListJobsResultTypeDef",
    {
        "jobSummaries": List[JobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDeploymentResultTypeDef = TypedDict(
    "StartDeploymentResultTypeDef",
    {
        "jobSummary": JobSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartJobResultTypeDef = TypedDict(
    "StartJobResultTypeDef",
    {
        "jobSummary": JobSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopJobResultTypeDef = TypedDict(
    "StopJobResultTypeDef",
    {
        "jobSummary": JobSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "summary": JobSummaryTypeDef,
        "steps": List[StepTypeDef],
    },
)

ListAppsRequestListAppsPaginateTypeDef = TypedDict(
    "ListAppsRequestListAppsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListBranchesRequestListBranchesPaginateTypeDef = TypedDict(
    "_RequiredListBranchesRequestListBranchesPaginateTypeDef",
    {
        "appId": str,
    },
)
_OptionalListBranchesRequestListBranchesPaginateTypeDef = TypedDict(
    "_OptionalListBranchesRequestListBranchesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListBranchesRequestListBranchesPaginateTypeDef(
    _RequiredListBranchesRequestListBranchesPaginateTypeDef,
    _OptionalListBranchesRequestListBranchesPaginateTypeDef,
):
    pass


_RequiredListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef = TypedDict(
    "_RequiredListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef",
    {
        "appId": str,
    },
)
_OptionalListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef = TypedDict(
    "_OptionalListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef(
    _RequiredListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef,
    _OptionalListDomainAssociationsRequestListDomainAssociationsPaginateTypeDef,
):
    pass


_RequiredListJobsRequestListJobsPaginateTypeDef = TypedDict(
    "_RequiredListJobsRequestListJobsPaginateTypeDef",
    {
        "appId": str,
        "branchName": str,
    },
)
_OptionalListJobsRequestListJobsPaginateTypeDef = TypedDict(
    "_OptionalListJobsRequestListJobsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListJobsRequestListJobsPaginateTypeDef(
    _RequiredListJobsRequestListJobsPaginateTypeDef, _OptionalListJobsRequestListJobsPaginateTypeDef
):
    pass


CreateAppResultTypeDef = TypedDict(
    "CreateAppResultTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAppResultTypeDef = TypedDict(
    "DeleteAppResultTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAppResultTypeDef = TypedDict(
    "GetAppResultTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAppsResultTypeDef = TypedDict(
    "ListAppsResultTypeDef",
    {
        "apps": List[AppTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAppResultTypeDef = TypedDict(
    "UpdateAppResultTypeDef",
    {
        "app": AppTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDomainAssociationTypeDef = TypedDict(
    "_RequiredDomainAssociationTypeDef",
    {
        "domainAssociationArn": str,
        "domainName": str,
        "enableAutoSubDomain": bool,
        "domainStatus": DomainStatusType,
        "statusReason": str,
        "subDomains": List[SubDomainTypeDef],
    },
)
_OptionalDomainAssociationTypeDef = TypedDict(
    "_OptionalDomainAssociationTypeDef",
    {
        "autoSubDomainCreationPatterns": List[str],
        "autoSubDomainIAMRole": str,
        "certificateVerificationDNSRecord": str,
    },
    total=False,
)


class DomainAssociationTypeDef(
    _RequiredDomainAssociationTypeDef, _OptionalDomainAssociationTypeDef
):
    pass


GetJobResultTypeDef = TypedDict(
    "GetJobResultTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDomainAssociationResultTypeDef = TypedDict(
    "CreateDomainAssociationResultTypeDef",
    {
        "domainAssociation": DomainAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDomainAssociationResultTypeDef = TypedDict(
    "DeleteDomainAssociationResultTypeDef",
    {
        "domainAssociation": DomainAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDomainAssociationResultTypeDef = TypedDict(
    "GetDomainAssociationResultTypeDef",
    {
        "domainAssociation": DomainAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDomainAssociationsResultTypeDef = TypedDict(
    "ListDomainAssociationsResultTypeDef",
    {
        "domainAssociations": List[DomainAssociationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDomainAssociationResultTypeDef = TypedDict(
    "UpdateDomainAssociationResultTypeDef",
    {
        "domainAssociation": DomainAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
