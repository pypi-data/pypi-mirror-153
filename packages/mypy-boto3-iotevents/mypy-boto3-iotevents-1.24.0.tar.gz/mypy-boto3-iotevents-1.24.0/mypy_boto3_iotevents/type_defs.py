"""
Type annotations for iotevents service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotevents/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotevents.type_defs import AcknowledgeFlowTypeDef

    data: AcknowledgeFlowTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AlarmModelVersionStatusType,
    AnalysisResultLevelType,
    AnalysisStatusType,
    ComparisonOperatorType,
    DetectorModelVersionStatusType,
    EvaluationMethodType,
    InputStatusType,
    LoggingLevelType,
    PayloadTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AcknowledgeFlowTypeDef",
    "ClearTimerActionTypeDef",
    "ResetTimerActionTypeDef",
    "SetTimerActionTypeDef",
    "SetVariableActionTypeDef",
    "InitializationConfigurationTypeDef",
    "AlarmModelSummaryTypeDef",
    "AlarmModelVersionSummaryTypeDef",
    "SimpleRuleTypeDef",
    "AnalysisResultLocationTypeDef",
    "AssetPropertyTimestampTypeDef",
    "AssetPropertyVariantTypeDef",
    "AttributeTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "DetectorModelConfigurationTypeDef",
    "InputConfigurationTypeDef",
    "DeleteAlarmModelRequestRequestTypeDef",
    "DeleteDetectorModelRequestRequestTypeDef",
    "DeleteInputRequestRequestTypeDef",
    "DescribeAlarmModelRequestRequestTypeDef",
    "DescribeDetectorModelAnalysisRequestRequestTypeDef",
    "DescribeDetectorModelRequestRequestTypeDef",
    "DescribeInputRequestRequestTypeDef",
    "DetectorDebugOptionTypeDef",
    "DetectorModelSummaryTypeDef",
    "DetectorModelVersionSummaryTypeDef",
    "PayloadTypeDef",
    "EmailContentTypeDef",
    "GetDetectorModelAnalysisResultsRequestRequestTypeDef",
    "IotEventsInputIdentifierTypeDef",
    "InputSummaryTypeDef",
    "IotSiteWiseAssetModelPropertyIdentifierTypeDef",
    "ListAlarmModelVersionsRequestRequestTypeDef",
    "ListAlarmModelsRequestRequestTypeDef",
    "ListDetectorModelVersionsRequestRequestTypeDef",
    "ListDetectorModelsRequestRequestTypeDef",
    "RoutedResourceTypeDef",
    "ListInputsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "SSOIdentityTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AlarmCapabilitiesTypeDef",
    "AlarmRuleTypeDef",
    "AnalysisResultTypeDef",
    "AssetPropertyValueTypeDef",
    "InputDefinitionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateAlarmModelResponseTypeDef",
    "DescribeDetectorModelAnalysisResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListAlarmModelVersionsResponseTypeDef",
    "ListAlarmModelsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartDetectorModelAnalysisResponseTypeDef",
    "UpdateAlarmModelResponseTypeDef",
    "CreateDetectorModelResponseTypeDef",
    "UpdateDetectorModelResponseTypeDef",
    "CreateInputResponseTypeDef",
    "UpdateInputResponseTypeDef",
    "LoggingOptionsTypeDef",
    "ListDetectorModelsResponseTypeDef",
    "ListDetectorModelVersionsResponseTypeDef",
    "DynamoDBActionTypeDef",
    "DynamoDBv2ActionTypeDef",
    "FirehoseActionTypeDef",
    "IotEventsActionTypeDef",
    "IotTopicPublishActionTypeDef",
    "LambdaActionTypeDef",
    "SNSTopicPublishActionTypeDef",
    "SqsActionTypeDef",
    "ListInputsResponseTypeDef",
    "IotSiteWiseInputIdentifierTypeDef",
    "ListInputRoutingsResponseTypeDef",
    "RecipientDetailTypeDef",
    "GetDetectorModelAnalysisResultsResponseTypeDef",
    "IotSiteWiseActionTypeDef",
    "CreateInputRequestRequestTypeDef",
    "InputTypeDef",
    "UpdateInputRequestRequestTypeDef",
    "DescribeLoggingOptionsResponseTypeDef",
    "PutLoggingOptionsRequestRequestTypeDef",
    "NotificationTargetActionsTypeDef",
    "InputIdentifierTypeDef",
    "EmailRecipientsTypeDef",
    "SMSConfigurationTypeDef",
    "ActionTypeDef",
    "AlarmActionTypeDef",
    "DescribeInputResponseTypeDef",
    "ListInputRoutingsRequestRequestTypeDef",
    "EmailConfigurationTypeDef",
    "EventTypeDef",
    "TransitionEventTypeDef",
    "AlarmEventActionsTypeDef",
    "NotificationActionTypeDef",
    "OnEnterLifecycleTypeDef",
    "OnExitLifecycleTypeDef",
    "OnInputLifecycleTypeDef",
    "AlarmNotificationTypeDef",
    "StateTypeDef",
    "CreateAlarmModelRequestRequestTypeDef",
    "DescribeAlarmModelResponseTypeDef",
    "UpdateAlarmModelRequestRequestTypeDef",
    "DetectorModelDefinitionTypeDef",
    "CreateDetectorModelRequestRequestTypeDef",
    "DetectorModelTypeDef",
    "StartDetectorModelAnalysisRequestRequestTypeDef",
    "UpdateDetectorModelRequestRequestTypeDef",
    "DescribeDetectorModelResponseTypeDef",
)

AcknowledgeFlowTypeDef = TypedDict(
    "AcknowledgeFlowTypeDef",
    {
        "enabled": bool,
    },
)

ClearTimerActionTypeDef = TypedDict(
    "ClearTimerActionTypeDef",
    {
        "timerName": str,
    },
)

ResetTimerActionTypeDef = TypedDict(
    "ResetTimerActionTypeDef",
    {
        "timerName": str,
    },
)

_RequiredSetTimerActionTypeDef = TypedDict(
    "_RequiredSetTimerActionTypeDef",
    {
        "timerName": str,
    },
)
_OptionalSetTimerActionTypeDef = TypedDict(
    "_OptionalSetTimerActionTypeDef",
    {
        "seconds": int,
        "durationExpression": str,
    },
    total=False,
)


class SetTimerActionTypeDef(_RequiredSetTimerActionTypeDef, _OptionalSetTimerActionTypeDef):
    pass


SetVariableActionTypeDef = TypedDict(
    "SetVariableActionTypeDef",
    {
        "variableName": str,
        "value": str,
    },
)

InitializationConfigurationTypeDef = TypedDict(
    "InitializationConfigurationTypeDef",
    {
        "disabledOnInitialization": bool,
    },
)

AlarmModelSummaryTypeDef = TypedDict(
    "AlarmModelSummaryTypeDef",
    {
        "creationTime": datetime,
        "alarmModelDescription": str,
        "alarmModelName": str,
    },
    total=False,
)

AlarmModelVersionSummaryTypeDef = TypedDict(
    "AlarmModelVersionSummaryTypeDef",
    {
        "alarmModelName": str,
        "alarmModelArn": str,
        "alarmModelVersion": str,
        "roleArn": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "status": AlarmModelVersionStatusType,
        "statusMessage": str,
    },
    total=False,
)

SimpleRuleTypeDef = TypedDict(
    "SimpleRuleTypeDef",
    {
        "inputProperty": str,
        "comparisonOperator": ComparisonOperatorType,
        "threshold": str,
    },
)

AnalysisResultLocationTypeDef = TypedDict(
    "AnalysisResultLocationTypeDef",
    {
        "path": str,
    },
    total=False,
)

_RequiredAssetPropertyTimestampTypeDef = TypedDict(
    "_RequiredAssetPropertyTimestampTypeDef",
    {
        "timeInSeconds": str,
    },
)
_OptionalAssetPropertyTimestampTypeDef = TypedDict(
    "_OptionalAssetPropertyTimestampTypeDef",
    {
        "offsetInNanos": str,
    },
    total=False,
)


class AssetPropertyTimestampTypeDef(
    _RequiredAssetPropertyTimestampTypeDef, _OptionalAssetPropertyTimestampTypeDef
):
    pass


AssetPropertyVariantTypeDef = TypedDict(
    "AssetPropertyVariantTypeDef",
    {
        "stringValue": str,
        "integerValue": str,
        "doubleValue": str,
        "booleanValue": str,
    },
    total=False,
)

AttributeTypeDef = TypedDict(
    "AttributeTypeDef",
    {
        "jsonPath": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
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

DetectorModelConfigurationTypeDef = TypedDict(
    "DetectorModelConfigurationTypeDef",
    {
        "detectorModelName": str,
        "detectorModelVersion": str,
        "detectorModelDescription": str,
        "detectorModelArn": str,
        "roleArn": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "status": DetectorModelVersionStatusType,
        "key": str,
        "evaluationMethod": EvaluationMethodType,
    },
    total=False,
)

_RequiredInputConfigurationTypeDef = TypedDict(
    "_RequiredInputConfigurationTypeDef",
    {
        "inputName": str,
        "inputArn": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "status": InputStatusType,
    },
)
_OptionalInputConfigurationTypeDef = TypedDict(
    "_OptionalInputConfigurationTypeDef",
    {
        "inputDescription": str,
    },
    total=False,
)


class InputConfigurationTypeDef(
    _RequiredInputConfigurationTypeDef, _OptionalInputConfigurationTypeDef
):
    pass


DeleteAlarmModelRequestRequestTypeDef = TypedDict(
    "DeleteAlarmModelRequestRequestTypeDef",
    {
        "alarmModelName": str,
    },
)

DeleteDetectorModelRequestRequestTypeDef = TypedDict(
    "DeleteDetectorModelRequestRequestTypeDef",
    {
        "detectorModelName": str,
    },
)

DeleteInputRequestRequestTypeDef = TypedDict(
    "DeleteInputRequestRequestTypeDef",
    {
        "inputName": str,
    },
)

_RequiredDescribeAlarmModelRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAlarmModelRequestRequestTypeDef",
    {
        "alarmModelName": str,
    },
)
_OptionalDescribeAlarmModelRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAlarmModelRequestRequestTypeDef",
    {
        "alarmModelVersion": str,
    },
    total=False,
)


class DescribeAlarmModelRequestRequestTypeDef(
    _RequiredDescribeAlarmModelRequestRequestTypeDef,
    _OptionalDescribeAlarmModelRequestRequestTypeDef,
):
    pass


DescribeDetectorModelAnalysisRequestRequestTypeDef = TypedDict(
    "DescribeDetectorModelAnalysisRequestRequestTypeDef",
    {
        "analysisId": str,
    },
)

_RequiredDescribeDetectorModelRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDetectorModelRequestRequestTypeDef",
    {
        "detectorModelName": str,
    },
)
_OptionalDescribeDetectorModelRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDetectorModelRequestRequestTypeDef",
    {
        "detectorModelVersion": str,
    },
    total=False,
)


class DescribeDetectorModelRequestRequestTypeDef(
    _RequiredDescribeDetectorModelRequestRequestTypeDef,
    _OptionalDescribeDetectorModelRequestRequestTypeDef,
):
    pass


DescribeInputRequestRequestTypeDef = TypedDict(
    "DescribeInputRequestRequestTypeDef",
    {
        "inputName": str,
    },
)

_RequiredDetectorDebugOptionTypeDef = TypedDict(
    "_RequiredDetectorDebugOptionTypeDef",
    {
        "detectorModelName": str,
    },
)
_OptionalDetectorDebugOptionTypeDef = TypedDict(
    "_OptionalDetectorDebugOptionTypeDef",
    {
        "keyValue": str,
    },
    total=False,
)


class DetectorDebugOptionTypeDef(
    _RequiredDetectorDebugOptionTypeDef, _OptionalDetectorDebugOptionTypeDef
):
    pass


DetectorModelSummaryTypeDef = TypedDict(
    "DetectorModelSummaryTypeDef",
    {
        "detectorModelName": str,
        "detectorModelDescription": str,
        "creationTime": datetime,
    },
    total=False,
)

DetectorModelVersionSummaryTypeDef = TypedDict(
    "DetectorModelVersionSummaryTypeDef",
    {
        "detectorModelName": str,
        "detectorModelVersion": str,
        "detectorModelArn": str,
        "roleArn": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "status": DetectorModelVersionStatusType,
        "evaluationMethod": EvaluationMethodType,
    },
    total=False,
)

PayloadTypeDef = TypedDict(
    "PayloadTypeDef",
    {
        "contentExpression": str,
        "type": PayloadTypeType,
    },
)

EmailContentTypeDef = TypedDict(
    "EmailContentTypeDef",
    {
        "subject": str,
        "additionalMessage": str,
    },
    total=False,
)

_RequiredGetDetectorModelAnalysisResultsRequestRequestTypeDef = TypedDict(
    "_RequiredGetDetectorModelAnalysisResultsRequestRequestTypeDef",
    {
        "analysisId": str,
    },
)
_OptionalGetDetectorModelAnalysisResultsRequestRequestTypeDef = TypedDict(
    "_OptionalGetDetectorModelAnalysisResultsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetDetectorModelAnalysisResultsRequestRequestTypeDef(
    _RequiredGetDetectorModelAnalysisResultsRequestRequestTypeDef,
    _OptionalGetDetectorModelAnalysisResultsRequestRequestTypeDef,
):
    pass


IotEventsInputIdentifierTypeDef = TypedDict(
    "IotEventsInputIdentifierTypeDef",
    {
        "inputName": str,
    },
)

InputSummaryTypeDef = TypedDict(
    "InputSummaryTypeDef",
    {
        "inputName": str,
        "inputDescription": str,
        "inputArn": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "status": InputStatusType,
    },
    total=False,
)

IotSiteWiseAssetModelPropertyIdentifierTypeDef = TypedDict(
    "IotSiteWiseAssetModelPropertyIdentifierTypeDef",
    {
        "assetModelId": str,
        "propertyId": str,
    },
)

_RequiredListAlarmModelVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListAlarmModelVersionsRequestRequestTypeDef",
    {
        "alarmModelName": str,
    },
)
_OptionalListAlarmModelVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListAlarmModelVersionsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAlarmModelVersionsRequestRequestTypeDef(
    _RequiredListAlarmModelVersionsRequestRequestTypeDef,
    _OptionalListAlarmModelVersionsRequestRequestTypeDef,
):
    pass


ListAlarmModelsRequestRequestTypeDef = TypedDict(
    "ListAlarmModelsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListDetectorModelVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListDetectorModelVersionsRequestRequestTypeDef",
    {
        "detectorModelName": str,
    },
)
_OptionalListDetectorModelVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListDetectorModelVersionsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListDetectorModelVersionsRequestRequestTypeDef(
    _RequiredListDetectorModelVersionsRequestRequestTypeDef,
    _OptionalListDetectorModelVersionsRequestRequestTypeDef,
):
    pass


ListDetectorModelsRequestRequestTypeDef = TypedDict(
    "ListDetectorModelsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

RoutedResourceTypeDef = TypedDict(
    "RoutedResourceTypeDef",
    {
        "name": str,
        "arn": str,
    },
    total=False,
)

ListInputsRequestRequestTypeDef = TypedDict(
    "ListInputsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

_RequiredSSOIdentityTypeDef = TypedDict(
    "_RequiredSSOIdentityTypeDef",
    {
        "identityStoreId": str,
    },
)
_OptionalSSOIdentityTypeDef = TypedDict(
    "_OptionalSSOIdentityTypeDef",
    {
        "userId": str,
    },
    total=False,
)


class SSOIdentityTypeDef(_RequiredSSOIdentityTypeDef, _OptionalSSOIdentityTypeDef):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

AlarmCapabilitiesTypeDef = TypedDict(
    "AlarmCapabilitiesTypeDef",
    {
        "initializationConfiguration": InitializationConfigurationTypeDef,
        "acknowledgeFlow": AcknowledgeFlowTypeDef,
    },
    total=False,
)

AlarmRuleTypeDef = TypedDict(
    "AlarmRuleTypeDef",
    {
        "simpleRule": SimpleRuleTypeDef,
    },
    total=False,
)

AnalysisResultTypeDef = TypedDict(
    "AnalysisResultTypeDef",
    {
        "type": str,
        "level": AnalysisResultLevelType,
        "message": str,
        "locations": List[AnalysisResultLocationTypeDef],
    },
    total=False,
)

AssetPropertyValueTypeDef = TypedDict(
    "AssetPropertyValueTypeDef",
    {
        "value": AssetPropertyVariantTypeDef,
        "timestamp": AssetPropertyTimestampTypeDef,
        "quality": str,
    },
    total=False,
)

InputDefinitionTypeDef = TypedDict(
    "InputDefinitionTypeDef",
    {
        "attributes": Sequence[AttributeTypeDef],
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

CreateAlarmModelResponseTypeDef = TypedDict(
    "CreateAlarmModelResponseTypeDef",
    {
        "creationTime": datetime,
        "alarmModelArn": str,
        "alarmModelVersion": str,
        "lastUpdateTime": datetime,
        "status": AlarmModelVersionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDetectorModelAnalysisResponseTypeDef = TypedDict(
    "DescribeDetectorModelAnalysisResponseTypeDef",
    {
        "status": AnalysisStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAlarmModelVersionsResponseTypeDef = TypedDict(
    "ListAlarmModelVersionsResponseTypeDef",
    {
        "alarmModelVersionSummaries": List[AlarmModelVersionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAlarmModelsResponseTypeDef = TypedDict(
    "ListAlarmModelsResponseTypeDef",
    {
        "alarmModelSummaries": List[AlarmModelSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDetectorModelAnalysisResponseTypeDef = TypedDict(
    "StartDetectorModelAnalysisResponseTypeDef",
    {
        "analysisId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAlarmModelResponseTypeDef = TypedDict(
    "UpdateAlarmModelResponseTypeDef",
    {
        "creationTime": datetime,
        "alarmModelArn": str,
        "alarmModelVersion": str,
        "lastUpdateTime": datetime,
        "status": AlarmModelVersionStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDetectorModelResponseTypeDef = TypedDict(
    "CreateDetectorModelResponseTypeDef",
    {
        "detectorModelConfiguration": DetectorModelConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDetectorModelResponseTypeDef = TypedDict(
    "UpdateDetectorModelResponseTypeDef",
    {
        "detectorModelConfiguration": DetectorModelConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateInputResponseTypeDef = TypedDict(
    "CreateInputResponseTypeDef",
    {
        "inputConfiguration": InputConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateInputResponseTypeDef = TypedDict(
    "UpdateInputResponseTypeDef",
    {
        "inputConfiguration": InputConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredLoggingOptionsTypeDef = TypedDict(
    "_RequiredLoggingOptionsTypeDef",
    {
        "roleArn": str,
        "level": LoggingLevelType,
        "enabled": bool,
    },
)
_OptionalLoggingOptionsTypeDef = TypedDict(
    "_OptionalLoggingOptionsTypeDef",
    {
        "detectorDebugOptions": List[DetectorDebugOptionTypeDef],
    },
    total=False,
)


class LoggingOptionsTypeDef(_RequiredLoggingOptionsTypeDef, _OptionalLoggingOptionsTypeDef):
    pass


ListDetectorModelsResponseTypeDef = TypedDict(
    "ListDetectorModelsResponseTypeDef",
    {
        "detectorModelSummaries": List[DetectorModelSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDetectorModelVersionsResponseTypeDef = TypedDict(
    "ListDetectorModelVersionsResponseTypeDef",
    {
        "detectorModelVersionSummaries": List[DetectorModelVersionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDynamoDBActionTypeDef = TypedDict(
    "_RequiredDynamoDBActionTypeDef",
    {
        "hashKeyField": str,
        "hashKeyValue": str,
        "tableName": str,
    },
)
_OptionalDynamoDBActionTypeDef = TypedDict(
    "_OptionalDynamoDBActionTypeDef",
    {
        "hashKeyType": str,
        "rangeKeyType": str,
        "rangeKeyField": str,
        "rangeKeyValue": str,
        "operation": str,
        "payloadField": str,
        "payload": PayloadTypeDef,
    },
    total=False,
)


class DynamoDBActionTypeDef(_RequiredDynamoDBActionTypeDef, _OptionalDynamoDBActionTypeDef):
    pass


_RequiredDynamoDBv2ActionTypeDef = TypedDict(
    "_RequiredDynamoDBv2ActionTypeDef",
    {
        "tableName": str,
    },
)
_OptionalDynamoDBv2ActionTypeDef = TypedDict(
    "_OptionalDynamoDBv2ActionTypeDef",
    {
        "payload": PayloadTypeDef,
    },
    total=False,
)


class DynamoDBv2ActionTypeDef(_RequiredDynamoDBv2ActionTypeDef, _OptionalDynamoDBv2ActionTypeDef):
    pass


_RequiredFirehoseActionTypeDef = TypedDict(
    "_RequiredFirehoseActionTypeDef",
    {
        "deliveryStreamName": str,
    },
)
_OptionalFirehoseActionTypeDef = TypedDict(
    "_OptionalFirehoseActionTypeDef",
    {
        "separator": str,
        "payload": PayloadTypeDef,
    },
    total=False,
)


class FirehoseActionTypeDef(_RequiredFirehoseActionTypeDef, _OptionalFirehoseActionTypeDef):
    pass


_RequiredIotEventsActionTypeDef = TypedDict(
    "_RequiredIotEventsActionTypeDef",
    {
        "inputName": str,
    },
)
_OptionalIotEventsActionTypeDef = TypedDict(
    "_OptionalIotEventsActionTypeDef",
    {
        "payload": PayloadTypeDef,
    },
    total=False,
)


class IotEventsActionTypeDef(_RequiredIotEventsActionTypeDef, _OptionalIotEventsActionTypeDef):
    pass


_RequiredIotTopicPublishActionTypeDef = TypedDict(
    "_RequiredIotTopicPublishActionTypeDef",
    {
        "mqttTopic": str,
    },
)
_OptionalIotTopicPublishActionTypeDef = TypedDict(
    "_OptionalIotTopicPublishActionTypeDef",
    {
        "payload": PayloadTypeDef,
    },
    total=False,
)


class IotTopicPublishActionTypeDef(
    _RequiredIotTopicPublishActionTypeDef, _OptionalIotTopicPublishActionTypeDef
):
    pass


_RequiredLambdaActionTypeDef = TypedDict(
    "_RequiredLambdaActionTypeDef",
    {
        "functionArn": str,
    },
)
_OptionalLambdaActionTypeDef = TypedDict(
    "_OptionalLambdaActionTypeDef",
    {
        "payload": PayloadTypeDef,
    },
    total=False,
)


class LambdaActionTypeDef(_RequiredLambdaActionTypeDef, _OptionalLambdaActionTypeDef):
    pass


_RequiredSNSTopicPublishActionTypeDef = TypedDict(
    "_RequiredSNSTopicPublishActionTypeDef",
    {
        "targetArn": str,
    },
)
_OptionalSNSTopicPublishActionTypeDef = TypedDict(
    "_OptionalSNSTopicPublishActionTypeDef",
    {
        "payload": PayloadTypeDef,
    },
    total=False,
)


class SNSTopicPublishActionTypeDef(
    _RequiredSNSTopicPublishActionTypeDef, _OptionalSNSTopicPublishActionTypeDef
):
    pass


_RequiredSqsActionTypeDef = TypedDict(
    "_RequiredSqsActionTypeDef",
    {
        "queueUrl": str,
    },
)
_OptionalSqsActionTypeDef = TypedDict(
    "_OptionalSqsActionTypeDef",
    {
        "useBase64": bool,
        "payload": PayloadTypeDef,
    },
    total=False,
)


class SqsActionTypeDef(_RequiredSqsActionTypeDef, _OptionalSqsActionTypeDef):
    pass


ListInputsResponseTypeDef = TypedDict(
    "ListInputsResponseTypeDef",
    {
        "inputSummaries": List[InputSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IotSiteWiseInputIdentifierTypeDef = TypedDict(
    "IotSiteWiseInputIdentifierTypeDef",
    {
        "iotSiteWiseAssetModelPropertyIdentifier": IotSiteWiseAssetModelPropertyIdentifierTypeDef,
    },
    total=False,
)

ListInputRoutingsResponseTypeDef = TypedDict(
    "ListInputRoutingsResponseTypeDef",
    {
        "routedResources": List[RoutedResourceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RecipientDetailTypeDef = TypedDict(
    "RecipientDetailTypeDef",
    {
        "ssoIdentity": SSOIdentityTypeDef,
    },
    total=False,
)

GetDetectorModelAnalysisResultsResponseTypeDef = TypedDict(
    "GetDetectorModelAnalysisResultsResponseTypeDef",
    {
        "analysisResults": List[AnalysisResultTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IotSiteWiseActionTypeDef = TypedDict(
    "IotSiteWiseActionTypeDef",
    {
        "entryId": str,
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "propertyValue": AssetPropertyValueTypeDef,
    },
    total=False,
)

_RequiredCreateInputRequestRequestTypeDef = TypedDict(
    "_RequiredCreateInputRequestRequestTypeDef",
    {
        "inputName": str,
        "inputDefinition": InputDefinitionTypeDef,
    },
)
_OptionalCreateInputRequestRequestTypeDef = TypedDict(
    "_OptionalCreateInputRequestRequestTypeDef",
    {
        "inputDescription": str,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateInputRequestRequestTypeDef(
    _RequiredCreateInputRequestRequestTypeDef, _OptionalCreateInputRequestRequestTypeDef
):
    pass


InputTypeDef = TypedDict(
    "InputTypeDef",
    {
        "inputConfiguration": InputConfigurationTypeDef,
        "inputDefinition": InputDefinitionTypeDef,
    },
    total=False,
)

_RequiredUpdateInputRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateInputRequestRequestTypeDef",
    {
        "inputName": str,
        "inputDefinition": InputDefinitionTypeDef,
    },
)
_OptionalUpdateInputRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateInputRequestRequestTypeDef",
    {
        "inputDescription": str,
    },
    total=False,
)


class UpdateInputRequestRequestTypeDef(
    _RequiredUpdateInputRequestRequestTypeDef, _OptionalUpdateInputRequestRequestTypeDef
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

NotificationTargetActionsTypeDef = TypedDict(
    "NotificationTargetActionsTypeDef",
    {
        "lambdaAction": LambdaActionTypeDef,
    },
    total=False,
)

InputIdentifierTypeDef = TypedDict(
    "InputIdentifierTypeDef",
    {
        "iotEventsInputIdentifier": IotEventsInputIdentifierTypeDef,
        "iotSiteWiseInputIdentifier": IotSiteWiseInputIdentifierTypeDef,
    },
    total=False,
)

EmailRecipientsTypeDef = TypedDict(
    "EmailRecipientsTypeDef",
    {
        "to": Sequence[RecipientDetailTypeDef],
    },
    total=False,
)

_RequiredSMSConfigurationTypeDef = TypedDict(
    "_RequiredSMSConfigurationTypeDef",
    {
        "recipients": Sequence[RecipientDetailTypeDef],
    },
)
_OptionalSMSConfigurationTypeDef = TypedDict(
    "_OptionalSMSConfigurationTypeDef",
    {
        "senderId": str,
        "additionalMessage": str,
    },
    total=False,
)


class SMSConfigurationTypeDef(_RequiredSMSConfigurationTypeDef, _OptionalSMSConfigurationTypeDef):
    pass


ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "setVariable": SetVariableActionTypeDef,
        "sns": SNSTopicPublishActionTypeDef,
        "iotTopicPublish": IotTopicPublishActionTypeDef,
        "setTimer": SetTimerActionTypeDef,
        "clearTimer": ClearTimerActionTypeDef,
        "resetTimer": ResetTimerActionTypeDef,
        "lambda": LambdaActionTypeDef,
        "iotEvents": IotEventsActionTypeDef,
        "sqs": SqsActionTypeDef,
        "firehose": FirehoseActionTypeDef,
        "dynamoDB": DynamoDBActionTypeDef,
        "dynamoDBv2": DynamoDBv2ActionTypeDef,
        "iotSiteWise": IotSiteWiseActionTypeDef,
    },
    total=False,
)

AlarmActionTypeDef = TypedDict(
    "AlarmActionTypeDef",
    {
        "sns": SNSTopicPublishActionTypeDef,
        "iotTopicPublish": IotTopicPublishActionTypeDef,
        "lambda": LambdaActionTypeDef,
        "iotEvents": IotEventsActionTypeDef,
        "sqs": SqsActionTypeDef,
        "firehose": FirehoseActionTypeDef,
        "dynamoDB": DynamoDBActionTypeDef,
        "dynamoDBv2": DynamoDBv2ActionTypeDef,
        "iotSiteWise": IotSiteWiseActionTypeDef,
    },
    total=False,
)

DescribeInputResponseTypeDef = TypedDict(
    "DescribeInputResponseTypeDef",
    {
        "input": InputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListInputRoutingsRequestRequestTypeDef = TypedDict(
    "_RequiredListInputRoutingsRequestRequestTypeDef",
    {
        "inputIdentifier": InputIdentifierTypeDef,
    },
)
_OptionalListInputRoutingsRequestRequestTypeDef = TypedDict(
    "_OptionalListInputRoutingsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListInputRoutingsRequestRequestTypeDef(
    _RequiredListInputRoutingsRequestRequestTypeDef, _OptionalListInputRoutingsRequestRequestTypeDef
):
    pass


_RequiredEmailConfigurationTypeDef = TypedDict(
    "_RequiredEmailConfigurationTypeDef",
    {
        "from": str,
        "recipients": EmailRecipientsTypeDef,
    },
)
_OptionalEmailConfigurationTypeDef = TypedDict(
    "_OptionalEmailConfigurationTypeDef",
    {
        "content": EmailContentTypeDef,
    },
    total=False,
)


class EmailConfigurationTypeDef(
    _RequiredEmailConfigurationTypeDef, _OptionalEmailConfigurationTypeDef
):
    pass


_RequiredEventTypeDef = TypedDict(
    "_RequiredEventTypeDef",
    {
        "eventName": str,
    },
)
_OptionalEventTypeDef = TypedDict(
    "_OptionalEventTypeDef",
    {
        "condition": str,
        "actions": Sequence[ActionTypeDef],
    },
    total=False,
)


class EventTypeDef(_RequiredEventTypeDef, _OptionalEventTypeDef):
    pass


_RequiredTransitionEventTypeDef = TypedDict(
    "_RequiredTransitionEventTypeDef",
    {
        "eventName": str,
        "condition": str,
        "nextState": str,
    },
)
_OptionalTransitionEventTypeDef = TypedDict(
    "_OptionalTransitionEventTypeDef",
    {
        "actions": Sequence[ActionTypeDef],
    },
    total=False,
)


class TransitionEventTypeDef(_RequiredTransitionEventTypeDef, _OptionalTransitionEventTypeDef):
    pass


AlarmEventActionsTypeDef = TypedDict(
    "AlarmEventActionsTypeDef",
    {
        "alarmActions": Sequence[AlarmActionTypeDef],
    },
    total=False,
)

_RequiredNotificationActionTypeDef = TypedDict(
    "_RequiredNotificationActionTypeDef",
    {
        "action": NotificationTargetActionsTypeDef,
    },
)
_OptionalNotificationActionTypeDef = TypedDict(
    "_OptionalNotificationActionTypeDef",
    {
        "smsConfigurations": Sequence[SMSConfigurationTypeDef],
        "emailConfigurations": Sequence[EmailConfigurationTypeDef],
    },
    total=False,
)


class NotificationActionTypeDef(
    _RequiredNotificationActionTypeDef, _OptionalNotificationActionTypeDef
):
    pass


OnEnterLifecycleTypeDef = TypedDict(
    "OnEnterLifecycleTypeDef",
    {
        "events": Sequence[EventTypeDef],
    },
    total=False,
)

OnExitLifecycleTypeDef = TypedDict(
    "OnExitLifecycleTypeDef",
    {
        "events": Sequence[EventTypeDef],
    },
    total=False,
)

OnInputLifecycleTypeDef = TypedDict(
    "OnInputLifecycleTypeDef",
    {
        "events": Sequence[EventTypeDef],
        "transitionEvents": Sequence[TransitionEventTypeDef],
    },
    total=False,
)

AlarmNotificationTypeDef = TypedDict(
    "AlarmNotificationTypeDef",
    {
        "notificationActions": Sequence[NotificationActionTypeDef],
    },
    total=False,
)

_RequiredStateTypeDef = TypedDict(
    "_RequiredStateTypeDef",
    {
        "stateName": str,
    },
)
_OptionalStateTypeDef = TypedDict(
    "_OptionalStateTypeDef",
    {
        "onInput": OnInputLifecycleTypeDef,
        "onEnter": OnEnterLifecycleTypeDef,
        "onExit": OnExitLifecycleTypeDef,
    },
    total=False,
)


class StateTypeDef(_RequiredStateTypeDef, _OptionalStateTypeDef):
    pass


_RequiredCreateAlarmModelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAlarmModelRequestRequestTypeDef",
    {
        "alarmModelName": str,
        "roleArn": str,
        "alarmRule": AlarmRuleTypeDef,
    },
)
_OptionalCreateAlarmModelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAlarmModelRequestRequestTypeDef",
    {
        "alarmModelDescription": str,
        "tags": Sequence[TagTypeDef],
        "key": str,
        "severity": int,
        "alarmNotification": AlarmNotificationTypeDef,
        "alarmEventActions": AlarmEventActionsTypeDef,
        "alarmCapabilities": AlarmCapabilitiesTypeDef,
    },
    total=False,
)


class CreateAlarmModelRequestRequestTypeDef(
    _RequiredCreateAlarmModelRequestRequestTypeDef, _OptionalCreateAlarmModelRequestRequestTypeDef
):
    pass


DescribeAlarmModelResponseTypeDef = TypedDict(
    "DescribeAlarmModelResponseTypeDef",
    {
        "creationTime": datetime,
        "alarmModelArn": str,
        "alarmModelVersion": str,
        "lastUpdateTime": datetime,
        "status": AlarmModelVersionStatusType,
        "statusMessage": str,
        "alarmModelName": str,
        "alarmModelDescription": str,
        "roleArn": str,
        "key": str,
        "severity": int,
        "alarmRule": AlarmRuleTypeDef,
        "alarmNotification": AlarmNotificationTypeDef,
        "alarmEventActions": AlarmEventActionsTypeDef,
        "alarmCapabilities": AlarmCapabilitiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateAlarmModelRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAlarmModelRequestRequestTypeDef",
    {
        "alarmModelName": str,
        "roleArn": str,
        "alarmRule": AlarmRuleTypeDef,
    },
)
_OptionalUpdateAlarmModelRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAlarmModelRequestRequestTypeDef",
    {
        "alarmModelDescription": str,
        "severity": int,
        "alarmNotification": AlarmNotificationTypeDef,
        "alarmEventActions": AlarmEventActionsTypeDef,
        "alarmCapabilities": AlarmCapabilitiesTypeDef,
    },
    total=False,
)


class UpdateAlarmModelRequestRequestTypeDef(
    _RequiredUpdateAlarmModelRequestRequestTypeDef, _OptionalUpdateAlarmModelRequestRequestTypeDef
):
    pass


DetectorModelDefinitionTypeDef = TypedDict(
    "DetectorModelDefinitionTypeDef",
    {
        "states": Sequence[StateTypeDef],
        "initialStateName": str,
    },
)

_RequiredCreateDetectorModelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDetectorModelRequestRequestTypeDef",
    {
        "detectorModelName": str,
        "detectorModelDefinition": DetectorModelDefinitionTypeDef,
        "roleArn": str,
    },
)
_OptionalCreateDetectorModelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDetectorModelRequestRequestTypeDef",
    {
        "detectorModelDescription": str,
        "key": str,
        "tags": Sequence[TagTypeDef],
        "evaluationMethod": EvaluationMethodType,
    },
    total=False,
)


class CreateDetectorModelRequestRequestTypeDef(
    _RequiredCreateDetectorModelRequestRequestTypeDef,
    _OptionalCreateDetectorModelRequestRequestTypeDef,
):
    pass


DetectorModelTypeDef = TypedDict(
    "DetectorModelTypeDef",
    {
        "detectorModelDefinition": DetectorModelDefinitionTypeDef,
        "detectorModelConfiguration": DetectorModelConfigurationTypeDef,
    },
    total=False,
)

StartDetectorModelAnalysisRequestRequestTypeDef = TypedDict(
    "StartDetectorModelAnalysisRequestRequestTypeDef",
    {
        "detectorModelDefinition": DetectorModelDefinitionTypeDef,
    },
)

_RequiredUpdateDetectorModelRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDetectorModelRequestRequestTypeDef",
    {
        "detectorModelName": str,
        "detectorModelDefinition": DetectorModelDefinitionTypeDef,
        "roleArn": str,
    },
)
_OptionalUpdateDetectorModelRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDetectorModelRequestRequestTypeDef",
    {
        "detectorModelDescription": str,
        "evaluationMethod": EvaluationMethodType,
    },
    total=False,
)


class UpdateDetectorModelRequestRequestTypeDef(
    _RequiredUpdateDetectorModelRequestRequestTypeDef,
    _OptionalUpdateDetectorModelRequestRequestTypeDef,
):
    pass


DescribeDetectorModelResponseTypeDef = TypedDict(
    "DescribeDetectorModelResponseTypeDef",
    {
        "detectorModel": DetectorModelTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
