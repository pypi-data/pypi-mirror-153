"""
Type annotations for kafkaconnect service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafkaconnect/type_defs/)

Usage::

    ```python
    from mypy_boto3_kafkaconnect.type_defs import VpcDescriptionTypeDef

    data: VpcDescriptionTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ConnectorStateType,
    CustomPluginContentTypeType,
    CustomPluginStateType,
    KafkaClusterClientAuthenticationTypeType,
    KafkaClusterEncryptionInTransitTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "VpcDescriptionTypeDef",
    "VpcTypeDef",
    "ScaleInPolicyDescriptionTypeDef",
    "ScaleOutPolicyDescriptionTypeDef",
    "ScaleInPolicyTypeDef",
    "ScaleOutPolicyTypeDef",
    "ScaleInPolicyUpdateTypeDef",
    "ScaleOutPolicyUpdateTypeDef",
    "ProvisionedCapacityDescriptionTypeDef",
    "ProvisionedCapacityTypeDef",
    "ProvisionedCapacityUpdateTypeDef",
    "CloudWatchLogsLogDeliveryDescriptionTypeDef",
    "CloudWatchLogsLogDeliveryTypeDef",
    "KafkaClusterClientAuthenticationDescriptionTypeDef",
    "KafkaClusterEncryptionInTransitDescriptionTypeDef",
    "WorkerConfigurationDescriptionTypeDef",
    "KafkaClusterClientAuthenticationTypeDef",
    "KafkaClusterEncryptionInTransitTypeDef",
    "WorkerConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "CreateWorkerConfigurationRequestRequestTypeDef",
    "WorkerConfigurationRevisionSummaryTypeDef",
    "CustomPluginDescriptionTypeDef",
    "CustomPluginFileDescriptionTypeDef",
    "S3LocationDescriptionTypeDef",
    "S3LocationTypeDef",
    "CustomPluginTypeDef",
    "DeleteConnectorRequestRequestTypeDef",
    "DeleteCustomPluginRequestRequestTypeDef",
    "DescribeConnectorRequestRequestTypeDef",
    "StateDescriptionTypeDef",
    "DescribeCustomPluginRequestRequestTypeDef",
    "DescribeWorkerConfigurationRequestRequestTypeDef",
    "WorkerConfigurationRevisionDescriptionTypeDef",
    "FirehoseLogDeliveryDescriptionTypeDef",
    "FirehoseLogDeliveryTypeDef",
    "PaginatorConfigTypeDef",
    "ListConnectorsRequestRequestTypeDef",
    "ListCustomPluginsRequestRequestTypeDef",
    "ListWorkerConfigurationsRequestRequestTypeDef",
    "S3LogDeliveryDescriptionTypeDef",
    "S3LogDeliveryTypeDef",
    "ApacheKafkaClusterDescriptionTypeDef",
    "ApacheKafkaClusterTypeDef",
    "AutoScalingDescriptionTypeDef",
    "AutoScalingTypeDef",
    "AutoScalingUpdateTypeDef",
    "CreateConnectorResponseTypeDef",
    "CreateCustomPluginResponseTypeDef",
    "DeleteConnectorResponseTypeDef",
    "DeleteCustomPluginResponseTypeDef",
    "UpdateConnectorResponseTypeDef",
    "CreateWorkerConfigurationResponseTypeDef",
    "WorkerConfigurationSummaryTypeDef",
    "PluginDescriptionTypeDef",
    "CustomPluginLocationDescriptionTypeDef",
    "CustomPluginLocationTypeDef",
    "PluginTypeDef",
    "DescribeWorkerConfigurationResponseTypeDef",
    "ListConnectorsRequestListConnectorsPaginateTypeDef",
    "ListCustomPluginsRequestListCustomPluginsPaginateTypeDef",
    "ListWorkerConfigurationsRequestListWorkerConfigurationsPaginateTypeDef",
    "WorkerLogDeliveryDescriptionTypeDef",
    "WorkerLogDeliveryTypeDef",
    "KafkaClusterDescriptionTypeDef",
    "KafkaClusterTypeDef",
    "CapacityDescriptionTypeDef",
    "CapacityTypeDef",
    "CapacityUpdateTypeDef",
    "ListWorkerConfigurationsResponseTypeDef",
    "CustomPluginRevisionSummaryTypeDef",
    "CreateCustomPluginRequestRequestTypeDef",
    "LogDeliveryDescriptionTypeDef",
    "LogDeliveryTypeDef",
    "UpdateConnectorRequestRequestTypeDef",
    "CustomPluginSummaryTypeDef",
    "DescribeCustomPluginResponseTypeDef",
    "ConnectorSummaryTypeDef",
    "DescribeConnectorResponseTypeDef",
    "CreateConnectorRequestRequestTypeDef",
    "ListCustomPluginsResponseTypeDef",
    "ListConnectorsResponseTypeDef",
)

VpcDescriptionTypeDef = TypedDict(
    "VpcDescriptionTypeDef",
    {
        "securityGroups": List[str],
        "subnets": List[str],
    },
    total=False,
)

_RequiredVpcTypeDef = TypedDict(
    "_RequiredVpcTypeDef",
    {
        "subnets": Sequence[str],
    },
)
_OptionalVpcTypeDef = TypedDict(
    "_OptionalVpcTypeDef",
    {
        "securityGroups": Sequence[str],
    },
    total=False,
)

class VpcTypeDef(_RequiredVpcTypeDef, _OptionalVpcTypeDef):
    pass

ScaleInPolicyDescriptionTypeDef = TypedDict(
    "ScaleInPolicyDescriptionTypeDef",
    {
        "cpuUtilizationPercentage": int,
    },
    total=False,
)

ScaleOutPolicyDescriptionTypeDef = TypedDict(
    "ScaleOutPolicyDescriptionTypeDef",
    {
        "cpuUtilizationPercentage": int,
    },
    total=False,
)

ScaleInPolicyTypeDef = TypedDict(
    "ScaleInPolicyTypeDef",
    {
        "cpuUtilizationPercentage": int,
    },
)

ScaleOutPolicyTypeDef = TypedDict(
    "ScaleOutPolicyTypeDef",
    {
        "cpuUtilizationPercentage": int,
    },
)

ScaleInPolicyUpdateTypeDef = TypedDict(
    "ScaleInPolicyUpdateTypeDef",
    {
        "cpuUtilizationPercentage": int,
    },
)

ScaleOutPolicyUpdateTypeDef = TypedDict(
    "ScaleOutPolicyUpdateTypeDef",
    {
        "cpuUtilizationPercentage": int,
    },
)

ProvisionedCapacityDescriptionTypeDef = TypedDict(
    "ProvisionedCapacityDescriptionTypeDef",
    {
        "mcuCount": int,
        "workerCount": int,
    },
    total=False,
)

ProvisionedCapacityTypeDef = TypedDict(
    "ProvisionedCapacityTypeDef",
    {
        "mcuCount": int,
        "workerCount": int,
    },
)

ProvisionedCapacityUpdateTypeDef = TypedDict(
    "ProvisionedCapacityUpdateTypeDef",
    {
        "mcuCount": int,
        "workerCount": int,
    },
)

CloudWatchLogsLogDeliveryDescriptionTypeDef = TypedDict(
    "CloudWatchLogsLogDeliveryDescriptionTypeDef",
    {
        "enabled": bool,
        "logGroup": str,
    },
    total=False,
)

_RequiredCloudWatchLogsLogDeliveryTypeDef = TypedDict(
    "_RequiredCloudWatchLogsLogDeliveryTypeDef",
    {
        "enabled": bool,
    },
)
_OptionalCloudWatchLogsLogDeliveryTypeDef = TypedDict(
    "_OptionalCloudWatchLogsLogDeliveryTypeDef",
    {
        "logGroup": str,
    },
    total=False,
)

class CloudWatchLogsLogDeliveryTypeDef(
    _RequiredCloudWatchLogsLogDeliveryTypeDef, _OptionalCloudWatchLogsLogDeliveryTypeDef
):
    pass

KafkaClusterClientAuthenticationDescriptionTypeDef = TypedDict(
    "KafkaClusterClientAuthenticationDescriptionTypeDef",
    {
        "authenticationType": KafkaClusterClientAuthenticationTypeType,
    },
    total=False,
)

KafkaClusterEncryptionInTransitDescriptionTypeDef = TypedDict(
    "KafkaClusterEncryptionInTransitDescriptionTypeDef",
    {
        "encryptionType": KafkaClusterEncryptionInTransitTypeType,
    },
    total=False,
)

WorkerConfigurationDescriptionTypeDef = TypedDict(
    "WorkerConfigurationDescriptionTypeDef",
    {
        "revision": int,
        "workerConfigurationArn": str,
    },
    total=False,
)

KafkaClusterClientAuthenticationTypeDef = TypedDict(
    "KafkaClusterClientAuthenticationTypeDef",
    {
        "authenticationType": KafkaClusterClientAuthenticationTypeType,
    },
)

KafkaClusterEncryptionInTransitTypeDef = TypedDict(
    "KafkaClusterEncryptionInTransitTypeDef",
    {
        "encryptionType": KafkaClusterEncryptionInTransitTypeType,
    },
)

WorkerConfigurationTypeDef = TypedDict(
    "WorkerConfigurationTypeDef",
    {
        "revision": int,
        "workerConfigurationArn": str,
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

_RequiredCreateWorkerConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWorkerConfigurationRequestRequestTypeDef",
    {
        "name": str,
        "propertiesFileContent": str,
    },
)
_OptionalCreateWorkerConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWorkerConfigurationRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)

class CreateWorkerConfigurationRequestRequestTypeDef(
    _RequiredCreateWorkerConfigurationRequestRequestTypeDef,
    _OptionalCreateWorkerConfigurationRequestRequestTypeDef,
):
    pass

WorkerConfigurationRevisionSummaryTypeDef = TypedDict(
    "WorkerConfigurationRevisionSummaryTypeDef",
    {
        "creationTime": datetime,
        "description": str,
        "revision": int,
    },
    total=False,
)

CustomPluginDescriptionTypeDef = TypedDict(
    "CustomPluginDescriptionTypeDef",
    {
        "customPluginArn": str,
        "revision": int,
    },
    total=False,
)

CustomPluginFileDescriptionTypeDef = TypedDict(
    "CustomPluginFileDescriptionTypeDef",
    {
        "fileMd5": str,
        "fileSize": int,
    },
    total=False,
)

S3LocationDescriptionTypeDef = TypedDict(
    "S3LocationDescriptionTypeDef",
    {
        "bucketArn": str,
        "fileKey": str,
        "objectVersion": str,
    },
    total=False,
)

_RequiredS3LocationTypeDef = TypedDict(
    "_RequiredS3LocationTypeDef",
    {
        "bucketArn": str,
        "fileKey": str,
    },
)
_OptionalS3LocationTypeDef = TypedDict(
    "_OptionalS3LocationTypeDef",
    {
        "objectVersion": str,
    },
    total=False,
)

class S3LocationTypeDef(_RequiredS3LocationTypeDef, _OptionalS3LocationTypeDef):
    pass

CustomPluginTypeDef = TypedDict(
    "CustomPluginTypeDef",
    {
        "customPluginArn": str,
        "revision": int,
    },
)

_RequiredDeleteConnectorRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteConnectorRequestRequestTypeDef",
    {
        "connectorArn": str,
    },
)
_OptionalDeleteConnectorRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteConnectorRequestRequestTypeDef",
    {
        "currentVersion": str,
    },
    total=False,
)

class DeleteConnectorRequestRequestTypeDef(
    _RequiredDeleteConnectorRequestRequestTypeDef, _OptionalDeleteConnectorRequestRequestTypeDef
):
    pass

DeleteCustomPluginRequestRequestTypeDef = TypedDict(
    "DeleteCustomPluginRequestRequestTypeDef",
    {
        "customPluginArn": str,
    },
)

DescribeConnectorRequestRequestTypeDef = TypedDict(
    "DescribeConnectorRequestRequestTypeDef",
    {
        "connectorArn": str,
    },
)

StateDescriptionTypeDef = TypedDict(
    "StateDescriptionTypeDef",
    {
        "code": str,
        "message": str,
    },
    total=False,
)

DescribeCustomPluginRequestRequestTypeDef = TypedDict(
    "DescribeCustomPluginRequestRequestTypeDef",
    {
        "customPluginArn": str,
    },
)

DescribeWorkerConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeWorkerConfigurationRequestRequestTypeDef",
    {
        "workerConfigurationArn": str,
    },
)

WorkerConfigurationRevisionDescriptionTypeDef = TypedDict(
    "WorkerConfigurationRevisionDescriptionTypeDef",
    {
        "creationTime": datetime,
        "description": str,
        "propertiesFileContent": str,
        "revision": int,
    },
    total=False,
)

FirehoseLogDeliveryDescriptionTypeDef = TypedDict(
    "FirehoseLogDeliveryDescriptionTypeDef",
    {
        "deliveryStream": str,
        "enabled": bool,
    },
    total=False,
)

_RequiredFirehoseLogDeliveryTypeDef = TypedDict(
    "_RequiredFirehoseLogDeliveryTypeDef",
    {
        "enabled": bool,
    },
)
_OptionalFirehoseLogDeliveryTypeDef = TypedDict(
    "_OptionalFirehoseLogDeliveryTypeDef",
    {
        "deliveryStream": str,
    },
    total=False,
)

class FirehoseLogDeliveryTypeDef(
    _RequiredFirehoseLogDeliveryTypeDef, _OptionalFirehoseLogDeliveryTypeDef
):
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

ListConnectorsRequestRequestTypeDef = TypedDict(
    "ListConnectorsRequestRequestTypeDef",
    {
        "connectorNamePrefix": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListCustomPluginsRequestRequestTypeDef = TypedDict(
    "ListCustomPluginsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListWorkerConfigurationsRequestRequestTypeDef = TypedDict(
    "ListWorkerConfigurationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

S3LogDeliveryDescriptionTypeDef = TypedDict(
    "S3LogDeliveryDescriptionTypeDef",
    {
        "bucket": str,
        "enabled": bool,
        "prefix": str,
    },
    total=False,
)

_RequiredS3LogDeliveryTypeDef = TypedDict(
    "_RequiredS3LogDeliveryTypeDef",
    {
        "enabled": bool,
    },
)
_OptionalS3LogDeliveryTypeDef = TypedDict(
    "_OptionalS3LogDeliveryTypeDef",
    {
        "bucket": str,
        "prefix": str,
    },
    total=False,
)

class S3LogDeliveryTypeDef(_RequiredS3LogDeliveryTypeDef, _OptionalS3LogDeliveryTypeDef):
    pass

ApacheKafkaClusterDescriptionTypeDef = TypedDict(
    "ApacheKafkaClusterDescriptionTypeDef",
    {
        "bootstrapServers": str,
        "vpc": VpcDescriptionTypeDef,
    },
    total=False,
)

ApacheKafkaClusterTypeDef = TypedDict(
    "ApacheKafkaClusterTypeDef",
    {
        "bootstrapServers": str,
        "vpc": VpcTypeDef,
    },
)

AutoScalingDescriptionTypeDef = TypedDict(
    "AutoScalingDescriptionTypeDef",
    {
        "maxWorkerCount": int,
        "mcuCount": int,
        "minWorkerCount": int,
        "scaleInPolicy": ScaleInPolicyDescriptionTypeDef,
        "scaleOutPolicy": ScaleOutPolicyDescriptionTypeDef,
    },
    total=False,
)

_RequiredAutoScalingTypeDef = TypedDict(
    "_RequiredAutoScalingTypeDef",
    {
        "maxWorkerCount": int,
        "mcuCount": int,
        "minWorkerCount": int,
    },
)
_OptionalAutoScalingTypeDef = TypedDict(
    "_OptionalAutoScalingTypeDef",
    {
        "scaleInPolicy": ScaleInPolicyTypeDef,
        "scaleOutPolicy": ScaleOutPolicyTypeDef,
    },
    total=False,
)

class AutoScalingTypeDef(_RequiredAutoScalingTypeDef, _OptionalAutoScalingTypeDef):
    pass

AutoScalingUpdateTypeDef = TypedDict(
    "AutoScalingUpdateTypeDef",
    {
        "maxWorkerCount": int,
        "mcuCount": int,
        "minWorkerCount": int,
        "scaleInPolicy": ScaleInPolicyUpdateTypeDef,
        "scaleOutPolicy": ScaleOutPolicyUpdateTypeDef,
    },
)

CreateConnectorResponseTypeDef = TypedDict(
    "CreateConnectorResponseTypeDef",
    {
        "connectorArn": str,
        "connectorName": str,
        "connectorState": ConnectorStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCustomPluginResponseTypeDef = TypedDict(
    "CreateCustomPluginResponseTypeDef",
    {
        "customPluginArn": str,
        "customPluginState": CustomPluginStateType,
        "name": str,
        "revision": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteConnectorResponseTypeDef = TypedDict(
    "DeleteConnectorResponseTypeDef",
    {
        "connectorArn": str,
        "connectorState": ConnectorStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteCustomPluginResponseTypeDef = TypedDict(
    "DeleteCustomPluginResponseTypeDef",
    {
        "customPluginArn": str,
        "customPluginState": CustomPluginStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateConnectorResponseTypeDef = TypedDict(
    "UpdateConnectorResponseTypeDef",
    {
        "connectorArn": str,
        "connectorState": ConnectorStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWorkerConfigurationResponseTypeDef = TypedDict(
    "CreateWorkerConfigurationResponseTypeDef",
    {
        "creationTime": datetime,
        "latestRevision": WorkerConfigurationRevisionSummaryTypeDef,
        "name": str,
        "workerConfigurationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

WorkerConfigurationSummaryTypeDef = TypedDict(
    "WorkerConfigurationSummaryTypeDef",
    {
        "creationTime": datetime,
        "description": str,
        "latestRevision": WorkerConfigurationRevisionSummaryTypeDef,
        "name": str,
        "workerConfigurationArn": str,
    },
    total=False,
)

PluginDescriptionTypeDef = TypedDict(
    "PluginDescriptionTypeDef",
    {
        "customPlugin": CustomPluginDescriptionTypeDef,
    },
    total=False,
)

CustomPluginLocationDescriptionTypeDef = TypedDict(
    "CustomPluginLocationDescriptionTypeDef",
    {
        "s3Location": S3LocationDescriptionTypeDef,
    },
    total=False,
)

CustomPluginLocationTypeDef = TypedDict(
    "CustomPluginLocationTypeDef",
    {
        "s3Location": S3LocationTypeDef,
    },
)

PluginTypeDef = TypedDict(
    "PluginTypeDef",
    {
        "customPlugin": CustomPluginTypeDef,
    },
)

DescribeWorkerConfigurationResponseTypeDef = TypedDict(
    "DescribeWorkerConfigurationResponseTypeDef",
    {
        "creationTime": datetime,
        "description": str,
        "latestRevision": WorkerConfigurationRevisionDescriptionTypeDef,
        "name": str,
        "workerConfigurationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConnectorsRequestListConnectorsPaginateTypeDef = TypedDict(
    "ListConnectorsRequestListConnectorsPaginateTypeDef",
    {
        "connectorNamePrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListCustomPluginsRequestListCustomPluginsPaginateTypeDef = TypedDict(
    "ListCustomPluginsRequestListCustomPluginsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListWorkerConfigurationsRequestListWorkerConfigurationsPaginateTypeDef = TypedDict(
    "ListWorkerConfigurationsRequestListWorkerConfigurationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

WorkerLogDeliveryDescriptionTypeDef = TypedDict(
    "WorkerLogDeliveryDescriptionTypeDef",
    {
        "cloudWatchLogs": CloudWatchLogsLogDeliveryDescriptionTypeDef,
        "firehose": FirehoseLogDeliveryDescriptionTypeDef,
        "s3": S3LogDeliveryDescriptionTypeDef,
    },
    total=False,
)

WorkerLogDeliveryTypeDef = TypedDict(
    "WorkerLogDeliveryTypeDef",
    {
        "cloudWatchLogs": CloudWatchLogsLogDeliveryTypeDef,
        "firehose": FirehoseLogDeliveryTypeDef,
        "s3": S3LogDeliveryTypeDef,
    },
    total=False,
)

KafkaClusterDescriptionTypeDef = TypedDict(
    "KafkaClusterDescriptionTypeDef",
    {
        "apacheKafkaCluster": ApacheKafkaClusterDescriptionTypeDef,
    },
    total=False,
)

KafkaClusterTypeDef = TypedDict(
    "KafkaClusterTypeDef",
    {
        "apacheKafkaCluster": ApacheKafkaClusterTypeDef,
    },
)

CapacityDescriptionTypeDef = TypedDict(
    "CapacityDescriptionTypeDef",
    {
        "autoScaling": AutoScalingDescriptionTypeDef,
        "provisionedCapacity": ProvisionedCapacityDescriptionTypeDef,
    },
    total=False,
)

CapacityTypeDef = TypedDict(
    "CapacityTypeDef",
    {
        "autoScaling": AutoScalingTypeDef,
        "provisionedCapacity": ProvisionedCapacityTypeDef,
    },
    total=False,
)

CapacityUpdateTypeDef = TypedDict(
    "CapacityUpdateTypeDef",
    {
        "autoScaling": AutoScalingUpdateTypeDef,
        "provisionedCapacity": ProvisionedCapacityUpdateTypeDef,
    },
    total=False,
)

ListWorkerConfigurationsResponseTypeDef = TypedDict(
    "ListWorkerConfigurationsResponseTypeDef",
    {
        "nextToken": str,
        "workerConfigurations": List[WorkerConfigurationSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CustomPluginRevisionSummaryTypeDef = TypedDict(
    "CustomPluginRevisionSummaryTypeDef",
    {
        "contentType": CustomPluginContentTypeType,
        "creationTime": datetime,
        "description": str,
        "fileDescription": CustomPluginFileDescriptionTypeDef,
        "location": CustomPluginLocationDescriptionTypeDef,
        "revision": int,
    },
    total=False,
)

_RequiredCreateCustomPluginRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCustomPluginRequestRequestTypeDef",
    {
        "contentType": CustomPluginContentTypeType,
        "location": CustomPluginLocationTypeDef,
        "name": str,
    },
)
_OptionalCreateCustomPluginRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCustomPluginRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)

class CreateCustomPluginRequestRequestTypeDef(
    _RequiredCreateCustomPluginRequestRequestTypeDef,
    _OptionalCreateCustomPluginRequestRequestTypeDef,
):
    pass

LogDeliveryDescriptionTypeDef = TypedDict(
    "LogDeliveryDescriptionTypeDef",
    {
        "workerLogDelivery": WorkerLogDeliveryDescriptionTypeDef,
    },
    total=False,
)

LogDeliveryTypeDef = TypedDict(
    "LogDeliveryTypeDef",
    {
        "workerLogDelivery": WorkerLogDeliveryTypeDef,
    },
)

UpdateConnectorRequestRequestTypeDef = TypedDict(
    "UpdateConnectorRequestRequestTypeDef",
    {
        "capacity": CapacityUpdateTypeDef,
        "connectorArn": str,
        "currentVersion": str,
    },
)

CustomPluginSummaryTypeDef = TypedDict(
    "CustomPluginSummaryTypeDef",
    {
        "creationTime": datetime,
        "customPluginArn": str,
        "customPluginState": CustomPluginStateType,
        "description": str,
        "latestRevision": CustomPluginRevisionSummaryTypeDef,
        "name": str,
    },
    total=False,
)

DescribeCustomPluginResponseTypeDef = TypedDict(
    "DescribeCustomPluginResponseTypeDef",
    {
        "creationTime": datetime,
        "customPluginArn": str,
        "customPluginState": CustomPluginStateType,
        "description": str,
        "latestRevision": CustomPluginRevisionSummaryTypeDef,
        "name": str,
        "stateDescription": StateDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConnectorSummaryTypeDef = TypedDict(
    "ConnectorSummaryTypeDef",
    {
        "capacity": CapacityDescriptionTypeDef,
        "connectorArn": str,
        "connectorDescription": str,
        "connectorName": str,
        "connectorState": ConnectorStateType,
        "creationTime": datetime,
        "currentVersion": str,
        "kafkaCluster": KafkaClusterDescriptionTypeDef,
        "kafkaClusterClientAuthentication": KafkaClusterClientAuthenticationDescriptionTypeDef,
        "kafkaClusterEncryptionInTransit": KafkaClusterEncryptionInTransitDescriptionTypeDef,
        "kafkaConnectVersion": str,
        "logDelivery": LogDeliveryDescriptionTypeDef,
        "plugins": List[PluginDescriptionTypeDef],
        "serviceExecutionRoleArn": str,
        "workerConfiguration": WorkerConfigurationDescriptionTypeDef,
    },
    total=False,
)

DescribeConnectorResponseTypeDef = TypedDict(
    "DescribeConnectorResponseTypeDef",
    {
        "capacity": CapacityDescriptionTypeDef,
        "connectorArn": str,
        "connectorConfiguration": Dict[str, str],
        "connectorDescription": str,
        "connectorName": str,
        "connectorState": ConnectorStateType,
        "creationTime": datetime,
        "currentVersion": str,
        "kafkaCluster": KafkaClusterDescriptionTypeDef,
        "kafkaClusterClientAuthentication": KafkaClusterClientAuthenticationDescriptionTypeDef,
        "kafkaClusterEncryptionInTransit": KafkaClusterEncryptionInTransitDescriptionTypeDef,
        "kafkaConnectVersion": str,
        "logDelivery": LogDeliveryDescriptionTypeDef,
        "plugins": List[PluginDescriptionTypeDef],
        "serviceExecutionRoleArn": str,
        "stateDescription": StateDescriptionTypeDef,
        "workerConfiguration": WorkerConfigurationDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateConnectorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateConnectorRequestRequestTypeDef",
    {
        "capacity": CapacityTypeDef,
        "connectorConfiguration": Mapping[str, str],
        "connectorName": str,
        "kafkaCluster": KafkaClusterTypeDef,
        "kafkaClusterClientAuthentication": KafkaClusterClientAuthenticationTypeDef,
        "kafkaClusterEncryptionInTransit": KafkaClusterEncryptionInTransitTypeDef,
        "kafkaConnectVersion": str,
        "plugins": Sequence[PluginTypeDef],
        "serviceExecutionRoleArn": str,
    },
)
_OptionalCreateConnectorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateConnectorRequestRequestTypeDef",
    {
        "connectorDescription": str,
        "logDelivery": LogDeliveryTypeDef,
        "workerConfiguration": WorkerConfigurationTypeDef,
    },
    total=False,
)

class CreateConnectorRequestRequestTypeDef(
    _RequiredCreateConnectorRequestRequestTypeDef, _OptionalCreateConnectorRequestRequestTypeDef
):
    pass

ListCustomPluginsResponseTypeDef = TypedDict(
    "ListCustomPluginsResponseTypeDef",
    {
        "customPlugins": List[CustomPluginSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConnectorsResponseTypeDef = TypedDict(
    "ListConnectorsResponseTypeDef",
    {
        "connectors": List[ConnectorSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
