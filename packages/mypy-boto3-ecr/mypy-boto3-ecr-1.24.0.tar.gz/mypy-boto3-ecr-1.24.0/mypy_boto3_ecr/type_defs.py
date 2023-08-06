"""
Type annotations for ecr service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecr/type_defs/)

Usage::

    ```python
    from mypy_boto3_ecr.type_defs import AttributeTypeDef

    data: AttributeTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    EncryptionTypeType,
    FindingSeverityType,
    ImageFailureCodeType,
    ImageTagMutabilityType,
    LayerAvailabilityType,
    LayerFailureCodeType,
    LifecyclePolicyPreviewStatusType,
    ReplicationStatusType,
    ScanFrequencyType,
    ScanStatusType,
    ScanTypeType,
    TagStatusType,
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
    "AttributeTypeDef",
    "AuthorizationDataTypeDef",
    "AwsEcrContainerImageDetailsTypeDef",
    "BatchCheckLayerAvailabilityRequestRequestTypeDef",
    "LayerFailureTypeDef",
    "LayerTypeDef",
    "ResponseMetadataTypeDef",
    "ImageIdentifierTypeDef",
    "BatchGetRepositoryScanningConfigurationRequestRequestTypeDef",
    "RepositoryScanningConfigurationFailureTypeDef",
    "CompleteLayerUploadRequestRequestTypeDef",
    "CreatePullThroughCacheRuleRequestRequestTypeDef",
    "EncryptionConfigurationTypeDef",
    "ImageScanningConfigurationTypeDef",
    "TagTypeDef",
    "CvssScoreAdjustmentTypeDef",
    "CvssScoreTypeDef",
    "DeleteLifecyclePolicyRequestRequestTypeDef",
    "DeletePullThroughCacheRuleRequestRequestTypeDef",
    "DeleteRepositoryPolicyRequestRequestTypeDef",
    "DeleteRepositoryRequestRequestTypeDef",
    "ImageReplicationStatusTypeDef",
    "PaginatorConfigTypeDef",
    "WaiterConfigTypeDef",
    "ImageScanStatusTypeDef",
    "DescribeImagesFilterTypeDef",
    "DescribePullThroughCacheRulesRequestRequestTypeDef",
    "PullThroughCacheRuleTypeDef",
    "DescribeRepositoriesRequestRequestTypeDef",
    "GetAuthorizationTokenRequestRequestTypeDef",
    "GetDownloadUrlForLayerRequestRequestTypeDef",
    "LifecyclePolicyPreviewFilterTypeDef",
    "LifecyclePolicyPreviewSummaryTypeDef",
    "GetLifecyclePolicyRequestRequestTypeDef",
    "GetRepositoryPolicyRequestRequestTypeDef",
    "ImageScanFindingsSummaryTypeDef",
    "InitiateLayerUploadRequestRequestTypeDef",
    "LifecyclePolicyRuleActionTypeDef",
    "ListImagesFilterTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "VulnerablePackageTypeDef",
    "PutImageRequestRequestTypeDef",
    "PutImageTagMutabilityRequestRequestTypeDef",
    "PutLifecyclePolicyRequestRequestTypeDef",
    "PutRegistryPolicyRequestRequestTypeDef",
    "RecommendationTypeDef",
    "ScanningRepositoryFilterTypeDef",
    "ReplicationDestinationTypeDef",
    "RepositoryFilterTypeDef",
    "SetRepositoryPolicyRequestRequestTypeDef",
    "StartLifecyclePolicyPreviewRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UploadLayerPartRequestRequestTypeDef",
    "ImageScanFindingTypeDef",
    "ResourceDetailsTypeDef",
    "BatchCheckLayerAvailabilityResponseTypeDef",
    "CompleteLayerUploadResponseTypeDef",
    "CreatePullThroughCacheRuleResponseTypeDef",
    "DeleteLifecyclePolicyResponseTypeDef",
    "DeletePullThroughCacheRuleResponseTypeDef",
    "DeleteRegistryPolicyResponseTypeDef",
    "DeleteRepositoryPolicyResponseTypeDef",
    "GetAuthorizationTokenResponseTypeDef",
    "GetDownloadUrlForLayerResponseTypeDef",
    "GetLifecyclePolicyResponseTypeDef",
    "GetRegistryPolicyResponseTypeDef",
    "GetRepositoryPolicyResponseTypeDef",
    "InitiateLayerUploadResponseTypeDef",
    "PutImageTagMutabilityResponseTypeDef",
    "PutLifecyclePolicyResponseTypeDef",
    "PutRegistryPolicyResponseTypeDef",
    "SetRepositoryPolicyResponseTypeDef",
    "StartLifecyclePolicyPreviewResponseTypeDef",
    "UploadLayerPartResponseTypeDef",
    "BatchDeleteImageRequestRequestTypeDef",
    "BatchGetImageRequestRequestTypeDef",
    "DescribeImageReplicationStatusRequestRequestTypeDef",
    "DescribeImageScanFindingsRequestRequestTypeDef",
    "ImageFailureTypeDef",
    "ImageTypeDef",
    "ListImagesResponseTypeDef",
    "StartImageScanRequestRequestTypeDef",
    "PutImageScanningConfigurationRequestRequestTypeDef",
    "PutImageScanningConfigurationResponseTypeDef",
    "RepositoryTypeDef",
    "CreateRepositoryRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CvssScoreDetailsTypeDef",
    "DescribeImageReplicationStatusResponseTypeDef",
    "DescribeImageScanFindingsRequestDescribeImageScanFindingsPaginateTypeDef",
    "DescribePullThroughCacheRulesRequestDescribePullThroughCacheRulesPaginateTypeDef",
    "DescribeRepositoriesRequestDescribeRepositoriesPaginateTypeDef",
    "DescribeImageScanFindingsRequestImageScanCompleteWaitTypeDef",
    "StartImageScanResponseTypeDef",
    "DescribeImagesRequestDescribeImagesPaginateTypeDef",
    "DescribeImagesRequestRequestTypeDef",
    "DescribePullThroughCacheRulesResponseTypeDef",
    "GetLifecyclePolicyPreviewRequestGetLifecyclePolicyPreviewPaginateTypeDef",
    "GetLifecyclePolicyPreviewRequestLifecyclePolicyPreviewCompleteWaitTypeDef",
    "GetLifecyclePolicyPreviewRequestRequestTypeDef",
    "ImageDetailTypeDef",
    "LifecyclePolicyPreviewResultTypeDef",
    "ListImagesRequestListImagesPaginateTypeDef",
    "ListImagesRequestRequestTypeDef",
    "PackageVulnerabilityDetailsTypeDef",
    "RemediationTypeDef",
    "RegistryScanningRuleTypeDef",
    "RepositoryScanningConfigurationTypeDef",
    "ReplicationRuleTypeDef",
    "ResourceTypeDef",
    "BatchDeleteImageResponseTypeDef",
    "BatchGetImageResponseTypeDef",
    "PutImageResponseTypeDef",
    "CreateRepositoryResponseTypeDef",
    "DeleteRepositoryResponseTypeDef",
    "DescribeRepositoriesResponseTypeDef",
    "ScoreDetailsTypeDef",
    "DescribeImagesResponseTypeDef",
    "GetLifecyclePolicyPreviewResponseTypeDef",
    "PutRegistryScanningConfigurationRequestRequestTypeDef",
    "RegistryScanningConfigurationTypeDef",
    "BatchGetRepositoryScanningConfigurationResponseTypeDef",
    "ReplicationConfigurationTypeDef",
    "EnhancedImageScanFindingTypeDef",
    "GetRegistryScanningConfigurationResponseTypeDef",
    "PutRegistryScanningConfigurationResponseTypeDef",
    "DescribeRegistryResponseTypeDef",
    "PutReplicationConfigurationRequestRequestTypeDef",
    "PutReplicationConfigurationResponseTypeDef",
    "ImageScanFindingsTypeDef",
    "DescribeImageScanFindingsResponseTypeDef",
)

_RequiredAttributeTypeDef = TypedDict(
    "_RequiredAttributeTypeDef",
    {
        "key": str,
    },
)
_OptionalAttributeTypeDef = TypedDict(
    "_OptionalAttributeTypeDef",
    {
        "value": str,
    },
    total=False,
)


class AttributeTypeDef(_RequiredAttributeTypeDef, _OptionalAttributeTypeDef):
    pass


AuthorizationDataTypeDef = TypedDict(
    "AuthorizationDataTypeDef",
    {
        "authorizationToken": str,
        "expiresAt": datetime,
        "proxyEndpoint": str,
    },
    total=False,
)

AwsEcrContainerImageDetailsTypeDef = TypedDict(
    "AwsEcrContainerImageDetailsTypeDef",
    {
        "architecture": str,
        "author": str,
        "imageHash": str,
        "imageTags": List[str],
        "platform": str,
        "pushedAt": datetime,
        "registry": str,
        "repositoryName": str,
    },
    total=False,
)

_RequiredBatchCheckLayerAvailabilityRequestRequestTypeDef = TypedDict(
    "_RequiredBatchCheckLayerAvailabilityRequestRequestTypeDef",
    {
        "repositoryName": str,
        "layerDigests": Sequence[str],
    },
)
_OptionalBatchCheckLayerAvailabilityRequestRequestTypeDef = TypedDict(
    "_OptionalBatchCheckLayerAvailabilityRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class BatchCheckLayerAvailabilityRequestRequestTypeDef(
    _RequiredBatchCheckLayerAvailabilityRequestRequestTypeDef,
    _OptionalBatchCheckLayerAvailabilityRequestRequestTypeDef,
):
    pass


LayerFailureTypeDef = TypedDict(
    "LayerFailureTypeDef",
    {
        "layerDigest": str,
        "failureCode": LayerFailureCodeType,
        "failureReason": str,
    },
    total=False,
)

LayerTypeDef = TypedDict(
    "LayerTypeDef",
    {
        "layerDigest": str,
        "layerAvailability": LayerAvailabilityType,
        "layerSize": int,
        "mediaType": str,
    },
    total=False,
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

ImageIdentifierTypeDef = TypedDict(
    "ImageIdentifierTypeDef",
    {
        "imageDigest": str,
        "imageTag": str,
    },
    total=False,
)

BatchGetRepositoryScanningConfigurationRequestRequestTypeDef = TypedDict(
    "BatchGetRepositoryScanningConfigurationRequestRequestTypeDef",
    {
        "repositoryNames": Sequence[str],
    },
)

RepositoryScanningConfigurationFailureTypeDef = TypedDict(
    "RepositoryScanningConfigurationFailureTypeDef",
    {
        "repositoryName": str,
        "failureCode": Literal["REPOSITORY_NOT_FOUND"],
        "failureReason": str,
    },
    total=False,
)

_RequiredCompleteLayerUploadRequestRequestTypeDef = TypedDict(
    "_RequiredCompleteLayerUploadRequestRequestTypeDef",
    {
        "repositoryName": str,
        "uploadId": str,
        "layerDigests": Sequence[str],
    },
)
_OptionalCompleteLayerUploadRequestRequestTypeDef = TypedDict(
    "_OptionalCompleteLayerUploadRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class CompleteLayerUploadRequestRequestTypeDef(
    _RequiredCompleteLayerUploadRequestRequestTypeDef,
    _OptionalCompleteLayerUploadRequestRequestTypeDef,
):
    pass


_RequiredCreatePullThroughCacheRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePullThroughCacheRuleRequestRequestTypeDef",
    {
        "ecrRepositoryPrefix": str,
        "upstreamRegistryUrl": str,
    },
)
_OptionalCreatePullThroughCacheRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePullThroughCacheRuleRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class CreatePullThroughCacheRuleRequestRequestTypeDef(
    _RequiredCreatePullThroughCacheRuleRequestRequestTypeDef,
    _OptionalCreatePullThroughCacheRuleRequestRequestTypeDef,
):
    pass


_RequiredEncryptionConfigurationTypeDef = TypedDict(
    "_RequiredEncryptionConfigurationTypeDef",
    {
        "encryptionType": EncryptionTypeType,
    },
)
_OptionalEncryptionConfigurationTypeDef = TypedDict(
    "_OptionalEncryptionConfigurationTypeDef",
    {
        "kmsKey": str,
    },
    total=False,
)


class EncryptionConfigurationTypeDef(
    _RequiredEncryptionConfigurationTypeDef, _OptionalEncryptionConfigurationTypeDef
):
    pass


ImageScanningConfigurationTypeDef = TypedDict(
    "ImageScanningConfigurationTypeDef",
    {
        "scanOnPush": bool,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

CvssScoreAdjustmentTypeDef = TypedDict(
    "CvssScoreAdjustmentTypeDef",
    {
        "metric": str,
        "reason": str,
    },
    total=False,
)

CvssScoreTypeDef = TypedDict(
    "CvssScoreTypeDef",
    {
        "baseScore": float,
        "scoringVector": str,
        "source": str,
        "version": str,
    },
    total=False,
)

_RequiredDeleteLifecyclePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteLifecyclePolicyRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalDeleteLifecyclePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteLifecyclePolicyRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class DeleteLifecyclePolicyRequestRequestTypeDef(
    _RequiredDeleteLifecyclePolicyRequestRequestTypeDef,
    _OptionalDeleteLifecyclePolicyRequestRequestTypeDef,
):
    pass


_RequiredDeletePullThroughCacheRuleRequestRequestTypeDef = TypedDict(
    "_RequiredDeletePullThroughCacheRuleRequestRequestTypeDef",
    {
        "ecrRepositoryPrefix": str,
    },
)
_OptionalDeletePullThroughCacheRuleRequestRequestTypeDef = TypedDict(
    "_OptionalDeletePullThroughCacheRuleRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class DeletePullThroughCacheRuleRequestRequestTypeDef(
    _RequiredDeletePullThroughCacheRuleRequestRequestTypeDef,
    _OptionalDeletePullThroughCacheRuleRequestRequestTypeDef,
):
    pass


_RequiredDeleteRepositoryPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteRepositoryPolicyRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalDeleteRepositoryPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteRepositoryPolicyRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class DeleteRepositoryPolicyRequestRequestTypeDef(
    _RequiredDeleteRepositoryPolicyRequestRequestTypeDef,
    _OptionalDeleteRepositoryPolicyRequestRequestTypeDef,
):
    pass


_RequiredDeleteRepositoryRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteRepositoryRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalDeleteRepositoryRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteRepositoryRequestRequestTypeDef",
    {
        "registryId": str,
        "force": bool,
    },
    total=False,
)


class DeleteRepositoryRequestRequestTypeDef(
    _RequiredDeleteRepositoryRequestRequestTypeDef, _OptionalDeleteRepositoryRequestRequestTypeDef
):
    pass


ImageReplicationStatusTypeDef = TypedDict(
    "ImageReplicationStatusTypeDef",
    {
        "region": str,
        "registryId": str,
        "status": ReplicationStatusType,
        "failureCode": str,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

ImageScanStatusTypeDef = TypedDict(
    "ImageScanStatusTypeDef",
    {
        "status": ScanStatusType,
        "description": str,
    },
    total=False,
)

DescribeImagesFilterTypeDef = TypedDict(
    "DescribeImagesFilterTypeDef",
    {
        "tagStatus": TagStatusType,
    },
    total=False,
)

DescribePullThroughCacheRulesRequestRequestTypeDef = TypedDict(
    "DescribePullThroughCacheRulesRequestRequestTypeDef",
    {
        "registryId": str,
        "ecrRepositoryPrefixes": Sequence[str],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

PullThroughCacheRuleTypeDef = TypedDict(
    "PullThroughCacheRuleTypeDef",
    {
        "ecrRepositoryPrefix": str,
        "upstreamRegistryUrl": str,
        "createdAt": datetime,
        "registryId": str,
    },
    total=False,
)

DescribeRepositoriesRequestRequestTypeDef = TypedDict(
    "DescribeRepositoriesRequestRequestTypeDef",
    {
        "registryId": str,
        "repositoryNames": Sequence[str],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

GetAuthorizationTokenRequestRequestTypeDef = TypedDict(
    "GetAuthorizationTokenRequestRequestTypeDef",
    {
        "registryIds": Sequence[str],
    },
    total=False,
)

_RequiredGetDownloadUrlForLayerRequestRequestTypeDef = TypedDict(
    "_RequiredGetDownloadUrlForLayerRequestRequestTypeDef",
    {
        "repositoryName": str,
        "layerDigest": str,
    },
)
_OptionalGetDownloadUrlForLayerRequestRequestTypeDef = TypedDict(
    "_OptionalGetDownloadUrlForLayerRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class GetDownloadUrlForLayerRequestRequestTypeDef(
    _RequiredGetDownloadUrlForLayerRequestRequestTypeDef,
    _OptionalGetDownloadUrlForLayerRequestRequestTypeDef,
):
    pass


LifecyclePolicyPreviewFilterTypeDef = TypedDict(
    "LifecyclePolicyPreviewFilterTypeDef",
    {
        "tagStatus": TagStatusType,
    },
    total=False,
)

LifecyclePolicyPreviewSummaryTypeDef = TypedDict(
    "LifecyclePolicyPreviewSummaryTypeDef",
    {
        "expiringImageTotalCount": int,
    },
    total=False,
)

_RequiredGetLifecyclePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredGetLifecyclePolicyRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalGetLifecyclePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalGetLifecyclePolicyRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class GetLifecyclePolicyRequestRequestTypeDef(
    _RequiredGetLifecyclePolicyRequestRequestTypeDef,
    _OptionalGetLifecyclePolicyRequestRequestTypeDef,
):
    pass


_RequiredGetRepositoryPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredGetRepositoryPolicyRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalGetRepositoryPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalGetRepositoryPolicyRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class GetRepositoryPolicyRequestRequestTypeDef(
    _RequiredGetRepositoryPolicyRequestRequestTypeDef,
    _OptionalGetRepositoryPolicyRequestRequestTypeDef,
):
    pass


ImageScanFindingsSummaryTypeDef = TypedDict(
    "ImageScanFindingsSummaryTypeDef",
    {
        "imageScanCompletedAt": datetime,
        "vulnerabilitySourceUpdatedAt": datetime,
        "findingSeverityCounts": Dict[FindingSeverityType, int],
    },
    total=False,
)

_RequiredInitiateLayerUploadRequestRequestTypeDef = TypedDict(
    "_RequiredInitiateLayerUploadRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalInitiateLayerUploadRequestRequestTypeDef = TypedDict(
    "_OptionalInitiateLayerUploadRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class InitiateLayerUploadRequestRequestTypeDef(
    _RequiredInitiateLayerUploadRequestRequestTypeDef,
    _OptionalInitiateLayerUploadRequestRequestTypeDef,
):
    pass


LifecyclePolicyRuleActionTypeDef = TypedDict(
    "LifecyclePolicyRuleActionTypeDef",
    {
        "type": Literal["EXPIRE"],
    },
    total=False,
)

ListImagesFilterTypeDef = TypedDict(
    "ListImagesFilterTypeDef",
    {
        "tagStatus": TagStatusType,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

VulnerablePackageTypeDef = TypedDict(
    "VulnerablePackageTypeDef",
    {
        "arch": str,
        "epoch": int,
        "filePath": str,
        "name": str,
        "packageManager": str,
        "release": str,
        "sourceLayerHash": str,
        "version": str,
    },
    total=False,
)

_RequiredPutImageRequestRequestTypeDef = TypedDict(
    "_RequiredPutImageRequestRequestTypeDef",
    {
        "repositoryName": str,
        "imageManifest": str,
    },
)
_OptionalPutImageRequestRequestTypeDef = TypedDict(
    "_OptionalPutImageRequestRequestTypeDef",
    {
        "registryId": str,
        "imageManifestMediaType": str,
        "imageTag": str,
        "imageDigest": str,
    },
    total=False,
)


class PutImageRequestRequestTypeDef(
    _RequiredPutImageRequestRequestTypeDef, _OptionalPutImageRequestRequestTypeDef
):
    pass


_RequiredPutImageTagMutabilityRequestRequestTypeDef = TypedDict(
    "_RequiredPutImageTagMutabilityRequestRequestTypeDef",
    {
        "repositoryName": str,
        "imageTagMutability": ImageTagMutabilityType,
    },
)
_OptionalPutImageTagMutabilityRequestRequestTypeDef = TypedDict(
    "_OptionalPutImageTagMutabilityRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class PutImageTagMutabilityRequestRequestTypeDef(
    _RequiredPutImageTagMutabilityRequestRequestTypeDef,
    _OptionalPutImageTagMutabilityRequestRequestTypeDef,
):
    pass


_RequiredPutLifecyclePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredPutLifecyclePolicyRequestRequestTypeDef",
    {
        "repositoryName": str,
        "lifecyclePolicyText": str,
    },
)
_OptionalPutLifecyclePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalPutLifecyclePolicyRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class PutLifecyclePolicyRequestRequestTypeDef(
    _RequiredPutLifecyclePolicyRequestRequestTypeDef,
    _OptionalPutLifecyclePolicyRequestRequestTypeDef,
):
    pass


PutRegistryPolicyRequestRequestTypeDef = TypedDict(
    "PutRegistryPolicyRequestRequestTypeDef",
    {
        "policyText": str,
    },
)

RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "url": str,
        "text": str,
    },
    total=False,
)

ScanningRepositoryFilterTypeDef = TypedDict(
    "ScanningRepositoryFilterTypeDef",
    {
        "filter": str,
        "filterType": Literal["WILDCARD"],
    },
)

ReplicationDestinationTypeDef = TypedDict(
    "ReplicationDestinationTypeDef",
    {
        "region": str,
        "registryId": str,
    },
)

RepositoryFilterTypeDef = TypedDict(
    "RepositoryFilterTypeDef",
    {
        "filter": str,
        "filterType": Literal["PREFIX_MATCH"],
    },
)

_RequiredSetRepositoryPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredSetRepositoryPolicyRequestRequestTypeDef",
    {
        "repositoryName": str,
        "policyText": str,
    },
)
_OptionalSetRepositoryPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalSetRepositoryPolicyRequestRequestTypeDef",
    {
        "registryId": str,
        "force": bool,
    },
    total=False,
)


class SetRepositoryPolicyRequestRequestTypeDef(
    _RequiredSetRepositoryPolicyRequestRequestTypeDef,
    _OptionalSetRepositoryPolicyRequestRequestTypeDef,
):
    pass


_RequiredStartLifecyclePolicyPreviewRequestRequestTypeDef = TypedDict(
    "_RequiredStartLifecyclePolicyPreviewRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalStartLifecyclePolicyPreviewRequestRequestTypeDef = TypedDict(
    "_OptionalStartLifecyclePolicyPreviewRequestRequestTypeDef",
    {
        "registryId": str,
        "lifecyclePolicyText": str,
    },
    total=False,
)


class StartLifecyclePolicyPreviewRequestRequestTypeDef(
    _RequiredStartLifecyclePolicyPreviewRequestRequestTypeDef,
    _OptionalStartLifecyclePolicyPreviewRequestRequestTypeDef,
):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUploadLayerPartRequestRequestTypeDef = TypedDict(
    "_RequiredUploadLayerPartRequestRequestTypeDef",
    {
        "repositoryName": str,
        "uploadId": str,
        "partFirstByte": int,
        "partLastByte": int,
        "layerPartBlob": Union[str, bytes, IO[Any], StreamingBody],
    },
)
_OptionalUploadLayerPartRequestRequestTypeDef = TypedDict(
    "_OptionalUploadLayerPartRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class UploadLayerPartRequestRequestTypeDef(
    _RequiredUploadLayerPartRequestRequestTypeDef, _OptionalUploadLayerPartRequestRequestTypeDef
):
    pass


ImageScanFindingTypeDef = TypedDict(
    "ImageScanFindingTypeDef",
    {
        "name": str,
        "description": str,
        "uri": str,
        "severity": FindingSeverityType,
        "attributes": List[AttributeTypeDef],
    },
    total=False,
)

ResourceDetailsTypeDef = TypedDict(
    "ResourceDetailsTypeDef",
    {
        "awsEcrContainerImage": AwsEcrContainerImageDetailsTypeDef,
    },
    total=False,
)

BatchCheckLayerAvailabilityResponseTypeDef = TypedDict(
    "BatchCheckLayerAvailabilityResponseTypeDef",
    {
        "layers": List[LayerTypeDef],
        "failures": List[LayerFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CompleteLayerUploadResponseTypeDef = TypedDict(
    "CompleteLayerUploadResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "uploadId": str,
        "layerDigest": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePullThroughCacheRuleResponseTypeDef = TypedDict(
    "CreatePullThroughCacheRuleResponseTypeDef",
    {
        "ecrRepositoryPrefix": str,
        "upstreamRegistryUrl": str,
        "createdAt": datetime,
        "registryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteLifecyclePolicyResponseTypeDef = TypedDict(
    "DeleteLifecyclePolicyResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "lifecyclePolicyText": str,
        "lastEvaluatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeletePullThroughCacheRuleResponseTypeDef = TypedDict(
    "DeletePullThroughCacheRuleResponseTypeDef",
    {
        "ecrRepositoryPrefix": str,
        "upstreamRegistryUrl": str,
        "createdAt": datetime,
        "registryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRegistryPolicyResponseTypeDef = TypedDict(
    "DeleteRegistryPolicyResponseTypeDef",
    {
        "registryId": str,
        "policyText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRepositoryPolicyResponseTypeDef = TypedDict(
    "DeleteRepositoryPolicyResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "policyText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAuthorizationTokenResponseTypeDef = TypedDict(
    "GetAuthorizationTokenResponseTypeDef",
    {
        "authorizationData": List[AuthorizationDataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDownloadUrlForLayerResponseTypeDef = TypedDict(
    "GetDownloadUrlForLayerResponseTypeDef",
    {
        "downloadUrl": str,
        "layerDigest": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLifecyclePolicyResponseTypeDef = TypedDict(
    "GetLifecyclePolicyResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "lifecyclePolicyText": str,
        "lastEvaluatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRegistryPolicyResponseTypeDef = TypedDict(
    "GetRegistryPolicyResponseTypeDef",
    {
        "registryId": str,
        "policyText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRepositoryPolicyResponseTypeDef = TypedDict(
    "GetRepositoryPolicyResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "policyText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InitiateLayerUploadResponseTypeDef = TypedDict(
    "InitiateLayerUploadResponseTypeDef",
    {
        "uploadId": str,
        "partSize": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutImageTagMutabilityResponseTypeDef = TypedDict(
    "PutImageTagMutabilityResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageTagMutability": ImageTagMutabilityType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutLifecyclePolicyResponseTypeDef = TypedDict(
    "PutLifecyclePolicyResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "lifecyclePolicyText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutRegistryPolicyResponseTypeDef = TypedDict(
    "PutRegistryPolicyResponseTypeDef",
    {
        "registryId": str,
        "policyText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SetRepositoryPolicyResponseTypeDef = TypedDict(
    "SetRepositoryPolicyResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "policyText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartLifecyclePolicyPreviewResponseTypeDef = TypedDict(
    "StartLifecyclePolicyPreviewResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "lifecyclePolicyText": str,
        "status": LifecyclePolicyPreviewStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UploadLayerPartResponseTypeDef = TypedDict(
    "UploadLayerPartResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "uploadId": str,
        "lastByteReceived": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredBatchDeleteImageRequestRequestTypeDef = TypedDict(
    "_RequiredBatchDeleteImageRequestRequestTypeDef",
    {
        "repositoryName": str,
        "imageIds": Sequence[ImageIdentifierTypeDef],
    },
)
_OptionalBatchDeleteImageRequestRequestTypeDef = TypedDict(
    "_OptionalBatchDeleteImageRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class BatchDeleteImageRequestRequestTypeDef(
    _RequiredBatchDeleteImageRequestRequestTypeDef, _OptionalBatchDeleteImageRequestRequestTypeDef
):
    pass


_RequiredBatchGetImageRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetImageRequestRequestTypeDef",
    {
        "repositoryName": str,
        "imageIds": Sequence[ImageIdentifierTypeDef],
    },
)
_OptionalBatchGetImageRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetImageRequestRequestTypeDef",
    {
        "registryId": str,
        "acceptedMediaTypes": Sequence[str],
    },
    total=False,
)


class BatchGetImageRequestRequestTypeDef(
    _RequiredBatchGetImageRequestRequestTypeDef, _OptionalBatchGetImageRequestRequestTypeDef
):
    pass


_RequiredDescribeImageReplicationStatusRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeImageReplicationStatusRequestRequestTypeDef",
    {
        "repositoryName": str,
        "imageId": ImageIdentifierTypeDef,
    },
)
_OptionalDescribeImageReplicationStatusRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeImageReplicationStatusRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class DescribeImageReplicationStatusRequestRequestTypeDef(
    _RequiredDescribeImageReplicationStatusRequestRequestTypeDef,
    _OptionalDescribeImageReplicationStatusRequestRequestTypeDef,
):
    pass


_RequiredDescribeImageScanFindingsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeImageScanFindingsRequestRequestTypeDef",
    {
        "repositoryName": str,
        "imageId": ImageIdentifierTypeDef,
    },
)
_OptionalDescribeImageScanFindingsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeImageScanFindingsRequestRequestTypeDef",
    {
        "registryId": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class DescribeImageScanFindingsRequestRequestTypeDef(
    _RequiredDescribeImageScanFindingsRequestRequestTypeDef,
    _OptionalDescribeImageScanFindingsRequestRequestTypeDef,
):
    pass


ImageFailureTypeDef = TypedDict(
    "ImageFailureTypeDef",
    {
        "imageId": ImageIdentifierTypeDef,
        "failureCode": ImageFailureCodeType,
        "failureReason": str,
    },
    total=False,
)

ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageId": ImageIdentifierTypeDef,
        "imageManifest": str,
        "imageManifestMediaType": str,
    },
    total=False,
)

ListImagesResponseTypeDef = TypedDict(
    "ListImagesResponseTypeDef",
    {
        "imageIds": List[ImageIdentifierTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartImageScanRequestRequestTypeDef = TypedDict(
    "_RequiredStartImageScanRequestRequestTypeDef",
    {
        "repositoryName": str,
        "imageId": ImageIdentifierTypeDef,
    },
)
_OptionalStartImageScanRequestRequestTypeDef = TypedDict(
    "_OptionalStartImageScanRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class StartImageScanRequestRequestTypeDef(
    _RequiredStartImageScanRequestRequestTypeDef, _OptionalStartImageScanRequestRequestTypeDef
):
    pass


_RequiredPutImageScanningConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutImageScanningConfigurationRequestRequestTypeDef",
    {
        "repositoryName": str,
        "imageScanningConfiguration": ImageScanningConfigurationTypeDef,
    },
)
_OptionalPutImageScanningConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutImageScanningConfigurationRequestRequestTypeDef",
    {
        "registryId": str,
    },
    total=False,
)


class PutImageScanningConfigurationRequestRequestTypeDef(
    _RequiredPutImageScanningConfigurationRequestRequestTypeDef,
    _OptionalPutImageScanningConfigurationRequestRequestTypeDef,
):
    pass


PutImageScanningConfigurationResponseTypeDef = TypedDict(
    "PutImageScanningConfigurationResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageScanningConfiguration": ImageScanningConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RepositoryTypeDef = TypedDict(
    "RepositoryTypeDef",
    {
        "repositoryArn": str,
        "registryId": str,
        "repositoryName": str,
        "repositoryUri": str,
        "createdAt": datetime,
        "imageTagMutability": ImageTagMutabilityType,
        "imageScanningConfiguration": ImageScanningConfigurationTypeDef,
        "encryptionConfiguration": EncryptionConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateRepositoryRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRepositoryRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalCreateRepositoryRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRepositoryRequestRequestTypeDef",
    {
        "registryId": str,
        "tags": Sequence[TagTypeDef],
        "imageTagMutability": ImageTagMutabilityType,
        "imageScanningConfiguration": ImageScanningConfigurationTypeDef,
        "encryptionConfiguration": EncryptionConfigurationTypeDef,
    },
    total=False,
)


class CreateRepositoryRequestRequestTypeDef(
    _RequiredCreateRepositoryRequestRequestTypeDef, _OptionalCreateRepositoryRequestRequestTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

CvssScoreDetailsTypeDef = TypedDict(
    "CvssScoreDetailsTypeDef",
    {
        "adjustments": List[CvssScoreAdjustmentTypeDef],
        "score": float,
        "scoreSource": str,
        "scoringVector": str,
        "version": str,
    },
    total=False,
)

DescribeImageReplicationStatusResponseTypeDef = TypedDict(
    "DescribeImageReplicationStatusResponseTypeDef",
    {
        "repositoryName": str,
        "imageId": ImageIdentifierTypeDef,
        "replicationStatuses": List[ImageReplicationStatusTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeImageScanFindingsRequestDescribeImageScanFindingsPaginateTypeDef = TypedDict(
    "_RequiredDescribeImageScanFindingsRequestDescribeImageScanFindingsPaginateTypeDef",
    {
        "repositoryName": str,
        "imageId": ImageIdentifierTypeDef,
    },
)
_OptionalDescribeImageScanFindingsRequestDescribeImageScanFindingsPaginateTypeDef = TypedDict(
    "_OptionalDescribeImageScanFindingsRequestDescribeImageScanFindingsPaginateTypeDef",
    {
        "registryId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeImageScanFindingsRequestDescribeImageScanFindingsPaginateTypeDef(
    _RequiredDescribeImageScanFindingsRequestDescribeImageScanFindingsPaginateTypeDef,
    _OptionalDescribeImageScanFindingsRequestDescribeImageScanFindingsPaginateTypeDef,
):
    pass


DescribePullThroughCacheRulesRequestDescribePullThroughCacheRulesPaginateTypeDef = TypedDict(
    "DescribePullThroughCacheRulesRequestDescribePullThroughCacheRulesPaginateTypeDef",
    {
        "registryId": str,
        "ecrRepositoryPrefixes": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeRepositoriesRequestDescribeRepositoriesPaginateTypeDef = TypedDict(
    "DescribeRepositoriesRequestDescribeRepositoriesPaginateTypeDef",
    {
        "registryId": str,
        "repositoryNames": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeImageScanFindingsRequestImageScanCompleteWaitTypeDef = TypedDict(
    "_RequiredDescribeImageScanFindingsRequestImageScanCompleteWaitTypeDef",
    {
        "repositoryName": str,
        "imageId": ImageIdentifierTypeDef,
    },
)
_OptionalDescribeImageScanFindingsRequestImageScanCompleteWaitTypeDef = TypedDict(
    "_OptionalDescribeImageScanFindingsRequestImageScanCompleteWaitTypeDef",
    {
        "registryId": str,
        "nextToken": str,
        "maxResults": int,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeImageScanFindingsRequestImageScanCompleteWaitTypeDef(
    _RequiredDescribeImageScanFindingsRequestImageScanCompleteWaitTypeDef,
    _OptionalDescribeImageScanFindingsRequestImageScanCompleteWaitTypeDef,
):
    pass


StartImageScanResponseTypeDef = TypedDict(
    "StartImageScanResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageId": ImageIdentifierTypeDef,
        "imageScanStatus": ImageScanStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeImagesRequestDescribeImagesPaginateTypeDef = TypedDict(
    "_RequiredDescribeImagesRequestDescribeImagesPaginateTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalDescribeImagesRequestDescribeImagesPaginateTypeDef = TypedDict(
    "_OptionalDescribeImagesRequestDescribeImagesPaginateTypeDef",
    {
        "registryId": str,
        "imageIds": Sequence[ImageIdentifierTypeDef],
        "filter": DescribeImagesFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeImagesRequestDescribeImagesPaginateTypeDef(
    _RequiredDescribeImagesRequestDescribeImagesPaginateTypeDef,
    _OptionalDescribeImagesRequestDescribeImagesPaginateTypeDef,
):
    pass


_RequiredDescribeImagesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeImagesRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalDescribeImagesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeImagesRequestRequestTypeDef",
    {
        "registryId": str,
        "imageIds": Sequence[ImageIdentifierTypeDef],
        "nextToken": str,
        "maxResults": int,
        "filter": DescribeImagesFilterTypeDef,
    },
    total=False,
)


class DescribeImagesRequestRequestTypeDef(
    _RequiredDescribeImagesRequestRequestTypeDef, _OptionalDescribeImagesRequestRequestTypeDef
):
    pass


DescribePullThroughCacheRulesResponseTypeDef = TypedDict(
    "DescribePullThroughCacheRulesResponseTypeDef",
    {
        "pullThroughCacheRules": List[PullThroughCacheRuleTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetLifecyclePolicyPreviewRequestGetLifecyclePolicyPreviewPaginateTypeDef = TypedDict(
    "_RequiredGetLifecyclePolicyPreviewRequestGetLifecyclePolicyPreviewPaginateTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalGetLifecyclePolicyPreviewRequestGetLifecyclePolicyPreviewPaginateTypeDef = TypedDict(
    "_OptionalGetLifecyclePolicyPreviewRequestGetLifecyclePolicyPreviewPaginateTypeDef",
    {
        "registryId": str,
        "imageIds": Sequence[ImageIdentifierTypeDef],
        "filter": LifecyclePolicyPreviewFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetLifecyclePolicyPreviewRequestGetLifecyclePolicyPreviewPaginateTypeDef(
    _RequiredGetLifecyclePolicyPreviewRequestGetLifecyclePolicyPreviewPaginateTypeDef,
    _OptionalGetLifecyclePolicyPreviewRequestGetLifecyclePolicyPreviewPaginateTypeDef,
):
    pass


_RequiredGetLifecyclePolicyPreviewRequestLifecyclePolicyPreviewCompleteWaitTypeDef = TypedDict(
    "_RequiredGetLifecyclePolicyPreviewRequestLifecyclePolicyPreviewCompleteWaitTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalGetLifecyclePolicyPreviewRequestLifecyclePolicyPreviewCompleteWaitTypeDef = TypedDict(
    "_OptionalGetLifecyclePolicyPreviewRequestLifecyclePolicyPreviewCompleteWaitTypeDef",
    {
        "registryId": str,
        "imageIds": Sequence[ImageIdentifierTypeDef],
        "nextToken": str,
        "maxResults": int,
        "filter": LifecyclePolicyPreviewFilterTypeDef,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class GetLifecyclePolicyPreviewRequestLifecyclePolicyPreviewCompleteWaitTypeDef(
    _RequiredGetLifecyclePolicyPreviewRequestLifecyclePolicyPreviewCompleteWaitTypeDef,
    _OptionalGetLifecyclePolicyPreviewRequestLifecyclePolicyPreviewCompleteWaitTypeDef,
):
    pass


_RequiredGetLifecyclePolicyPreviewRequestRequestTypeDef = TypedDict(
    "_RequiredGetLifecyclePolicyPreviewRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalGetLifecyclePolicyPreviewRequestRequestTypeDef = TypedDict(
    "_OptionalGetLifecyclePolicyPreviewRequestRequestTypeDef",
    {
        "registryId": str,
        "imageIds": Sequence[ImageIdentifierTypeDef],
        "nextToken": str,
        "maxResults": int,
        "filter": LifecyclePolicyPreviewFilterTypeDef,
    },
    total=False,
)


class GetLifecyclePolicyPreviewRequestRequestTypeDef(
    _RequiredGetLifecyclePolicyPreviewRequestRequestTypeDef,
    _OptionalGetLifecyclePolicyPreviewRequestRequestTypeDef,
):
    pass


ImageDetailTypeDef = TypedDict(
    "ImageDetailTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageDigest": str,
        "imageTags": List[str],
        "imageSizeInBytes": int,
        "imagePushedAt": datetime,
        "imageScanStatus": ImageScanStatusTypeDef,
        "imageScanFindingsSummary": ImageScanFindingsSummaryTypeDef,
        "imageManifestMediaType": str,
        "artifactMediaType": str,
        "lastRecordedPullTime": datetime,
    },
    total=False,
)

LifecyclePolicyPreviewResultTypeDef = TypedDict(
    "LifecyclePolicyPreviewResultTypeDef",
    {
        "imageTags": List[str],
        "imageDigest": str,
        "imagePushedAt": datetime,
        "action": LifecyclePolicyRuleActionTypeDef,
        "appliedRulePriority": int,
    },
    total=False,
)

_RequiredListImagesRequestListImagesPaginateTypeDef = TypedDict(
    "_RequiredListImagesRequestListImagesPaginateTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalListImagesRequestListImagesPaginateTypeDef = TypedDict(
    "_OptionalListImagesRequestListImagesPaginateTypeDef",
    {
        "registryId": str,
        "filter": ListImagesFilterTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListImagesRequestListImagesPaginateTypeDef(
    _RequiredListImagesRequestListImagesPaginateTypeDef,
    _OptionalListImagesRequestListImagesPaginateTypeDef,
):
    pass


_RequiredListImagesRequestRequestTypeDef = TypedDict(
    "_RequiredListImagesRequestRequestTypeDef",
    {
        "repositoryName": str,
    },
)
_OptionalListImagesRequestRequestTypeDef = TypedDict(
    "_OptionalListImagesRequestRequestTypeDef",
    {
        "registryId": str,
        "nextToken": str,
        "maxResults": int,
        "filter": ListImagesFilterTypeDef,
    },
    total=False,
)


class ListImagesRequestRequestTypeDef(
    _RequiredListImagesRequestRequestTypeDef, _OptionalListImagesRequestRequestTypeDef
):
    pass


PackageVulnerabilityDetailsTypeDef = TypedDict(
    "PackageVulnerabilityDetailsTypeDef",
    {
        "cvss": List[CvssScoreTypeDef],
        "referenceUrls": List[str],
        "relatedVulnerabilities": List[str],
        "source": str,
        "sourceUrl": str,
        "vendorCreatedAt": datetime,
        "vendorSeverity": str,
        "vendorUpdatedAt": datetime,
        "vulnerabilityId": str,
        "vulnerablePackages": List[VulnerablePackageTypeDef],
    },
    total=False,
)

RemediationTypeDef = TypedDict(
    "RemediationTypeDef",
    {
        "recommendation": RecommendationTypeDef,
    },
    total=False,
)

RegistryScanningRuleTypeDef = TypedDict(
    "RegistryScanningRuleTypeDef",
    {
        "scanFrequency": ScanFrequencyType,
        "repositoryFilters": List[ScanningRepositoryFilterTypeDef],
    },
)

RepositoryScanningConfigurationTypeDef = TypedDict(
    "RepositoryScanningConfigurationTypeDef",
    {
        "repositoryArn": str,
        "repositoryName": str,
        "scanOnPush": bool,
        "scanFrequency": ScanFrequencyType,
        "appliedScanFilters": List[ScanningRepositoryFilterTypeDef],
    },
    total=False,
)

_RequiredReplicationRuleTypeDef = TypedDict(
    "_RequiredReplicationRuleTypeDef",
    {
        "destinations": List[ReplicationDestinationTypeDef],
    },
)
_OptionalReplicationRuleTypeDef = TypedDict(
    "_OptionalReplicationRuleTypeDef",
    {
        "repositoryFilters": List[RepositoryFilterTypeDef],
    },
    total=False,
)


class ReplicationRuleTypeDef(_RequiredReplicationRuleTypeDef, _OptionalReplicationRuleTypeDef):
    pass


ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "details": ResourceDetailsTypeDef,
        "id": str,
        "tags": Dict[str, str],
        "type": str,
    },
    total=False,
)

BatchDeleteImageResponseTypeDef = TypedDict(
    "BatchDeleteImageResponseTypeDef",
    {
        "imageIds": List[ImageIdentifierTypeDef],
        "failures": List[ImageFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetImageResponseTypeDef = TypedDict(
    "BatchGetImageResponseTypeDef",
    {
        "images": List[ImageTypeDef],
        "failures": List[ImageFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutImageResponseTypeDef = TypedDict(
    "PutImageResponseTypeDef",
    {
        "image": ImageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRepositoryResponseTypeDef = TypedDict(
    "CreateRepositoryResponseTypeDef",
    {
        "repository": RepositoryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRepositoryResponseTypeDef = TypedDict(
    "DeleteRepositoryResponseTypeDef",
    {
        "repository": RepositoryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRepositoriesResponseTypeDef = TypedDict(
    "DescribeRepositoriesResponseTypeDef",
    {
        "repositories": List[RepositoryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ScoreDetailsTypeDef = TypedDict(
    "ScoreDetailsTypeDef",
    {
        "cvss": CvssScoreDetailsTypeDef,
    },
    total=False,
)

DescribeImagesResponseTypeDef = TypedDict(
    "DescribeImagesResponseTypeDef",
    {
        "imageDetails": List[ImageDetailTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLifecyclePolicyPreviewResponseTypeDef = TypedDict(
    "GetLifecyclePolicyPreviewResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "lifecyclePolicyText": str,
        "status": LifecyclePolicyPreviewStatusType,
        "nextToken": str,
        "previewResults": List[LifecyclePolicyPreviewResultTypeDef],
        "summary": LifecyclePolicyPreviewSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutRegistryScanningConfigurationRequestRequestTypeDef = TypedDict(
    "PutRegistryScanningConfigurationRequestRequestTypeDef",
    {
        "scanType": ScanTypeType,
        "rules": Sequence[RegistryScanningRuleTypeDef],
    },
    total=False,
)

RegistryScanningConfigurationTypeDef = TypedDict(
    "RegistryScanningConfigurationTypeDef",
    {
        "scanType": ScanTypeType,
        "rules": List[RegistryScanningRuleTypeDef],
    },
    total=False,
)

BatchGetRepositoryScanningConfigurationResponseTypeDef = TypedDict(
    "BatchGetRepositoryScanningConfigurationResponseTypeDef",
    {
        "scanningConfigurations": List[RepositoryScanningConfigurationTypeDef],
        "failures": List[RepositoryScanningConfigurationFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReplicationConfigurationTypeDef = TypedDict(
    "ReplicationConfigurationTypeDef",
    {
        "rules": List[ReplicationRuleTypeDef],
    },
)

EnhancedImageScanFindingTypeDef = TypedDict(
    "EnhancedImageScanFindingTypeDef",
    {
        "awsAccountId": str,
        "description": str,
        "findingArn": str,
        "firstObservedAt": datetime,
        "lastObservedAt": datetime,
        "packageVulnerabilityDetails": PackageVulnerabilityDetailsTypeDef,
        "remediation": RemediationTypeDef,
        "resources": List[ResourceTypeDef],
        "score": float,
        "scoreDetails": ScoreDetailsTypeDef,
        "severity": str,
        "status": str,
        "title": str,
        "type": str,
        "updatedAt": datetime,
    },
    total=False,
)

GetRegistryScanningConfigurationResponseTypeDef = TypedDict(
    "GetRegistryScanningConfigurationResponseTypeDef",
    {
        "registryId": str,
        "scanningConfiguration": RegistryScanningConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutRegistryScanningConfigurationResponseTypeDef = TypedDict(
    "PutRegistryScanningConfigurationResponseTypeDef",
    {
        "registryScanningConfiguration": RegistryScanningConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRegistryResponseTypeDef = TypedDict(
    "DescribeRegistryResponseTypeDef",
    {
        "registryId": str,
        "replicationConfiguration": ReplicationConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "PutReplicationConfigurationRequestRequestTypeDef",
    {
        "replicationConfiguration": ReplicationConfigurationTypeDef,
    },
)

PutReplicationConfigurationResponseTypeDef = TypedDict(
    "PutReplicationConfigurationResponseTypeDef",
    {
        "replicationConfiguration": ReplicationConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImageScanFindingsTypeDef = TypedDict(
    "ImageScanFindingsTypeDef",
    {
        "imageScanCompletedAt": datetime,
        "vulnerabilitySourceUpdatedAt": datetime,
        "findingSeverityCounts": Dict[FindingSeverityType, int],
        "findings": List[ImageScanFindingTypeDef],
        "enhancedFindings": List[EnhancedImageScanFindingTypeDef],
    },
    total=False,
)

DescribeImageScanFindingsResponseTypeDef = TypedDict(
    "DescribeImageScanFindingsResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageId": ImageIdentifierTypeDef,
        "imageScanStatus": ImageScanStatusTypeDef,
        "imageScanFindings": ImageScanFindingsTypeDef,
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
