"""
Type annotations for cloud9 service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloud9.client import Cloud9Client

    session = Session()
    client: Cloud9Client = session.client("cloud9")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    ConnectionTypeType,
    ManagedCredentialsActionType,
    MemberPermissionsType,
    PermissionsType,
)
from .paginator import DescribeEnvironmentMembershipsPaginator, ListEnvironmentsPaginator
from .type_defs import (
    CreateEnvironmentEC2ResultTypeDef,
    CreateEnvironmentMembershipResultTypeDef,
    DescribeEnvironmentMembershipsResultTypeDef,
    DescribeEnvironmentsResultTypeDef,
    DescribeEnvironmentStatusResultTypeDef,
    ListEnvironmentsResultTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagTypeDef,
    UpdateEnvironmentMembershipResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("Cloud9Client",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentAccessException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class Cloud9Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Cloud9Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#can_paginate)
        """

    def create_environment_ec2(
        self,
        *,
        name: str,
        instanceType: str,
        description: str = ...,
        clientRequestToken: str = ...,
        subnetId: str = ...,
        imageId: str = ...,
        automaticStopTimeMinutes: int = ...,
        ownerArn: str = ...,
        tags: Sequence[TagTypeDef] = ...,
        connectionType: ConnectionTypeType = ...,
        dryRun: bool = ...
    ) -> CreateEnvironmentEC2ResultTypeDef:
        """
        Creates an Cloud9 development environment, launches an Amazon Elastic Compute
        Cloud (Amazon EC2) instance, and then connects from the instance to the
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.create_environment_ec2)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#create_environment_ec2)
        """

    def create_environment_membership(
        self, *, environmentId: str, userArn: str, permissions: MemberPermissionsType
    ) -> CreateEnvironmentMembershipResultTypeDef:
        """
        Adds an environment member to an Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.create_environment_membership)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#create_environment_membership)
        """

    def delete_environment(self, *, environmentId: str) -> Dict[str, Any]:
        """
        Deletes an Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.delete_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#delete_environment)
        """

    def delete_environment_membership(self, *, environmentId: str, userArn: str) -> Dict[str, Any]:
        """
        Deletes an environment member from an Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.delete_environment_membership)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#delete_environment_membership)
        """

    def describe_environment_memberships(
        self,
        *,
        userArn: str = ...,
        environmentId: str = ...,
        permissions: Sequence[PermissionsType] = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> DescribeEnvironmentMembershipsResultTypeDef:
        """
        Gets information about environment members for an Cloud9 development
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.describe_environment_memberships)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#describe_environment_memberships)
        """

    def describe_environment_status(
        self, *, environmentId: str
    ) -> DescribeEnvironmentStatusResultTypeDef:
        """
        Gets status information for an Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.describe_environment_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#describe_environment_status)
        """

    def describe_environments(
        self, *, environmentIds: Sequence[str]
    ) -> DescribeEnvironmentsResultTypeDef:
        """
        Gets information about Cloud9 development environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.describe_environments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#describe_environments)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#generate_presigned_url)
        """

    def list_environments(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListEnvironmentsResultTypeDef:
        """
        Gets a list of Cloud9 development environment identifiers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.list_environments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#list_environments)
        """

    def list_tags_for_resource(self, *, ResourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        Gets a list of the tags associated with an Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#list_tags_for_resource)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to an Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from an Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#untag_resource)
        """

    def update_environment(
        self,
        *,
        environmentId: str,
        name: str = ...,
        description: str = ...,
        managedCredentialsAction: ManagedCredentialsActionType = ...
    ) -> Dict[str, Any]:
        """
        Changes the settings of an existing Cloud9 development environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.update_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#update_environment)
        """

    def update_environment_membership(
        self, *, environmentId: str, userArn: str, permissions: MemberPermissionsType
    ) -> UpdateEnvironmentMembershipResultTypeDef:
        """
        Changes the settings of an existing environment member for an Cloud9 development
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.update_environment_membership)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#update_environment_membership)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_environment_memberships"]
    ) -> DescribeEnvironmentMembershipsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloud9.html#Cloud9.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloud9/client/#get_paginator)
        """
