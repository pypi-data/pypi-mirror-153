"""
Type annotations for imagebuilder service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/type_defs/)

Usage::

    ```python
    from mypy_boto3_imagebuilder.type_defs import SystemsManagerAgentTypeDef

    data: SystemsManagerAgentTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    BuildTypeType,
    ComponentTypeType,
    DiskImageFormatType,
    EbsVolumeTypeType,
    ImageStatusType,
    ImageTypeType,
    OwnershipType,
    PipelineExecutionStartConditionType,
    PipelineStatusType,
    PlatformType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "SystemsManagerAgentTypeDef",
    "LaunchPermissionConfigurationTypeDef",
    "ImageStateTypeDef",
    "CancelImageCreationRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ComponentParameterTypeDef",
    "ComponentParameterDetailTypeDef",
    "ComponentStateTypeDef",
    "ComponentVersionTypeDef",
    "TargetContainerRepositoryTypeDef",
    "ContainerRecipeSummaryTypeDef",
    "ContainerTypeDef",
    "CreateComponentRequestRequestTypeDef",
    "ImageTestsConfigurationTypeDef",
    "ScheduleTypeDef",
    "InstanceMetadataOptionsTypeDef",
    "DeleteComponentRequestRequestTypeDef",
    "DeleteContainerRecipeRequestRequestTypeDef",
    "DeleteDistributionConfigurationRequestRequestTypeDef",
    "DeleteImagePipelineRequestRequestTypeDef",
    "DeleteImageRecipeRequestRequestTypeDef",
    "DeleteImageRequestRequestTypeDef",
    "DeleteInfrastructureConfigurationRequestRequestTypeDef",
    "DistributionConfigurationSummaryTypeDef",
    "LaunchTemplateConfigurationTypeDef",
    "S3ExportConfigurationTypeDef",
    "EbsInstanceBlockDeviceSpecificationTypeDef",
    "FastLaunchLaunchTemplateSpecificationTypeDef",
    "FastLaunchSnapshotConfigurationTypeDef",
    "FilterTypeDef",
    "GetComponentPolicyRequestRequestTypeDef",
    "GetComponentRequestRequestTypeDef",
    "GetContainerRecipePolicyRequestRequestTypeDef",
    "GetContainerRecipeRequestRequestTypeDef",
    "GetDistributionConfigurationRequestRequestTypeDef",
    "GetImagePipelineRequestRequestTypeDef",
    "GetImagePolicyRequestRequestTypeDef",
    "GetImageRecipePolicyRequestRequestTypeDef",
    "GetImageRecipeRequestRequestTypeDef",
    "GetImageRequestRequestTypeDef",
    "GetInfrastructureConfigurationRequestRequestTypeDef",
    "ImagePackageTypeDef",
    "ImageRecipeSummaryTypeDef",
    "ImageVersionTypeDef",
    "ImportComponentRequestRequestTypeDef",
    "ImportVmImageRequestRequestTypeDef",
    "InfrastructureConfigurationSummaryTypeDef",
    "ListComponentBuildVersionsRequestRequestTypeDef",
    "ListImagePackagesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "S3LogsTypeDef",
    "PutComponentPolicyRequestRequestTypeDef",
    "PutContainerRecipePolicyRequestRequestTypeDef",
    "PutImagePolicyRequestRequestTypeDef",
    "PutImageRecipePolicyRequestRequestTypeDef",
    "StartImagePipelineExecutionRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AdditionalInstanceConfigurationTypeDef",
    "AmiDistributionConfigurationTypeDef",
    "AmiTypeDef",
    "CancelImageCreationResponseTypeDef",
    "CreateComponentResponseTypeDef",
    "CreateContainerRecipeResponseTypeDef",
    "CreateDistributionConfigurationResponseTypeDef",
    "CreateImagePipelineResponseTypeDef",
    "CreateImageRecipeResponseTypeDef",
    "CreateImageResponseTypeDef",
    "CreateInfrastructureConfigurationResponseTypeDef",
    "DeleteComponentResponseTypeDef",
    "DeleteContainerRecipeResponseTypeDef",
    "DeleteDistributionConfigurationResponseTypeDef",
    "DeleteImagePipelineResponseTypeDef",
    "DeleteImageRecipeResponseTypeDef",
    "DeleteImageResponseTypeDef",
    "DeleteInfrastructureConfigurationResponseTypeDef",
    "GetComponentPolicyResponseTypeDef",
    "GetContainerRecipePolicyResponseTypeDef",
    "GetImagePolicyResponseTypeDef",
    "GetImageRecipePolicyResponseTypeDef",
    "ImportComponentResponseTypeDef",
    "ImportVmImageResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutComponentPolicyResponseTypeDef",
    "PutContainerRecipePolicyResponseTypeDef",
    "PutImagePolicyResponseTypeDef",
    "PutImageRecipePolicyResponseTypeDef",
    "StartImagePipelineExecutionResponseTypeDef",
    "UpdateDistributionConfigurationResponseTypeDef",
    "UpdateImagePipelineResponseTypeDef",
    "UpdateInfrastructureConfigurationResponseTypeDef",
    "ComponentConfigurationTypeDef",
    "ComponentSummaryTypeDef",
    "ComponentTypeDef",
    "ListComponentsResponseTypeDef",
    "ContainerDistributionConfigurationTypeDef",
    "ListContainerRecipesResponseTypeDef",
    "CreateImageRequestRequestTypeDef",
    "CreateImagePipelineRequestRequestTypeDef",
    "ImagePipelineTypeDef",
    "UpdateImagePipelineRequestRequestTypeDef",
    "ListDistributionConfigurationsResponseTypeDef",
    "InstanceBlockDeviceMappingTypeDef",
    "FastLaunchConfigurationTypeDef",
    "ListComponentsRequestRequestTypeDef",
    "ListContainerRecipesRequestRequestTypeDef",
    "ListDistributionConfigurationsRequestRequestTypeDef",
    "ListImageBuildVersionsRequestRequestTypeDef",
    "ListImagePipelineImagesRequestRequestTypeDef",
    "ListImagePipelinesRequestRequestTypeDef",
    "ListImageRecipesRequestRequestTypeDef",
    "ListImagesRequestRequestTypeDef",
    "ListInfrastructureConfigurationsRequestRequestTypeDef",
    "ListImagePackagesResponseTypeDef",
    "ListImageRecipesResponseTypeDef",
    "ListImagesResponseTypeDef",
    "ListInfrastructureConfigurationsResponseTypeDef",
    "LoggingTypeDef",
    "OutputResourcesTypeDef",
    "ListComponentBuildVersionsResponseTypeDef",
    "GetComponentResponseTypeDef",
    "GetImagePipelineResponseTypeDef",
    "ListImagePipelinesResponseTypeDef",
    "CreateImageRecipeRequestRequestTypeDef",
    "ImageRecipeTypeDef",
    "InstanceConfigurationTypeDef",
    "DistributionTypeDef",
    "CreateInfrastructureConfigurationRequestRequestTypeDef",
    "InfrastructureConfigurationTypeDef",
    "UpdateInfrastructureConfigurationRequestRequestTypeDef",
    "ImageSummaryTypeDef",
    "GetImageRecipeResponseTypeDef",
    "ContainerRecipeTypeDef",
    "CreateContainerRecipeRequestRequestTypeDef",
    "CreateDistributionConfigurationRequestRequestTypeDef",
    "DistributionConfigurationTypeDef",
    "UpdateDistributionConfigurationRequestRequestTypeDef",
    "GetInfrastructureConfigurationResponseTypeDef",
    "ListImageBuildVersionsResponseTypeDef",
    "ListImagePipelineImagesResponseTypeDef",
    "GetContainerRecipeResponseTypeDef",
    "GetDistributionConfigurationResponseTypeDef",
    "ImageTypeDef",
    "GetImageResponseTypeDef",
)

SystemsManagerAgentTypeDef = TypedDict(
    "SystemsManagerAgentTypeDef",
    {
        "uninstallAfterBuild": bool,
    },
    total=False,
)

LaunchPermissionConfigurationTypeDef = TypedDict(
    "LaunchPermissionConfigurationTypeDef",
    {
        "userIds": Sequence[str],
        "userGroups": Sequence[str],
        "organizationArns": Sequence[str],
        "organizationalUnitArns": Sequence[str],
    },
    total=False,
)

ImageStateTypeDef = TypedDict(
    "ImageStateTypeDef",
    {
        "status": ImageStatusType,
        "reason": str,
    },
    total=False,
)

CancelImageCreationRequestRequestTypeDef = TypedDict(
    "CancelImageCreationRequestRequestTypeDef",
    {
        "imageBuildVersionArn": str,
        "clientToken": str,
    },
)

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

ComponentParameterTypeDef = TypedDict(
    "ComponentParameterTypeDef",
    {
        "name": str,
        "value": Sequence[str],
    },
)

_RequiredComponentParameterDetailTypeDef = TypedDict(
    "_RequiredComponentParameterDetailTypeDef",
    {
        "name": str,
        "type": str,
    },
)
_OptionalComponentParameterDetailTypeDef = TypedDict(
    "_OptionalComponentParameterDetailTypeDef",
    {
        "defaultValue": List[str],
        "description": str,
    },
    total=False,
)


class ComponentParameterDetailTypeDef(
    _RequiredComponentParameterDetailTypeDef, _OptionalComponentParameterDetailTypeDef
):
    pass


ComponentStateTypeDef = TypedDict(
    "ComponentStateTypeDef",
    {
        "status": Literal["DEPRECATED"],
        "reason": str,
    },
    total=False,
)

ComponentVersionTypeDef = TypedDict(
    "ComponentVersionTypeDef",
    {
        "arn": str,
        "name": str,
        "version": str,
        "description": str,
        "platform": PlatformType,
        "supportedOsVersions": List[str],
        "type": ComponentTypeType,
        "owner": str,
        "dateCreated": str,
    },
    total=False,
)

TargetContainerRepositoryTypeDef = TypedDict(
    "TargetContainerRepositoryTypeDef",
    {
        "service": Literal["ECR"],
        "repositoryName": str,
    },
)

ContainerRecipeSummaryTypeDef = TypedDict(
    "ContainerRecipeSummaryTypeDef",
    {
        "arn": str,
        "containerType": Literal["DOCKER"],
        "name": str,
        "platform": PlatformType,
        "owner": str,
        "parentImage": str,
        "dateCreated": str,
        "tags": Dict[str, str],
    },
    total=False,
)

ContainerTypeDef = TypedDict(
    "ContainerTypeDef",
    {
        "region": str,
        "imageUris": List[str],
    },
    total=False,
)

_RequiredCreateComponentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateComponentRequestRequestTypeDef",
    {
        "name": str,
        "semanticVersion": str,
        "platform": PlatformType,
        "clientToken": str,
    },
)
_OptionalCreateComponentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateComponentRequestRequestTypeDef",
    {
        "description": str,
        "changeDescription": str,
        "supportedOsVersions": Sequence[str],
        "data": str,
        "uri": str,
        "kmsKeyId": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateComponentRequestRequestTypeDef(
    _RequiredCreateComponentRequestRequestTypeDef, _OptionalCreateComponentRequestRequestTypeDef
):
    pass


ImageTestsConfigurationTypeDef = TypedDict(
    "ImageTestsConfigurationTypeDef",
    {
        "imageTestsEnabled": bool,
        "timeoutMinutes": int,
    },
    total=False,
)

ScheduleTypeDef = TypedDict(
    "ScheduleTypeDef",
    {
        "scheduleExpression": str,
        "timezone": str,
        "pipelineExecutionStartCondition": PipelineExecutionStartConditionType,
    },
    total=False,
)

InstanceMetadataOptionsTypeDef = TypedDict(
    "InstanceMetadataOptionsTypeDef",
    {
        "httpTokens": str,
        "httpPutResponseHopLimit": int,
    },
    total=False,
)

DeleteComponentRequestRequestTypeDef = TypedDict(
    "DeleteComponentRequestRequestTypeDef",
    {
        "componentBuildVersionArn": str,
    },
)

DeleteContainerRecipeRequestRequestTypeDef = TypedDict(
    "DeleteContainerRecipeRequestRequestTypeDef",
    {
        "containerRecipeArn": str,
    },
)

DeleteDistributionConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteDistributionConfigurationRequestRequestTypeDef",
    {
        "distributionConfigurationArn": str,
    },
)

DeleteImagePipelineRequestRequestTypeDef = TypedDict(
    "DeleteImagePipelineRequestRequestTypeDef",
    {
        "imagePipelineArn": str,
    },
)

DeleteImageRecipeRequestRequestTypeDef = TypedDict(
    "DeleteImageRecipeRequestRequestTypeDef",
    {
        "imageRecipeArn": str,
    },
)

DeleteImageRequestRequestTypeDef = TypedDict(
    "DeleteImageRequestRequestTypeDef",
    {
        "imageBuildVersionArn": str,
    },
)

DeleteInfrastructureConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteInfrastructureConfigurationRequestRequestTypeDef",
    {
        "infrastructureConfigurationArn": str,
    },
)

DistributionConfigurationSummaryTypeDef = TypedDict(
    "DistributionConfigurationSummaryTypeDef",
    {
        "arn": str,
        "name": str,
        "description": str,
        "dateCreated": str,
        "dateUpdated": str,
        "tags": Dict[str, str],
        "regions": List[str],
    },
    total=False,
)

_RequiredLaunchTemplateConfigurationTypeDef = TypedDict(
    "_RequiredLaunchTemplateConfigurationTypeDef",
    {
        "launchTemplateId": str,
    },
)
_OptionalLaunchTemplateConfigurationTypeDef = TypedDict(
    "_OptionalLaunchTemplateConfigurationTypeDef",
    {
        "accountId": str,
        "setDefaultVersion": bool,
    },
    total=False,
)


class LaunchTemplateConfigurationTypeDef(
    _RequiredLaunchTemplateConfigurationTypeDef, _OptionalLaunchTemplateConfigurationTypeDef
):
    pass


_RequiredS3ExportConfigurationTypeDef = TypedDict(
    "_RequiredS3ExportConfigurationTypeDef",
    {
        "roleName": str,
        "diskImageFormat": DiskImageFormatType,
        "s3Bucket": str,
    },
)
_OptionalS3ExportConfigurationTypeDef = TypedDict(
    "_OptionalS3ExportConfigurationTypeDef",
    {
        "s3Prefix": str,
    },
    total=False,
)


class S3ExportConfigurationTypeDef(
    _RequiredS3ExportConfigurationTypeDef, _OptionalS3ExportConfigurationTypeDef
):
    pass


EbsInstanceBlockDeviceSpecificationTypeDef = TypedDict(
    "EbsInstanceBlockDeviceSpecificationTypeDef",
    {
        "encrypted": bool,
        "deleteOnTermination": bool,
        "iops": int,
        "kmsKeyId": str,
        "snapshotId": str,
        "volumeSize": int,
        "volumeType": EbsVolumeTypeType,
        "throughput": int,
    },
    total=False,
)

FastLaunchLaunchTemplateSpecificationTypeDef = TypedDict(
    "FastLaunchLaunchTemplateSpecificationTypeDef",
    {
        "launchTemplateId": str,
        "launchTemplateName": str,
        "launchTemplateVersion": str,
    },
    total=False,
)

FastLaunchSnapshotConfigurationTypeDef = TypedDict(
    "FastLaunchSnapshotConfigurationTypeDef",
    {
        "targetResourceCount": int,
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "name": str,
        "values": Sequence[str],
    },
    total=False,
)

GetComponentPolicyRequestRequestTypeDef = TypedDict(
    "GetComponentPolicyRequestRequestTypeDef",
    {
        "componentArn": str,
    },
)

GetComponentRequestRequestTypeDef = TypedDict(
    "GetComponentRequestRequestTypeDef",
    {
        "componentBuildVersionArn": str,
    },
)

GetContainerRecipePolicyRequestRequestTypeDef = TypedDict(
    "GetContainerRecipePolicyRequestRequestTypeDef",
    {
        "containerRecipeArn": str,
    },
)

GetContainerRecipeRequestRequestTypeDef = TypedDict(
    "GetContainerRecipeRequestRequestTypeDef",
    {
        "containerRecipeArn": str,
    },
)

GetDistributionConfigurationRequestRequestTypeDef = TypedDict(
    "GetDistributionConfigurationRequestRequestTypeDef",
    {
        "distributionConfigurationArn": str,
    },
)

GetImagePipelineRequestRequestTypeDef = TypedDict(
    "GetImagePipelineRequestRequestTypeDef",
    {
        "imagePipelineArn": str,
    },
)

GetImagePolicyRequestRequestTypeDef = TypedDict(
    "GetImagePolicyRequestRequestTypeDef",
    {
        "imageArn": str,
    },
)

GetImageRecipePolicyRequestRequestTypeDef = TypedDict(
    "GetImageRecipePolicyRequestRequestTypeDef",
    {
        "imageRecipeArn": str,
    },
)

GetImageRecipeRequestRequestTypeDef = TypedDict(
    "GetImageRecipeRequestRequestTypeDef",
    {
        "imageRecipeArn": str,
    },
)

GetImageRequestRequestTypeDef = TypedDict(
    "GetImageRequestRequestTypeDef",
    {
        "imageBuildVersionArn": str,
    },
)

GetInfrastructureConfigurationRequestRequestTypeDef = TypedDict(
    "GetInfrastructureConfigurationRequestRequestTypeDef",
    {
        "infrastructureConfigurationArn": str,
    },
)

ImagePackageTypeDef = TypedDict(
    "ImagePackageTypeDef",
    {
        "packageName": str,
        "packageVersion": str,
    },
    total=False,
)

ImageRecipeSummaryTypeDef = TypedDict(
    "ImageRecipeSummaryTypeDef",
    {
        "arn": str,
        "name": str,
        "platform": PlatformType,
        "owner": str,
        "parentImage": str,
        "dateCreated": str,
        "tags": Dict[str, str],
    },
    total=False,
)

ImageVersionTypeDef = TypedDict(
    "ImageVersionTypeDef",
    {
        "arn": str,
        "name": str,
        "type": ImageTypeType,
        "version": str,
        "platform": PlatformType,
        "osVersion": str,
        "owner": str,
        "dateCreated": str,
        "buildType": BuildTypeType,
    },
    total=False,
)

_RequiredImportComponentRequestRequestTypeDef = TypedDict(
    "_RequiredImportComponentRequestRequestTypeDef",
    {
        "name": str,
        "semanticVersion": str,
        "type": ComponentTypeType,
        "format": Literal["SHELL"],
        "platform": PlatformType,
        "clientToken": str,
    },
)
_OptionalImportComponentRequestRequestTypeDef = TypedDict(
    "_OptionalImportComponentRequestRequestTypeDef",
    {
        "description": str,
        "changeDescription": str,
        "data": str,
        "uri": str,
        "kmsKeyId": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class ImportComponentRequestRequestTypeDef(
    _RequiredImportComponentRequestRequestTypeDef, _OptionalImportComponentRequestRequestTypeDef
):
    pass


_RequiredImportVmImageRequestRequestTypeDef = TypedDict(
    "_RequiredImportVmImageRequestRequestTypeDef",
    {
        "name": str,
        "semanticVersion": str,
        "platform": PlatformType,
        "vmImportTaskId": str,
        "clientToken": str,
    },
)
_OptionalImportVmImageRequestRequestTypeDef = TypedDict(
    "_OptionalImportVmImageRequestRequestTypeDef",
    {
        "description": str,
        "osVersion": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class ImportVmImageRequestRequestTypeDef(
    _RequiredImportVmImageRequestRequestTypeDef, _OptionalImportVmImageRequestRequestTypeDef
):
    pass


InfrastructureConfigurationSummaryTypeDef = TypedDict(
    "InfrastructureConfigurationSummaryTypeDef",
    {
        "arn": str,
        "name": str,
        "description": str,
        "dateCreated": str,
        "dateUpdated": str,
        "resourceTags": Dict[str, str],
        "tags": Dict[str, str],
        "instanceTypes": List[str],
        "instanceProfileName": str,
    },
    total=False,
)

_RequiredListComponentBuildVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListComponentBuildVersionsRequestRequestTypeDef",
    {
        "componentVersionArn": str,
    },
)
_OptionalListComponentBuildVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListComponentBuildVersionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListComponentBuildVersionsRequestRequestTypeDef(
    _RequiredListComponentBuildVersionsRequestRequestTypeDef,
    _OptionalListComponentBuildVersionsRequestRequestTypeDef,
):
    pass


_RequiredListImagePackagesRequestRequestTypeDef = TypedDict(
    "_RequiredListImagePackagesRequestRequestTypeDef",
    {
        "imageBuildVersionArn": str,
    },
)
_OptionalListImagePackagesRequestRequestTypeDef = TypedDict(
    "_OptionalListImagePackagesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListImagePackagesRequestRequestTypeDef(
    _RequiredListImagePackagesRequestRequestTypeDef, _OptionalListImagePackagesRequestRequestTypeDef
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

S3LogsTypeDef = TypedDict(
    "S3LogsTypeDef",
    {
        "s3BucketName": str,
        "s3KeyPrefix": str,
    },
    total=False,
)

PutComponentPolicyRequestRequestTypeDef = TypedDict(
    "PutComponentPolicyRequestRequestTypeDef",
    {
        "componentArn": str,
        "policy": str,
    },
)

PutContainerRecipePolicyRequestRequestTypeDef = TypedDict(
    "PutContainerRecipePolicyRequestRequestTypeDef",
    {
        "containerRecipeArn": str,
        "policy": str,
    },
)

PutImagePolicyRequestRequestTypeDef = TypedDict(
    "PutImagePolicyRequestRequestTypeDef",
    {
        "imageArn": str,
        "policy": str,
    },
)

PutImageRecipePolicyRequestRequestTypeDef = TypedDict(
    "PutImageRecipePolicyRequestRequestTypeDef",
    {
        "imageRecipeArn": str,
        "policy": str,
    },
)

StartImagePipelineExecutionRequestRequestTypeDef = TypedDict(
    "StartImagePipelineExecutionRequestRequestTypeDef",
    {
        "imagePipelineArn": str,
        "clientToken": str,
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

AdditionalInstanceConfigurationTypeDef = TypedDict(
    "AdditionalInstanceConfigurationTypeDef",
    {
        "systemsManagerAgent": SystemsManagerAgentTypeDef,
        "userDataOverride": str,
    },
    total=False,
)

AmiDistributionConfigurationTypeDef = TypedDict(
    "AmiDistributionConfigurationTypeDef",
    {
        "name": str,
        "description": str,
        "targetAccountIds": Sequence[str],
        "amiTags": Mapping[str, str],
        "kmsKeyId": str,
        "launchPermission": LaunchPermissionConfigurationTypeDef,
    },
    total=False,
)

AmiTypeDef = TypedDict(
    "AmiTypeDef",
    {
        "region": str,
        "image": str,
        "name": str,
        "description": str,
        "state": ImageStateTypeDef,
        "accountId": str,
    },
    total=False,
)

CancelImageCreationResponseTypeDef = TypedDict(
    "CancelImageCreationResponseTypeDef",
    {
        "requestId": str,
        "clientToken": str,
        "imageBuildVersionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateComponentResponseTypeDef = TypedDict(
    "CreateComponentResponseTypeDef",
    {
        "requestId": str,
        "clientToken": str,
        "componentBuildVersionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateContainerRecipeResponseTypeDef = TypedDict(
    "CreateContainerRecipeResponseTypeDef",
    {
        "requestId": str,
        "clientToken": str,
        "containerRecipeArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDistributionConfigurationResponseTypeDef = TypedDict(
    "CreateDistributionConfigurationResponseTypeDef",
    {
        "requestId": str,
        "clientToken": str,
        "distributionConfigurationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateImagePipelineResponseTypeDef = TypedDict(
    "CreateImagePipelineResponseTypeDef",
    {
        "requestId": str,
        "clientToken": str,
        "imagePipelineArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateImageRecipeResponseTypeDef = TypedDict(
    "CreateImageRecipeResponseTypeDef",
    {
        "requestId": str,
        "clientToken": str,
        "imageRecipeArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateImageResponseTypeDef = TypedDict(
    "CreateImageResponseTypeDef",
    {
        "requestId": str,
        "clientToken": str,
        "imageBuildVersionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateInfrastructureConfigurationResponseTypeDef = TypedDict(
    "CreateInfrastructureConfigurationResponseTypeDef",
    {
        "requestId": str,
        "clientToken": str,
        "infrastructureConfigurationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteComponentResponseTypeDef = TypedDict(
    "DeleteComponentResponseTypeDef",
    {
        "requestId": str,
        "componentBuildVersionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteContainerRecipeResponseTypeDef = TypedDict(
    "DeleteContainerRecipeResponseTypeDef",
    {
        "requestId": str,
        "containerRecipeArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDistributionConfigurationResponseTypeDef = TypedDict(
    "DeleteDistributionConfigurationResponseTypeDef",
    {
        "requestId": str,
        "distributionConfigurationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteImagePipelineResponseTypeDef = TypedDict(
    "DeleteImagePipelineResponseTypeDef",
    {
        "requestId": str,
        "imagePipelineArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteImageRecipeResponseTypeDef = TypedDict(
    "DeleteImageRecipeResponseTypeDef",
    {
        "requestId": str,
        "imageRecipeArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteImageResponseTypeDef = TypedDict(
    "DeleteImageResponseTypeDef",
    {
        "requestId": str,
        "imageBuildVersionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteInfrastructureConfigurationResponseTypeDef = TypedDict(
    "DeleteInfrastructureConfigurationResponseTypeDef",
    {
        "requestId": str,
        "infrastructureConfigurationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetComponentPolicyResponseTypeDef = TypedDict(
    "GetComponentPolicyResponseTypeDef",
    {
        "requestId": str,
        "policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContainerRecipePolicyResponseTypeDef = TypedDict(
    "GetContainerRecipePolicyResponseTypeDef",
    {
        "requestId": str,
        "policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetImagePolicyResponseTypeDef = TypedDict(
    "GetImagePolicyResponseTypeDef",
    {
        "requestId": str,
        "policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetImageRecipePolicyResponseTypeDef = TypedDict(
    "GetImageRecipePolicyResponseTypeDef",
    {
        "requestId": str,
        "policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportComponentResponseTypeDef = TypedDict(
    "ImportComponentResponseTypeDef",
    {
        "requestId": str,
        "clientToken": str,
        "componentBuildVersionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportVmImageResponseTypeDef = TypedDict(
    "ImportVmImageResponseTypeDef",
    {
        "requestId": str,
        "imageArn": str,
        "clientToken": str,
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

PutComponentPolicyResponseTypeDef = TypedDict(
    "PutComponentPolicyResponseTypeDef",
    {
        "requestId": str,
        "componentArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutContainerRecipePolicyResponseTypeDef = TypedDict(
    "PutContainerRecipePolicyResponseTypeDef",
    {
        "requestId": str,
        "containerRecipeArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutImagePolicyResponseTypeDef = TypedDict(
    "PutImagePolicyResponseTypeDef",
    {
        "requestId": str,
        "imageArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutImageRecipePolicyResponseTypeDef = TypedDict(
    "PutImageRecipePolicyResponseTypeDef",
    {
        "requestId": str,
        "imageRecipeArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartImagePipelineExecutionResponseTypeDef = TypedDict(
    "StartImagePipelineExecutionResponseTypeDef",
    {
        "requestId": str,
        "clientToken": str,
        "imageBuildVersionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDistributionConfigurationResponseTypeDef = TypedDict(
    "UpdateDistributionConfigurationResponseTypeDef",
    {
        "requestId": str,
        "clientToken": str,
        "distributionConfigurationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateImagePipelineResponseTypeDef = TypedDict(
    "UpdateImagePipelineResponseTypeDef",
    {
        "requestId": str,
        "clientToken": str,
        "imagePipelineArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateInfrastructureConfigurationResponseTypeDef = TypedDict(
    "UpdateInfrastructureConfigurationResponseTypeDef",
    {
        "requestId": str,
        "clientToken": str,
        "infrastructureConfigurationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredComponentConfigurationTypeDef = TypedDict(
    "_RequiredComponentConfigurationTypeDef",
    {
        "componentArn": str,
    },
)
_OptionalComponentConfigurationTypeDef = TypedDict(
    "_OptionalComponentConfigurationTypeDef",
    {
        "parameters": Sequence[ComponentParameterTypeDef],
    },
    total=False,
)


class ComponentConfigurationTypeDef(
    _RequiredComponentConfigurationTypeDef, _OptionalComponentConfigurationTypeDef
):
    pass


ComponentSummaryTypeDef = TypedDict(
    "ComponentSummaryTypeDef",
    {
        "arn": str,
        "name": str,
        "version": str,
        "platform": PlatformType,
        "supportedOsVersions": List[str],
        "state": ComponentStateTypeDef,
        "type": ComponentTypeType,
        "owner": str,
        "description": str,
        "changeDescription": str,
        "dateCreated": str,
        "tags": Dict[str, str],
    },
    total=False,
)

ComponentTypeDef = TypedDict(
    "ComponentTypeDef",
    {
        "arn": str,
        "name": str,
        "version": str,
        "description": str,
        "changeDescription": str,
        "type": ComponentTypeType,
        "platform": PlatformType,
        "supportedOsVersions": List[str],
        "state": ComponentStateTypeDef,
        "parameters": List[ComponentParameterDetailTypeDef],
        "owner": str,
        "data": str,
        "kmsKeyId": str,
        "encrypted": bool,
        "dateCreated": str,
        "tags": Dict[str, str],
    },
    total=False,
)

ListComponentsResponseTypeDef = TypedDict(
    "ListComponentsResponseTypeDef",
    {
        "requestId": str,
        "componentVersionList": List[ComponentVersionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredContainerDistributionConfigurationTypeDef = TypedDict(
    "_RequiredContainerDistributionConfigurationTypeDef",
    {
        "targetRepository": TargetContainerRepositoryTypeDef,
    },
)
_OptionalContainerDistributionConfigurationTypeDef = TypedDict(
    "_OptionalContainerDistributionConfigurationTypeDef",
    {
        "description": str,
        "containerTags": Sequence[str],
    },
    total=False,
)


class ContainerDistributionConfigurationTypeDef(
    _RequiredContainerDistributionConfigurationTypeDef,
    _OptionalContainerDistributionConfigurationTypeDef,
):
    pass


ListContainerRecipesResponseTypeDef = TypedDict(
    "ListContainerRecipesResponseTypeDef",
    {
        "requestId": str,
        "containerRecipeSummaryList": List[ContainerRecipeSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateImageRequestRequestTypeDef = TypedDict(
    "_RequiredCreateImageRequestRequestTypeDef",
    {
        "infrastructureConfigurationArn": str,
        "clientToken": str,
    },
)
_OptionalCreateImageRequestRequestTypeDef = TypedDict(
    "_OptionalCreateImageRequestRequestTypeDef",
    {
        "imageRecipeArn": str,
        "containerRecipeArn": str,
        "distributionConfigurationArn": str,
        "imageTestsConfiguration": ImageTestsConfigurationTypeDef,
        "enhancedImageMetadataEnabled": bool,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateImageRequestRequestTypeDef(
    _RequiredCreateImageRequestRequestTypeDef, _OptionalCreateImageRequestRequestTypeDef
):
    pass


_RequiredCreateImagePipelineRequestRequestTypeDef = TypedDict(
    "_RequiredCreateImagePipelineRequestRequestTypeDef",
    {
        "name": str,
        "infrastructureConfigurationArn": str,
        "clientToken": str,
    },
)
_OptionalCreateImagePipelineRequestRequestTypeDef = TypedDict(
    "_OptionalCreateImagePipelineRequestRequestTypeDef",
    {
        "description": str,
        "imageRecipeArn": str,
        "containerRecipeArn": str,
        "distributionConfigurationArn": str,
        "imageTestsConfiguration": ImageTestsConfigurationTypeDef,
        "enhancedImageMetadataEnabled": bool,
        "schedule": ScheduleTypeDef,
        "status": PipelineStatusType,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateImagePipelineRequestRequestTypeDef(
    _RequiredCreateImagePipelineRequestRequestTypeDef,
    _OptionalCreateImagePipelineRequestRequestTypeDef,
):
    pass


ImagePipelineTypeDef = TypedDict(
    "ImagePipelineTypeDef",
    {
        "arn": str,
        "name": str,
        "description": str,
        "platform": PlatformType,
        "enhancedImageMetadataEnabled": bool,
        "imageRecipeArn": str,
        "containerRecipeArn": str,
        "infrastructureConfigurationArn": str,
        "distributionConfigurationArn": str,
        "imageTestsConfiguration": ImageTestsConfigurationTypeDef,
        "schedule": ScheduleTypeDef,
        "status": PipelineStatusType,
        "dateCreated": str,
        "dateUpdated": str,
        "dateLastRun": str,
        "dateNextRun": str,
        "tags": Dict[str, str],
    },
    total=False,
)

_RequiredUpdateImagePipelineRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateImagePipelineRequestRequestTypeDef",
    {
        "imagePipelineArn": str,
        "infrastructureConfigurationArn": str,
        "clientToken": str,
    },
)
_OptionalUpdateImagePipelineRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateImagePipelineRequestRequestTypeDef",
    {
        "description": str,
        "imageRecipeArn": str,
        "containerRecipeArn": str,
        "distributionConfigurationArn": str,
        "imageTestsConfiguration": ImageTestsConfigurationTypeDef,
        "enhancedImageMetadataEnabled": bool,
        "schedule": ScheduleTypeDef,
        "status": PipelineStatusType,
    },
    total=False,
)


class UpdateImagePipelineRequestRequestTypeDef(
    _RequiredUpdateImagePipelineRequestRequestTypeDef,
    _OptionalUpdateImagePipelineRequestRequestTypeDef,
):
    pass


ListDistributionConfigurationsResponseTypeDef = TypedDict(
    "ListDistributionConfigurationsResponseTypeDef",
    {
        "requestId": str,
        "distributionConfigurationSummaryList": List[DistributionConfigurationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstanceBlockDeviceMappingTypeDef = TypedDict(
    "InstanceBlockDeviceMappingTypeDef",
    {
        "deviceName": str,
        "ebs": EbsInstanceBlockDeviceSpecificationTypeDef,
        "virtualName": str,
        "noDevice": str,
    },
    total=False,
)

_RequiredFastLaunchConfigurationTypeDef = TypedDict(
    "_RequiredFastLaunchConfigurationTypeDef",
    {
        "enabled": bool,
    },
)
_OptionalFastLaunchConfigurationTypeDef = TypedDict(
    "_OptionalFastLaunchConfigurationTypeDef",
    {
        "snapshotConfiguration": FastLaunchSnapshotConfigurationTypeDef,
        "maxParallelLaunches": int,
        "launchTemplate": FastLaunchLaunchTemplateSpecificationTypeDef,
        "accountId": str,
    },
    total=False,
)


class FastLaunchConfigurationTypeDef(
    _RequiredFastLaunchConfigurationTypeDef, _OptionalFastLaunchConfigurationTypeDef
):
    pass


ListComponentsRequestRequestTypeDef = TypedDict(
    "ListComponentsRequestRequestTypeDef",
    {
        "owner": OwnershipType,
        "filters": Sequence[FilterTypeDef],
        "byName": bool,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListContainerRecipesRequestRequestTypeDef = TypedDict(
    "ListContainerRecipesRequestRequestTypeDef",
    {
        "owner": OwnershipType,
        "filters": Sequence[FilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListDistributionConfigurationsRequestRequestTypeDef = TypedDict(
    "ListDistributionConfigurationsRequestRequestTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListImageBuildVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListImageBuildVersionsRequestRequestTypeDef",
    {
        "imageVersionArn": str,
    },
)
_OptionalListImageBuildVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListImageBuildVersionsRequestRequestTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListImageBuildVersionsRequestRequestTypeDef(
    _RequiredListImageBuildVersionsRequestRequestTypeDef,
    _OptionalListImageBuildVersionsRequestRequestTypeDef,
):
    pass


_RequiredListImagePipelineImagesRequestRequestTypeDef = TypedDict(
    "_RequiredListImagePipelineImagesRequestRequestTypeDef",
    {
        "imagePipelineArn": str,
    },
)
_OptionalListImagePipelineImagesRequestRequestTypeDef = TypedDict(
    "_OptionalListImagePipelineImagesRequestRequestTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListImagePipelineImagesRequestRequestTypeDef(
    _RequiredListImagePipelineImagesRequestRequestTypeDef,
    _OptionalListImagePipelineImagesRequestRequestTypeDef,
):
    pass


ListImagePipelinesRequestRequestTypeDef = TypedDict(
    "ListImagePipelinesRequestRequestTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListImageRecipesRequestRequestTypeDef = TypedDict(
    "ListImageRecipesRequestRequestTypeDef",
    {
        "owner": OwnershipType,
        "filters": Sequence[FilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListImagesRequestRequestTypeDef = TypedDict(
    "ListImagesRequestRequestTypeDef",
    {
        "owner": OwnershipType,
        "filters": Sequence[FilterTypeDef],
        "byName": bool,
        "maxResults": int,
        "nextToken": str,
        "includeDeprecated": bool,
    },
    total=False,
)

ListInfrastructureConfigurationsRequestRequestTypeDef = TypedDict(
    "ListInfrastructureConfigurationsRequestRequestTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListImagePackagesResponseTypeDef = TypedDict(
    "ListImagePackagesResponseTypeDef",
    {
        "requestId": str,
        "imagePackageList": List[ImagePackageTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListImageRecipesResponseTypeDef = TypedDict(
    "ListImageRecipesResponseTypeDef",
    {
        "requestId": str,
        "imageRecipeSummaryList": List[ImageRecipeSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListImagesResponseTypeDef = TypedDict(
    "ListImagesResponseTypeDef",
    {
        "requestId": str,
        "imageVersionList": List[ImageVersionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInfrastructureConfigurationsResponseTypeDef = TypedDict(
    "ListInfrastructureConfigurationsResponseTypeDef",
    {
        "requestId": str,
        "infrastructureConfigurationSummaryList": List[InfrastructureConfigurationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LoggingTypeDef = TypedDict(
    "LoggingTypeDef",
    {
        "s3Logs": S3LogsTypeDef,
    },
    total=False,
)

OutputResourcesTypeDef = TypedDict(
    "OutputResourcesTypeDef",
    {
        "amis": List[AmiTypeDef],
        "containers": List[ContainerTypeDef],
    },
    total=False,
)

ListComponentBuildVersionsResponseTypeDef = TypedDict(
    "ListComponentBuildVersionsResponseTypeDef",
    {
        "requestId": str,
        "componentSummaryList": List[ComponentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetComponentResponseTypeDef = TypedDict(
    "GetComponentResponseTypeDef",
    {
        "requestId": str,
        "component": ComponentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetImagePipelineResponseTypeDef = TypedDict(
    "GetImagePipelineResponseTypeDef",
    {
        "requestId": str,
        "imagePipeline": ImagePipelineTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListImagePipelinesResponseTypeDef = TypedDict(
    "ListImagePipelinesResponseTypeDef",
    {
        "requestId": str,
        "imagePipelineList": List[ImagePipelineTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateImageRecipeRequestRequestTypeDef = TypedDict(
    "_RequiredCreateImageRecipeRequestRequestTypeDef",
    {
        "name": str,
        "semanticVersion": str,
        "components": Sequence[ComponentConfigurationTypeDef],
        "parentImage": str,
        "clientToken": str,
    },
)
_OptionalCreateImageRecipeRequestRequestTypeDef = TypedDict(
    "_OptionalCreateImageRecipeRequestRequestTypeDef",
    {
        "description": str,
        "blockDeviceMappings": Sequence[InstanceBlockDeviceMappingTypeDef],
        "tags": Mapping[str, str],
        "workingDirectory": str,
        "additionalInstanceConfiguration": AdditionalInstanceConfigurationTypeDef,
    },
    total=False,
)


class CreateImageRecipeRequestRequestTypeDef(
    _RequiredCreateImageRecipeRequestRequestTypeDef, _OptionalCreateImageRecipeRequestRequestTypeDef
):
    pass


ImageRecipeTypeDef = TypedDict(
    "ImageRecipeTypeDef",
    {
        "arn": str,
        "type": ImageTypeType,
        "name": str,
        "description": str,
        "platform": PlatformType,
        "owner": str,
        "version": str,
        "components": List[ComponentConfigurationTypeDef],
        "parentImage": str,
        "blockDeviceMappings": List[InstanceBlockDeviceMappingTypeDef],
        "dateCreated": str,
        "tags": Dict[str, str],
        "workingDirectory": str,
        "additionalInstanceConfiguration": AdditionalInstanceConfigurationTypeDef,
    },
    total=False,
)

InstanceConfigurationTypeDef = TypedDict(
    "InstanceConfigurationTypeDef",
    {
        "image": str,
        "blockDeviceMappings": Sequence[InstanceBlockDeviceMappingTypeDef],
    },
    total=False,
)

_RequiredDistributionTypeDef = TypedDict(
    "_RequiredDistributionTypeDef",
    {
        "region": str,
    },
)
_OptionalDistributionTypeDef = TypedDict(
    "_OptionalDistributionTypeDef",
    {
        "amiDistributionConfiguration": AmiDistributionConfigurationTypeDef,
        "containerDistributionConfiguration": ContainerDistributionConfigurationTypeDef,
        "licenseConfigurationArns": Sequence[str],
        "launchTemplateConfigurations": Sequence[LaunchTemplateConfigurationTypeDef],
        "s3ExportConfiguration": S3ExportConfigurationTypeDef,
        "fastLaunchConfigurations": Sequence[FastLaunchConfigurationTypeDef],
    },
    total=False,
)


class DistributionTypeDef(_RequiredDistributionTypeDef, _OptionalDistributionTypeDef):
    pass


_RequiredCreateInfrastructureConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateInfrastructureConfigurationRequestRequestTypeDef",
    {
        "name": str,
        "instanceProfileName": str,
        "clientToken": str,
    },
)
_OptionalCreateInfrastructureConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateInfrastructureConfigurationRequestRequestTypeDef",
    {
        "description": str,
        "instanceTypes": Sequence[str],
        "securityGroupIds": Sequence[str],
        "subnetId": str,
        "logging": LoggingTypeDef,
        "keyPair": str,
        "terminateInstanceOnFailure": bool,
        "snsTopicArn": str,
        "resourceTags": Mapping[str, str],
        "instanceMetadataOptions": InstanceMetadataOptionsTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateInfrastructureConfigurationRequestRequestTypeDef(
    _RequiredCreateInfrastructureConfigurationRequestRequestTypeDef,
    _OptionalCreateInfrastructureConfigurationRequestRequestTypeDef,
):
    pass


InfrastructureConfigurationTypeDef = TypedDict(
    "InfrastructureConfigurationTypeDef",
    {
        "arn": str,
        "name": str,
        "description": str,
        "instanceTypes": List[str],
        "instanceProfileName": str,
        "securityGroupIds": List[str],
        "subnetId": str,
        "logging": LoggingTypeDef,
        "keyPair": str,
        "terminateInstanceOnFailure": bool,
        "snsTopicArn": str,
        "dateCreated": str,
        "dateUpdated": str,
        "resourceTags": Dict[str, str],
        "instanceMetadataOptions": InstanceMetadataOptionsTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)

_RequiredUpdateInfrastructureConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateInfrastructureConfigurationRequestRequestTypeDef",
    {
        "infrastructureConfigurationArn": str,
        "instanceProfileName": str,
        "clientToken": str,
    },
)
_OptionalUpdateInfrastructureConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateInfrastructureConfigurationRequestRequestTypeDef",
    {
        "description": str,
        "instanceTypes": Sequence[str],
        "securityGroupIds": Sequence[str],
        "subnetId": str,
        "logging": LoggingTypeDef,
        "keyPair": str,
        "terminateInstanceOnFailure": bool,
        "snsTopicArn": str,
        "resourceTags": Mapping[str, str],
        "instanceMetadataOptions": InstanceMetadataOptionsTypeDef,
    },
    total=False,
)


class UpdateInfrastructureConfigurationRequestRequestTypeDef(
    _RequiredUpdateInfrastructureConfigurationRequestRequestTypeDef,
    _OptionalUpdateInfrastructureConfigurationRequestRequestTypeDef,
):
    pass


ImageSummaryTypeDef = TypedDict(
    "ImageSummaryTypeDef",
    {
        "arn": str,
        "name": str,
        "type": ImageTypeType,
        "version": str,
        "platform": PlatformType,
        "osVersion": str,
        "state": ImageStateTypeDef,
        "owner": str,
        "dateCreated": str,
        "outputResources": OutputResourcesTypeDef,
        "tags": Dict[str, str],
        "buildType": BuildTypeType,
    },
    total=False,
)

GetImageRecipeResponseTypeDef = TypedDict(
    "GetImageRecipeResponseTypeDef",
    {
        "requestId": str,
        "imageRecipe": ImageRecipeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ContainerRecipeTypeDef = TypedDict(
    "ContainerRecipeTypeDef",
    {
        "arn": str,
        "containerType": Literal["DOCKER"],
        "name": str,
        "description": str,
        "platform": PlatformType,
        "owner": str,
        "version": str,
        "components": List[ComponentConfigurationTypeDef],
        "instanceConfiguration": InstanceConfigurationTypeDef,
        "dockerfileTemplateData": str,
        "kmsKeyId": str,
        "encrypted": bool,
        "parentImage": str,
        "dateCreated": str,
        "tags": Dict[str, str],
        "workingDirectory": str,
        "targetRepository": TargetContainerRepositoryTypeDef,
    },
    total=False,
)

_RequiredCreateContainerRecipeRequestRequestTypeDef = TypedDict(
    "_RequiredCreateContainerRecipeRequestRequestTypeDef",
    {
        "containerType": Literal["DOCKER"],
        "name": str,
        "semanticVersion": str,
        "components": Sequence[ComponentConfigurationTypeDef],
        "parentImage": str,
        "targetRepository": TargetContainerRepositoryTypeDef,
        "clientToken": str,
    },
)
_OptionalCreateContainerRecipeRequestRequestTypeDef = TypedDict(
    "_OptionalCreateContainerRecipeRequestRequestTypeDef",
    {
        "description": str,
        "instanceConfiguration": InstanceConfigurationTypeDef,
        "dockerfileTemplateData": str,
        "dockerfileTemplateUri": str,
        "platformOverride": PlatformType,
        "imageOsVersionOverride": str,
        "tags": Mapping[str, str],
        "workingDirectory": str,
        "kmsKeyId": str,
    },
    total=False,
)


class CreateContainerRecipeRequestRequestTypeDef(
    _RequiredCreateContainerRecipeRequestRequestTypeDef,
    _OptionalCreateContainerRecipeRequestRequestTypeDef,
):
    pass


_RequiredCreateDistributionConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDistributionConfigurationRequestRequestTypeDef",
    {
        "name": str,
        "distributions": Sequence[DistributionTypeDef],
        "clientToken": str,
    },
)
_OptionalCreateDistributionConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDistributionConfigurationRequestRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateDistributionConfigurationRequestRequestTypeDef(
    _RequiredCreateDistributionConfigurationRequestRequestTypeDef,
    _OptionalCreateDistributionConfigurationRequestRequestTypeDef,
):
    pass


_RequiredDistributionConfigurationTypeDef = TypedDict(
    "_RequiredDistributionConfigurationTypeDef",
    {
        "timeoutMinutes": int,
    },
)
_OptionalDistributionConfigurationTypeDef = TypedDict(
    "_OptionalDistributionConfigurationTypeDef",
    {
        "arn": str,
        "name": str,
        "description": str,
        "distributions": List[DistributionTypeDef],
        "dateCreated": str,
        "dateUpdated": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class DistributionConfigurationTypeDef(
    _RequiredDistributionConfigurationTypeDef, _OptionalDistributionConfigurationTypeDef
):
    pass


_RequiredUpdateDistributionConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDistributionConfigurationRequestRequestTypeDef",
    {
        "distributionConfigurationArn": str,
        "distributions": Sequence[DistributionTypeDef],
        "clientToken": str,
    },
)
_OptionalUpdateDistributionConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDistributionConfigurationRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)


class UpdateDistributionConfigurationRequestRequestTypeDef(
    _RequiredUpdateDistributionConfigurationRequestRequestTypeDef,
    _OptionalUpdateDistributionConfigurationRequestRequestTypeDef,
):
    pass


GetInfrastructureConfigurationResponseTypeDef = TypedDict(
    "GetInfrastructureConfigurationResponseTypeDef",
    {
        "requestId": str,
        "infrastructureConfiguration": InfrastructureConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListImageBuildVersionsResponseTypeDef = TypedDict(
    "ListImageBuildVersionsResponseTypeDef",
    {
        "requestId": str,
        "imageSummaryList": List[ImageSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListImagePipelineImagesResponseTypeDef = TypedDict(
    "ListImagePipelineImagesResponseTypeDef",
    {
        "requestId": str,
        "imageSummaryList": List[ImageSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContainerRecipeResponseTypeDef = TypedDict(
    "GetContainerRecipeResponseTypeDef",
    {
        "requestId": str,
        "containerRecipe": ContainerRecipeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDistributionConfigurationResponseTypeDef = TypedDict(
    "GetDistributionConfigurationResponseTypeDef",
    {
        "requestId": str,
        "distributionConfiguration": DistributionConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "arn": str,
        "type": ImageTypeType,
        "name": str,
        "version": str,
        "platform": PlatformType,
        "enhancedImageMetadataEnabled": bool,
        "osVersion": str,
        "state": ImageStateTypeDef,
        "imageRecipe": ImageRecipeTypeDef,
        "containerRecipe": ContainerRecipeTypeDef,
        "sourcePipelineName": str,
        "sourcePipelineArn": str,
        "infrastructureConfiguration": InfrastructureConfigurationTypeDef,
        "distributionConfiguration": DistributionConfigurationTypeDef,
        "imageTestsConfiguration": ImageTestsConfigurationTypeDef,
        "dateCreated": str,
        "outputResources": OutputResourcesTypeDef,
        "tags": Dict[str, str],
        "buildType": BuildTypeType,
    },
    total=False,
)

GetImageResponseTypeDef = TypedDict(
    "GetImageResponseTypeDef",
    {
        "requestId": str,
        "image": ImageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
