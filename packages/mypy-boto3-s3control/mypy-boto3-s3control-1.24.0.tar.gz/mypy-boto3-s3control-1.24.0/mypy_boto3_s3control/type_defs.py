"""
Type annotations for s3control service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/type_defs/)

Usage::

    ```python
    from mypy_boto3_s3control.type_defs import AbortIncompleteMultipartUploadTypeDef

    data: AbortIncompleteMultipartUploadTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AsyncOperationNameType,
    BucketCannedACLType,
    BucketLocationConstraintType,
    ExpirationStatusType,
    FormatType,
    JobManifestFieldNameType,
    JobManifestFormatType,
    JobReportScopeType,
    JobStatusType,
    MultiRegionAccessPointStatusType,
    NetworkOriginType,
    ObjectLambdaAllowedFeatureType,
    OperationNameType,
    ReplicationStatusType,
    RequestedJobStatusType,
    S3CannedAccessControlListType,
    S3ChecksumAlgorithmType,
    S3GlacierJobTierType,
    S3GranteeTypeIdentifierType,
    S3MetadataDirectiveType,
    S3ObjectLockLegalHoldStatusType,
    S3ObjectLockModeType,
    S3ObjectLockRetentionModeType,
    S3PermissionType,
    S3SSEAlgorithmType,
    S3StorageClassType,
    TransitionStorageClassType,
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
    "AbortIncompleteMultipartUploadTypeDef",
    "VpcConfigurationTypeDef",
    "ActivityMetricsTypeDef",
    "AsyncErrorDetailsTypeDef",
    "DeleteMultiRegionAccessPointInputTypeDef",
    "PutMultiRegionAccessPointPolicyInputTypeDef",
    "AwsLambdaTransformationTypeDef",
    "CloudWatchMetricsTypeDef",
    "ResponseMetadataTypeDef",
    "PublicAccessBlockConfigurationTypeDef",
    "CreateBucketConfigurationTypeDef",
    "JobReportTypeDef",
    "S3TagTypeDef",
    "RegionTypeDef",
    "DeleteAccessPointForObjectLambdaRequestRequestTypeDef",
    "DeleteAccessPointPolicyForObjectLambdaRequestRequestTypeDef",
    "DeleteAccessPointPolicyRequestRequestTypeDef",
    "DeleteAccessPointRequestRequestTypeDef",
    "DeleteBucketLifecycleConfigurationRequestRequestTypeDef",
    "DeleteBucketPolicyRequestRequestTypeDef",
    "DeleteBucketRequestRequestTypeDef",
    "DeleteBucketTaggingRequestRequestTypeDef",
    "DeleteJobTaggingRequestRequestTypeDef",
    "DeletePublicAccessBlockRequestRequestTypeDef",
    "DeleteStorageLensConfigurationRequestRequestTypeDef",
    "DeleteStorageLensConfigurationTaggingRequestRequestTypeDef",
    "DescribeJobRequestRequestTypeDef",
    "DescribeMultiRegionAccessPointOperationRequestRequestTypeDef",
    "EstablishedMultiRegionAccessPointPolicyTypeDef",
    "ExcludeTypeDef",
    "SSEKMSEncryptionTypeDef",
    "GetAccessPointConfigurationForObjectLambdaRequestRequestTypeDef",
    "GetAccessPointForObjectLambdaRequestRequestTypeDef",
    "GetAccessPointPolicyForObjectLambdaRequestRequestTypeDef",
    "GetAccessPointPolicyRequestRequestTypeDef",
    "GetAccessPointPolicyStatusForObjectLambdaRequestRequestTypeDef",
    "PolicyStatusTypeDef",
    "GetAccessPointPolicyStatusRequestRequestTypeDef",
    "GetAccessPointRequestRequestTypeDef",
    "GetBucketLifecycleConfigurationRequestRequestTypeDef",
    "GetBucketPolicyRequestRequestTypeDef",
    "GetBucketRequestRequestTypeDef",
    "GetBucketTaggingRequestRequestTypeDef",
    "GetJobTaggingRequestRequestTypeDef",
    "GetMultiRegionAccessPointPolicyRequestRequestTypeDef",
    "GetMultiRegionAccessPointPolicyStatusRequestRequestTypeDef",
    "GetMultiRegionAccessPointRequestRequestTypeDef",
    "GetPublicAccessBlockRequestRequestTypeDef",
    "GetStorageLensConfigurationRequestRequestTypeDef",
    "GetStorageLensConfigurationTaggingRequestRequestTypeDef",
    "StorageLensTagTypeDef",
    "IncludeTypeDef",
    "JobFailureTypeDef",
    "JobManifestGeneratorFilterTypeDef",
    "JobManifestLocationTypeDef",
    "JobManifestSpecTypeDef",
    "LambdaInvokeOperationTypeDef",
    "S3InitiateRestoreObjectOperationTypeDef",
    "JobTimersTypeDef",
    "LifecycleExpirationTypeDef",
    "NoncurrentVersionExpirationTypeDef",
    "NoncurrentVersionTransitionTypeDef",
    "TransitionTypeDef",
    "PaginatorConfigTypeDef",
    "ListAccessPointsForObjectLambdaRequestRequestTypeDef",
    "ObjectLambdaAccessPointTypeDef",
    "ListAccessPointsRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListMultiRegionAccessPointsRequestRequestTypeDef",
    "ListRegionalBucketsRequestRequestTypeDef",
    "RegionalBucketTypeDef",
    "ListStorageLensConfigurationEntryTypeDef",
    "ListStorageLensConfigurationsRequestRequestTypeDef",
    "ProposedMultiRegionAccessPointPolicyTypeDef",
    "MultiRegionAccessPointRegionalResponseTypeDef",
    "RegionReportTypeDef",
    "SelectionCriteriaTypeDef",
    "PutAccessPointPolicyForObjectLambdaRequestRequestTypeDef",
    "PutAccessPointPolicyRequestRequestTypeDef",
    "PutBucketPolicyRequestRequestTypeDef",
    "S3ObjectOwnerTypeDef",
    "S3ObjectMetadataTypeDef",
    "S3GranteeTypeDef",
    "S3ObjectLockLegalHoldTypeDef",
    "S3RetentionTypeDef",
    "SSEKMSTypeDef",
    "StorageLensAwsOrgTypeDef",
    "UpdateJobPriorityRequestRequestTypeDef",
    "UpdateJobStatusRequestRequestTypeDef",
    "AccessPointTypeDef",
    "DeleteMultiRegionAccessPointRequestRequestTypeDef",
    "PutMultiRegionAccessPointPolicyRequestRequestTypeDef",
    "ObjectLambdaContentTransformationTypeDef",
    "CreateAccessPointForObjectLambdaResultTypeDef",
    "CreateAccessPointResultTypeDef",
    "CreateBucketResultTypeDef",
    "CreateJobResultTypeDef",
    "CreateMultiRegionAccessPointResultTypeDef",
    "DeleteMultiRegionAccessPointResultTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAccessPointPolicyForObjectLambdaResultTypeDef",
    "GetAccessPointPolicyResultTypeDef",
    "GetBucketPolicyResultTypeDef",
    "GetBucketResultTypeDef",
    "PutMultiRegionAccessPointPolicyResultTypeDef",
    "UpdateJobPriorityResultTypeDef",
    "UpdateJobStatusResultTypeDef",
    "CreateAccessPointRequestRequestTypeDef",
    "GetAccessPointForObjectLambdaResultTypeDef",
    "GetAccessPointResultTypeDef",
    "GetPublicAccessBlockOutputTypeDef",
    "PutPublicAccessBlockRequestRequestTypeDef",
    "CreateBucketRequestRequestTypeDef",
    "GetBucketTaggingResultTypeDef",
    "GetJobTaggingResultTypeDef",
    "LifecycleRuleAndOperatorTypeDef",
    "PutJobTaggingRequestRequestTypeDef",
    "S3SetObjectTaggingOperationTypeDef",
    "TaggingTypeDef",
    "CreateMultiRegionAccessPointInputTypeDef",
    "GeneratedManifestEncryptionTypeDef",
    "GetAccessPointPolicyStatusForObjectLambdaResultTypeDef",
    "GetAccessPointPolicyStatusResultTypeDef",
    "GetMultiRegionAccessPointPolicyStatusResultTypeDef",
    "GetStorageLensConfigurationTaggingResultTypeDef",
    "PutStorageLensConfigurationTaggingRequestRequestTypeDef",
    "S3GeneratedManifestDescriptorTypeDef",
    "JobManifestTypeDef",
    "JobProgressSummaryTypeDef",
    "ListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef",
    "ListAccessPointsForObjectLambdaResultTypeDef",
    "ListRegionalBucketsResultTypeDef",
    "ListStorageLensConfigurationsResultTypeDef",
    "MultiRegionAccessPointPolicyDocumentTypeDef",
    "MultiRegionAccessPointsAsyncResponseTypeDef",
    "MultiRegionAccessPointReportTypeDef",
    "PrefixLevelStorageMetricsTypeDef",
    "S3GrantTypeDef",
    "S3SetObjectLegalHoldOperationTypeDef",
    "S3SetObjectRetentionOperationTypeDef",
    "StorageLensDataExportEncryptionTypeDef",
    "ListAccessPointsResultTypeDef",
    "ObjectLambdaTransformationConfigurationTypeDef",
    "LifecycleRuleFilterTypeDef",
    "PutBucketTaggingRequestRequestTypeDef",
    "AsyncRequestParametersTypeDef",
    "CreateMultiRegionAccessPointRequestRequestTypeDef",
    "S3ManifestOutputLocationTypeDef",
    "JobListDescriptorTypeDef",
    "GetMultiRegionAccessPointPolicyResultTypeDef",
    "AsyncResponseDetailsTypeDef",
    "GetMultiRegionAccessPointResultTypeDef",
    "ListMultiRegionAccessPointsResultTypeDef",
    "PrefixLevelTypeDef",
    "S3AccessControlListTypeDef",
    "S3CopyObjectOperationTypeDef",
    "S3BucketDestinationTypeDef",
    "ObjectLambdaConfigurationTypeDef",
    "LifecycleRuleTypeDef",
    "S3JobManifestGeneratorTypeDef",
    "ListJobsResultTypeDef",
    "AsyncOperationTypeDef",
    "BucketLevelTypeDef",
    "S3AccessControlPolicyTypeDef",
    "StorageLensDataExportTypeDef",
    "CreateAccessPointForObjectLambdaRequestRequestTypeDef",
    "GetAccessPointConfigurationForObjectLambdaResultTypeDef",
    "PutAccessPointConfigurationForObjectLambdaRequestRequestTypeDef",
    "GetBucketLifecycleConfigurationResultTypeDef",
    "LifecycleConfigurationTypeDef",
    "JobManifestGeneratorTypeDef",
    "DescribeMultiRegionAccessPointOperationResultTypeDef",
    "AccountLevelTypeDef",
    "S3SetObjectAclOperationTypeDef",
    "PutBucketLifecycleConfigurationRequestRequestTypeDef",
    "StorageLensConfigurationTypeDef",
    "JobOperationTypeDef",
    "GetStorageLensConfigurationResultTypeDef",
    "PutStorageLensConfigurationRequestRequestTypeDef",
    "CreateJobRequestRequestTypeDef",
    "JobDescriptorTypeDef",
    "DescribeJobResultTypeDef",
)

AbortIncompleteMultipartUploadTypeDef = TypedDict(
    "AbortIncompleteMultipartUploadTypeDef",
    {
        "DaysAfterInitiation": int,
    },
    total=False,
)

VpcConfigurationTypeDef = TypedDict(
    "VpcConfigurationTypeDef",
    {
        "VpcId": str,
    },
)

ActivityMetricsTypeDef = TypedDict(
    "ActivityMetricsTypeDef",
    {
        "IsEnabled": bool,
    },
    total=False,
)

AsyncErrorDetailsTypeDef = TypedDict(
    "AsyncErrorDetailsTypeDef",
    {
        "Code": str,
        "Message": str,
        "Resource": str,
        "RequestId": str,
    },
    total=False,
)

DeleteMultiRegionAccessPointInputTypeDef = TypedDict(
    "DeleteMultiRegionAccessPointInputTypeDef",
    {
        "Name": str,
    },
)

PutMultiRegionAccessPointPolicyInputTypeDef = TypedDict(
    "PutMultiRegionAccessPointPolicyInputTypeDef",
    {
        "Name": str,
        "Policy": str,
    },
)

_RequiredAwsLambdaTransformationTypeDef = TypedDict(
    "_RequiredAwsLambdaTransformationTypeDef",
    {
        "FunctionArn": str,
    },
)
_OptionalAwsLambdaTransformationTypeDef = TypedDict(
    "_OptionalAwsLambdaTransformationTypeDef",
    {
        "FunctionPayload": str,
    },
    total=False,
)


class AwsLambdaTransformationTypeDef(
    _RequiredAwsLambdaTransformationTypeDef, _OptionalAwsLambdaTransformationTypeDef
):
    pass


CloudWatchMetricsTypeDef = TypedDict(
    "CloudWatchMetricsTypeDef",
    {
        "IsEnabled": bool,
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

PublicAccessBlockConfigurationTypeDef = TypedDict(
    "PublicAccessBlockConfigurationTypeDef",
    {
        "BlockPublicAcls": bool,
        "IgnorePublicAcls": bool,
        "BlockPublicPolicy": bool,
        "RestrictPublicBuckets": bool,
    },
    total=False,
)

CreateBucketConfigurationTypeDef = TypedDict(
    "CreateBucketConfigurationTypeDef",
    {
        "LocationConstraint": BucketLocationConstraintType,
    },
    total=False,
)

_RequiredJobReportTypeDef = TypedDict(
    "_RequiredJobReportTypeDef",
    {
        "Enabled": bool,
    },
)
_OptionalJobReportTypeDef = TypedDict(
    "_OptionalJobReportTypeDef",
    {
        "Bucket": str,
        "Format": Literal["Report_CSV_20180820"],
        "Prefix": str,
        "ReportScope": JobReportScopeType,
    },
    total=False,
)


class JobReportTypeDef(_RequiredJobReportTypeDef, _OptionalJobReportTypeDef):
    pass


S3TagTypeDef = TypedDict(
    "S3TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

RegionTypeDef = TypedDict(
    "RegionTypeDef",
    {
        "Bucket": str,
    },
)

DeleteAccessPointForObjectLambdaRequestRequestTypeDef = TypedDict(
    "DeleteAccessPointForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

DeleteAccessPointPolicyForObjectLambdaRequestRequestTypeDef = TypedDict(
    "DeleteAccessPointPolicyForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

DeleteAccessPointPolicyRequestRequestTypeDef = TypedDict(
    "DeleteAccessPointPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

DeleteAccessPointRequestRequestTypeDef = TypedDict(
    "DeleteAccessPointRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

DeleteBucketLifecycleConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteBucketLifecycleConfigurationRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

DeleteBucketPolicyRequestRequestTypeDef = TypedDict(
    "DeleteBucketPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

DeleteBucketRequestRequestTypeDef = TypedDict(
    "DeleteBucketRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

DeleteBucketTaggingRequestRequestTypeDef = TypedDict(
    "DeleteBucketTaggingRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

DeleteJobTaggingRequestRequestTypeDef = TypedDict(
    "DeleteJobTaggingRequestRequestTypeDef",
    {
        "AccountId": str,
        "JobId": str,
    },
)

DeletePublicAccessBlockRequestRequestTypeDef = TypedDict(
    "DeletePublicAccessBlockRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)

DeleteStorageLensConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteStorageLensConfigurationRequestRequestTypeDef",
    {
        "ConfigId": str,
        "AccountId": str,
    },
)

DeleteStorageLensConfigurationTaggingRequestRequestTypeDef = TypedDict(
    "DeleteStorageLensConfigurationTaggingRequestRequestTypeDef",
    {
        "ConfigId": str,
        "AccountId": str,
    },
)

DescribeJobRequestRequestTypeDef = TypedDict(
    "DescribeJobRequestRequestTypeDef",
    {
        "AccountId": str,
        "JobId": str,
    },
)

DescribeMultiRegionAccessPointOperationRequestRequestTypeDef = TypedDict(
    "DescribeMultiRegionAccessPointOperationRequestRequestTypeDef",
    {
        "AccountId": str,
        "RequestTokenARN": str,
    },
)

EstablishedMultiRegionAccessPointPolicyTypeDef = TypedDict(
    "EstablishedMultiRegionAccessPointPolicyTypeDef",
    {
        "Policy": str,
    },
    total=False,
)

ExcludeTypeDef = TypedDict(
    "ExcludeTypeDef",
    {
        "Buckets": List[str],
        "Regions": List[str],
    },
    total=False,
)

SSEKMSEncryptionTypeDef = TypedDict(
    "SSEKMSEncryptionTypeDef",
    {
        "KeyId": str,
    },
)

GetAccessPointConfigurationForObjectLambdaRequestRequestTypeDef = TypedDict(
    "GetAccessPointConfigurationForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetAccessPointForObjectLambdaRequestRequestTypeDef = TypedDict(
    "GetAccessPointForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetAccessPointPolicyForObjectLambdaRequestRequestTypeDef = TypedDict(
    "GetAccessPointPolicyForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetAccessPointPolicyRequestRequestTypeDef = TypedDict(
    "GetAccessPointPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetAccessPointPolicyStatusForObjectLambdaRequestRequestTypeDef = TypedDict(
    "GetAccessPointPolicyStatusForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

PolicyStatusTypeDef = TypedDict(
    "PolicyStatusTypeDef",
    {
        "IsPublic": bool,
    },
    total=False,
)

GetAccessPointPolicyStatusRequestRequestTypeDef = TypedDict(
    "GetAccessPointPolicyStatusRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetAccessPointRequestRequestTypeDef = TypedDict(
    "GetAccessPointRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetBucketLifecycleConfigurationRequestRequestTypeDef = TypedDict(
    "GetBucketLifecycleConfigurationRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

GetBucketPolicyRequestRequestTypeDef = TypedDict(
    "GetBucketPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

GetBucketRequestRequestTypeDef = TypedDict(
    "GetBucketRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

GetBucketTaggingRequestRequestTypeDef = TypedDict(
    "GetBucketTaggingRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

GetJobTaggingRequestRequestTypeDef = TypedDict(
    "GetJobTaggingRequestRequestTypeDef",
    {
        "AccountId": str,
        "JobId": str,
    },
)

GetMultiRegionAccessPointPolicyRequestRequestTypeDef = TypedDict(
    "GetMultiRegionAccessPointPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetMultiRegionAccessPointPolicyStatusRequestRequestTypeDef = TypedDict(
    "GetMultiRegionAccessPointPolicyStatusRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetMultiRegionAccessPointRequestRequestTypeDef = TypedDict(
    "GetMultiRegionAccessPointRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetPublicAccessBlockRequestRequestTypeDef = TypedDict(
    "GetPublicAccessBlockRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)

GetStorageLensConfigurationRequestRequestTypeDef = TypedDict(
    "GetStorageLensConfigurationRequestRequestTypeDef",
    {
        "ConfigId": str,
        "AccountId": str,
    },
)

GetStorageLensConfigurationTaggingRequestRequestTypeDef = TypedDict(
    "GetStorageLensConfigurationTaggingRequestRequestTypeDef",
    {
        "ConfigId": str,
        "AccountId": str,
    },
)

StorageLensTagTypeDef = TypedDict(
    "StorageLensTagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

IncludeTypeDef = TypedDict(
    "IncludeTypeDef",
    {
        "Buckets": List[str],
        "Regions": List[str],
    },
    total=False,
)

JobFailureTypeDef = TypedDict(
    "JobFailureTypeDef",
    {
        "FailureCode": str,
        "FailureReason": str,
    },
    total=False,
)

JobManifestGeneratorFilterTypeDef = TypedDict(
    "JobManifestGeneratorFilterTypeDef",
    {
        "EligibleForReplication": bool,
        "CreatedAfter": Union[datetime, str],
        "CreatedBefore": Union[datetime, str],
        "ObjectReplicationStatuses": Sequence[ReplicationStatusType],
    },
    total=False,
)

_RequiredJobManifestLocationTypeDef = TypedDict(
    "_RequiredJobManifestLocationTypeDef",
    {
        "ObjectArn": str,
        "ETag": str,
    },
)
_OptionalJobManifestLocationTypeDef = TypedDict(
    "_OptionalJobManifestLocationTypeDef",
    {
        "ObjectVersionId": str,
    },
    total=False,
)


class JobManifestLocationTypeDef(
    _RequiredJobManifestLocationTypeDef, _OptionalJobManifestLocationTypeDef
):
    pass


_RequiredJobManifestSpecTypeDef = TypedDict(
    "_RequiredJobManifestSpecTypeDef",
    {
        "Format": JobManifestFormatType,
    },
)
_OptionalJobManifestSpecTypeDef = TypedDict(
    "_OptionalJobManifestSpecTypeDef",
    {
        "Fields": Sequence[JobManifestFieldNameType],
    },
    total=False,
)


class JobManifestSpecTypeDef(_RequiredJobManifestSpecTypeDef, _OptionalJobManifestSpecTypeDef):
    pass


LambdaInvokeOperationTypeDef = TypedDict(
    "LambdaInvokeOperationTypeDef",
    {
        "FunctionArn": str,
    },
    total=False,
)

S3InitiateRestoreObjectOperationTypeDef = TypedDict(
    "S3InitiateRestoreObjectOperationTypeDef",
    {
        "ExpirationInDays": int,
        "GlacierJobTier": S3GlacierJobTierType,
    },
    total=False,
)

JobTimersTypeDef = TypedDict(
    "JobTimersTypeDef",
    {
        "ElapsedTimeInActiveSeconds": int,
    },
    total=False,
)

LifecycleExpirationTypeDef = TypedDict(
    "LifecycleExpirationTypeDef",
    {
        "Date": datetime,
        "Days": int,
        "ExpiredObjectDeleteMarker": bool,
    },
    total=False,
)

NoncurrentVersionExpirationTypeDef = TypedDict(
    "NoncurrentVersionExpirationTypeDef",
    {
        "NoncurrentDays": int,
    },
    total=False,
)

NoncurrentVersionTransitionTypeDef = TypedDict(
    "NoncurrentVersionTransitionTypeDef",
    {
        "NoncurrentDays": int,
        "StorageClass": TransitionStorageClassType,
    },
    total=False,
)

TransitionTypeDef = TypedDict(
    "TransitionTypeDef",
    {
        "Date": datetime,
        "Days": int,
        "StorageClass": TransitionStorageClassType,
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

_RequiredListAccessPointsForObjectLambdaRequestRequestTypeDef = TypedDict(
    "_RequiredListAccessPointsForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalListAccessPointsForObjectLambdaRequestRequestTypeDef = TypedDict(
    "_OptionalListAccessPointsForObjectLambdaRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListAccessPointsForObjectLambdaRequestRequestTypeDef(
    _RequiredListAccessPointsForObjectLambdaRequestRequestTypeDef,
    _OptionalListAccessPointsForObjectLambdaRequestRequestTypeDef,
):
    pass


_RequiredObjectLambdaAccessPointTypeDef = TypedDict(
    "_RequiredObjectLambdaAccessPointTypeDef",
    {
        "Name": str,
    },
)
_OptionalObjectLambdaAccessPointTypeDef = TypedDict(
    "_OptionalObjectLambdaAccessPointTypeDef",
    {
        "ObjectLambdaAccessPointArn": str,
    },
    total=False,
)


class ObjectLambdaAccessPointTypeDef(
    _RequiredObjectLambdaAccessPointTypeDef, _OptionalObjectLambdaAccessPointTypeDef
):
    pass


_RequiredListAccessPointsRequestRequestTypeDef = TypedDict(
    "_RequiredListAccessPointsRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalListAccessPointsRequestRequestTypeDef = TypedDict(
    "_OptionalListAccessPointsRequestRequestTypeDef",
    {
        "Bucket": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListAccessPointsRequestRequestTypeDef(
    _RequiredListAccessPointsRequestRequestTypeDef, _OptionalListAccessPointsRequestRequestTypeDef
):
    pass


_RequiredListJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListJobsRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalListJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListJobsRequestRequestTypeDef",
    {
        "JobStatuses": Sequence[JobStatusType],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListJobsRequestRequestTypeDef(
    _RequiredListJobsRequestRequestTypeDef, _OptionalListJobsRequestRequestTypeDef
):
    pass


_RequiredListMultiRegionAccessPointsRequestRequestTypeDef = TypedDict(
    "_RequiredListMultiRegionAccessPointsRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalListMultiRegionAccessPointsRequestRequestTypeDef = TypedDict(
    "_OptionalListMultiRegionAccessPointsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListMultiRegionAccessPointsRequestRequestTypeDef(
    _RequiredListMultiRegionAccessPointsRequestRequestTypeDef,
    _OptionalListMultiRegionAccessPointsRequestRequestTypeDef,
):
    pass


_RequiredListRegionalBucketsRequestRequestTypeDef = TypedDict(
    "_RequiredListRegionalBucketsRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalListRegionalBucketsRequestRequestTypeDef = TypedDict(
    "_OptionalListRegionalBucketsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "OutpostId": str,
    },
    total=False,
)


class ListRegionalBucketsRequestRequestTypeDef(
    _RequiredListRegionalBucketsRequestRequestTypeDef,
    _OptionalListRegionalBucketsRequestRequestTypeDef,
):
    pass


_RequiredRegionalBucketTypeDef = TypedDict(
    "_RequiredRegionalBucketTypeDef",
    {
        "Bucket": str,
        "PublicAccessBlockEnabled": bool,
        "CreationDate": datetime,
    },
)
_OptionalRegionalBucketTypeDef = TypedDict(
    "_OptionalRegionalBucketTypeDef",
    {
        "BucketArn": str,
        "OutpostId": str,
    },
    total=False,
)


class RegionalBucketTypeDef(_RequiredRegionalBucketTypeDef, _OptionalRegionalBucketTypeDef):
    pass


_RequiredListStorageLensConfigurationEntryTypeDef = TypedDict(
    "_RequiredListStorageLensConfigurationEntryTypeDef",
    {
        "Id": str,
        "StorageLensArn": str,
        "HomeRegion": str,
    },
)
_OptionalListStorageLensConfigurationEntryTypeDef = TypedDict(
    "_OptionalListStorageLensConfigurationEntryTypeDef",
    {
        "IsEnabled": bool,
    },
    total=False,
)


class ListStorageLensConfigurationEntryTypeDef(
    _RequiredListStorageLensConfigurationEntryTypeDef,
    _OptionalListStorageLensConfigurationEntryTypeDef,
):
    pass


_RequiredListStorageLensConfigurationsRequestRequestTypeDef = TypedDict(
    "_RequiredListStorageLensConfigurationsRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalListStorageLensConfigurationsRequestRequestTypeDef = TypedDict(
    "_OptionalListStorageLensConfigurationsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class ListStorageLensConfigurationsRequestRequestTypeDef(
    _RequiredListStorageLensConfigurationsRequestRequestTypeDef,
    _OptionalListStorageLensConfigurationsRequestRequestTypeDef,
):
    pass


ProposedMultiRegionAccessPointPolicyTypeDef = TypedDict(
    "ProposedMultiRegionAccessPointPolicyTypeDef",
    {
        "Policy": str,
    },
    total=False,
)

MultiRegionAccessPointRegionalResponseTypeDef = TypedDict(
    "MultiRegionAccessPointRegionalResponseTypeDef",
    {
        "Name": str,
        "RequestStatus": str,
    },
    total=False,
)

RegionReportTypeDef = TypedDict(
    "RegionReportTypeDef",
    {
        "Bucket": str,
        "Region": str,
    },
    total=False,
)

SelectionCriteriaTypeDef = TypedDict(
    "SelectionCriteriaTypeDef",
    {
        "Delimiter": str,
        "MaxDepth": int,
        "MinStorageBytesPercentage": float,
    },
    total=False,
)

PutAccessPointPolicyForObjectLambdaRequestRequestTypeDef = TypedDict(
    "PutAccessPointPolicyForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
        "Policy": str,
    },
)

PutAccessPointPolicyRequestRequestTypeDef = TypedDict(
    "PutAccessPointPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
        "Policy": str,
    },
)

_RequiredPutBucketPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
        "Policy": str,
    },
)
_OptionalPutBucketPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketPolicyRequestRequestTypeDef",
    {
        "ConfirmRemoveSelfBucketAccess": bool,
    },
    total=False,
)


class PutBucketPolicyRequestRequestTypeDef(
    _RequiredPutBucketPolicyRequestRequestTypeDef, _OptionalPutBucketPolicyRequestRequestTypeDef
):
    pass


S3ObjectOwnerTypeDef = TypedDict(
    "S3ObjectOwnerTypeDef",
    {
        "ID": str,
        "DisplayName": str,
    },
    total=False,
)

S3ObjectMetadataTypeDef = TypedDict(
    "S3ObjectMetadataTypeDef",
    {
        "CacheControl": str,
        "ContentDisposition": str,
        "ContentEncoding": str,
        "ContentLanguage": str,
        "UserMetadata": Mapping[str, str],
        "ContentLength": int,
        "ContentMD5": str,
        "ContentType": str,
        "HttpExpiresDate": Union[datetime, str],
        "RequesterCharged": bool,
        "SSEAlgorithm": S3SSEAlgorithmType,
    },
    total=False,
)

S3GranteeTypeDef = TypedDict(
    "S3GranteeTypeDef",
    {
        "TypeIdentifier": S3GranteeTypeIdentifierType,
        "Identifier": str,
        "DisplayName": str,
    },
    total=False,
)

S3ObjectLockLegalHoldTypeDef = TypedDict(
    "S3ObjectLockLegalHoldTypeDef",
    {
        "Status": S3ObjectLockLegalHoldStatusType,
    },
)

S3RetentionTypeDef = TypedDict(
    "S3RetentionTypeDef",
    {
        "RetainUntilDate": Union[datetime, str],
        "Mode": S3ObjectLockRetentionModeType,
    },
    total=False,
)

SSEKMSTypeDef = TypedDict(
    "SSEKMSTypeDef",
    {
        "KeyId": str,
    },
)

StorageLensAwsOrgTypeDef = TypedDict(
    "StorageLensAwsOrgTypeDef",
    {
        "Arn": str,
    },
)

UpdateJobPriorityRequestRequestTypeDef = TypedDict(
    "UpdateJobPriorityRequestRequestTypeDef",
    {
        "AccountId": str,
        "JobId": str,
        "Priority": int,
    },
)

_RequiredUpdateJobStatusRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateJobStatusRequestRequestTypeDef",
    {
        "AccountId": str,
        "JobId": str,
        "RequestedJobStatus": RequestedJobStatusType,
    },
)
_OptionalUpdateJobStatusRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateJobStatusRequestRequestTypeDef",
    {
        "StatusUpdateReason": str,
    },
    total=False,
)


class UpdateJobStatusRequestRequestTypeDef(
    _RequiredUpdateJobStatusRequestRequestTypeDef, _OptionalUpdateJobStatusRequestRequestTypeDef
):
    pass


_RequiredAccessPointTypeDef = TypedDict(
    "_RequiredAccessPointTypeDef",
    {
        "Name": str,
        "NetworkOrigin": NetworkOriginType,
        "Bucket": str,
    },
)
_OptionalAccessPointTypeDef = TypedDict(
    "_OptionalAccessPointTypeDef",
    {
        "VpcConfiguration": VpcConfigurationTypeDef,
        "AccessPointArn": str,
        "Alias": str,
    },
    total=False,
)


class AccessPointTypeDef(_RequiredAccessPointTypeDef, _OptionalAccessPointTypeDef):
    pass


DeleteMultiRegionAccessPointRequestRequestTypeDef = TypedDict(
    "DeleteMultiRegionAccessPointRequestRequestTypeDef",
    {
        "AccountId": str,
        "ClientToken": str,
        "Details": DeleteMultiRegionAccessPointInputTypeDef,
    },
)

PutMultiRegionAccessPointPolicyRequestRequestTypeDef = TypedDict(
    "PutMultiRegionAccessPointPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "ClientToken": str,
        "Details": PutMultiRegionAccessPointPolicyInputTypeDef,
    },
)

ObjectLambdaContentTransformationTypeDef = TypedDict(
    "ObjectLambdaContentTransformationTypeDef",
    {
        "AwsLambda": AwsLambdaTransformationTypeDef,
    },
    total=False,
)

CreateAccessPointForObjectLambdaResultTypeDef = TypedDict(
    "CreateAccessPointForObjectLambdaResultTypeDef",
    {
        "ObjectLambdaAccessPointArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAccessPointResultTypeDef = TypedDict(
    "CreateAccessPointResultTypeDef",
    {
        "AccessPointArn": str,
        "Alias": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBucketResultTypeDef = TypedDict(
    "CreateBucketResultTypeDef",
    {
        "Location": str,
        "BucketArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateJobResultTypeDef = TypedDict(
    "CreateJobResultTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMultiRegionAccessPointResultTypeDef = TypedDict(
    "CreateMultiRegionAccessPointResultTypeDef",
    {
        "RequestTokenARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteMultiRegionAccessPointResultTypeDef = TypedDict(
    "DeleteMultiRegionAccessPointResultTypeDef",
    {
        "RequestTokenARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessPointPolicyForObjectLambdaResultTypeDef = TypedDict(
    "GetAccessPointPolicyForObjectLambdaResultTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessPointPolicyResultTypeDef = TypedDict(
    "GetAccessPointPolicyResultTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBucketPolicyResultTypeDef = TypedDict(
    "GetBucketPolicyResultTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBucketResultTypeDef = TypedDict(
    "GetBucketResultTypeDef",
    {
        "Bucket": str,
        "PublicAccessBlockEnabled": bool,
        "CreationDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutMultiRegionAccessPointPolicyResultTypeDef = TypedDict(
    "PutMultiRegionAccessPointPolicyResultTypeDef",
    {
        "RequestTokenARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateJobPriorityResultTypeDef = TypedDict(
    "UpdateJobPriorityResultTypeDef",
    {
        "JobId": str,
        "Priority": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateJobStatusResultTypeDef = TypedDict(
    "UpdateJobStatusResultTypeDef",
    {
        "JobId": str,
        "Status": JobStatusType,
        "StatusUpdateReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateAccessPointRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAccessPointRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
        "Bucket": str,
    },
)
_OptionalCreateAccessPointRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAccessPointRequestRequestTypeDef",
    {
        "VpcConfiguration": VpcConfigurationTypeDef,
        "PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef,
    },
    total=False,
)


class CreateAccessPointRequestRequestTypeDef(
    _RequiredCreateAccessPointRequestRequestTypeDef, _OptionalCreateAccessPointRequestRequestTypeDef
):
    pass


GetAccessPointForObjectLambdaResultTypeDef = TypedDict(
    "GetAccessPointForObjectLambdaResultTypeDef",
    {
        "Name": str,
        "PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef,
        "CreationDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessPointResultTypeDef = TypedDict(
    "GetAccessPointResultTypeDef",
    {
        "Name": str,
        "Bucket": str,
        "NetworkOrigin": NetworkOriginType,
        "VpcConfiguration": VpcConfigurationTypeDef,
        "PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef,
        "CreationDate": datetime,
        "Alias": str,
        "AccessPointArn": str,
        "Endpoints": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPublicAccessBlockOutputTypeDef = TypedDict(
    "GetPublicAccessBlockOutputTypeDef",
    {
        "PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutPublicAccessBlockRequestRequestTypeDef = TypedDict(
    "PutPublicAccessBlockRequestRequestTypeDef",
    {
        "PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef,
        "AccountId": str,
    },
)

_RequiredCreateBucketRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBucketRequestRequestTypeDef",
    {
        "Bucket": str,
    },
)
_OptionalCreateBucketRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBucketRequestRequestTypeDef",
    {
        "ACL": BucketCannedACLType,
        "CreateBucketConfiguration": CreateBucketConfigurationTypeDef,
        "GrantFullControl": str,
        "GrantRead": str,
        "GrantReadACP": str,
        "GrantWrite": str,
        "GrantWriteACP": str,
        "ObjectLockEnabledForBucket": bool,
        "OutpostId": str,
    },
    total=False,
)


class CreateBucketRequestRequestTypeDef(
    _RequiredCreateBucketRequestRequestTypeDef, _OptionalCreateBucketRequestRequestTypeDef
):
    pass


GetBucketTaggingResultTypeDef = TypedDict(
    "GetBucketTaggingResultTypeDef",
    {
        "TagSet": List[S3TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobTaggingResultTypeDef = TypedDict(
    "GetJobTaggingResultTypeDef",
    {
        "Tags": List[S3TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LifecycleRuleAndOperatorTypeDef = TypedDict(
    "LifecycleRuleAndOperatorTypeDef",
    {
        "Prefix": str,
        "Tags": List[S3TagTypeDef],
    },
    total=False,
)

PutJobTaggingRequestRequestTypeDef = TypedDict(
    "PutJobTaggingRequestRequestTypeDef",
    {
        "AccountId": str,
        "JobId": str,
        "Tags": Sequence[S3TagTypeDef],
    },
)

S3SetObjectTaggingOperationTypeDef = TypedDict(
    "S3SetObjectTaggingOperationTypeDef",
    {
        "TagSet": Sequence[S3TagTypeDef],
    },
    total=False,
)

TaggingTypeDef = TypedDict(
    "TaggingTypeDef",
    {
        "TagSet": Sequence[S3TagTypeDef],
    },
)

_RequiredCreateMultiRegionAccessPointInputTypeDef = TypedDict(
    "_RequiredCreateMultiRegionAccessPointInputTypeDef",
    {
        "Name": str,
        "Regions": Sequence[RegionTypeDef],
    },
)
_OptionalCreateMultiRegionAccessPointInputTypeDef = TypedDict(
    "_OptionalCreateMultiRegionAccessPointInputTypeDef",
    {
        "PublicAccessBlock": PublicAccessBlockConfigurationTypeDef,
    },
    total=False,
)


class CreateMultiRegionAccessPointInputTypeDef(
    _RequiredCreateMultiRegionAccessPointInputTypeDef,
    _OptionalCreateMultiRegionAccessPointInputTypeDef,
):
    pass


GeneratedManifestEncryptionTypeDef = TypedDict(
    "GeneratedManifestEncryptionTypeDef",
    {
        "SSES3": Mapping[str, Any],
        "SSEKMS": SSEKMSEncryptionTypeDef,
    },
    total=False,
)

GetAccessPointPolicyStatusForObjectLambdaResultTypeDef = TypedDict(
    "GetAccessPointPolicyStatusForObjectLambdaResultTypeDef",
    {
        "PolicyStatus": PolicyStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessPointPolicyStatusResultTypeDef = TypedDict(
    "GetAccessPointPolicyStatusResultTypeDef",
    {
        "PolicyStatus": PolicyStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMultiRegionAccessPointPolicyStatusResultTypeDef = TypedDict(
    "GetMultiRegionAccessPointPolicyStatusResultTypeDef",
    {
        "Established": PolicyStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetStorageLensConfigurationTaggingResultTypeDef = TypedDict(
    "GetStorageLensConfigurationTaggingResultTypeDef",
    {
        "Tags": List[StorageLensTagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutStorageLensConfigurationTaggingRequestRequestTypeDef = TypedDict(
    "PutStorageLensConfigurationTaggingRequestRequestTypeDef",
    {
        "ConfigId": str,
        "AccountId": str,
        "Tags": Sequence[StorageLensTagTypeDef],
    },
)

S3GeneratedManifestDescriptorTypeDef = TypedDict(
    "S3GeneratedManifestDescriptorTypeDef",
    {
        "Format": Literal["S3InventoryReport_CSV_20211130"],
        "Location": JobManifestLocationTypeDef,
    },
    total=False,
)

JobManifestTypeDef = TypedDict(
    "JobManifestTypeDef",
    {
        "Spec": JobManifestSpecTypeDef,
        "Location": JobManifestLocationTypeDef,
    },
)

JobProgressSummaryTypeDef = TypedDict(
    "JobProgressSummaryTypeDef",
    {
        "TotalNumberOfTasks": int,
        "NumberOfTasksSucceeded": int,
        "NumberOfTasksFailed": int,
        "Timers": JobTimersTypeDef,
    },
    total=False,
)

_RequiredListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef = TypedDict(
    "_RequiredListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef = TypedDict(
    "_OptionalListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef(
    _RequiredListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef,
    _OptionalListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef,
):
    pass


ListAccessPointsForObjectLambdaResultTypeDef = TypedDict(
    "ListAccessPointsForObjectLambdaResultTypeDef",
    {
        "ObjectLambdaAccessPointList": List[ObjectLambdaAccessPointTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRegionalBucketsResultTypeDef = TypedDict(
    "ListRegionalBucketsResultTypeDef",
    {
        "RegionalBucketList": List[RegionalBucketTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStorageLensConfigurationsResultTypeDef = TypedDict(
    "ListStorageLensConfigurationsResultTypeDef",
    {
        "NextToken": str,
        "StorageLensConfigurationList": List[ListStorageLensConfigurationEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MultiRegionAccessPointPolicyDocumentTypeDef = TypedDict(
    "MultiRegionAccessPointPolicyDocumentTypeDef",
    {
        "Established": EstablishedMultiRegionAccessPointPolicyTypeDef,
        "Proposed": ProposedMultiRegionAccessPointPolicyTypeDef,
    },
    total=False,
)

MultiRegionAccessPointsAsyncResponseTypeDef = TypedDict(
    "MultiRegionAccessPointsAsyncResponseTypeDef",
    {
        "Regions": List[MultiRegionAccessPointRegionalResponseTypeDef],
    },
    total=False,
)

MultiRegionAccessPointReportTypeDef = TypedDict(
    "MultiRegionAccessPointReportTypeDef",
    {
        "Name": str,
        "Alias": str,
        "CreatedAt": datetime,
        "PublicAccessBlock": PublicAccessBlockConfigurationTypeDef,
        "Status": MultiRegionAccessPointStatusType,
        "Regions": List[RegionReportTypeDef],
    },
    total=False,
)

PrefixLevelStorageMetricsTypeDef = TypedDict(
    "PrefixLevelStorageMetricsTypeDef",
    {
        "IsEnabled": bool,
        "SelectionCriteria": SelectionCriteriaTypeDef,
    },
    total=False,
)

S3GrantTypeDef = TypedDict(
    "S3GrantTypeDef",
    {
        "Grantee": S3GranteeTypeDef,
        "Permission": S3PermissionType,
    },
    total=False,
)

S3SetObjectLegalHoldOperationTypeDef = TypedDict(
    "S3SetObjectLegalHoldOperationTypeDef",
    {
        "LegalHold": S3ObjectLockLegalHoldTypeDef,
    },
)

_RequiredS3SetObjectRetentionOperationTypeDef = TypedDict(
    "_RequiredS3SetObjectRetentionOperationTypeDef",
    {
        "Retention": S3RetentionTypeDef,
    },
)
_OptionalS3SetObjectRetentionOperationTypeDef = TypedDict(
    "_OptionalS3SetObjectRetentionOperationTypeDef",
    {
        "BypassGovernanceRetention": bool,
    },
    total=False,
)


class S3SetObjectRetentionOperationTypeDef(
    _RequiredS3SetObjectRetentionOperationTypeDef, _OptionalS3SetObjectRetentionOperationTypeDef
):
    pass


StorageLensDataExportEncryptionTypeDef = TypedDict(
    "StorageLensDataExportEncryptionTypeDef",
    {
        "SSES3": Dict[str, Any],
        "SSEKMS": SSEKMSTypeDef,
    },
    total=False,
)

ListAccessPointsResultTypeDef = TypedDict(
    "ListAccessPointsResultTypeDef",
    {
        "AccessPointList": List[AccessPointTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ObjectLambdaTransformationConfigurationTypeDef = TypedDict(
    "ObjectLambdaTransformationConfigurationTypeDef",
    {
        "Actions": Sequence[Literal["GetObject"]],
        "ContentTransformation": ObjectLambdaContentTransformationTypeDef,
    },
)

LifecycleRuleFilterTypeDef = TypedDict(
    "LifecycleRuleFilterTypeDef",
    {
        "Prefix": str,
        "Tag": S3TagTypeDef,
        "And": LifecycleRuleAndOperatorTypeDef,
    },
    total=False,
)

PutBucketTaggingRequestRequestTypeDef = TypedDict(
    "PutBucketTaggingRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
        "Tagging": TaggingTypeDef,
    },
)

AsyncRequestParametersTypeDef = TypedDict(
    "AsyncRequestParametersTypeDef",
    {
        "CreateMultiRegionAccessPointRequest": CreateMultiRegionAccessPointInputTypeDef,
        "DeleteMultiRegionAccessPointRequest": DeleteMultiRegionAccessPointInputTypeDef,
        "PutMultiRegionAccessPointPolicyRequest": PutMultiRegionAccessPointPolicyInputTypeDef,
    },
    total=False,
)

CreateMultiRegionAccessPointRequestRequestTypeDef = TypedDict(
    "CreateMultiRegionAccessPointRequestRequestTypeDef",
    {
        "AccountId": str,
        "ClientToken": str,
        "Details": CreateMultiRegionAccessPointInputTypeDef,
    },
)

_RequiredS3ManifestOutputLocationTypeDef = TypedDict(
    "_RequiredS3ManifestOutputLocationTypeDef",
    {
        "Bucket": str,
        "ManifestFormat": Literal["S3InventoryReport_CSV_20211130"],
    },
)
_OptionalS3ManifestOutputLocationTypeDef = TypedDict(
    "_OptionalS3ManifestOutputLocationTypeDef",
    {
        "ExpectedManifestBucketOwner": str,
        "ManifestPrefix": str,
        "ManifestEncryption": GeneratedManifestEncryptionTypeDef,
    },
    total=False,
)


class S3ManifestOutputLocationTypeDef(
    _RequiredS3ManifestOutputLocationTypeDef, _OptionalS3ManifestOutputLocationTypeDef
):
    pass


JobListDescriptorTypeDef = TypedDict(
    "JobListDescriptorTypeDef",
    {
        "JobId": str,
        "Description": str,
        "Operation": OperationNameType,
        "Priority": int,
        "Status": JobStatusType,
        "CreationTime": datetime,
        "TerminationDate": datetime,
        "ProgressSummary": JobProgressSummaryTypeDef,
    },
    total=False,
)

GetMultiRegionAccessPointPolicyResultTypeDef = TypedDict(
    "GetMultiRegionAccessPointPolicyResultTypeDef",
    {
        "Policy": MultiRegionAccessPointPolicyDocumentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AsyncResponseDetailsTypeDef = TypedDict(
    "AsyncResponseDetailsTypeDef",
    {
        "MultiRegionAccessPointDetails": MultiRegionAccessPointsAsyncResponseTypeDef,
        "ErrorDetails": AsyncErrorDetailsTypeDef,
    },
    total=False,
)

GetMultiRegionAccessPointResultTypeDef = TypedDict(
    "GetMultiRegionAccessPointResultTypeDef",
    {
        "AccessPoint": MultiRegionAccessPointReportTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMultiRegionAccessPointsResultTypeDef = TypedDict(
    "ListMultiRegionAccessPointsResultTypeDef",
    {
        "AccessPoints": List[MultiRegionAccessPointReportTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PrefixLevelTypeDef = TypedDict(
    "PrefixLevelTypeDef",
    {
        "StorageMetrics": PrefixLevelStorageMetricsTypeDef,
    },
)

_RequiredS3AccessControlListTypeDef = TypedDict(
    "_RequiredS3AccessControlListTypeDef",
    {
        "Owner": S3ObjectOwnerTypeDef,
    },
)
_OptionalS3AccessControlListTypeDef = TypedDict(
    "_OptionalS3AccessControlListTypeDef",
    {
        "Grants": Sequence[S3GrantTypeDef],
    },
    total=False,
)


class S3AccessControlListTypeDef(
    _RequiredS3AccessControlListTypeDef, _OptionalS3AccessControlListTypeDef
):
    pass


S3CopyObjectOperationTypeDef = TypedDict(
    "S3CopyObjectOperationTypeDef",
    {
        "TargetResource": str,
        "CannedAccessControlList": S3CannedAccessControlListType,
        "AccessControlGrants": Sequence[S3GrantTypeDef],
        "MetadataDirective": S3MetadataDirectiveType,
        "ModifiedSinceConstraint": Union[datetime, str],
        "NewObjectMetadata": S3ObjectMetadataTypeDef,
        "NewObjectTagging": Sequence[S3TagTypeDef],
        "RedirectLocation": str,
        "RequesterPays": bool,
        "StorageClass": S3StorageClassType,
        "UnModifiedSinceConstraint": Union[datetime, str],
        "SSEAwsKmsKeyId": str,
        "TargetKeyPrefix": str,
        "ObjectLockLegalHoldStatus": S3ObjectLockLegalHoldStatusType,
        "ObjectLockMode": S3ObjectLockModeType,
        "ObjectLockRetainUntilDate": Union[datetime, str],
        "BucketKeyEnabled": bool,
        "ChecksumAlgorithm": S3ChecksumAlgorithmType,
    },
    total=False,
)

_RequiredS3BucketDestinationTypeDef = TypedDict(
    "_RequiredS3BucketDestinationTypeDef",
    {
        "Format": FormatType,
        "OutputSchemaVersion": Literal["V_1"],
        "AccountId": str,
        "Arn": str,
    },
)
_OptionalS3BucketDestinationTypeDef = TypedDict(
    "_OptionalS3BucketDestinationTypeDef",
    {
        "Prefix": str,
        "Encryption": StorageLensDataExportEncryptionTypeDef,
    },
    total=False,
)


class S3BucketDestinationTypeDef(
    _RequiredS3BucketDestinationTypeDef, _OptionalS3BucketDestinationTypeDef
):
    pass


_RequiredObjectLambdaConfigurationTypeDef = TypedDict(
    "_RequiredObjectLambdaConfigurationTypeDef",
    {
        "SupportingAccessPoint": str,
        "TransformationConfigurations": Sequence[ObjectLambdaTransformationConfigurationTypeDef],
    },
)
_OptionalObjectLambdaConfigurationTypeDef = TypedDict(
    "_OptionalObjectLambdaConfigurationTypeDef",
    {
        "CloudWatchMetricsEnabled": bool,
        "AllowedFeatures": Sequence[ObjectLambdaAllowedFeatureType],
    },
    total=False,
)


class ObjectLambdaConfigurationTypeDef(
    _RequiredObjectLambdaConfigurationTypeDef, _OptionalObjectLambdaConfigurationTypeDef
):
    pass


_RequiredLifecycleRuleTypeDef = TypedDict(
    "_RequiredLifecycleRuleTypeDef",
    {
        "Status": ExpirationStatusType,
    },
)
_OptionalLifecycleRuleTypeDef = TypedDict(
    "_OptionalLifecycleRuleTypeDef",
    {
        "Expiration": LifecycleExpirationTypeDef,
        "ID": str,
        "Filter": LifecycleRuleFilterTypeDef,
        "Transitions": List[TransitionTypeDef],
        "NoncurrentVersionTransitions": List[NoncurrentVersionTransitionTypeDef],
        "NoncurrentVersionExpiration": NoncurrentVersionExpirationTypeDef,
        "AbortIncompleteMultipartUpload": AbortIncompleteMultipartUploadTypeDef,
    },
    total=False,
)


class LifecycleRuleTypeDef(_RequiredLifecycleRuleTypeDef, _OptionalLifecycleRuleTypeDef):
    pass


_RequiredS3JobManifestGeneratorTypeDef = TypedDict(
    "_RequiredS3JobManifestGeneratorTypeDef",
    {
        "SourceBucket": str,
        "EnableManifestOutput": bool,
    },
)
_OptionalS3JobManifestGeneratorTypeDef = TypedDict(
    "_OptionalS3JobManifestGeneratorTypeDef",
    {
        "ExpectedBucketOwner": str,
        "ManifestOutputLocation": S3ManifestOutputLocationTypeDef,
        "Filter": JobManifestGeneratorFilterTypeDef,
    },
    total=False,
)


class S3JobManifestGeneratorTypeDef(
    _RequiredS3JobManifestGeneratorTypeDef, _OptionalS3JobManifestGeneratorTypeDef
):
    pass


ListJobsResultTypeDef = TypedDict(
    "ListJobsResultTypeDef",
    {
        "NextToken": str,
        "Jobs": List[JobListDescriptorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AsyncOperationTypeDef = TypedDict(
    "AsyncOperationTypeDef",
    {
        "CreationTime": datetime,
        "Operation": AsyncOperationNameType,
        "RequestTokenARN": str,
        "RequestParameters": AsyncRequestParametersTypeDef,
        "RequestStatus": str,
        "ResponseDetails": AsyncResponseDetailsTypeDef,
    },
    total=False,
)

BucketLevelTypeDef = TypedDict(
    "BucketLevelTypeDef",
    {
        "ActivityMetrics": ActivityMetricsTypeDef,
        "PrefixLevel": PrefixLevelTypeDef,
    },
    total=False,
)

S3AccessControlPolicyTypeDef = TypedDict(
    "S3AccessControlPolicyTypeDef",
    {
        "AccessControlList": S3AccessControlListTypeDef,
        "CannedAccessControlList": S3CannedAccessControlListType,
    },
    total=False,
)

StorageLensDataExportTypeDef = TypedDict(
    "StorageLensDataExportTypeDef",
    {
        "S3BucketDestination": S3BucketDestinationTypeDef,
        "CloudWatchMetrics": CloudWatchMetricsTypeDef,
    },
    total=False,
)

CreateAccessPointForObjectLambdaRequestRequestTypeDef = TypedDict(
    "CreateAccessPointForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
        "Configuration": ObjectLambdaConfigurationTypeDef,
    },
)

GetAccessPointConfigurationForObjectLambdaResultTypeDef = TypedDict(
    "GetAccessPointConfigurationForObjectLambdaResultTypeDef",
    {
        "Configuration": ObjectLambdaConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutAccessPointConfigurationForObjectLambdaRequestRequestTypeDef = TypedDict(
    "PutAccessPointConfigurationForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
        "Configuration": ObjectLambdaConfigurationTypeDef,
    },
)

GetBucketLifecycleConfigurationResultTypeDef = TypedDict(
    "GetBucketLifecycleConfigurationResultTypeDef",
    {
        "Rules": List[LifecycleRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LifecycleConfigurationTypeDef = TypedDict(
    "LifecycleConfigurationTypeDef",
    {
        "Rules": Sequence[LifecycleRuleTypeDef],
    },
    total=False,
)

JobManifestGeneratorTypeDef = TypedDict(
    "JobManifestGeneratorTypeDef",
    {
        "S3JobManifestGenerator": S3JobManifestGeneratorTypeDef,
    },
    total=False,
)

DescribeMultiRegionAccessPointOperationResultTypeDef = TypedDict(
    "DescribeMultiRegionAccessPointOperationResultTypeDef",
    {
        "AsyncOperation": AsyncOperationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAccountLevelTypeDef = TypedDict(
    "_RequiredAccountLevelTypeDef",
    {
        "BucketLevel": BucketLevelTypeDef,
    },
)
_OptionalAccountLevelTypeDef = TypedDict(
    "_OptionalAccountLevelTypeDef",
    {
        "ActivityMetrics": ActivityMetricsTypeDef,
    },
    total=False,
)


class AccountLevelTypeDef(_RequiredAccountLevelTypeDef, _OptionalAccountLevelTypeDef):
    pass


S3SetObjectAclOperationTypeDef = TypedDict(
    "S3SetObjectAclOperationTypeDef",
    {
        "AccessControlPolicy": S3AccessControlPolicyTypeDef,
    },
    total=False,
)

_RequiredPutBucketLifecycleConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutBucketLifecycleConfigurationRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)
_OptionalPutBucketLifecycleConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutBucketLifecycleConfigurationRequestRequestTypeDef",
    {
        "LifecycleConfiguration": LifecycleConfigurationTypeDef,
    },
    total=False,
)


class PutBucketLifecycleConfigurationRequestRequestTypeDef(
    _RequiredPutBucketLifecycleConfigurationRequestRequestTypeDef,
    _OptionalPutBucketLifecycleConfigurationRequestRequestTypeDef,
):
    pass


_RequiredStorageLensConfigurationTypeDef = TypedDict(
    "_RequiredStorageLensConfigurationTypeDef",
    {
        "Id": str,
        "AccountLevel": AccountLevelTypeDef,
        "IsEnabled": bool,
    },
)
_OptionalStorageLensConfigurationTypeDef = TypedDict(
    "_OptionalStorageLensConfigurationTypeDef",
    {
        "Include": IncludeTypeDef,
        "Exclude": ExcludeTypeDef,
        "DataExport": StorageLensDataExportTypeDef,
        "AwsOrg": StorageLensAwsOrgTypeDef,
        "StorageLensArn": str,
    },
    total=False,
)


class StorageLensConfigurationTypeDef(
    _RequiredStorageLensConfigurationTypeDef, _OptionalStorageLensConfigurationTypeDef
):
    pass


JobOperationTypeDef = TypedDict(
    "JobOperationTypeDef",
    {
        "LambdaInvoke": LambdaInvokeOperationTypeDef,
        "S3PutObjectCopy": S3CopyObjectOperationTypeDef,
        "S3PutObjectAcl": S3SetObjectAclOperationTypeDef,
        "S3PutObjectTagging": S3SetObjectTaggingOperationTypeDef,
        "S3DeleteObjectTagging": Mapping[str, Any],
        "S3InitiateRestoreObject": S3InitiateRestoreObjectOperationTypeDef,
        "S3PutObjectLegalHold": S3SetObjectLegalHoldOperationTypeDef,
        "S3PutObjectRetention": S3SetObjectRetentionOperationTypeDef,
        "S3ReplicateObject": Mapping[str, Any],
    },
    total=False,
)

GetStorageLensConfigurationResultTypeDef = TypedDict(
    "GetStorageLensConfigurationResultTypeDef",
    {
        "StorageLensConfiguration": StorageLensConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutStorageLensConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutStorageLensConfigurationRequestRequestTypeDef",
    {
        "ConfigId": str,
        "AccountId": str,
        "StorageLensConfiguration": StorageLensConfigurationTypeDef,
    },
)
_OptionalPutStorageLensConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutStorageLensConfigurationRequestRequestTypeDef",
    {
        "Tags": Sequence[StorageLensTagTypeDef],
    },
    total=False,
)


class PutStorageLensConfigurationRequestRequestTypeDef(
    _RequiredPutStorageLensConfigurationRequestRequestTypeDef,
    _OptionalPutStorageLensConfigurationRequestRequestTypeDef,
):
    pass


_RequiredCreateJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateJobRequestRequestTypeDef",
    {
        "AccountId": str,
        "Operation": JobOperationTypeDef,
        "Report": JobReportTypeDef,
        "ClientRequestToken": str,
        "Priority": int,
        "RoleArn": str,
    },
)
_OptionalCreateJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateJobRequestRequestTypeDef",
    {
        "ConfirmationRequired": bool,
        "Manifest": JobManifestTypeDef,
        "Description": str,
        "Tags": Sequence[S3TagTypeDef],
        "ManifestGenerator": JobManifestGeneratorTypeDef,
    },
    total=False,
)


class CreateJobRequestRequestTypeDef(
    _RequiredCreateJobRequestRequestTypeDef, _OptionalCreateJobRequestRequestTypeDef
):
    pass


JobDescriptorTypeDef = TypedDict(
    "JobDescriptorTypeDef",
    {
        "JobId": str,
        "ConfirmationRequired": bool,
        "Description": str,
        "JobArn": str,
        "Status": JobStatusType,
        "Manifest": JobManifestTypeDef,
        "Operation": JobOperationTypeDef,
        "Priority": int,
        "ProgressSummary": JobProgressSummaryTypeDef,
        "StatusUpdateReason": str,
        "FailureReasons": List[JobFailureTypeDef],
        "Report": JobReportTypeDef,
        "CreationTime": datetime,
        "TerminationDate": datetime,
        "RoleArn": str,
        "SuspendedDate": datetime,
        "SuspendedCause": str,
        "ManifestGenerator": JobManifestGeneratorTypeDef,
        "GeneratedManifestDescriptor": S3GeneratedManifestDescriptorTypeDef,
    },
    total=False,
)

DescribeJobResultTypeDef = TypedDict(
    "DescribeJobResultTypeDef",
    {
        "Job": JobDescriptorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
