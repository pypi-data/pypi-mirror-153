"""
Type annotations for lex-models service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/type_defs/)

Usage::

    ```python
    from mypy_boto3_lex_models.type_defs import BotChannelAssociationTypeDef

    data: BotChannelAssociationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ChannelStatusType,
    ChannelTypeType,
    ContentTypeType,
    DestinationType,
    ExportStatusType,
    ExportTypeType,
    FulfillmentActivityTypeType,
    ImportStatusType,
    LocaleType,
    LogTypeType,
    MergeStrategyType,
    MigrationAlertTypeType,
    MigrationSortAttributeType,
    MigrationStatusType,
    MigrationStrategyType,
    ObfuscationSettingType,
    ProcessBehaviorType,
    ResourceTypeType,
    SlotConstraintType,
    SlotValueSelectionStrategyType,
    SortOrderType,
    StatusType,
    StatusTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BotChannelAssociationTypeDef",
    "BotMetadataTypeDef",
    "BuiltinIntentMetadataTypeDef",
    "BuiltinIntentSlotTypeDef",
    "BuiltinSlotTypeMetadataTypeDef",
    "CodeHookTypeDef",
    "LogSettingsRequestTypeDef",
    "LogSettingsResponseTypeDef",
    "CreateBotVersionRequestRequestTypeDef",
    "IntentTypeDef",
    "ResponseMetadataTypeDef",
    "CreateIntentVersionRequestRequestTypeDef",
    "InputContextTypeDef",
    "KendraConfigurationTypeDef",
    "OutputContextTypeDef",
    "CreateSlotTypeVersionRequestRequestTypeDef",
    "EnumerationValueTypeDef",
    "DeleteBotAliasRequestRequestTypeDef",
    "DeleteBotChannelAssociationRequestRequestTypeDef",
    "DeleteBotRequestRequestTypeDef",
    "DeleteBotVersionRequestRequestTypeDef",
    "DeleteIntentRequestRequestTypeDef",
    "DeleteIntentVersionRequestRequestTypeDef",
    "DeleteSlotTypeRequestRequestTypeDef",
    "DeleteSlotTypeVersionRequestRequestTypeDef",
    "DeleteUtterancesRequestRequestTypeDef",
    "GetBotAliasRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "GetBotAliasesRequestRequestTypeDef",
    "GetBotChannelAssociationRequestRequestTypeDef",
    "GetBotChannelAssociationsRequestRequestTypeDef",
    "GetBotRequestRequestTypeDef",
    "GetBotVersionsRequestRequestTypeDef",
    "GetBotsRequestRequestTypeDef",
    "GetBuiltinIntentRequestRequestTypeDef",
    "GetBuiltinIntentsRequestRequestTypeDef",
    "GetBuiltinSlotTypesRequestRequestTypeDef",
    "GetExportRequestRequestTypeDef",
    "GetImportRequestRequestTypeDef",
    "GetIntentRequestRequestTypeDef",
    "GetIntentVersionsRequestRequestTypeDef",
    "IntentMetadataTypeDef",
    "GetIntentsRequestRequestTypeDef",
    "GetMigrationRequestRequestTypeDef",
    "MigrationAlertTypeDef",
    "GetMigrationsRequestRequestTypeDef",
    "MigrationSummaryTypeDef",
    "GetSlotTypeRequestRequestTypeDef",
    "GetSlotTypeVersionsRequestRequestTypeDef",
    "SlotTypeMetadataTypeDef",
    "GetSlotTypesRequestRequestTypeDef",
    "GetUtterancesViewRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TagTypeDef",
    "MessageTypeDef",
    "SlotDefaultValueTypeDef",
    "SlotTypeRegexConfigurationTypeDef",
    "StartMigrationRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UtteranceDataTypeDef",
    "FulfillmentActivityTypeDef",
    "ConversationLogsRequestTypeDef",
    "ConversationLogsResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetBotChannelAssociationResponseTypeDef",
    "GetBotChannelAssociationsResponseTypeDef",
    "GetBotVersionsResponseTypeDef",
    "GetBotsResponseTypeDef",
    "GetBuiltinIntentResponseTypeDef",
    "GetBuiltinIntentsResponseTypeDef",
    "GetBuiltinSlotTypesResponseTypeDef",
    "GetExportResponseTypeDef",
    "GetImportResponseTypeDef",
    "StartMigrationResponseTypeDef",
    "GetBotAliasesRequestGetBotAliasesPaginateTypeDef",
    "GetBotChannelAssociationsRequestGetBotChannelAssociationsPaginateTypeDef",
    "GetBotVersionsRequestGetBotVersionsPaginateTypeDef",
    "GetBotsRequestGetBotsPaginateTypeDef",
    "GetBuiltinIntentsRequestGetBuiltinIntentsPaginateTypeDef",
    "GetBuiltinSlotTypesRequestGetBuiltinSlotTypesPaginateTypeDef",
    "GetIntentVersionsRequestGetIntentVersionsPaginateTypeDef",
    "GetIntentsRequestGetIntentsPaginateTypeDef",
    "GetSlotTypeVersionsRequestGetSlotTypeVersionsPaginateTypeDef",
    "GetSlotTypesRequestGetSlotTypesPaginateTypeDef",
    "GetIntentVersionsResponseTypeDef",
    "GetIntentsResponseTypeDef",
    "GetMigrationResponseTypeDef",
    "GetMigrationsResponseTypeDef",
    "GetSlotTypeVersionsResponseTypeDef",
    "GetSlotTypesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartImportRequestRequestTypeDef",
    "StartImportResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "PromptTypeDef",
    "StatementTypeDef",
    "SlotDefaultValueSpecTypeDef",
    "SlotTypeConfigurationTypeDef",
    "UtteranceListTypeDef",
    "PutBotAliasRequestRequestTypeDef",
    "BotAliasMetadataTypeDef",
    "GetBotAliasResponseTypeDef",
    "PutBotAliasResponseTypeDef",
    "CreateBotVersionResponseTypeDef",
    "FollowUpPromptTypeDef",
    "GetBotResponseTypeDef",
    "PutBotRequestRequestTypeDef",
    "PutBotResponseTypeDef",
    "SlotTypeDef",
    "CreateSlotTypeVersionResponseTypeDef",
    "GetSlotTypeResponseTypeDef",
    "PutSlotTypeRequestRequestTypeDef",
    "PutSlotTypeResponseTypeDef",
    "GetUtterancesViewResponseTypeDef",
    "GetBotAliasesResponseTypeDef",
    "CreateIntentVersionResponseTypeDef",
    "GetIntentResponseTypeDef",
    "PutIntentRequestRequestTypeDef",
    "PutIntentResponseTypeDef",
)

BotChannelAssociationTypeDef = TypedDict(
    "BotChannelAssociationTypeDef",
    {
        "name": str,
        "description": str,
        "botAlias": str,
        "botName": str,
        "createdDate": datetime,
        "type": ChannelTypeType,
        "botConfiguration": Dict[str, str],
        "status": ChannelStatusType,
        "failureReason": str,
    },
    total=False,
)

BotMetadataTypeDef = TypedDict(
    "BotMetadataTypeDef",
    {
        "name": str,
        "description": str,
        "status": StatusType,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
    },
    total=False,
)

BuiltinIntentMetadataTypeDef = TypedDict(
    "BuiltinIntentMetadataTypeDef",
    {
        "signature": str,
        "supportedLocales": List[LocaleType],
    },
    total=False,
)

BuiltinIntentSlotTypeDef = TypedDict(
    "BuiltinIntentSlotTypeDef",
    {
        "name": str,
    },
    total=False,
)

BuiltinSlotTypeMetadataTypeDef = TypedDict(
    "BuiltinSlotTypeMetadataTypeDef",
    {
        "signature": str,
        "supportedLocales": List[LocaleType],
    },
    total=False,
)

CodeHookTypeDef = TypedDict(
    "CodeHookTypeDef",
    {
        "uri": str,
        "messageVersion": str,
    },
)

_RequiredLogSettingsRequestTypeDef = TypedDict(
    "_RequiredLogSettingsRequestTypeDef",
    {
        "logType": LogTypeType,
        "destination": DestinationType,
        "resourceArn": str,
    },
)
_OptionalLogSettingsRequestTypeDef = TypedDict(
    "_OptionalLogSettingsRequestTypeDef",
    {
        "kmsKeyArn": str,
    },
    total=False,
)


class LogSettingsRequestTypeDef(
    _RequiredLogSettingsRequestTypeDef, _OptionalLogSettingsRequestTypeDef
):
    pass


LogSettingsResponseTypeDef = TypedDict(
    "LogSettingsResponseTypeDef",
    {
        "logType": LogTypeType,
        "destination": DestinationType,
        "kmsKeyArn": str,
        "resourceArn": str,
        "resourcePrefix": str,
    },
    total=False,
)

_RequiredCreateBotVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBotVersionRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateBotVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBotVersionRequestRequestTypeDef",
    {
        "checksum": str,
    },
    total=False,
)


class CreateBotVersionRequestRequestTypeDef(
    _RequiredCreateBotVersionRequestRequestTypeDef, _OptionalCreateBotVersionRequestRequestTypeDef
):
    pass


IntentTypeDef = TypedDict(
    "IntentTypeDef",
    {
        "intentName": str,
        "intentVersion": str,
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

_RequiredCreateIntentVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIntentVersionRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateIntentVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIntentVersionRequestRequestTypeDef",
    {
        "checksum": str,
    },
    total=False,
)


class CreateIntentVersionRequestRequestTypeDef(
    _RequiredCreateIntentVersionRequestRequestTypeDef,
    _OptionalCreateIntentVersionRequestRequestTypeDef,
):
    pass


InputContextTypeDef = TypedDict(
    "InputContextTypeDef",
    {
        "name": str,
    },
)

_RequiredKendraConfigurationTypeDef = TypedDict(
    "_RequiredKendraConfigurationTypeDef",
    {
        "kendraIndex": str,
        "role": str,
    },
)
_OptionalKendraConfigurationTypeDef = TypedDict(
    "_OptionalKendraConfigurationTypeDef",
    {
        "queryFilterString": str,
    },
    total=False,
)


class KendraConfigurationTypeDef(
    _RequiredKendraConfigurationTypeDef, _OptionalKendraConfigurationTypeDef
):
    pass


OutputContextTypeDef = TypedDict(
    "OutputContextTypeDef",
    {
        "name": str,
        "timeToLiveInSeconds": int,
        "turnsToLive": int,
    },
)

_RequiredCreateSlotTypeVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSlotTypeVersionRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateSlotTypeVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSlotTypeVersionRequestRequestTypeDef",
    {
        "checksum": str,
    },
    total=False,
)


class CreateSlotTypeVersionRequestRequestTypeDef(
    _RequiredCreateSlotTypeVersionRequestRequestTypeDef,
    _OptionalCreateSlotTypeVersionRequestRequestTypeDef,
):
    pass


_RequiredEnumerationValueTypeDef = TypedDict(
    "_RequiredEnumerationValueTypeDef",
    {
        "value": str,
    },
)
_OptionalEnumerationValueTypeDef = TypedDict(
    "_OptionalEnumerationValueTypeDef",
    {
        "synonyms": List[str],
    },
    total=False,
)


class EnumerationValueTypeDef(_RequiredEnumerationValueTypeDef, _OptionalEnumerationValueTypeDef):
    pass


DeleteBotAliasRequestRequestTypeDef = TypedDict(
    "DeleteBotAliasRequestRequestTypeDef",
    {
        "name": str,
        "botName": str,
    },
)

DeleteBotChannelAssociationRequestRequestTypeDef = TypedDict(
    "DeleteBotChannelAssociationRequestRequestTypeDef",
    {
        "name": str,
        "botName": str,
        "botAlias": str,
    },
)

DeleteBotRequestRequestTypeDef = TypedDict(
    "DeleteBotRequestRequestTypeDef",
    {
        "name": str,
    },
)

DeleteBotVersionRequestRequestTypeDef = TypedDict(
    "DeleteBotVersionRequestRequestTypeDef",
    {
        "name": str,
        "version": str,
    },
)

DeleteIntentRequestRequestTypeDef = TypedDict(
    "DeleteIntentRequestRequestTypeDef",
    {
        "name": str,
    },
)

DeleteIntentVersionRequestRequestTypeDef = TypedDict(
    "DeleteIntentVersionRequestRequestTypeDef",
    {
        "name": str,
        "version": str,
    },
)

DeleteSlotTypeRequestRequestTypeDef = TypedDict(
    "DeleteSlotTypeRequestRequestTypeDef",
    {
        "name": str,
    },
)

DeleteSlotTypeVersionRequestRequestTypeDef = TypedDict(
    "DeleteSlotTypeVersionRequestRequestTypeDef",
    {
        "name": str,
        "version": str,
    },
)

DeleteUtterancesRequestRequestTypeDef = TypedDict(
    "DeleteUtterancesRequestRequestTypeDef",
    {
        "botName": str,
        "userId": str,
    },
)

GetBotAliasRequestRequestTypeDef = TypedDict(
    "GetBotAliasRequestRequestTypeDef",
    {
        "name": str,
        "botName": str,
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

_RequiredGetBotAliasesRequestRequestTypeDef = TypedDict(
    "_RequiredGetBotAliasesRequestRequestTypeDef",
    {
        "botName": str,
    },
)
_OptionalGetBotAliasesRequestRequestTypeDef = TypedDict(
    "_OptionalGetBotAliasesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "nameContains": str,
    },
    total=False,
)


class GetBotAliasesRequestRequestTypeDef(
    _RequiredGetBotAliasesRequestRequestTypeDef, _OptionalGetBotAliasesRequestRequestTypeDef
):
    pass


GetBotChannelAssociationRequestRequestTypeDef = TypedDict(
    "GetBotChannelAssociationRequestRequestTypeDef",
    {
        "name": str,
        "botName": str,
        "botAlias": str,
    },
)

_RequiredGetBotChannelAssociationsRequestRequestTypeDef = TypedDict(
    "_RequiredGetBotChannelAssociationsRequestRequestTypeDef",
    {
        "botName": str,
        "botAlias": str,
    },
)
_OptionalGetBotChannelAssociationsRequestRequestTypeDef = TypedDict(
    "_OptionalGetBotChannelAssociationsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "nameContains": str,
    },
    total=False,
)


class GetBotChannelAssociationsRequestRequestTypeDef(
    _RequiredGetBotChannelAssociationsRequestRequestTypeDef,
    _OptionalGetBotChannelAssociationsRequestRequestTypeDef,
):
    pass


GetBotRequestRequestTypeDef = TypedDict(
    "GetBotRequestRequestTypeDef",
    {
        "name": str,
        "versionOrAlias": str,
    },
)

_RequiredGetBotVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredGetBotVersionsRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalGetBotVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalGetBotVersionsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetBotVersionsRequestRequestTypeDef(
    _RequiredGetBotVersionsRequestRequestTypeDef, _OptionalGetBotVersionsRequestRequestTypeDef
):
    pass


GetBotsRequestRequestTypeDef = TypedDict(
    "GetBotsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "nameContains": str,
    },
    total=False,
)

GetBuiltinIntentRequestRequestTypeDef = TypedDict(
    "GetBuiltinIntentRequestRequestTypeDef",
    {
        "signature": str,
    },
)

GetBuiltinIntentsRequestRequestTypeDef = TypedDict(
    "GetBuiltinIntentsRequestRequestTypeDef",
    {
        "locale": LocaleType,
        "signatureContains": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

GetBuiltinSlotTypesRequestRequestTypeDef = TypedDict(
    "GetBuiltinSlotTypesRequestRequestTypeDef",
    {
        "locale": LocaleType,
        "signatureContains": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

GetExportRequestRequestTypeDef = TypedDict(
    "GetExportRequestRequestTypeDef",
    {
        "name": str,
        "version": str,
        "resourceType": ResourceTypeType,
        "exportType": ExportTypeType,
    },
)

GetImportRequestRequestTypeDef = TypedDict(
    "GetImportRequestRequestTypeDef",
    {
        "importId": str,
    },
)

GetIntentRequestRequestTypeDef = TypedDict(
    "GetIntentRequestRequestTypeDef",
    {
        "name": str,
        "version": str,
    },
)

_RequiredGetIntentVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredGetIntentVersionsRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalGetIntentVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalGetIntentVersionsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetIntentVersionsRequestRequestTypeDef(
    _RequiredGetIntentVersionsRequestRequestTypeDef, _OptionalGetIntentVersionsRequestRequestTypeDef
):
    pass


IntentMetadataTypeDef = TypedDict(
    "IntentMetadataTypeDef",
    {
        "name": str,
        "description": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
    },
    total=False,
)

GetIntentsRequestRequestTypeDef = TypedDict(
    "GetIntentsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "nameContains": str,
    },
    total=False,
)

GetMigrationRequestRequestTypeDef = TypedDict(
    "GetMigrationRequestRequestTypeDef",
    {
        "migrationId": str,
    },
)

MigrationAlertTypeDef = TypedDict(
    "MigrationAlertTypeDef",
    {
        "type": MigrationAlertTypeType,
        "message": str,
        "details": List[str],
        "referenceURLs": List[str],
    },
    total=False,
)

GetMigrationsRequestRequestTypeDef = TypedDict(
    "GetMigrationsRequestRequestTypeDef",
    {
        "sortByAttribute": MigrationSortAttributeType,
        "sortByOrder": SortOrderType,
        "v1BotNameContains": str,
        "migrationStatusEquals": MigrationStatusType,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

MigrationSummaryTypeDef = TypedDict(
    "MigrationSummaryTypeDef",
    {
        "migrationId": str,
        "v1BotName": str,
        "v1BotVersion": str,
        "v1BotLocale": LocaleType,
        "v2BotId": str,
        "v2BotRole": str,
        "migrationStatus": MigrationStatusType,
        "migrationStrategy": MigrationStrategyType,
        "migrationTimestamp": datetime,
    },
    total=False,
)

GetSlotTypeRequestRequestTypeDef = TypedDict(
    "GetSlotTypeRequestRequestTypeDef",
    {
        "name": str,
        "version": str,
    },
)

_RequiredGetSlotTypeVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredGetSlotTypeVersionsRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalGetSlotTypeVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalGetSlotTypeVersionsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetSlotTypeVersionsRequestRequestTypeDef(
    _RequiredGetSlotTypeVersionsRequestRequestTypeDef,
    _OptionalGetSlotTypeVersionsRequestRequestTypeDef,
):
    pass


SlotTypeMetadataTypeDef = TypedDict(
    "SlotTypeMetadataTypeDef",
    {
        "name": str,
        "description": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
    },
    total=False,
)

GetSlotTypesRequestRequestTypeDef = TypedDict(
    "GetSlotTypesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "nameContains": str,
    },
    total=False,
)

GetUtterancesViewRequestRequestTypeDef = TypedDict(
    "GetUtterancesViewRequestRequestTypeDef",
    {
        "botName": str,
        "botVersions": Sequence[str],
        "statusType": StatusTypeType,
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

_RequiredMessageTypeDef = TypedDict(
    "_RequiredMessageTypeDef",
    {
        "contentType": ContentTypeType,
        "content": str,
    },
)
_OptionalMessageTypeDef = TypedDict(
    "_OptionalMessageTypeDef",
    {
        "groupNumber": int,
    },
    total=False,
)


class MessageTypeDef(_RequiredMessageTypeDef, _OptionalMessageTypeDef):
    pass


SlotDefaultValueTypeDef = TypedDict(
    "SlotDefaultValueTypeDef",
    {
        "defaultValue": str,
    },
)

SlotTypeRegexConfigurationTypeDef = TypedDict(
    "SlotTypeRegexConfigurationTypeDef",
    {
        "pattern": str,
    },
)

StartMigrationRequestRequestTypeDef = TypedDict(
    "StartMigrationRequestRequestTypeDef",
    {
        "v1BotName": str,
        "v1BotVersion": str,
        "v2BotName": str,
        "v2BotRole": str,
        "migrationStrategy": MigrationStrategyType,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UtteranceDataTypeDef = TypedDict(
    "UtteranceDataTypeDef",
    {
        "utteranceString": str,
        "count": int,
        "distinctUsers": int,
        "firstUtteredDate": datetime,
        "lastUtteredDate": datetime,
    },
    total=False,
)

_RequiredFulfillmentActivityTypeDef = TypedDict(
    "_RequiredFulfillmentActivityTypeDef",
    {
        "type": FulfillmentActivityTypeType,
    },
)
_OptionalFulfillmentActivityTypeDef = TypedDict(
    "_OptionalFulfillmentActivityTypeDef",
    {
        "codeHook": CodeHookTypeDef,
    },
    total=False,
)


class FulfillmentActivityTypeDef(
    _RequiredFulfillmentActivityTypeDef, _OptionalFulfillmentActivityTypeDef
):
    pass


ConversationLogsRequestTypeDef = TypedDict(
    "ConversationLogsRequestTypeDef",
    {
        "logSettings": Sequence[LogSettingsRequestTypeDef],
        "iamRoleArn": str,
    },
)

ConversationLogsResponseTypeDef = TypedDict(
    "ConversationLogsResponseTypeDef",
    {
        "logSettings": List[LogSettingsResponseTypeDef],
        "iamRoleArn": str,
    },
    total=False,
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBotChannelAssociationResponseTypeDef = TypedDict(
    "GetBotChannelAssociationResponseTypeDef",
    {
        "name": str,
        "description": str,
        "botAlias": str,
        "botName": str,
        "createdDate": datetime,
        "type": ChannelTypeType,
        "botConfiguration": Dict[str, str],
        "status": ChannelStatusType,
        "failureReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBotChannelAssociationsResponseTypeDef = TypedDict(
    "GetBotChannelAssociationsResponseTypeDef",
    {
        "botChannelAssociations": List[BotChannelAssociationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBotVersionsResponseTypeDef = TypedDict(
    "GetBotVersionsResponseTypeDef",
    {
        "bots": List[BotMetadataTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBotsResponseTypeDef = TypedDict(
    "GetBotsResponseTypeDef",
    {
        "bots": List[BotMetadataTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBuiltinIntentResponseTypeDef = TypedDict(
    "GetBuiltinIntentResponseTypeDef",
    {
        "signature": str,
        "supportedLocales": List[LocaleType],
        "slots": List[BuiltinIntentSlotTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBuiltinIntentsResponseTypeDef = TypedDict(
    "GetBuiltinIntentsResponseTypeDef",
    {
        "intents": List[BuiltinIntentMetadataTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBuiltinSlotTypesResponseTypeDef = TypedDict(
    "GetBuiltinSlotTypesResponseTypeDef",
    {
        "slotTypes": List[BuiltinSlotTypeMetadataTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetExportResponseTypeDef = TypedDict(
    "GetExportResponseTypeDef",
    {
        "name": str,
        "version": str,
        "resourceType": ResourceTypeType,
        "exportType": ExportTypeType,
        "exportStatus": ExportStatusType,
        "failureReason": str,
        "url": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetImportResponseTypeDef = TypedDict(
    "GetImportResponseTypeDef",
    {
        "name": str,
        "resourceType": ResourceTypeType,
        "mergeStrategy": MergeStrategyType,
        "importId": str,
        "importStatus": ImportStatusType,
        "failureReason": List[str],
        "createdDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMigrationResponseTypeDef = TypedDict(
    "StartMigrationResponseTypeDef",
    {
        "v1BotName": str,
        "v1BotVersion": str,
        "v1BotLocale": LocaleType,
        "v2BotId": str,
        "v2BotRole": str,
        "migrationId": str,
        "migrationStrategy": MigrationStrategyType,
        "migrationTimestamp": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetBotAliasesRequestGetBotAliasesPaginateTypeDef = TypedDict(
    "_RequiredGetBotAliasesRequestGetBotAliasesPaginateTypeDef",
    {
        "botName": str,
    },
)
_OptionalGetBotAliasesRequestGetBotAliasesPaginateTypeDef = TypedDict(
    "_OptionalGetBotAliasesRequestGetBotAliasesPaginateTypeDef",
    {
        "nameContains": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetBotAliasesRequestGetBotAliasesPaginateTypeDef(
    _RequiredGetBotAliasesRequestGetBotAliasesPaginateTypeDef,
    _OptionalGetBotAliasesRequestGetBotAliasesPaginateTypeDef,
):
    pass


_RequiredGetBotChannelAssociationsRequestGetBotChannelAssociationsPaginateTypeDef = TypedDict(
    "_RequiredGetBotChannelAssociationsRequestGetBotChannelAssociationsPaginateTypeDef",
    {
        "botName": str,
        "botAlias": str,
    },
)
_OptionalGetBotChannelAssociationsRequestGetBotChannelAssociationsPaginateTypeDef = TypedDict(
    "_OptionalGetBotChannelAssociationsRequestGetBotChannelAssociationsPaginateTypeDef",
    {
        "nameContains": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetBotChannelAssociationsRequestGetBotChannelAssociationsPaginateTypeDef(
    _RequiredGetBotChannelAssociationsRequestGetBotChannelAssociationsPaginateTypeDef,
    _OptionalGetBotChannelAssociationsRequestGetBotChannelAssociationsPaginateTypeDef,
):
    pass


_RequiredGetBotVersionsRequestGetBotVersionsPaginateTypeDef = TypedDict(
    "_RequiredGetBotVersionsRequestGetBotVersionsPaginateTypeDef",
    {
        "name": str,
    },
)
_OptionalGetBotVersionsRequestGetBotVersionsPaginateTypeDef = TypedDict(
    "_OptionalGetBotVersionsRequestGetBotVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetBotVersionsRequestGetBotVersionsPaginateTypeDef(
    _RequiredGetBotVersionsRequestGetBotVersionsPaginateTypeDef,
    _OptionalGetBotVersionsRequestGetBotVersionsPaginateTypeDef,
):
    pass


GetBotsRequestGetBotsPaginateTypeDef = TypedDict(
    "GetBotsRequestGetBotsPaginateTypeDef",
    {
        "nameContains": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetBuiltinIntentsRequestGetBuiltinIntentsPaginateTypeDef = TypedDict(
    "GetBuiltinIntentsRequestGetBuiltinIntentsPaginateTypeDef",
    {
        "locale": LocaleType,
        "signatureContains": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetBuiltinSlotTypesRequestGetBuiltinSlotTypesPaginateTypeDef = TypedDict(
    "GetBuiltinSlotTypesRequestGetBuiltinSlotTypesPaginateTypeDef",
    {
        "locale": LocaleType,
        "signatureContains": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetIntentVersionsRequestGetIntentVersionsPaginateTypeDef = TypedDict(
    "_RequiredGetIntentVersionsRequestGetIntentVersionsPaginateTypeDef",
    {
        "name": str,
    },
)
_OptionalGetIntentVersionsRequestGetIntentVersionsPaginateTypeDef = TypedDict(
    "_OptionalGetIntentVersionsRequestGetIntentVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetIntentVersionsRequestGetIntentVersionsPaginateTypeDef(
    _RequiredGetIntentVersionsRequestGetIntentVersionsPaginateTypeDef,
    _OptionalGetIntentVersionsRequestGetIntentVersionsPaginateTypeDef,
):
    pass


GetIntentsRequestGetIntentsPaginateTypeDef = TypedDict(
    "GetIntentsRequestGetIntentsPaginateTypeDef",
    {
        "nameContains": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredGetSlotTypeVersionsRequestGetSlotTypeVersionsPaginateTypeDef = TypedDict(
    "_RequiredGetSlotTypeVersionsRequestGetSlotTypeVersionsPaginateTypeDef",
    {
        "name": str,
    },
)
_OptionalGetSlotTypeVersionsRequestGetSlotTypeVersionsPaginateTypeDef = TypedDict(
    "_OptionalGetSlotTypeVersionsRequestGetSlotTypeVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetSlotTypeVersionsRequestGetSlotTypeVersionsPaginateTypeDef(
    _RequiredGetSlotTypeVersionsRequestGetSlotTypeVersionsPaginateTypeDef,
    _OptionalGetSlotTypeVersionsRequestGetSlotTypeVersionsPaginateTypeDef,
):
    pass


GetSlotTypesRequestGetSlotTypesPaginateTypeDef = TypedDict(
    "GetSlotTypesRequestGetSlotTypesPaginateTypeDef",
    {
        "nameContains": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetIntentVersionsResponseTypeDef = TypedDict(
    "GetIntentVersionsResponseTypeDef",
    {
        "intents": List[IntentMetadataTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetIntentsResponseTypeDef = TypedDict(
    "GetIntentsResponseTypeDef",
    {
        "intents": List[IntentMetadataTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMigrationResponseTypeDef = TypedDict(
    "GetMigrationResponseTypeDef",
    {
        "migrationId": str,
        "v1BotName": str,
        "v1BotVersion": str,
        "v1BotLocale": LocaleType,
        "v2BotId": str,
        "v2BotRole": str,
        "migrationStatus": MigrationStatusType,
        "migrationStrategy": MigrationStrategyType,
        "migrationTimestamp": datetime,
        "alerts": List[MigrationAlertTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMigrationsResponseTypeDef = TypedDict(
    "GetMigrationsResponseTypeDef",
    {
        "migrationSummaries": List[MigrationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSlotTypeVersionsResponseTypeDef = TypedDict(
    "GetSlotTypeVersionsResponseTypeDef",
    {
        "slotTypes": List[SlotTypeMetadataTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSlotTypesResponseTypeDef = TypedDict(
    "GetSlotTypesResponseTypeDef",
    {
        "slotTypes": List[SlotTypeMetadataTypeDef],
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

_RequiredStartImportRequestRequestTypeDef = TypedDict(
    "_RequiredStartImportRequestRequestTypeDef",
    {
        "payload": Union[str, bytes, IO[Any], StreamingBody],
        "resourceType": ResourceTypeType,
        "mergeStrategy": MergeStrategyType,
    },
)
_OptionalStartImportRequestRequestTypeDef = TypedDict(
    "_OptionalStartImportRequestRequestTypeDef",
    {
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class StartImportRequestRequestTypeDef(
    _RequiredStartImportRequestRequestTypeDef, _OptionalStartImportRequestRequestTypeDef
):
    pass


StartImportResponseTypeDef = TypedDict(
    "StartImportResponseTypeDef",
    {
        "name": str,
        "resourceType": ResourceTypeType,
        "mergeStrategy": MergeStrategyType,
        "importId": str,
        "importStatus": ImportStatusType,
        "tags": List[TagTypeDef],
        "createdDate": datetime,
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

_RequiredPromptTypeDef = TypedDict(
    "_RequiredPromptTypeDef",
    {
        "messages": List[MessageTypeDef],
        "maxAttempts": int,
    },
)
_OptionalPromptTypeDef = TypedDict(
    "_OptionalPromptTypeDef",
    {
        "responseCard": str,
    },
    total=False,
)


class PromptTypeDef(_RequiredPromptTypeDef, _OptionalPromptTypeDef):
    pass


_RequiredStatementTypeDef = TypedDict(
    "_RequiredStatementTypeDef",
    {
        "messages": List[MessageTypeDef],
    },
)
_OptionalStatementTypeDef = TypedDict(
    "_OptionalStatementTypeDef",
    {
        "responseCard": str,
    },
    total=False,
)


class StatementTypeDef(_RequiredStatementTypeDef, _OptionalStatementTypeDef):
    pass


SlotDefaultValueSpecTypeDef = TypedDict(
    "SlotDefaultValueSpecTypeDef",
    {
        "defaultValueList": List[SlotDefaultValueTypeDef],
    },
)

SlotTypeConfigurationTypeDef = TypedDict(
    "SlotTypeConfigurationTypeDef",
    {
        "regexConfiguration": SlotTypeRegexConfigurationTypeDef,
    },
    total=False,
)

UtteranceListTypeDef = TypedDict(
    "UtteranceListTypeDef",
    {
        "botVersion": str,
        "utterances": List[UtteranceDataTypeDef],
    },
    total=False,
)

_RequiredPutBotAliasRequestRequestTypeDef = TypedDict(
    "_RequiredPutBotAliasRequestRequestTypeDef",
    {
        "name": str,
        "botVersion": str,
        "botName": str,
    },
)
_OptionalPutBotAliasRequestRequestTypeDef = TypedDict(
    "_OptionalPutBotAliasRequestRequestTypeDef",
    {
        "description": str,
        "checksum": str,
        "conversationLogs": ConversationLogsRequestTypeDef,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class PutBotAliasRequestRequestTypeDef(
    _RequiredPutBotAliasRequestRequestTypeDef, _OptionalPutBotAliasRequestRequestTypeDef
):
    pass


BotAliasMetadataTypeDef = TypedDict(
    "BotAliasMetadataTypeDef",
    {
        "name": str,
        "description": str,
        "botVersion": str,
        "botName": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "checksum": str,
        "conversationLogs": ConversationLogsResponseTypeDef,
    },
    total=False,
)

GetBotAliasResponseTypeDef = TypedDict(
    "GetBotAliasResponseTypeDef",
    {
        "name": str,
        "description": str,
        "botVersion": str,
        "botName": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "checksum": str,
        "conversationLogs": ConversationLogsResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutBotAliasResponseTypeDef = TypedDict(
    "PutBotAliasResponseTypeDef",
    {
        "name": str,
        "description": str,
        "botVersion": str,
        "botName": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "checksum": str,
        "conversationLogs": ConversationLogsResponseTypeDef,
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBotVersionResponseTypeDef = TypedDict(
    "CreateBotVersionResponseTypeDef",
    {
        "name": str,
        "description": str,
        "intents": List[IntentTypeDef],
        "clarificationPrompt": PromptTypeDef,
        "abortStatement": StatementTypeDef,
        "status": StatusType,
        "failureReason": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "idleSessionTTLInSeconds": int,
        "voiceId": str,
        "checksum": str,
        "version": str,
        "locale": LocaleType,
        "childDirected": bool,
        "enableModelImprovements": bool,
        "detectSentiment": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FollowUpPromptTypeDef = TypedDict(
    "FollowUpPromptTypeDef",
    {
        "prompt": PromptTypeDef,
        "rejectionStatement": StatementTypeDef,
    },
)

GetBotResponseTypeDef = TypedDict(
    "GetBotResponseTypeDef",
    {
        "name": str,
        "description": str,
        "intents": List[IntentTypeDef],
        "enableModelImprovements": bool,
        "nluIntentConfidenceThreshold": float,
        "clarificationPrompt": PromptTypeDef,
        "abortStatement": StatementTypeDef,
        "status": StatusType,
        "failureReason": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "idleSessionTTLInSeconds": int,
        "voiceId": str,
        "checksum": str,
        "version": str,
        "locale": LocaleType,
        "childDirected": bool,
        "detectSentiment": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutBotRequestRequestTypeDef = TypedDict(
    "_RequiredPutBotRequestRequestTypeDef",
    {
        "name": str,
        "locale": LocaleType,
        "childDirected": bool,
    },
)
_OptionalPutBotRequestRequestTypeDef = TypedDict(
    "_OptionalPutBotRequestRequestTypeDef",
    {
        "description": str,
        "intents": Sequence[IntentTypeDef],
        "enableModelImprovements": bool,
        "nluIntentConfidenceThreshold": float,
        "clarificationPrompt": PromptTypeDef,
        "abortStatement": StatementTypeDef,
        "idleSessionTTLInSeconds": int,
        "voiceId": str,
        "checksum": str,
        "processBehavior": ProcessBehaviorType,
        "detectSentiment": bool,
        "createVersion": bool,
        "tags": Sequence[TagTypeDef],
    },
    total=False,
)


class PutBotRequestRequestTypeDef(
    _RequiredPutBotRequestRequestTypeDef, _OptionalPutBotRequestRequestTypeDef
):
    pass


PutBotResponseTypeDef = TypedDict(
    "PutBotResponseTypeDef",
    {
        "name": str,
        "description": str,
        "intents": List[IntentTypeDef],
        "enableModelImprovements": bool,
        "nluIntentConfidenceThreshold": float,
        "clarificationPrompt": PromptTypeDef,
        "abortStatement": StatementTypeDef,
        "status": StatusType,
        "failureReason": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "idleSessionTTLInSeconds": int,
        "voiceId": str,
        "checksum": str,
        "version": str,
        "locale": LocaleType,
        "childDirected": bool,
        "createVersion": bool,
        "detectSentiment": bool,
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSlotTypeDef = TypedDict(
    "_RequiredSlotTypeDef",
    {
        "name": str,
        "slotConstraint": SlotConstraintType,
    },
)
_OptionalSlotTypeDef = TypedDict(
    "_OptionalSlotTypeDef",
    {
        "description": str,
        "slotType": str,
        "slotTypeVersion": str,
        "valueElicitationPrompt": PromptTypeDef,
        "priority": int,
        "sampleUtterances": List[str],
        "responseCard": str,
        "obfuscationSetting": ObfuscationSettingType,
        "defaultValueSpec": SlotDefaultValueSpecTypeDef,
    },
    total=False,
)


class SlotTypeDef(_RequiredSlotTypeDef, _OptionalSlotTypeDef):
    pass


CreateSlotTypeVersionResponseTypeDef = TypedDict(
    "CreateSlotTypeVersionResponseTypeDef",
    {
        "name": str,
        "description": str,
        "enumerationValues": List[EnumerationValueTypeDef],
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "valueSelectionStrategy": SlotValueSelectionStrategyType,
        "parentSlotTypeSignature": str,
        "slotTypeConfigurations": List[SlotTypeConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSlotTypeResponseTypeDef = TypedDict(
    "GetSlotTypeResponseTypeDef",
    {
        "name": str,
        "description": str,
        "enumerationValues": List[EnumerationValueTypeDef],
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "valueSelectionStrategy": SlotValueSelectionStrategyType,
        "parentSlotTypeSignature": str,
        "slotTypeConfigurations": List[SlotTypeConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutSlotTypeRequestRequestTypeDef = TypedDict(
    "_RequiredPutSlotTypeRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalPutSlotTypeRequestRequestTypeDef = TypedDict(
    "_OptionalPutSlotTypeRequestRequestTypeDef",
    {
        "description": str,
        "enumerationValues": Sequence[EnumerationValueTypeDef],
        "checksum": str,
        "valueSelectionStrategy": SlotValueSelectionStrategyType,
        "createVersion": bool,
        "parentSlotTypeSignature": str,
        "slotTypeConfigurations": Sequence[SlotTypeConfigurationTypeDef],
    },
    total=False,
)


class PutSlotTypeRequestRequestTypeDef(
    _RequiredPutSlotTypeRequestRequestTypeDef, _OptionalPutSlotTypeRequestRequestTypeDef
):
    pass


PutSlotTypeResponseTypeDef = TypedDict(
    "PutSlotTypeResponseTypeDef",
    {
        "name": str,
        "description": str,
        "enumerationValues": List[EnumerationValueTypeDef],
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "valueSelectionStrategy": SlotValueSelectionStrategyType,
        "createVersion": bool,
        "parentSlotTypeSignature": str,
        "slotTypeConfigurations": List[SlotTypeConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetUtterancesViewResponseTypeDef = TypedDict(
    "GetUtterancesViewResponseTypeDef",
    {
        "botName": str,
        "utterances": List[UtteranceListTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBotAliasesResponseTypeDef = TypedDict(
    "GetBotAliasesResponseTypeDef",
    {
        "BotAliases": List[BotAliasMetadataTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateIntentVersionResponseTypeDef = TypedDict(
    "CreateIntentVersionResponseTypeDef",
    {
        "name": str,
        "description": str,
        "slots": List[SlotTypeDef],
        "sampleUtterances": List[str],
        "confirmationPrompt": PromptTypeDef,
        "rejectionStatement": StatementTypeDef,
        "followUpPrompt": FollowUpPromptTypeDef,
        "conclusionStatement": StatementTypeDef,
        "dialogCodeHook": CodeHookTypeDef,
        "fulfillmentActivity": FulfillmentActivityTypeDef,
        "parentIntentSignature": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "kendraConfiguration": KendraConfigurationTypeDef,
        "inputContexts": List[InputContextTypeDef],
        "outputContexts": List[OutputContextTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetIntentResponseTypeDef = TypedDict(
    "GetIntentResponseTypeDef",
    {
        "name": str,
        "description": str,
        "slots": List[SlotTypeDef],
        "sampleUtterances": List[str],
        "confirmationPrompt": PromptTypeDef,
        "rejectionStatement": StatementTypeDef,
        "followUpPrompt": FollowUpPromptTypeDef,
        "conclusionStatement": StatementTypeDef,
        "dialogCodeHook": CodeHookTypeDef,
        "fulfillmentActivity": FulfillmentActivityTypeDef,
        "parentIntentSignature": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "kendraConfiguration": KendraConfigurationTypeDef,
        "inputContexts": List[InputContextTypeDef],
        "outputContexts": List[OutputContextTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutIntentRequestRequestTypeDef = TypedDict(
    "_RequiredPutIntentRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalPutIntentRequestRequestTypeDef = TypedDict(
    "_OptionalPutIntentRequestRequestTypeDef",
    {
        "description": str,
        "slots": Sequence[SlotTypeDef],
        "sampleUtterances": Sequence[str],
        "confirmationPrompt": PromptTypeDef,
        "rejectionStatement": StatementTypeDef,
        "followUpPrompt": FollowUpPromptTypeDef,
        "conclusionStatement": StatementTypeDef,
        "dialogCodeHook": CodeHookTypeDef,
        "fulfillmentActivity": FulfillmentActivityTypeDef,
        "parentIntentSignature": str,
        "checksum": str,
        "createVersion": bool,
        "kendraConfiguration": KendraConfigurationTypeDef,
        "inputContexts": Sequence[InputContextTypeDef],
        "outputContexts": Sequence[OutputContextTypeDef],
    },
    total=False,
)


class PutIntentRequestRequestTypeDef(
    _RequiredPutIntentRequestRequestTypeDef, _OptionalPutIntentRequestRequestTypeDef
):
    pass


PutIntentResponseTypeDef = TypedDict(
    "PutIntentResponseTypeDef",
    {
        "name": str,
        "description": str,
        "slots": List[SlotTypeDef],
        "sampleUtterances": List[str],
        "confirmationPrompt": PromptTypeDef,
        "rejectionStatement": StatementTypeDef,
        "followUpPrompt": FollowUpPromptTypeDef,
        "conclusionStatement": StatementTypeDef,
        "dialogCodeHook": CodeHookTypeDef,
        "fulfillmentActivity": FulfillmentActivityTypeDef,
        "parentIntentSignature": str,
        "lastUpdatedDate": datetime,
        "createdDate": datetime,
        "version": str,
        "checksum": str,
        "createVersion": bool,
        "kendraConfiguration": KendraConfigurationTypeDef,
        "inputContexts": List[InputContextTypeDef],
        "outputContexts": List[OutputContextTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
