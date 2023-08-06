"""
Type annotations for iotsitewise service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotsitewise.type_defs import AggregatesTypeDef

    data: AggregatesTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AggregateTypeType,
    AssetModelStateType,
    AssetStateType,
    AuthModeType,
    BatchEntryCompletionStatusType,
    BatchGetAssetPropertyAggregatesErrorCodeType,
    BatchGetAssetPropertyValueErrorCodeType,
    BatchGetAssetPropertyValueHistoryErrorCodeType,
    BatchPutAssetPropertyValueErrorCodeType,
    CapabilitySyncStatusType,
    ComputeLocationType,
    ConfigurationStateType,
    DetailedErrorCodeType,
    DisassociatedDataStorageStateType,
    EncryptionTypeType,
    ErrorCodeType,
    ForwardingConfigStateType,
    IdentityTypeType,
    ListAssetsFilterType,
    ListTimeSeriesTypeType,
    LoggingLevelType,
    MonitorErrorCodeType,
    PermissionType,
    PortalStateType,
    PropertyDataTypeType,
    PropertyNotificationStateType,
    QualityType,
    ResourceTypeType,
    StorageTypeType,
    TimeOrderingType,
    TraversalDirectionType,
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
    "AggregatesTypeDef",
    "AlarmsTypeDef",
    "AssetErrorDetailsTypeDef",
    "AssetHierarchyInfoTypeDef",
    "AssetHierarchyTypeDef",
    "AssetModelHierarchyDefinitionTypeDef",
    "AssetModelHierarchyTypeDef",
    "PropertyNotificationTypeDef",
    "TimeInNanosTypeDef",
    "VariantTypeDef",
    "AssociateAssetsRequestRequestTypeDef",
    "AssociateTimeSeriesToAssetPropertyRequestRequestTypeDef",
    "AttributeTypeDef",
    "BatchAssociateProjectAssetsRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "BatchDisassociateProjectAssetsRequestRequestTypeDef",
    "BatchGetAssetPropertyAggregatesEntryTypeDef",
    "BatchGetAssetPropertyAggregatesErrorEntryTypeDef",
    "BatchGetAssetPropertyAggregatesErrorInfoTypeDef",
    "BatchGetAssetPropertyValueEntryTypeDef",
    "BatchGetAssetPropertyValueErrorEntryTypeDef",
    "BatchGetAssetPropertyValueErrorInfoTypeDef",
    "BatchGetAssetPropertyValueHistoryEntryTypeDef",
    "BatchGetAssetPropertyValueHistoryErrorEntryTypeDef",
    "BatchGetAssetPropertyValueHistoryErrorInfoTypeDef",
    "ConfigurationErrorDetailsTypeDef",
    "CreateAssetRequestRequestTypeDef",
    "CreateDashboardRequestRequestTypeDef",
    "ImageFileTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "CustomerManagedS3StorageTypeDef",
    "DashboardSummaryTypeDef",
    "DeleteAccessPolicyRequestRequestTypeDef",
    "DeleteAssetModelRequestRequestTypeDef",
    "DeleteAssetRequestRequestTypeDef",
    "DeleteDashboardRequestRequestTypeDef",
    "DeleteGatewayRequestRequestTypeDef",
    "DeletePortalRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteTimeSeriesRequestRequestTypeDef",
    "DescribeAccessPolicyRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeAssetModelRequestRequestTypeDef",
    "DescribeAssetPropertyRequestRequestTypeDef",
    "DescribeAssetRequestRequestTypeDef",
    "DescribeDashboardRequestRequestTypeDef",
    "DescribeGatewayCapabilityConfigurationRequestRequestTypeDef",
    "DescribeGatewayRequestRequestTypeDef",
    "GatewayCapabilitySummaryTypeDef",
    "LoggingOptionsTypeDef",
    "DescribePortalRequestRequestTypeDef",
    "ImageLocationTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "RetentionPeriodTypeDef",
    "DescribeTimeSeriesRequestRequestTypeDef",
    "DetailedErrorTypeDef",
    "DisassociateAssetsRequestRequestTypeDef",
    "DisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef",
    "VariableValueTypeDef",
    "ForwardingConfigTypeDef",
    "GreengrassTypeDef",
    "GreengrassV2TypeDef",
    "PaginatorConfigTypeDef",
    "GetAssetPropertyAggregatesRequestRequestTypeDef",
    "GetAssetPropertyValueHistoryRequestRequestTypeDef",
    "GetAssetPropertyValueRequestRequestTypeDef",
    "GetInterpolatedAssetPropertyValuesRequestRequestTypeDef",
    "GroupIdentityTypeDef",
    "IAMRoleIdentityTypeDef",
    "IAMUserIdentityTypeDef",
    "UserIdentityTypeDef",
    "ListAccessPoliciesRequestRequestTypeDef",
    "ListAssetModelsRequestRequestTypeDef",
    "ListAssetRelationshipsRequestRequestTypeDef",
    "ListAssetsRequestRequestTypeDef",
    "ListAssociatedAssetsRequestRequestTypeDef",
    "ListDashboardsRequestRequestTypeDef",
    "ListGatewaysRequestRequestTypeDef",
    "ListPortalsRequestRequestTypeDef",
    "ListProjectAssetsRequestRequestTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ProjectSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTimeSeriesRequestRequestTypeDef",
    "TimeSeriesSummaryTypeDef",
    "MetricProcessingConfigTypeDef",
    "TumblingWindowTypeDef",
    "MonitorErrorDetailsTypeDef",
    "PortalResourceTypeDef",
    "ProjectResourceTypeDef",
    "PutDefaultEncryptionConfigurationRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAssetPropertyRequestRequestTypeDef",
    "UpdateAssetRequestRequestTypeDef",
    "UpdateDashboardRequestRequestTypeDef",
    "UpdateGatewayCapabilityConfigurationRequestRequestTypeDef",
    "UpdateGatewayRequestRequestTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "AggregatedValueTypeDef",
    "AssetRelationshipSummaryTypeDef",
    "AssetPropertyTypeDef",
    "BatchPutAssetPropertyErrorTypeDef",
    "AssetPropertyValueTypeDef",
    "InterpolatedAssetPropertyValueTypeDef",
    "BatchAssociateProjectAssetsResponseTypeDef",
    "BatchDisassociateProjectAssetsResponseTypeDef",
    "CreateAccessPolicyResponseTypeDef",
    "CreateDashboardResponseTypeDef",
    "CreateGatewayResponseTypeDef",
    "CreateProjectResponseTypeDef",
    "DescribeDashboardResponseTypeDef",
    "DescribeGatewayCapabilityConfigurationResponseTypeDef",
    "DescribeProjectResponseTypeDef",
    "DescribeTimeSeriesResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListProjectAssetsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateGatewayCapabilityConfigurationResponseTypeDef",
    "BatchGetAssetPropertyAggregatesRequestRequestTypeDef",
    "BatchGetAssetPropertyAggregatesSkippedEntryTypeDef",
    "BatchGetAssetPropertyValueRequestRequestTypeDef",
    "BatchGetAssetPropertyValueSkippedEntryTypeDef",
    "BatchGetAssetPropertyValueHistoryRequestRequestTypeDef",
    "BatchGetAssetPropertyValueHistorySkippedEntryTypeDef",
    "ConfigurationStatusTypeDef",
    "CreatePortalRequestRequestTypeDef",
    "ImageTypeDef",
    "MultiLayerStorageTypeDef",
    "ListDashboardsResponseTypeDef",
    "DescribeAssetModelRequestAssetModelActiveWaitTypeDef",
    "DescribeAssetModelRequestAssetModelNotExistsWaitTypeDef",
    "DescribeAssetRequestAssetActiveWaitTypeDef",
    "DescribeAssetRequestAssetNotExistsWaitTypeDef",
    "DescribePortalRequestPortalActiveWaitTypeDef",
    "DescribePortalRequestPortalNotExistsWaitTypeDef",
    "DescribeLoggingOptionsResponseTypeDef",
    "PutLoggingOptionsRequestRequestTypeDef",
    "ErrorDetailsTypeDef",
    "ExpressionVariableTypeDef",
    "MeasurementProcessingConfigTypeDef",
    "TransformProcessingConfigTypeDef",
    "GatewayPlatformTypeDef",
    "GetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef",
    "GetAssetPropertyValueHistoryRequestGetAssetPropertyValueHistoryPaginateTypeDef",
    "GetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef",
    "ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef",
    "ListAssetModelsRequestListAssetModelsPaginateTypeDef",
    "ListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef",
    "ListAssetsRequestListAssetsPaginateTypeDef",
    "ListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef",
    "ListDashboardsRequestListDashboardsPaginateTypeDef",
    "ListGatewaysRequestListGatewaysPaginateTypeDef",
    "ListPortalsRequestListPortalsPaginateTypeDef",
    "ListProjectAssetsRequestListProjectAssetsPaginateTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListTimeSeriesRequestListTimeSeriesPaginateTypeDef",
    "IdentityTypeDef",
    "ListProjectsResponseTypeDef",
    "ListTimeSeriesResponseTypeDef",
    "MetricWindowTypeDef",
    "PortalStatusTypeDef",
    "ResourceTypeDef",
    "BatchGetAssetPropertyAggregatesSuccessEntryTypeDef",
    "GetAssetPropertyAggregatesResponseTypeDef",
    "ListAssetRelationshipsResponseTypeDef",
    "AssetCompositeModelTypeDef",
    "BatchPutAssetPropertyErrorEntryTypeDef",
    "BatchGetAssetPropertyValueHistorySuccessEntryTypeDef",
    "BatchGetAssetPropertyValueSuccessEntryTypeDef",
    "GetAssetPropertyValueHistoryResponseTypeDef",
    "GetAssetPropertyValueResponseTypeDef",
    "PutAssetPropertyValueEntryTypeDef",
    "GetInterpolatedAssetPropertyValuesResponseTypeDef",
    "DescribeDefaultEncryptionConfigurationResponseTypeDef",
    "PutDefaultEncryptionConfigurationResponseTypeDef",
    "UpdatePortalRequestRequestTypeDef",
    "DescribeStorageConfigurationResponseTypeDef",
    "PutStorageConfigurationRequestRequestTypeDef",
    "PutStorageConfigurationResponseTypeDef",
    "AssetModelStatusTypeDef",
    "AssetStatusTypeDef",
    "MeasurementTypeDef",
    "TransformTypeDef",
    "CreateGatewayRequestRequestTypeDef",
    "DescribeGatewayResponseTypeDef",
    "GatewaySummaryTypeDef",
    "MetricTypeDef",
    "CreatePortalResponseTypeDef",
    "DeletePortalResponseTypeDef",
    "DescribePortalResponseTypeDef",
    "PortalSummaryTypeDef",
    "UpdatePortalResponseTypeDef",
    "AccessPolicySummaryTypeDef",
    "CreateAccessPolicyRequestRequestTypeDef",
    "DescribeAccessPolicyResponseTypeDef",
    "UpdateAccessPolicyRequestRequestTypeDef",
    "BatchGetAssetPropertyAggregatesResponseTypeDef",
    "BatchPutAssetPropertyValueResponseTypeDef",
    "BatchGetAssetPropertyValueHistoryResponseTypeDef",
    "BatchGetAssetPropertyValueResponseTypeDef",
    "BatchPutAssetPropertyValueRequestRequestTypeDef",
    "AssetModelSummaryTypeDef",
    "CreateAssetModelResponseTypeDef",
    "DeleteAssetModelResponseTypeDef",
    "UpdateAssetModelResponseTypeDef",
    "AssetSummaryTypeDef",
    "AssociatedAssetsSummaryTypeDef",
    "CreateAssetResponseTypeDef",
    "DeleteAssetResponseTypeDef",
    "DescribeAssetResponseTypeDef",
    "UpdateAssetResponseTypeDef",
    "ListGatewaysResponseTypeDef",
    "PropertyTypeTypeDef",
    "ListPortalsResponseTypeDef",
    "ListAccessPoliciesResponseTypeDef",
    "ListAssetModelsResponseTypeDef",
    "ListAssetsResponseTypeDef",
    "ListAssociatedAssetsResponseTypeDef",
    "AssetModelPropertyDefinitionTypeDef",
    "AssetModelPropertyTypeDef",
    "PropertyTypeDef",
    "AssetModelCompositeModelDefinitionTypeDef",
    "AssetModelCompositeModelTypeDef",
    "CompositeModelPropertyTypeDef",
    "CreateAssetModelRequestRequestTypeDef",
    "DescribeAssetModelResponseTypeDef",
    "UpdateAssetModelRequestRequestTypeDef",
    "DescribeAssetPropertyResponseTypeDef",
)

AggregatesTypeDef = TypedDict(
    "AggregatesTypeDef",
    {
        "average": float,
        "count": float,
        "maximum": float,
        "minimum": float,
        "sum": float,
        "standardDeviation": float,
    },
    total=False,
)

_RequiredAlarmsTypeDef = TypedDict(
    "_RequiredAlarmsTypeDef",
    {
        "alarmRoleArn": str,
    },
)
_OptionalAlarmsTypeDef = TypedDict(
    "_OptionalAlarmsTypeDef",
    {
        "notificationLambdaArn": str,
    },
    total=False,
)


class AlarmsTypeDef(_RequiredAlarmsTypeDef, _OptionalAlarmsTypeDef):
    pass


AssetErrorDetailsTypeDef = TypedDict(
    "AssetErrorDetailsTypeDef",
    {
        "assetId": str,
        "code": Literal["INTERNAL_FAILURE"],
        "message": str,
    },
)

AssetHierarchyInfoTypeDef = TypedDict(
    "AssetHierarchyInfoTypeDef",
    {
        "parentAssetId": str,
        "childAssetId": str,
    },
    total=False,
)

_RequiredAssetHierarchyTypeDef = TypedDict(
    "_RequiredAssetHierarchyTypeDef",
    {
        "name": str,
    },
)
_OptionalAssetHierarchyTypeDef = TypedDict(
    "_OptionalAssetHierarchyTypeDef",
    {
        "id": str,
    },
    total=False,
)


class AssetHierarchyTypeDef(_RequiredAssetHierarchyTypeDef, _OptionalAssetHierarchyTypeDef):
    pass


AssetModelHierarchyDefinitionTypeDef = TypedDict(
    "AssetModelHierarchyDefinitionTypeDef",
    {
        "name": str,
        "childAssetModelId": str,
    },
)

_RequiredAssetModelHierarchyTypeDef = TypedDict(
    "_RequiredAssetModelHierarchyTypeDef",
    {
        "name": str,
        "childAssetModelId": str,
    },
)
_OptionalAssetModelHierarchyTypeDef = TypedDict(
    "_OptionalAssetModelHierarchyTypeDef",
    {
        "id": str,
    },
    total=False,
)


class AssetModelHierarchyTypeDef(
    _RequiredAssetModelHierarchyTypeDef, _OptionalAssetModelHierarchyTypeDef
):
    pass


PropertyNotificationTypeDef = TypedDict(
    "PropertyNotificationTypeDef",
    {
        "topic": str,
        "state": PropertyNotificationStateType,
    },
)

_RequiredTimeInNanosTypeDef = TypedDict(
    "_RequiredTimeInNanosTypeDef",
    {
        "timeInSeconds": int,
    },
)
_OptionalTimeInNanosTypeDef = TypedDict(
    "_OptionalTimeInNanosTypeDef",
    {
        "offsetInNanos": int,
    },
    total=False,
)


class TimeInNanosTypeDef(_RequiredTimeInNanosTypeDef, _OptionalTimeInNanosTypeDef):
    pass


VariantTypeDef = TypedDict(
    "VariantTypeDef",
    {
        "stringValue": str,
        "integerValue": int,
        "doubleValue": float,
        "booleanValue": bool,
    },
    total=False,
)

_RequiredAssociateAssetsRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateAssetsRequestRequestTypeDef",
    {
        "assetId": str,
        "hierarchyId": str,
        "childAssetId": str,
    },
)
_OptionalAssociateAssetsRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateAssetsRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class AssociateAssetsRequestRequestTypeDef(
    _RequiredAssociateAssetsRequestRequestTypeDef, _OptionalAssociateAssetsRequestRequestTypeDef
):
    pass


_RequiredAssociateTimeSeriesToAssetPropertyRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateTimeSeriesToAssetPropertyRequestRequestTypeDef",
    {
        "alias": str,
        "assetId": str,
        "propertyId": str,
    },
)
_OptionalAssociateTimeSeriesToAssetPropertyRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateTimeSeriesToAssetPropertyRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class AssociateTimeSeriesToAssetPropertyRequestRequestTypeDef(
    _RequiredAssociateTimeSeriesToAssetPropertyRequestRequestTypeDef,
    _OptionalAssociateTimeSeriesToAssetPropertyRequestRequestTypeDef,
):
    pass


AttributeTypeDef = TypedDict(
    "AttributeTypeDef",
    {
        "defaultValue": str,
    },
    total=False,
)

_RequiredBatchAssociateProjectAssetsRequestRequestTypeDef = TypedDict(
    "_RequiredBatchAssociateProjectAssetsRequestRequestTypeDef",
    {
        "projectId": str,
        "assetIds": Sequence[str],
    },
)
_OptionalBatchAssociateProjectAssetsRequestRequestTypeDef = TypedDict(
    "_OptionalBatchAssociateProjectAssetsRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class BatchAssociateProjectAssetsRequestRequestTypeDef(
    _RequiredBatchAssociateProjectAssetsRequestRequestTypeDef,
    _OptionalBatchAssociateProjectAssetsRequestRequestTypeDef,
):
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

_RequiredBatchDisassociateProjectAssetsRequestRequestTypeDef = TypedDict(
    "_RequiredBatchDisassociateProjectAssetsRequestRequestTypeDef",
    {
        "projectId": str,
        "assetIds": Sequence[str],
    },
)
_OptionalBatchDisassociateProjectAssetsRequestRequestTypeDef = TypedDict(
    "_OptionalBatchDisassociateProjectAssetsRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class BatchDisassociateProjectAssetsRequestRequestTypeDef(
    _RequiredBatchDisassociateProjectAssetsRequestRequestTypeDef,
    _OptionalBatchDisassociateProjectAssetsRequestRequestTypeDef,
):
    pass


_RequiredBatchGetAssetPropertyAggregatesEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyAggregatesEntryTypeDef",
    {
        "entryId": str,
        "aggregateTypes": Sequence[AggregateTypeType],
        "resolution": str,
        "startDate": Union[datetime, str],
        "endDate": Union[datetime, str],
    },
)
_OptionalBatchGetAssetPropertyAggregatesEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyAggregatesEntryTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "qualities": Sequence[QualityType],
        "timeOrdering": TimeOrderingType,
    },
    total=False,
)


class BatchGetAssetPropertyAggregatesEntryTypeDef(
    _RequiredBatchGetAssetPropertyAggregatesEntryTypeDef,
    _OptionalBatchGetAssetPropertyAggregatesEntryTypeDef,
):
    pass


BatchGetAssetPropertyAggregatesErrorEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesErrorEntryTypeDef",
    {
        "errorCode": BatchGetAssetPropertyAggregatesErrorCodeType,
        "errorMessage": str,
        "entryId": str,
    },
)

BatchGetAssetPropertyAggregatesErrorInfoTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesErrorInfoTypeDef",
    {
        "errorCode": BatchGetAssetPropertyAggregatesErrorCodeType,
        "errorTimestamp": datetime,
    },
)

_RequiredBatchGetAssetPropertyValueEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueEntryTypeDef",
    {
        "entryId": str,
    },
)
_OptionalBatchGetAssetPropertyValueEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueEntryTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
    },
    total=False,
)


class BatchGetAssetPropertyValueEntryTypeDef(
    _RequiredBatchGetAssetPropertyValueEntryTypeDef, _OptionalBatchGetAssetPropertyValueEntryTypeDef
):
    pass


BatchGetAssetPropertyValueErrorEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueErrorEntryTypeDef",
    {
        "errorCode": BatchGetAssetPropertyValueErrorCodeType,
        "errorMessage": str,
        "entryId": str,
    },
)

BatchGetAssetPropertyValueErrorInfoTypeDef = TypedDict(
    "BatchGetAssetPropertyValueErrorInfoTypeDef",
    {
        "errorCode": BatchGetAssetPropertyValueErrorCodeType,
        "errorTimestamp": datetime,
    },
)

_RequiredBatchGetAssetPropertyValueHistoryEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueHistoryEntryTypeDef",
    {
        "entryId": str,
    },
)
_OptionalBatchGetAssetPropertyValueHistoryEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueHistoryEntryTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "startDate": Union[datetime, str],
        "endDate": Union[datetime, str],
        "qualities": Sequence[QualityType],
        "timeOrdering": TimeOrderingType,
    },
    total=False,
)


class BatchGetAssetPropertyValueHistoryEntryTypeDef(
    _RequiredBatchGetAssetPropertyValueHistoryEntryTypeDef,
    _OptionalBatchGetAssetPropertyValueHistoryEntryTypeDef,
):
    pass


BatchGetAssetPropertyValueHistoryErrorEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistoryErrorEntryTypeDef",
    {
        "errorCode": BatchGetAssetPropertyValueHistoryErrorCodeType,
        "errorMessage": str,
        "entryId": str,
    },
)

BatchGetAssetPropertyValueHistoryErrorInfoTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistoryErrorInfoTypeDef",
    {
        "errorCode": BatchGetAssetPropertyValueHistoryErrorCodeType,
        "errorTimestamp": datetime,
    },
)

ConfigurationErrorDetailsTypeDef = TypedDict(
    "ConfigurationErrorDetailsTypeDef",
    {
        "code": ErrorCodeType,
        "message": str,
    },
)

_RequiredCreateAssetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAssetRequestRequestTypeDef",
    {
        "assetName": str,
        "assetModelId": str,
    },
)
_OptionalCreateAssetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAssetRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Mapping[str, str],
        "assetDescription": str,
    },
    total=False,
)


class CreateAssetRequestRequestTypeDef(
    _RequiredCreateAssetRequestRequestTypeDef, _OptionalCreateAssetRequestRequestTypeDef
):
    pass


_RequiredCreateDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDashboardRequestRequestTypeDef",
    {
        "projectId": str,
        "dashboardName": str,
        "dashboardDefinition": str,
    },
)
_OptionalCreateDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDashboardRequestRequestTypeDef",
    {
        "dashboardDescription": str,
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateDashboardRequestRequestTypeDef(
    _RequiredCreateDashboardRequestRequestTypeDef, _OptionalCreateDashboardRequestRequestTypeDef
):
    pass


ImageFileTypeDef = TypedDict(
    "ImageFileTypeDef",
    {
        "data": Union[str, bytes, IO[Any], StreamingBody],
        "type": Literal["PNG"],
    },
)

_RequiredCreateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProjectRequestRequestTypeDef",
    {
        "portalId": str,
        "projectName": str,
    },
)
_OptionalCreateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProjectRequestRequestTypeDef",
    {
        "projectDescription": str,
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateProjectRequestRequestTypeDef(
    _RequiredCreateProjectRequestRequestTypeDef, _OptionalCreateProjectRequestRequestTypeDef
):
    pass


CustomerManagedS3StorageTypeDef = TypedDict(
    "CustomerManagedS3StorageTypeDef",
    {
        "s3ResourceArn": str,
        "roleArn": str,
    },
)

_RequiredDashboardSummaryTypeDef = TypedDict(
    "_RequiredDashboardSummaryTypeDef",
    {
        "id": str,
        "name": str,
    },
)
_OptionalDashboardSummaryTypeDef = TypedDict(
    "_OptionalDashboardSummaryTypeDef",
    {
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
    },
    total=False,
)


class DashboardSummaryTypeDef(_RequiredDashboardSummaryTypeDef, _OptionalDashboardSummaryTypeDef):
    pass


_RequiredDeleteAccessPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAccessPolicyRequestRequestTypeDef",
    {
        "accessPolicyId": str,
    },
)
_OptionalDeleteAccessPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAccessPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteAccessPolicyRequestRequestTypeDef(
    _RequiredDeleteAccessPolicyRequestRequestTypeDef,
    _OptionalDeleteAccessPolicyRequestRequestTypeDef,
):
    pass


_RequiredDeleteAssetModelRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAssetModelRequestRequestTypeDef",
    {
        "assetModelId": str,
    },
)
_OptionalDeleteAssetModelRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAssetModelRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteAssetModelRequestRequestTypeDef(
    _RequiredDeleteAssetModelRequestRequestTypeDef, _OptionalDeleteAssetModelRequestRequestTypeDef
):
    pass


_RequiredDeleteAssetRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAssetRequestRequestTypeDef",
    {
        "assetId": str,
    },
)
_OptionalDeleteAssetRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAssetRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteAssetRequestRequestTypeDef(
    _RequiredDeleteAssetRequestRequestTypeDef, _OptionalDeleteAssetRequestRequestTypeDef
):
    pass


_RequiredDeleteDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteDashboardRequestRequestTypeDef",
    {
        "dashboardId": str,
    },
)
_OptionalDeleteDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteDashboardRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteDashboardRequestRequestTypeDef(
    _RequiredDeleteDashboardRequestRequestTypeDef, _OptionalDeleteDashboardRequestRequestTypeDef
):
    pass


DeleteGatewayRequestRequestTypeDef = TypedDict(
    "DeleteGatewayRequestRequestTypeDef",
    {
        "gatewayId": str,
    },
)

_RequiredDeletePortalRequestRequestTypeDef = TypedDict(
    "_RequiredDeletePortalRequestRequestTypeDef",
    {
        "portalId": str,
    },
)
_OptionalDeletePortalRequestRequestTypeDef = TypedDict(
    "_OptionalDeletePortalRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeletePortalRequestRequestTypeDef(
    _RequiredDeletePortalRequestRequestTypeDef, _OptionalDeletePortalRequestRequestTypeDef
):
    pass


_RequiredDeleteProjectRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
_OptionalDeleteProjectRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteProjectRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteProjectRequestRequestTypeDef(
    _RequiredDeleteProjectRequestRequestTypeDef, _OptionalDeleteProjectRequestRequestTypeDef
):
    pass


DeleteTimeSeriesRequestRequestTypeDef = TypedDict(
    "DeleteTimeSeriesRequestRequestTypeDef",
    {
        "alias": str,
        "assetId": str,
        "propertyId": str,
        "clientToken": str,
    },
    total=False,
)

DescribeAccessPolicyRequestRequestTypeDef = TypedDict(
    "DescribeAccessPolicyRequestRequestTypeDef",
    {
        "accessPolicyId": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeAssetModelRequestRequestTypeDef = TypedDict(
    "DescribeAssetModelRequestRequestTypeDef",
    {
        "assetModelId": str,
    },
)

DescribeAssetPropertyRequestRequestTypeDef = TypedDict(
    "DescribeAssetPropertyRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
    },
)

DescribeAssetRequestRequestTypeDef = TypedDict(
    "DescribeAssetRequestRequestTypeDef",
    {
        "assetId": str,
    },
)

DescribeDashboardRequestRequestTypeDef = TypedDict(
    "DescribeDashboardRequestRequestTypeDef",
    {
        "dashboardId": str,
    },
)

DescribeGatewayCapabilityConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeGatewayCapabilityConfigurationRequestRequestTypeDef",
    {
        "gatewayId": str,
        "capabilityNamespace": str,
    },
)

DescribeGatewayRequestRequestTypeDef = TypedDict(
    "DescribeGatewayRequestRequestTypeDef",
    {
        "gatewayId": str,
    },
)

GatewayCapabilitySummaryTypeDef = TypedDict(
    "GatewayCapabilitySummaryTypeDef",
    {
        "capabilityNamespace": str,
        "capabilitySyncStatus": CapabilitySyncStatusType,
    },
)

LoggingOptionsTypeDef = TypedDict(
    "LoggingOptionsTypeDef",
    {
        "level": LoggingLevelType,
    },
)

DescribePortalRequestRequestTypeDef = TypedDict(
    "DescribePortalRequestRequestTypeDef",
    {
        "portalId": str,
    },
)

ImageLocationTypeDef = TypedDict(
    "ImageLocationTypeDef",
    {
        "id": str,
        "url": str,
    },
)

DescribeProjectRequestRequestTypeDef = TypedDict(
    "DescribeProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)

RetentionPeriodTypeDef = TypedDict(
    "RetentionPeriodTypeDef",
    {
        "numberOfDays": int,
        "unlimited": bool,
    },
    total=False,
)

DescribeTimeSeriesRequestRequestTypeDef = TypedDict(
    "DescribeTimeSeriesRequestRequestTypeDef",
    {
        "alias": str,
        "assetId": str,
        "propertyId": str,
    },
    total=False,
)

DetailedErrorTypeDef = TypedDict(
    "DetailedErrorTypeDef",
    {
        "code": DetailedErrorCodeType,
        "message": str,
    },
)

_RequiredDisassociateAssetsRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateAssetsRequestRequestTypeDef",
    {
        "assetId": str,
        "hierarchyId": str,
        "childAssetId": str,
    },
)
_OptionalDisassociateAssetsRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateAssetsRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DisassociateAssetsRequestRequestTypeDef(
    _RequiredDisassociateAssetsRequestRequestTypeDef,
    _OptionalDisassociateAssetsRequestRequestTypeDef,
):
    pass


_RequiredDisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef",
    {
        "alias": str,
        "assetId": str,
        "propertyId": str,
    },
)
_OptionalDisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef(
    _RequiredDisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef,
    _OptionalDisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef,
):
    pass


_RequiredVariableValueTypeDef = TypedDict(
    "_RequiredVariableValueTypeDef",
    {
        "propertyId": str,
    },
)
_OptionalVariableValueTypeDef = TypedDict(
    "_OptionalVariableValueTypeDef",
    {
        "hierarchyId": str,
    },
    total=False,
)


class VariableValueTypeDef(_RequiredVariableValueTypeDef, _OptionalVariableValueTypeDef):
    pass


ForwardingConfigTypeDef = TypedDict(
    "ForwardingConfigTypeDef",
    {
        "state": ForwardingConfigStateType,
    },
)

GreengrassTypeDef = TypedDict(
    "GreengrassTypeDef",
    {
        "groupArn": str,
    },
)

GreengrassV2TypeDef = TypedDict(
    "GreengrassV2TypeDef",
    {
        "coreDeviceThingName": str,
    },
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

_RequiredGetAssetPropertyAggregatesRequestRequestTypeDef = TypedDict(
    "_RequiredGetAssetPropertyAggregatesRequestRequestTypeDef",
    {
        "aggregateTypes": Sequence[AggregateTypeType],
        "resolution": str,
        "startDate": Union[datetime, str],
        "endDate": Union[datetime, str],
    },
)
_OptionalGetAssetPropertyAggregatesRequestRequestTypeDef = TypedDict(
    "_OptionalGetAssetPropertyAggregatesRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "qualities": Sequence[QualityType],
        "timeOrdering": TimeOrderingType,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetAssetPropertyAggregatesRequestRequestTypeDef(
    _RequiredGetAssetPropertyAggregatesRequestRequestTypeDef,
    _OptionalGetAssetPropertyAggregatesRequestRequestTypeDef,
):
    pass


GetAssetPropertyValueHistoryRequestRequestTypeDef = TypedDict(
    "GetAssetPropertyValueHistoryRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "startDate": Union[datetime, str],
        "endDate": Union[datetime, str],
        "qualities": Sequence[QualityType],
        "timeOrdering": TimeOrderingType,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

GetAssetPropertyValueRequestRequestTypeDef = TypedDict(
    "GetAssetPropertyValueRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
    },
    total=False,
)

_RequiredGetInterpolatedAssetPropertyValuesRequestRequestTypeDef = TypedDict(
    "_RequiredGetInterpolatedAssetPropertyValuesRequestRequestTypeDef",
    {
        "startTimeInSeconds": int,
        "endTimeInSeconds": int,
        "quality": QualityType,
        "intervalInSeconds": int,
        "type": str,
    },
)
_OptionalGetInterpolatedAssetPropertyValuesRequestRequestTypeDef = TypedDict(
    "_OptionalGetInterpolatedAssetPropertyValuesRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "startTimeOffsetInNanos": int,
        "endTimeOffsetInNanos": int,
        "nextToken": str,
        "maxResults": int,
        "intervalWindowInSeconds": int,
    },
    total=False,
)


class GetInterpolatedAssetPropertyValuesRequestRequestTypeDef(
    _RequiredGetInterpolatedAssetPropertyValuesRequestRequestTypeDef,
    _OptionalGetInterpolatedAssetPropertyValuesRequestRequestTypeDef,
):
    pass


GroupIdentityTypeDef = TypedDict(
    "GroupIdentityTypeDef",
    {
        "id": str,
    },
)

IAMRoleIdentityTypeDef = TypedDict(
    "IAMRoleIdentityTypeDef",
    {
        "arn": str,
    },
)

IAMUserIdentityTypeDef = TypedDict(
    "IAMUserIdentityTypeDef",
    {
        "arn": str,
    },
)

UserIdentityTypeDef = TypedDict(
    "UserIdentityTypeDef",
    {
        "id": str,
    },
)

ListAccessPoliciesRequestRequestTypeDef = TypedDict(
    "ListAccessPoliciesRequestRequestTypeDef",
    {
        "identityType": IdentityTypeType,
        "identityId": str,
        "resourceType": ResourceTypeType,
        "resourceId": str,
        "iamArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListAssetModelsRequestRequestTypeDef = TypedDict(
    "ListAssetModelsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListAssetRelationshipsRequestRequestTypeDef = TypedDict(
    "_RequiredListAssetRelationshipsRequestRequestTypeDef",
    {
        "assetId": str,
        "traversalType": Literal["PATH_TO_ROOT"],
    },
)
_OptionalListAssetRelationshipsRequestRequestTypeDef = TypedDict(
    "_OptionalListAssetRelationshipsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAssetRelationshipsRequestRequestTypeDef(
    _RequiredListAssetRelationshipsRequestRequestTypeDef,
    _OptionalListAssetRelationshipsRequestRequestTypeDef,
):
    pass


ListAssetsRequestRequestTypeDef = TypedDict(
    "ListAssetsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "assetModelId": str,
        "filter": ListAssetsFilterType,
    },
    total=False,
)

_RequiredListAssociatedAssetsRequestRequestTypeDef = TypedDict(
    "_RequiredListAssociatedAssetsRequestRequestTypeDef",
    {
        "assetId": str,
    },
)
_OptionalListAssociatedAssetsRequestRequestTypeDef = TypedDict(
    "_OptionalListAssociatedAssetsRequestRequestTypeDef",
    {
        "hierarchyId": str,
        "traversalDirection": TraversalDirectionType,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAssociatedAssetsRequestRequestTypeDef(
    _RequiredListAssociatedAssetsRequestRequestTypeDef,
    _OptionalListAssociatedAssetsRequestRequestTypeDef,
):
    pass


_RequiredListDashboardsRequestRequestTypeDef = TypedDict(
    "_RequiredListDashboardsRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
_OptionalListDashboardsRequestRequestTypeDef = TypedDict(
    "_OptionalListDashboardsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListDashboardsRequestRequestTypeDef(
    _RequiredListDashboardsRequestRequestTypeDef, _OptionalListDashboardsRequestRequestTypeDef
):
    pass


ListGatewaysRequestRequestTypeDef = TypedDict(
    "ListGatewaysRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListPortalsRequestRequestTypeDef = TypedDict(
    "ListPortalsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListProjectAssetsRequestRequestTypeDef = TypedDict(
    "_RequiredListProjectAssetsRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
_OptionalListProjectAssetsRequestRequestTypeDef = TypedDict(
    "_OptionalListProjectAssetsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListProjectAssetsRequestRequestTypeDef(
    _RequiredListProjectAssetsRequestRequestTypeDef, _OptionalListProjectAssetsRequestRequestTypeDef
):
    pass


_RequiredListProjectsRequestRequestTypeDef = TypedDict(
    "_RequiredListProjectsRequestRequestTypeDef",
    {
        "portalId": str,
    },
)
_OptionalListProjectsRequestRequestTypeDef = TypedDict(
    "_OptionalListProjectsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListProjectsRequestRequestTypeDef(
    _RequiredListProjectsRequestRequestTypeDef, _OptionalListProjectsRequestRequestTypeDef
):
    pass


_RequiredProjectSummaryTypeDef = TypedDict(
    "_RequiredProjectSummaryTypeDef",
    {
        "id": str,
        "name": str,
    },
)
_OptionalProjectSummaryTypeDef = TypedDict(
    "_OptionalProjectSummaryTypeDef",
    {
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
    },
    total=False,
)


class ProjectSummaryTypeDef(_RequiredProjectSummaryTypeDef, _OptionalProjectSummaryTypeDef):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTimeSeriesRequestRequestTypeDef = TypedDict(
    "ListTimeSeriesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "assetId": str,
        "aliasPrefix": str,
        "timeSeriesType": ListTimeSeriesTypeType,
    },
    total=False,
)

_RequiredTimeSeriesSummaryTypeDef = TypedDict(
    "_RequiredTimeSeriesSummaryTypeDef",
    {
        "timeSeriesId": str,
        "dataType": PropertyDataTypeType,
        "timeSeriesCreationDate": datetime,
        "timeSeriesLastUpdateDate": datetime,
    },
)
_OptionalTimeSeriesSummaryTypeDef = TypedDict(
    "_OptionalTimeSeriesSummaryTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "alias": str,
        "dataTypeSpec": str,
    },
    total=False,
)


class TimeSeriesSummaryTypeDef(
    _RequiredTimeSeriesSummaryTypeDef, _OptionalTimeSeriesSummaryTypeDef
):
    pass


MetricProcessingConfigTypeDef = TypedDict(
    "MetricProcessingConfigTypeDef",
    {
        "computeLocation": ComputeLocationType,
    },
)

_RequiredTumblingWindowTypeDef = TypedDict(
    "_RequiredTumblingWindowTypeDef",
    {
        "interval": str,
    },
)
_OptionalTumblingWindowTypeDef = TypedDict(
    "_OptionalTumblingWindowTypeDef",
    {
        "offset": str,
    },
    total=False,
)


class TumblingWindowTypeDef(_RequiredTumblingWindowTypeDef, _OptionalTumblingWindowTypeDef):
    pass


MonitorErrorDetailsTypeDef = TypedDict(
    "MonitorErrorDetailsTypeDef",
    {
        "code": MonitorErrorCodeType,
        "message": str,
    },
    total=False,
)

PortalResourceTypeDef = TypedDict(
    "PortalResourceTypeDef",
    {
        "id": str,
    },
)

ProjectResourceTypeDef = TypedDict(
    "ProjectResourceTypeDef",
    {
        "id": str,
    },
)

_RequiredPutDefaultEncryptionConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutDefaultEncryptionConfigurationRequestRequestTypeDef",
    {
        "encryptionType": EncryptionTypeType,
    },
)
_OptionalPutDefaultEncryptionConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutDefaultEncryptionConfigurationRequestRequestTypeDef",
    {
        "kmsKeyId": str,
    },
    total=False,
)


class PutDefaultEncryptionConfigurationRequestRequestTypeDef(
    _RequiredPutDefaultEncryptionConfigurationRequestRequestTypeDef,
    _OptionalPutDefaultEncryptionConfigurationRequestRequestTypeDef,
):
    pass


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

_RequiredUpdateAssetPropertyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAssetPropertyRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
    },
)
_OptionalUpdateAssetPropertyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAssetPropertyRequestRequestTypeDef",
    {
        "propertyAlias": str,
        "propertyNotificationState": PropertyNotificationStateType,
        "clientToken": str,
    },
    total=False,
)


class UpdateAssetPropertyRequestRequestTypeDef(
    _RequiredUpdateAssetPropertyRequestRequestTypeDef,
    _OptionalUpdateAssetPropertyRequestRequestTypeDef,
):
    pass


_RequiredUpdateAssetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAssetRequestRequestTypeDef",
    {
        "assetId": str,
        "assetName": str,
    },
)
_OptionalUpdateAssetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAssetRequestRequestTypeDef",
    {
        "clientToken": str,
        "assetDescription": str,
    },
    total=False,
)


class UpdateAssetRequestRequestTypeDef(
    _RequiredUpdateAssetRequestRequestTypeDef, _OptionalUpdateAssetRequestRequestTypeDef
):
    pass


_RequiredUpdateDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDashboardRequestRequestTypeDef",
    {
        "dashboardId": str,
        "dashboardName": str,
        "dashboardDefinition": str,
    },
)
_OptionalUpdateDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDashboardRequestRequestTypeDef",
    {
        "dashboardDescription": str,
        "clientToken": str,
    },
    total=False,
)


class UpdateDashboardRequestRequestTypeDef(
    _RequiredUpdateDashboardRequestRequestTypeDef, _OptionalUpdateDashboardRequestRequestTypeDef
):
    pass


UpdateGatewayCapabilityConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateGatewayCapabilityConfigurationRequestRequestTypeDef",
    {
        "gatewayId": str,
        "capabilityNamespace": str,
        "capabilityConfiguration": str,
    },
)

UpdateGatewayRequestRequestTypeDef = TypedDict(
    "UpdateGatewayRequestRequestTypeDef",
    {
        "gatewayId": str,
        "gatewayName": str,
    },
)

_RequiredUpdateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateProjectRequestRequestTypeDef",
    {
        "projectId": str,
        "projectName": str,
    },
)
_OptionalUpdateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateProjectRequestRequestTypeDef",
    {
        "projectDescription": str,
        "clientToken": str,
    },
    total=False,
)


class UpdateProjectRequestRequestTypeDef(
    _RequiredUpdateProjectRequestRequestTypeDef, _OptionalUpdateProjectRequestRequestTypeDef
):
    pass


_RequiredAggregatedValueTypeDef = TypedDict(
    "_RequiredAggregatedValueTypeDef",
    {
        "timestamp": datetime,
        "value": AggregatesTypeDef,
    },
)
_OptionalAggregatedValueTypeDef = TypedDict(
    "_OptionalAggregatedValueTypeDef",
    {
        "quality": QualityType,
    },
    total=False,
)


class AggregatedValueTypeDef(_RequiredAggregatedValueTypeDef, _OptionalAggregatedValueTypeDef):
    pass


_RequiredAssetRelationshipSummaryTypeDef = TypedDict(
    "_RequiredAssetRelationshipSummaryTypeDef",
    {
        "relationshipType": Literal["HIERARCHY"],
    },
)
_OptionalAssetRelationshipSummaryTypeDef = TypedDict(
    "_OptionalAssetRelationshipSummaryTypeDef",
    {
        "hierarchyInfo": AssetHierarchyInfoTypeDef,
    },
    total=False,
)


class AssetRelationshipSummaryTypeDef(
    _RequiredAssetRelationshipSummaryTypeDef, _OptionalAssetRelationshipSummaryTypeDef
):
    pass


_RequiredAssetPropertyTypeDef = TypedDict(
    "_RequiredAssetPropertyTypeDef",
    {
        "id": str,
        "name": str,
        "dataType": PropertyDataTypeType,
    },
)
_OptionalAssetPropertyTypeDef = TypedDict(
    "_OptionalAssetPropertyTypeDef",
    {
        "alias": str,
        "notification": PropertyNotificationTypeDef,
        "dataTypeSpec": str,
        "unit": str,
    },
    total=False,
)


class AssetPropertyTypeDef(_RequiredAssetPropertyTypeDef, _OptionalAssetPropertyTypeDef):
    pass


BatchPutAssetPropertyErrorTypeDef = TypedDict(
    "BatchPutAssetPropertyErrorTypeDef",
    {
        "errorCode": BatchPutAssetPropertyValueErrorCodeType,
        "errorMessage": str,
        "timestamps": List[TimeInNanosTypeDef],
    },
)

_RequiredAssetPropertyValueTypeDef = TypedDict(
    "_RequiredAssetPropertyValueTypeDef",
    {
        "value": VariantTypeDef,
        "timestamp": TimeInNanosTypeDef,
    },
)
_OptionalAssetPropertyValueTypeDef = TypedDict(
    "_OptionalAssetPropertyValueTypeDef",
    {
        "quality": QualityType,
    },
    total=False,
)


class AssetPropertyValueTypeDef(
    _RequiredAssetPropertyValueTypeDef, _OptionalAssetPropertyValueTypeDef
):
    pass


InterpolatedAssetPropertyValueTypeDef = TypedDict(
    "InterpolatedAssetPropertyValueTypeDef",
    {
        "timestamp": TimeInNanosTypeDef,
        "value": VariantTypeDef,
    },
)

BatchAssociateProjectAssetsResponseTypeDef = TypedDict(
    "BatchAssociateProjectAssetsResponseTypeDef",
    {
        "errors": List[AssetErrorDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDisassociateProjectAssetsResponseTypeDef = TypedDict(
    "BatchDisassociateProjectAssetsResponseTypeDef",
    {
        "errors": List[AssetErrorDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAccessPolicyResponseTypeDef = TypedDict(
    "CreateAccessPolicyResponseTypeDef",
    {
        "accessPolicyId": str,
        "accessPolicyArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDashboardResponseTypeDef = TypedDict(
    "CreateDashboardResponseTypeDef",
    {
        "dashboardId": str,
        "dashboardArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGatewayResponseTypeDef = TypedDict(
    "CreateGatewayResponseTypeDef",
    {
        "gatewayId": str,
        "gatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateProjectResponseTypeDef = TypedDict(
    "CreateProjectResponseTypeDef",
    {
        "projectId": str,
        "projectArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDashboardResponseTypeDef = TypedDict(
    "DescribeDashboardResponseTypeDef",
    {
        "dashboardId": str,
        "dashboardArn": str,
        "dashboardName": str,
        "projectId": str,
        "dashboardDescription": str,
        "dashboardDefinition": str,
        "dashboardCreationDate": datetime,
        "dashboardLastUpdateDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGatewayCapabilityConfigurationResponseTypeDef = TypedDict(
    "DescribeGatewayCapabilityConfigurationResponseTypeDef",
    {
        "gatewayId": str,
        "capabilityNamespace": str,
        "capabilityConfiguration": str,
        "capabilitySyncStatus": CapabilitySyncStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeProjectResponseTypeDef = TypedDict(
    "DescribeProjectResponseTypeDef",
    {
        "projectId": str,
        "projectArn": str,
        "projectName": str,
        "portalId": str,
        "projectDescription": str,
        "projectCreationDate": datetime,
        "projectLastUpdateDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTimeSeriesResponseTypeDef = TypedDict(
    "DescribeTimeSeriesResponseTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "alias": str,
        "timeSeriesId": str,
        "dataType": PropertyDataTypeType,
        "dataTypeSpec": str,
        "timeSeriesCreationDate": datetime,
        "timeSeriesLastUpdateDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProjectAssetsResponseTypeDef = TypedDict(
    "ListProjectAssetsResponseTypeDef",
    {
        "assetIds": List[str],
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

UpdateGatewayCapabilityConfigurationResponseTypeDef = TypedDict(
    "UpdateGatewayCapabilityConfigurationResponseTypeDef",
    {
        "capabilityNamespace": str,
        "capabilitySyncStatus": CapabilitySyncStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredBatchGetAssetPropertyAggregatesRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyAggregatesRequestRequestTypeDef",
    {
        "entries": Sequence[BatchGetAssetPropertyAggregatesEntryTypeDef],
    },
)
_OptionalBatchGetAssetPropertyAggregatesRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyAggregatesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class BatchGetAssetPropertyAggregatesRequestRequestTypeDef(
    _RequiredBatchGetAssetPropertyAggregatesRequestRequestTypeDef,
    _OptionalBatchGetAssetPropertyAggregatesRequestRequestTypeDef,
):
    pass


_RequiredBatchGetAssetPropertyAggregatesSkippedEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyAggregatesSkippedEntryTypeDef",
    {
        "entryId": str,
        "completionStatus": BatchEntryCompletionStatusType,
    },
)
_OptionalBatchGetAssetPropertyAggregatesSkippedEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyAggregatesSkippedEntryTypeDef",
    {
        "errorInfo": BatchGetAssetPropertyAggregatesErrorInfoTypeDef,
    },
    total=False,
)


class BatchGetAssetPropertyAggregatesSkippedEntryTypeDef(
    _RequiredBatchGetAssetPropertyAggregatesSkippedEntryTypeDef,
    _OptionalBatchGetAssetPropertyAggregatesSkippedEntryTypeDef,
):
    pass


_RequiredBatchGetAssetPropertyValueRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueRequestRequestTypeDef",
    {
        "entries": Sequence[BatchGetAssetPropertyValueEntryTypeDef],
    },
)
_OptionalBatchGetAssetPropertyValueRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class BatchGetAssetPropertyValueRequestRequestTypeDef(
    _RequiredBatchGetAssetPropertyValueRequestRequestTypeDef,
    _OptionalBatchGetAssetPropertyValueRequestRequestTypeDef,
):
    pass


_RequiredBatchGetAssetPropertyValueSkippedEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueSkippedEntryTypeDef",
    {
        "entryId": str,
        "completionStatus": BatchEntryCompletionStatusType,
    },
)
_OptionalBatchGetAssetPropertyValueSkippedEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueSkippedEntryTypeDef",
    {
        "errorInfo": BatchGetAssetPropertyValueErrorInfoTypeDef,
    },
    total=False,
)


class BatchGetAssetPropertyValueSkippedEntryTypeDef(
    _RequiredBatchGetAssetPropertyValueSkippedEntryTypeDef,
    _OptionalBatchGetAssetPropertyValueSkippedEntryTypeDef,
):
    pass


_RequiredBatchGetAssetPropertyValueHistoryRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueHistoryRequestRequestTypeDef",
    {
        "entries": Sequence[BatchGetAssetPropertyValueHistoryEntryTypeDef],
    },
)
_OptionalBatchGetAssetPropertyValueHistoryRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueHistoryRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class BatchGetAssetPropertyValueHistoryRequestRequestTypeDef(
    _RequiredBatchGetAssetPropertyValueHistoryRequestRequestTypeDef,
    _OptionalBatchGetAssetPropertyValueHistoryRequestRequestTypeDef,
):
    pass


_RequiredBatchGetAssetPropertyValueHistorySkippedEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueHistorySkippedEntryTypeDef",
    {
        "entryId": str,
        "completionStatus": BatchEntryCompletionStatusType,
    },
)
_OptionalBatchGetAssetPropertyValueHistorySkippedEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueHistorySkippedEntryTypeDef",
    {
        "errorInfo": BatchGetAssetPropertyValueHistoryErrorInfoTypeDef,
    },
    total=False,
)


class BatchGetAssetPropertyValueHistorySkippedEntryTypeDef(
    _RequiredBatchGetAssetPropertyValueHistorySkippedEntryTypeDef,
    _OptionalBatchGetAssetPropertyValueHistorySkippedEntryTypeDef,
):
    pass


_RequiredConfigurationStatusTypeDef = TypedDict(
    "_RequiredConfigurationStatusTypeDef",
    {
        "state": ConfigurationStateType,
    },
)
_OptionalConfigurationStatusTypeDef = TypedDict(
    "_OptionalConfigurationStatusTypeDef",
    {
        "error": ConfigurationErrorDetailsTypeDef,
    },
    total=False,
)


class ConfigurationStatusTypeDef(
    _RequiredConfigurationStatusTypeDef, _OptionalConfigurationStatusTypeDef
):
    pass


_RequiredCreatePortalRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePortalRequestRequestTypeDef",
    {
        "portalName": str,
        "portalContactEmail": str,
        "roleArn": str,
    },
)
_OptionalCreatePortalRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePortalRequestRequestTypeDef",
    {
        "portalDescription": str,
        "clientToken": str,
        "portalLogoImageFile": ImageFileTypeDef,
        "tags": Mapping[str, str],
        "portalAuthMode": AuthModeType,
        "notificationSenderEmail": str,
        "alarms": AlarmsTypeDef,
    },
    total=False,
)


class CreatePortalRequestRequestTypeDef(
    _RequiredCreatePortalRequestRequestTypeDef, _OptionalCreatePortalRequestRequestTypeDef
):
    pass


ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "id": str,
        "file": ImageFileTypeDef,
    },
    total=False,
)

MultiLayerStorageTypeDef = TypedDict(
    "MultiLayerStorageTypeDef",
    {
        "customerManagedS3Storage": CustomerManagedS3StorageTypeDef,
    },
)

ListDashboardsResponseTypeDef = TypedDict(
    "ListDashboardsResponseTypeDef",
    {
        "dashboardSummaries": List[DashboardSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDescribeAssetModelRequestAssetModelActiveWaitTypeDef = TypedDict(
    "_RequiredDescribeAssetModelRequestAssetModelActiveWaitTypeDef",
    {
        "assetModelId": str,
    },
)
_OptionalDescribeAssetModelRequestAssetModelActiveWaitTypeDef = TypedDict(
    "_OptionalDescribeAssetModelRequestAssetModelActiveWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeAssetModelRequestAssetModelActiveWaitTypeDef(
    _RequiredDescribeAssetModelRequestAssetModelActiveWaitTypeDef,
    _OptionalDescribeAssetModelRequestAssetModelActiveWaitTypeDef,
):
    pass


_RequiredDescribeAssetModelRequestAssetModelNotExistsWaitTypeDef = TypedDict(
    "_RequiredDescribeAssetModelRequestAssetModelNotExistsWaitTypeDef",
    {
        "assetModelId": str,
    },
)
_OptionalDescribeAssetModelRequestAssetModelNotExistsWaitTypeDef = TypedDict(
    "_OptionalDescribeAssetModelRequestAssetModelNotExistsWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeAssetModelRequestAssetModelNotExistsWaitTypeDef(
    _RequiredDescribeAssetModelRequestAssetModelNotExistsWaitTypeDef,
    _OptionalDescribeAssetModelRequestAssetModelNotExistsWaitTypeDef,
):
    pass


_RequiredDescribeAssetRequestAssetActiveWaitTypeDef = TypedDict(
    "_RequiredDescribeAssetRequestAssetActiveWaitTypeDef",
    {
        "assetId": str,
    },
)
_OptionalDescribeAssetRequestAssetActiveWaitTypeDef = TypedDict(
    "_OptionalDescribeAssetRequestAssetActiveWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeAssetRequestAssetActiveWaitTypeDef(
    _RequiredDescribeAssetRequestAssetActiveWaitTypeDef,
    _OptionalDescribeAssetRequestAssetActiveWaitTypeDef,
):
    pass


_RequiredDescribeAssetRequestAssetNotExistsWaitTypeDef = TypedDict(
    "_RequiredDescribeAssetRequestAssetNotExistsWaitTypeDef",
    {
        "assetId": str,
    },
)
_OptionalDescribeAssetRequestAssetNotExistsWaitTypeDef = TypedDict(
    "_OptionalDescribeAssetRequestAssetNotExistsWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeAssetRequestAssetNotExistsWaitTypeDef(
    _RequiredDescribeAssetRequestAssetNotExistsWaitTypeDef,
    _OptionalDescribeAssetRequestAssetNotExistsWaitTypeDef,
):
    pass


_RequiredDescribePortalRequestPortalActiveWaitTypeDef = TypedDict(
    "_RequiredDescribePortalRequestPortalActiveWaitTypeDef",
    {
        "portalId": str,
    },
)
_OptionalDescribePortalRequestPortalActiveWaitTypeDef = TypedDict(
    "_OptionalDescribePortalRequestPortalActiveWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribePortalRequestPortalActiveWaitTypeDef(
    _RequiredDescribePortalRequestPortalActiveWaitTypeDef,
    _OptionalDescribePortalRequestPortalActiveWaitTypeDef,
):
    pass


_RequiredDescribePortalRequestPortalNotExistsWaitTypeDef = TypedDict(
    "_RequiredDescribePortalRequestPortalNotExistsWaitTypeDef",
    {
        "portalId": str,
    },
)
_OptionalDescribePortalRequestPortalNotExistsWaitTypeDef = TypedDict(
    "_OptionalDescribePortalRequestPortalNotExistsWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribePortalRequestPortalNotExistsWaitTypeDef(
    _RequiredDescribePortalRequestPortalNotExistsWaitTypeDef,
    _OptionalDescribePortalRequestPortalNotExistsWaitTypeDef,
):
    pass


DescribeLoggingOptionsResponseTypeDef = TypedDict(
    "DescribeLoggingOptionsResponseTypeDef",
    {
        "loggingOptions": LoggingOptionsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutLoggingOptionsRequestRequestTypeDef = TypedDict(
    "PutLoggingOptionsRequestRequestTypeDef",
    {
        "loggingOptions": LoggingOptionsTypeDef,
    },
)

_RequiredErrorDetailsTypeDef = TypedDict(
    "_RequiredErrorDetailsTypeDef",
    {
        "code": ErrorCodeType,
        "message": str,
    },
)
_OptionalErrorDetailsTypeDef = TypedDict(
    "_OptionalErrorDetailsTypeDef",
    {
        "details": List[DetailedErrorTypeDef],
    },
    total=False,
)


class ErrorDetailsTypeDef(_RequiredErrorDetailsTypeDef, _OptionalErrorDetailsTypeDef):
    pass


ExpressionVariableTypeDef = TypedDict(
    "ExpressionVariableTypeDef",
    {
        "name": str,
        "value": VariableValueTypeDef,
    },
)

MeasurementProcessingConfigTypeDef = TypedDict(
    "MeasurementProcessingConfigTypeDef",
    {
        "forwardingConfig": ForwardingConfigTypeDef,
    },
)

_RequiredTransformProcessingConfigTypeDef = TypedDict(
    "_RequiredTransformProcessingConfigTypeDef",
    {
        "computeLocation": ComputeLocationType,
    },
)
_OptionalTransformProcessingConfigTypeDef = TypedDict(
    "_OptionalTransformProcessingConfigTypeDef",
    {
        "forwardingConfig": ForwardingConfigTypeDef,
    },
    total=False,
)


class TransformProcessingConfigTypeDef(
    _RequiredTransformProcessingConfigTypeDef, _OptionalTransformProcessingConfigTypeDef
):
    pass


GatewayPlatformTypeDef = TypedDict(
    "GatewayPlatformTypeDef",
    {
        "greengrass": GreengrassTypeDef,
        "greengrassV2": GreengrassV2TypeDef,
    },
    total=False,
)

_RequiredGetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef = TypedDict(
    "_RequiredGetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef",
    {
        "aggregateTypes": Sequence[AggregateTypeType],
        "resolution": str,
        "startDate": Union[datetime, str],
        "endDate": Union[datetime, str],
    },
)
_OptionalGetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef = TypedDict(
    "_OptionalGetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "qualities": Sequence[QualityType],
        "timeOrdering": TimeOrderingType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef(
    _RequiredGetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef,
    _OptionalGetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef,
):
    pass


GetAssetPropertyValueHistoryRequestGetAssetPropertyValueHistoryPaginateTypeDef = TypedDict(
    "GetAssetPropertyValueHistoryRequestGetAssetPropertyValueHistoryPaginateTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "startDate": Union[datetime, str],
        "endDate": Union[datetime, str],
        "qualities": Sequence[QualityType],
        "timeOrdering": TimeOrderingType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef = TypedDict(
    "_RequiredGetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef",
    {
        "startTimeInSeconds": int,
        "endTimeInSeconds": int,
        "quality": QualityType,
        "intervalInSeconds": int,
        "type": str,
    },
)
_OptionalGetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef = TypedDict(
    "_OptionalGetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "startTimeOffsetInNanos": int,
        "endTimeOffsetInNanos": int,
        "intervalWindowInSeconds": int,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef(
    _RequiredGetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef,
    _OptionalGetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef,
):
    pass


ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef = TypedDict(
    "ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef",
    {
        "identityType": IdentityTypeType,
        "identityId": str,
        "resourceType": ResourceTypeType,
        "resourceId": str,
        "iamArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListAssetModelsRequestListAssetModelsPaginateTypeDef = TypedDict(
    "ListAssetModelsRequestListAssetModelsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef = TypedDict(
    "_RequiredListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef",
    {
        "assetId": str,
        "traversalType": Literal["PATH_TO_ROOT"],
    },
)
_OptionalListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef = TypedDict(
    "_OptionalListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef(
    _RequiredListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef,
    _OptionalListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef,
):
    pass


ListAssetsRequestListAssetsPaginateTypeDef = TypedDict(
    "ListAssetsRequestListAssetsPaginateTypeDef",
    {
        "assetModelId": str,
        "filter": ListAssetsFilterType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef = TypedDict(
    "_RequiredListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef",
    {
        "assetId": str,
    },
)
_OptionalListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef = TypedDict(
    "_OptionalListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef",
    {
        "hierarchyId": str,
        "traversalDirection": TraversalDirectionType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef(
    _RequiredListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef,
    _OptionalListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef,
):
    pass


_RequiredListDashboardsRequestListDashboardsPaginateTypeDef = TypedDict(
    "_RequiredListDashboardsRequestListDashboardsPaginateTypeDef",
    {
        "projectId": str,
    },
)
_OptionalListDashboardsRequestListDashboardsPaginateTypeDef = TypedDict(
    "_OptionalListDashboardsRequestListDashboardsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDashboardsRequestListDashboardsPaginateTypeDef(
    _RequiredListDashboardsRequestListDashboardsPaginateTypeDef,
    _OptionalListDashboardsRequestListDashboardsPaginateTypeDef,
):
    pass


ListGatewaysRequestListGatewaysPaginateTypeDef = TypedDict(
    "ListGatewaysRequestListGatewaysPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPortalsRequestListPortalsPaginateTypeDef = TypedDict(
    "ListPortalsRequestListPortalsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListProjectAssetsRequestListProjectAssetsPaginateTypeDef = TypedDict(
    "_RequiredListProjectAssetsRequestListProjectAssetsPaginateTypeDef",
    {
        "projectId": str,
    },
)
_OptionalListProjectAssetsRequestListProjectAssetsPaginateTypeDef = TypedDict(
    "_OptionalListProjectAssetsRequestListProjectAssetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListProjectAssetsRequestListProjectAssetsPaginateTypeDef(
    _RequiredListProjectAssetsRequestListProjectAssetsPaginateTypeDef,
    _OptionalListProjectAssetsRequestListProjectAssetsPaginateTypeDef,
):
    pass


_RequiredListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "_RequiredListProjectsRequestListProjectsPaginateTypeDef",
    {
        "portalId": str,
    },
)
_OptionalListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "_OptionalListProjectsRequestListProjectsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListProjectsRequestListProjectsPaginateTypeDef(
    _RequiredListProjectsRequestListProjectsPaginateTypeDef,
    _OptionalListProjectsRequestListProjectsPaginateTypeDef,
):
    pass


ListTimeSeriesRequestListTimeSeriesPaginateTypeDef = TypedDict(
    "ListTimeSeriesRequestListTimeSeriesPaginateTypeDef",
    {
        "assetId": str,
        "aliasPrefix": str,
        "timeSeriesType": ListTimeSeriesTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

IdentityTypeDef = TypedDict(
    "IdentityTypeDef",
    {
        "user": UserIdentityTypeDef,
        "group": GroupIdentityTypeDef,
        "iamUser": IAMUserIdentityTypeDef,
        "iamRole": IAMRoleIdentityTypeDef,
    },
    total=False,
)

ListProjectsResponseTypeDef = TypedDict(
    "ListProjectsResponseTypeDef",
    {
        "projectSummaries": List[ProjectSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTimeSeriesResponseTypeDef = TypedDict(
    "ListTimeSeriesResponseTypeDef",
    {
        "TimeSeriesSummaries": List[TimeSeriesSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MetricWindowTypeDef = TypedDict(
    "MetricWindowTypeDef",
    {
        "tumbling": TumblingWindowTypeDef,
    },
    total=False,
)

_RequiredPortalStatusTypeDef = TypedDict(
    "_RequiredPortalStatusTypeDef",
    {
        "state": PortalStateType,
    },
)
_OptionalPortalStatusTypeDef = TypedDict(
    "_OptionalPortalStatusTypeDef",
    {
        "error": MonitorErrorDetailsTypeDef,
    },
    total=False,
)


class PortalStatusTypeDef(_RequiredPortalStatusTypeDef, _OptionalPortalStatusTypeDef):
    pass


ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "portal": PortalResourceTypeDef,
        "project": ProjectResourceTypeDef,
    },
    total=False,
)

BatchGetAssetPropertyAggregatesSuccessEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesSuccessEntryTypeDef",
    {
        "entryId": str,
        "aggregatedValues": List[AggregatedValueTypeDef],
    },
)

GetAssetPropertyAggregatesResponseTypeDef = TypedDict(
    "GetAssetPropertyAggregatesResponseTypeDef",
    {
        "aggregatedValues": List[AggregatedValueTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssetRelationshipsResponseTypeDef = TypedDict(
    "ListAssetRelationshipsResponseTypeDef",
    {
        "assetRelationshipSummaries": List[AssetRelationshipSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAssetCompositeModelTypeDef = TypedDict(
    "_RequiredAssetCompositeModelTypeDef",
    {
        "name": str,
        "type": str,
        "properties": List[AssetPropertyTypeDef],
    },
)
_OptionalAssetCompositeModelTypeDef = TypedDict(
    "_OptionalAssetCompositeModelTypeDef",
    {
        "description": str,
    },
    total=False,
)


class AssetCompositeModelTypeDef(
    _RequiredAssetCompositeModelTypeDef, _OptionalAssetCompositeModelTypeDef
):
    pass


BatchPutAssetPropertyErrorEntryTypeDef = TypedDict(
    "BatchPutAssetPropertyErrorEntryTypeDef",
    {
        "entryId": str,
        "errors": List[BatchPutAssetPropertyErrorTypeDef],
    },
)

BatchGetAssetPropertyValueHistorySuccessEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistorySuccessEntryTypeDef",
    {
        "entryId": str,
        "assetPropertyValueHistory": List[AssetPropertyValueTypeDef],
    },
)

_RequiredBatchGetAssetPropertyValueSuccessEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueSuccessEntryTypeDef",
    {
        "entryId": str,
    },
)
_OptionalBatchGetAssetPropertyValueSuccessEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueSuccessEntryTypeDef",
    {
        "assetPropertyValue": AssetPropertyValueTypeDef,
    },
    total=False,
)


class BatchGetAssetPropertyValueSuccessEntryTypeDef(
    _RequiredBatchGetAssetPropertyValueSuccessEntryTypeDef,
    _OptionalBatchGetAssetPropertyValueSuccessEntryTypeDef,
):
    pass


GetAssetPropertyValueHistoryResponseTypeDef = TypedDict(
    "GetAssetPropertyValueHistoryResponseTypeDef",
    {
        "assetPropertyValueHistory": List[AssetPropertyValueTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAssetPropertyValueResponseTypeDef = TypedDict(
    "GetAssetPropertyValueResponseTypeDef",
    {
        "propertyValue": AssetPropertyValueTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutAssetPropertyValueEntryTypeDef = TypedDict(
    "_RequiredPutAssetPropertyValueEntryTypeDef",
    {
        "entryId": str,
        "propertyValues": Sequence[AssetPropertyValueTypeDef],
    },
)
_OptionalPutAssetPropertyValueEntryTypeDef = TypedDict(
    "_OptionalPutAssetPropertyValueEntryTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
    },
    total=False,
)


class PutAssetPropertyValueEntryTypeDef(
    _RequiredPutAssetPropertyValueEntryTypeDef, _OptionalPutAssetPropertyValueEntryTypeDef
):
    pass


GetInterpolatedAssetPropertyValuesResponseTypeDef = TypedDict(
    "GetInterpolatedAssetPropertyValuesResponseTypeDef",
    {
        "interpolatedAssetPropertyValues": List[InterpolatedAssetPropertyValueTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDefaultEncryptionConfigurationResponseTypeDef = TypedDict(
    "DescribeDefaultEncryptionConfigurationResponseTypeDef",
    {
        "encryptionType": EncryptionTypeType,
        "kmsKeyArn": str,
        "configurationStatus": ConfigurationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDefaultEncryptionConfigurationResponseTypeDef = TypedDict(
    "PutDefaultEncryptionConfigurationResponseTypeDef",
    {
        "encryptionType": EncryptionTypeType,
        "kmsKeyArn": str,
        "configurationStatus": ConfigurationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdatePortalRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePortalRequestRequestTypeDef",
    {
        "portalId": str,
        "portalName": str,
        "portalContactEmail": str,
        "roleArn": str,
    },
)
_OptionalUpdatePortalRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePortalRequestRequestTypeDef",
    {
        "portalDescription": str,
        "portalLogoImage": ImageTypeDef,
        "clientToken": str,
        "notificationSenderEmail": str,
        "alarms": AlarmsTypeDef,
    },
    total=False,
)


class UpdatePortalRequestRequestTypeDef(
    _RequiredUpdatePortalRequestRequestTypeDef, _OptionalUpdatePortalRequestRequestTypeDef
):
    pass


DescribeStorageConfigurationResponseTypeDef = TypedDict(
    "DescribeStorageConfigurationResponseTypeDef",
    {
        "storageType": StorageTypeType,
        "multiLayerStorage": MultiLayerStorageTypeDef,
        "disassociatedDataStorage": DisassociatedDataStorageStateType,
        "retentionPeriod": RetentionPeriodTypeDef,
        "configurationStatus": ConfigurationStatusTypeDef,
        "lastUpdateDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutStorageConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutStorageConfigurationRequestRequestTypeDef",
    {
        "storageType": StorageTypeType,
    },
)
_OptionalPutStorageConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutStorageConfigurationRequestRequestTypeDef",
    {
        "multiLayerStorage": MultiLayerStorageTypeDef,
        "disassociatedDataStorage": DisassociatedDataStorageStateType,
        "retentionPeriod": RetentionPeriodTypeDef,
    },
    total=False,
)


class PutStorageConfigurationRequestRequestTypeDef(
    _RequiredPutStorageConfigurationRequestRequestTypeDef,
    _OptionalPutStorageConfigurationRequestRequestTypeDef,
):
    pass


PutStorageConfigurationResponseTypeDef = TypedDict(
    "PutStorageConfigurationResponseTypeDef",
    {
        "storageType": StorageTypeType,
        "multiLayerStorage": MultiLayerStorageTypeDef,
        "disassociatedDataStorage": DisassociatedDataStorageStateType,
        "retentionPeriod": RetentionPeriodTypeDef,
        "configurationStatus": ConfigurationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAssetModelStatusTypeDef = TypedDict(
    "_RequiredAssetModelStatusTypeDef",
    {
        "state": AssetModelStateType,
    },
)
_OptionalAssetModelStatusTypeDef = TypedDict(
    "_OptionalAssetModelStatusTypeDef",
    {
        "error": ErrorDetailsTypeDef,
    },
    total=False,
)


class AssetModelStatusTypeDef(_RequiredAssetModelStatusTypeDef, _OptionalAssetModelStatusTypeDef):
    pass


_RequiredAssetStatusTypeDef = TypedDict(
    "_RequiredAssetStatusTypeDef",
    {
        "state": AssetStateType,
    },
)
_OptionalAssetStatusTypeDef = TypedDict(
    "_OptionalAssetStatusTypeDef",
    {
        "error": ErrorDetailsTypeDef,
    },
    total=False,
)


class AssetStatusTypeDef(_RequiredAssetStatusTypeDef, _OptionalAssetStatusTypeDef):
    pass


MeasurementTypeDef = TypedDict(
    "MeasurementTypeDef",
    {
        "processingConfig": MeasurementProcessingConfigTypeDef,
    },
    total=False,
)

_RequiredTransformTypeDef = TypedDict(
    "_RequiredTransformTypeDef",
    {
        "expression": str,
        "variables": Sequence[ExpressionVariableTypeDef],
    },
)
_OptionalTransformTypeDef = TypedDict(
    "_OptionalTransformTypeDef",
    {
        "processingConfig": TransformProcessingConfigTypeDef,
    },
    total=False,
)


class TransformTypeDef(_RequiredTransformTypeDef, _OptionalTransformTypeDef):
    pass


_RequiredCreateGatewayRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGatewayRequestRequestTypeDef",
    {
        "gatewayName": str,
        "gatewayPlatform": GatewayPlatformTypeDef,
    },
)
_OptionalCreateGatewayRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGatewayRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateGatewayRequestRequestTypeDef(
    _RequiredCreateGatewayRequestRequestTypeDef, _OptionalCreateGatewayRequestRequestTypeDef
):
    pass


DescribeGatewayResponseTypeDef = TypedDict(
    "DescribeGatewayResponseTypeDef",
    {
        "gatewayId": str,
        "gatewayName": str,
        "gatewayArn": str,
        "gatewayPlatform": GatewayPlatformTypeDef,
        "gatewayCapabilitySummaries": List[GatewayCapabilitySummaryTypeDef],
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGatewaySummaryTypeDef = TypedDict(
    "_RequiredGatewaySummaryTypeDef",
    {
        "gatewayId": str,
        "gatewayName": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
    },
)
_OptionalGatewaySummaryTypeDef = TypedDict(
    "_OptionalGatewaySummaryTypeDef",
    {
        "gatewayPlatform": GatewayPlatformTypeDef,
        "gatewayCapabilitySummaries": List[GatewayCapabilitySummaryTypeDef],
    },
    total=False,
)


class GatewaySummaryTypeDef(_RequiredGatewaySummaryTypeDef, _OptionalGatewaySummaryTypeDef):
    pass


_RequiredMetricTypeDef = TypedDict(
    "_RequiredMetricTypeDef",
    {
        "expression": str,
        "variables": Sequence[ExpressionVariableTypeDef],
        "window": MetricWindowTypeDef,
    },
)
_OptionalMetricTypeDef = TypedDict(
    "_OptionalMetricTypeDef",
    {
        "processingConfig": MetricProcessingConfigTypeDef,
    },
    total=False,
)


class MetricTypeDef(_RequiredMetricTypeDef, _OptionalMetricTypeDef):
    pass


CreatePortalResponseTypeDef = TypedDict(
    "CreatePortalResponseTypeDef",
    {
        "portalId": str,
        "portalArn": str,
        "portalStartUrl": str,
        "portalStatus": PortalStatusTypeDef,
        "ssoApplicationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeletePortalResponseTypeDef = TypedDict(
    "DeletePortalResponseTypeDef",
    {
        "portalStatus": PortalStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePortalResponseTypeDef = TypedDict(
    "DescribePortalResponseTypeDef",
    {
        "portalId": str,
        "portalArn": str,
        "portalName": str,
        "portalDescription": str,
        "portalClientId": str,
        "portalStartUrl": str,
        "portalContactEmail": str,
        "portalStatus": PortalStatusTypeDef,
        "portalCreationDate": datetime,
        "portalLastUpdateDate": datetime,
        "portalLogoImageLocation": ImageLocationTypeDef,
        "roleArn": str,
        "portalAuthMode": AuthModeType,
        "notificationSenderEmail": str,
        "alarms": AlarmsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPortalSummaryTypeDef = TypedDict(
    "_RequiredPortalSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "startUrl": str,
        "status": PortalStatusTypeDef,
    },
)
_OptionalPortalSummaryTypeDef = TypedDict(
    "_OptionalPortalSummaryTypeDef",
    {
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "roleArn": str,
    },
    total=False,
)


class PortalSummaryTypeDef(_RequiredPortalSummaryTypeDef, _OptionalPortalSummaryTypeDef):
    pass


UpdatePortalResponseTypeDef = TypedDict(
    "UpdatePortalResponseTypeDef",
    {
        "portalStatus": PortalStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAccessPolicySummaryTypeDef = TypedDict(
    "_RequiredAccessPolicySummaryTypeDef",
    {
        "id": str,
        "identity": IdentityTypeDef,
        "resource": ResourceTypeDef,
        "permission": PermissionType,
    },
)
_OptionalAccessPolicySummaryTypeDef = TypedDict(
    "_OptionalAccessPolicySummaryTypeDef",
    {
        "creationDate": datetime,
        "lastUpdateDate": datetime,
    },
    total=False,
)


class AccessPolicySummaryTypeDef(
    _RequiredAccessPolicySummaryTypeDef, _OptionalAccessPolicySummaryTypeDef
):
    pass


_RequiredCreateAccessPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAccessPolicyRequestRequestTypeDef",
    {
        "accessPolicyIdentity": IdentityTypeDef,
        "accessPolicyResource": ResourceTypeDef,
        "accessPolicyPermission": PermissionType,
    },
)
_OptionalCreateAccessPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAccessPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateAccessPolicyRequestRequestTypeDef(
    _RequiredCreateAccessPolicyRequestRequestTypeDef,
    _OptionalCreateAccessPolicyRequestRequestTypeDef,
):
    pass


DescribeAccessPolicyResponseTypeDef = TypedDict(
    "DescribeAccessPolicyResponseTypeDef",
    {
        "accessPolicyId": str,
        "accessPolicyArn": str,
        "accessPolicyIdentity": IdentityTypeDef,
        "accessPolicyResource": ResourceTypeDef,
        "accessPolicyPermission": PermissionType,
        "accessPolicyCreationDate": datetime,
        "accessPolicyLastUpdateDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateAccessPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAccessPolicyRequestRequestTypeDef",
    {
        "accessPolicyId": str,
        "accessPolicyIdentity": IdentityTypeDef,
        "accessPolicyResource": ResourceTypeDef,
        "accessPolicyPermission": PermissionType,
    },
)
_OptionalUpdateAccessPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAccessPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class UpdateAccessPolicyRequestRequestTypeDef(
    _RequiredUpdateAccessPolicyRequestRequestTypeDef,
    _OptionalUpdateAccessPolicyRequestRequestTypeDef,
):
    pass


BatchGetAssetPropertyAggregatesResponseTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesResponseTypeDef",
    {
        "errorEntries": List[BatchGetAssetPropertyAggregatesErrorEntryTypeDef],
        "successEntries": List[BatchGetAssetPropertyAggregatesSuccessEntryTypeDef],
        "skippedEntries": List[BatchGetAssetPropertyAggregatesSkippedEntryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutAssetPropertyValueResponseTypeDef = TypedDict(
    "BatchPutAssetPropertyValueResponseTypeDef",
    {
        "errorEntries": List[BatchPutAssetPropertyErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetAssetPropertyValueHistoryResponseTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistoryResponseTypeDef",
    {
        "errorEntries": List[BatchGetAssetPropertyValueHistoryErrorEntryTypeDef],
        "successEntries": List[BatchGetAssetPropertyValueHistorySuccessEntryTypeDef],
        "skippedEntries": List[BatchGetAssetPropertyValueHistorySkippedEntryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetAssetPropertyValueResponseTypeDef = TypedDict(
    "BatchGetAssetPropertyValueResponseTypeDef",
    {
        "errorEntries": List[BatchGetAssetPropertyValueErrorEntryTypeDef],
        "successEntries": List[BatchGetAssetPropertyValueSuccessEntryTypeDef],
        "skippedEntries": List[BatchGetAssetPropertyValueSkippedEntryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutAssetPropertyValueRequestRequestTypeDef = TypedDict(
    "BatchPutAssetPropertyValueRequestRequestTypeDef",
    {
        "entries": Sequence[PutAssetPropertyValueEntryTypeDef],
    },
)

AssetModelSummaryTypeDef = TypedDict(
    "AssetModelSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetModelStatusTypeDef,
    },
)

CreateAssetModelResponseTypeDef = TypedDict(
    "CreateAssetModelResponseTypeDef",
    {
        "assetModelId": str,
        "assetModelArn": str,
        "assetModelStatus": AssetModelStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAssetModelResponseTypeDef = TypedDict(
    "DeleteAssetModelResponseTypeDef",
    {
        "assetModelStatus": AssetModelStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssetModelResponseTypeDef = TypedDict(
    "UpdateAssetModelResponseTypeDef",
    {
        "assetModelStatus": AssetModelStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAssetSummaryTypeDef = TypedDict(
    "_RequiredAssetSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "assetModelId": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetStatusTypeDef,
        "hierarchies": List[AssetHierarchyTypeDef],
    },
)
_OptionalAssetSummaryTypeDef = TypedDict(
    "_OptionalAssetSummaryTypeDef",
    {
        "description": str,
    },
    total=False,
)


class AssetSummaryTypeDef(_RequiredAssetSummaryTypeDef, _OptionalAssetSummaryTypeDef):
    pass


_RequiredAssociatedAssetsSummaryTypeDef = TypedDict(
    "_RequiredAssociatedAssetsSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "assetModelId": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetStatusTypeDef,
        "hierarchies": List[AssetHierarchyTypeDef],
    },
)
_OptionalAssociatedAssetsSummaryTypeDef = TypedDict(
    "_OptionalAssociatedAssetsSummaryTypeDef",
    {
        "description": str,
    },
    total=False,
)


class AssociatedAssetsSummaryTypeDef(
    _RequiredAssociatedAssetsSummaryTypeDef, _OptionalAssociatedAssetsSummaryTypeDef
):
    pass


CreateAssetResponseTypeDef = TypedDict(
    "CreateAssetResponseTypeDef",
    {
        "assetId": str,
        "assetArn": str,
        "assetStatus": AssetStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAssetResponseTypeDef = TypedDict(
    "DeleteAssetResponseTypeDef",
    {
        "assetStatus": AssetStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAssetResponseTypeDef = TypedDict(
    "DescribeAssetResponseTypeDef",
    {
        "assetId": str,
        "assetArn": str,
        "assetName": str,
        "assetModelId": str,
        "assetProperties": List[AssetPropertyTypeDef],
        "assetHierarchies": List[AssetHierarchyTypeDef],
        "assetCompositeModels": List[AssetCompositeModelTypeDef],
        "assetCreationDate": datetime,
        "assetLastUpdateDate": datetime,
        "assetStatus": AssetStatusTypeDef,
        "assetDescription": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssetResponseTypeDef = TypedDict(
    "UpdateAssetResponseTypeDef",
    {
        "assetStatus": AssetStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGatewaysResponseTypeDef = TypedDict(
    "ListGatewaysResponseTypeDef",
    {
        "gatewaySummaries": List[GatewaySummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PropertyTypeTypeDef = TypedDict(
    "PropertyTypeTypeDef",
    {
        "attribute": AttributeTypeDef,
        "measurement": MeasurementTypeDef,
        "transform": TransformTypeDef,
        "metric": MetricTypeDef,
    },
    total=False,
)

ListPortalsResponseTypeDef = TypedDict(
    "ListPortalsResponseTypeDef",
    {
        "portalSummaries": List[PortalSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccessPoliciesResponseTypeDef = TypedDict(
    "ListAccessPoliciesResponseTypeDef",
    {
        "accessPolicySummaries": List[AccessPolicySummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssetModelsResponseTypeDef = TypedDict(
    "ListAssetModelsResponseTypeDef",
    {
        "assetModelSummaries": List[AssetModelSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssetsResponseTypeDef = TypedDict(
    "ListAssetsResponseTypeDef",
    {
        "assetSummaries": List[AssetSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssociatedAssetsResponseTypeDef = TypedDict(
    "ListAssociatedAssetsResponseTypeDef",
    {
        "assetSummaries": List[AssociatedAssetsSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredAssetModelPropertyDefinitionTypeDef = TypedDict(
    "_RequiredAssetModelPropertyDefinitionTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypeTypeDef,
    },
)
_OptionalAssetModelPropertyDefinitionTypeDef = TypedDict(
    "_OptionalAssetModelPropertyDefinitionTypeDef",
    {
        "dataTypeSpec": str,
        "unit": str,
    },
    total=False,
)


class AssetModelPropertyDefinitionTypeDef(
    _RequiredAssetModelPropertyDefinitionTypeDef, _OptionalAssetModelPropertyDefinitionTypeDef
):
    pass


_RequiredAssetModelPropertyTypeDef = TypedDict(
    "_RequiredAssetModelPropertyTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypeTypeDef,
    },
)
_OptionalAssetModelPropertyTypeDef = TypedDict(
    "_OptionalAssetModelPropertyTypeDef",
    {
        "id": str,
        "dataTypeSpec": str,
        "unit": str,
    },
    total=False,
)


class AssetModelPropertyTypeDef(
    _RequiredAssetModelPropertyTypeDef, _OptionalAssetModelPropertyTypeDef
):
    pass


_RequiredPropertyTypeDef = TypedDict(
    "_RequiredPropertyTypeDef",
    {
        "id": str,
        "name": str,
        "dataType": PropertyDataTypeType,
    },
)
_OptionalPropertyTypeDef = TypedDict(
    "_OptionalPropertyTypeDef",
    {
        "alias": str,
        "notification": PropertyNotificationTypeDef,
        "unit": str,
        "type": PropertyTypeTypeDef,
    },
    total=False,
)


class PropertyTypeDef(_RequiredPropertyTypeDef, _OptionalPropertyTypeDef):
    pass


_RequiredAssetModelCompositeModelDefinitionTypeDef = TypedDict(
    "_RequiredAssetModelCompositeModelDefinitionTypeDef",
    {
        "name": str,
        "type": str,
    },
)
_OptionalAssetModelCompositeModelDefinitionTypeDef = TypedDict(
    "_OptionalAssetModelCompositeModelDefinitionTypeDef",
    {
        "description": str,
        "properties": Sequence[AssetModelPropertyDefinitionTypeDef],
    },
    total=False,
)


class AssetModelCompositeModelDefinitionTypeDef(
    _RequiredAssetModelCompositeModelDefinitionTypeDef,
    _OptionalAssetModelCompositeModelDefinitionTypeDef,
):
    pass


_RequiredAssetModelCompositeModelTypeDef = TypedDict(
    "_RequiredAssetModelCompositeModelTypeDef",
    {
        "name": str,
        "type": str,
    },
)
_OptionalAssetModelCompositeModelTypeDef = TypedDict(
    "_OptionalAssetModelCompositeModelTypeDef",
    {
        "description": str,
        "properties": List[AssetModelPropertyTypeDef],
    },
    total=False,
)


class AssetModelCompositeModelTypeDef(
    _RequiredAssetModelCompositeModelTypeDef, _OptionalAssetModelCompositeModelTypeDef
):
    pass


CompositeModelPropertyTypeDef = TypedDict(
    "CompositeModelPropertyTypeDef",
    {
        "name": str,
        "type": str,
        "assetProperty": PropertyTypeDef,
    },
)

_RequiredCreateAssetModelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAssetModelRequestRequestTypeDef",
    {
        "assetModelName": str,
    },
)
_OptionalCreateAssetModelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAssetModelRequestRequestTypeDef",
    {
        "assetModelDescription": str,
        "assetModelProperties": Sequence[AssetModelPropertyDefinitionTypeDef],
        "assetModelHierarchies": Sequence[AssetModelHierarchyDefinitionTypeDef],
        "assetModelCompositeModels": Sequence[AssetModelCompositeModelDefinitionTypeDef],
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateAssetModelRequestRequestTypeDef(
    _RequiredCreateAssetModelRequestRequestTypeDef, _OptionalCreateAssetModelRequestRequestTypeDef
):
    pass


DescribeAssetModelResponseTypeDef = TypedDict(
    "DescribeAssetModelResponseTypeDef",
    {
        "assetModelId": str,
        "assetModelArn": str,
        "assetModelName": str,
        "assetModelDescription": str,
        "assetModelProperties": List[AssetModelPropertyTypeDef],
        "assetModelHierarchies": List[AssetModelHierarchyTypeDef],
        "assetModelCompositeModels": List[AssetModelCompositeModelTypeDef],
        "assetModelCreationDate": datetime,
        "assetModelLastUpdateDate": datetime,
        "assetModelStatus": AssetModelStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateAssetModelRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAssetModelRequestRequestTypeDef",
    {
        "assetModelId": str,
        "assetModelName": str,
    },
)
_OptionalUpdateAssetModelRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAssetModelRequestRequestTypeDef",
    {
        "assetModelDescription": str,
        "assetModelProperties": Sequence[AssetModelPropertyTypeDef],
        "assetModelHierarchies": Sequence[AssetModelHierarchyTypeDef],
        "assetModelCompositeModels": Sequence[AssetModelCompositeModelTypeDef],
        "clientToken": str,
    },
    total=False,
)


class UpdateAssetModelRequestRequestTypeDef(
    _RequiredUpdateAssetModelRequestRequestTypeDef, _OptionalUpdateAssetModelRequestRequestTypeDef
):
    pass


DescribeAssetPropertyResponseTypeDef = TypedDict(
    "DescribeAssetPropertyResponseTypeDef",
    {
        "assetId": str,
        "assetName": str,
        "assetModelId": str,
        "assetProperty": PropertyTypeDef,
        "compositeModel": CompositeModelPropertyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
