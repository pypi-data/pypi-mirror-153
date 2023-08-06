"""
Type annotations for lex-models service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_lex_models.client import LexModelBuildingServiceClient
    from mypy_boto3_lex_models.paginator import (
        GetBotAliasesPaginator,
        GetBotChannelAssociationsPaginator,
        GetBotVersionsPaginator,
        GetBotsPaginator,
        GetBuiltinIntentsPaginator,
        GetBuiltinSlotTypesPaginator,
        GetIntentVersionsPaginator,
        GetIntentsPaginator,
        GetSlotTypeVersionsPaginator,
        GetSlotTypesPaginator,
    )

    session = Session()
    client: LexModelBuildingServiceClient = session.client("lex-models")

    get_bot_aliases_paginator: GetBotAliasesPaginator = client.get_paginator("get_bot_aliases")
    get_bot_channel_associations_paginator: GetBotChannelAssociationsPaginator = client.get_paginator("get_bot_channel_associations")
    get_bot_versions_paginator: GetBotVersionsPaginator = client.get_paginator("get_bot_versions")
    get_bots_paginator: GetBotsPaginator = client.get_paginator("get_bots")
    get_builtin_intents_paginator: GetBuiltinIntentsPaginator = client.get_paginator("get_builtin_intents")
    get_builtin_slot_types_paginator: GetBuiltinSlotTypesPaginator = client.get_paginator("get_builtin_slot_types")
    get_intent_versions_paginator: GetIntentVersionsPaginator = client.get_paginator("get_intent_versions")
    get_intents_paginator: GetIntentsPaginator = client.get_paginator("get_intents")
    get_slot_type_versions_paginator: GetSlotTypeVersionsPaginator = client.get_paginator("get_slot_type_versions")
    get_slot_types_paginator: GetSlotTypesPaginator = client.get_paginator("get_slot_types")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import LocaleType
from .type_defs import (
    GetBotAliasesResponseTypeDef,
    GetBotChannelAssociationsResponseTypeDef,
    GetBotsResponseTypeDef,
    GetBotVersionsResponseTypeDef,
    GetBuiltinIntentsResponseTypeDef,
    GetBuiltinSlotTypesResponseTypeDef,
    GetIntentsResponseTypeDef,
    GetIntentVersionsResponseTypeDef,
    GetSlotTypesResponseTypeDef,
    GetSlotTypeVersionsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetBotAliasesPaginator",
    "GetBotChannelAssociationsPaginator",
    "GetBotVersionsPaginator",
    "GetBotsPaginator",
    "GetBuiltinIntentsPaginator",
    "GetBuiltinSlotTypesPaginator",
    "GetIntentVersionsPaginator",
    "GetIntentsPaginator",
    "GetSlotTypeVersionsPaginator",
    "GetSlotTypesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetBotAliasesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBotAliases)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotaliasespaginator)
    """

    def paginate(
        self,
        *,
        botName: str,
        nameContains: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetBotAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBotAliases.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotaliasespaginator)
        """


class GetBotChannelAssociationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBotChannelAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotchannelassociationspaginator)
    """

    def paginate(
        self,
        *,
        botName: str,
        botAlias: str,
        nameContains: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetBotChannelAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBotChannelAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotchannelassociationspaginator)
        """


class GetBotVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBotVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotversionspaginator)
    """

    def paginate(
        self, *, name: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetBotVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBotVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotversionspaginator)
        """


class GetBotsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBots)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotspaginator)
    """

    def paginate(
        self, *, nameContains: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBots.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbotspaginator)
        """


class GetBuiltinIntentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBuiltinIntents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbuiltinintentspaginator)
    """

    def paginate(
        self,
        *,
        locale: LocaleType = ...,
        signatureContains: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetBuiltinIntentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBuiltinIntents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbuiltinintentspaginator)
        """


class GetBuiltinSlotTypesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBuiltinSlotTypes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbuiltinslottypespaginator)
    """

    def paginate(
        self,
        *,
        locale: LocaleType = ...,
        signatureContains: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetBuiltinSlotTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetBuiltinSlotTypes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getbuiltinslottypespaginator)
        """


class GetIntentVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetIntentVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getintentversionspaginator)
    """

    def paginate(
        self, *, name: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetIntentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetIntentVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getintentversionspaginator)
        """


class GetIntentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetIntents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getintentspaginator)
    """

    def paginate(
        self, *, nameContains: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetIntentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetIntents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getintentspaginator)
        """


class GetSlotTypeVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetSlotTypeVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getslottypeversionspaginator)
    """

    def paginate(
        self, *, name: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetSlotTypeVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetSlotTypeVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getslottypeversionspaginator)
        """


class GetSlotTypesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetSlotTypes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getslottypespaginator)
    """

    def paginate(
        self, *, nameContains: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetSlotTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Paginator.GetSlotTypes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lex_models/paginators/#getslottypespaginator)
        """
