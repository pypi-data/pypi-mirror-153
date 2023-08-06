"""
Type annotations for codepipeline service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codepipeline.client import CodePipelineClient
    from mypy_boto3_codepipeline.paginator import (
        ListActionExecutionsPaginator,
        ListActionTypesPaginator,
        ListPipelineExecutionsPaginator,
        ListPipelinesPaginator,
        ListTagsForResourcePaginator,
        ListWebhooksPaginator,
    )

    session = Session()
    client: CodePipelineClient = session.client("codepipeline")

    list_action_executions_paginator: ListActionExecutionsPaginator = client.get_paginator("list_action_executions")
    list_action_types_paginator: ListActionTypesPaginator = client.get_paginator("list_action_types")
    list_pipeline_executions_paginator: ListPipelineExecutionsPaginator = client.get_paginator("list_pipeline_executions")
    list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    list_webhooks_paginator: ListWebhooksPaginator = client.get_paginator("list_webhooks")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import ActionOwnerType
from .type_defs import (
    ActionExecutionFilterTypeDef,
    ListActionExecutionsOutputTypeDef,
    ListActionTypesOutputTypeDef,
    ListPipelineExecutionsOutputTypeDef,
    ListPipelinesOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListWebhooksOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListActionExecutionsPaginator",
    "ListActionTypesPaginator",
    "ListPipelineExecutionsPaginator",
    "ListPipelinesPaginator",
    "ListTagsForResourcePaginator",
    "ListWebhooksPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListActionExecutionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Paginator.ListActionExecutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listactionexecutionspaginator)
    """

    def paginate(
        self,
        *,
        pipelineName: str,
        filter: ActionExecutionFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListActionExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Paginator.ListActionExecutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listactionexecutionspaginator)
        """


class ListActionTypesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Paginator.ListActionTypes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listactiontypespaginator)
    """

    def paginate(
        self,
        *,
        actionOwnerFilter: ActionOwnerType = ...,
        regionFilter: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListActionTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Paginator.ListActionTypes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listactiontypespaginator)
        """


class ListPipelineExecutionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Paginator.ListPipelineExecutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listpipelineexecutionspaginator)
    """

    def paginate(
        self, *, pipelineName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPipelineExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Paginator.ListPipelineExecutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listpipelineexecutionspaginator)
        """


class ListPipelinesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Paginator.ListPipelines)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listpipelinespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPipelinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Paginator.ListPipelines.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listpipelinespaginator)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Paginator.ListTagsForResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, *, resourceArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listtagsforresourcepaginator)
        """


class ListWebhooksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Paginator.ListWebhooks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listwebhookspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWebhooksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline.html#CodePipeline.Paginator.ListWebhooks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codepipeline/paginators/#listwebhookspaginator)
        """
