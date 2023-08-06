"""
Type annotations for nimble service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_nimble.client import NimbleStudioClient

    session = Session()
    client: NimbleStudioClient = session.client("nimble")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    LaunchProfileStateType,
    StreamingInstanceTypeType,
    StudioComponentStateType,
    StudioComponentSubtypeType,
    StudioComponentTypeType,
)
from .paginator import (
    ListEulaAcceptancesPaginator,
    ListEulasPaginator,
    ListLaunchProfileMembersPaginator,
    ListLaunchProfilesPaginator,
    ListStreamingImagesPaginator,
    ListStreamingSessionsPaginator,
    ListStudioComponentsPaginator,
    ListStudioMembersPaginator,
    ListStudiosPaginator,
)
from .type_defs import (
    AcceptEulasResponseTypeDef,
    CreateLaunchProfileResponseTypeDef,
    CreateStreamingImageResponseTypeDef,
    CreateStreamingSessionResponseTypeDef,
    CreateStreamingSessionStreamResponseTypeDef,
    CreateStudioComponentResponseTypeDef,
    CreateStudioResponseTypeDef,
    DeleteLaunchProfileResponseTypeDef,
    DeleteStreamingImageResponseTypeDef,
    DeleteStreamingSessionResponseTypeDef,
    DeleteStudioComponentResponseTypeDef,
    DeleteStudioResponseTypeDef,
    GetEulaResponseTypeDef,
    GetLaunchProfileDetailsResponseTypeDef,
    GetLaunchProfileInitializationResponseTypeDef,
    GetLaunchProfileMemberResponseTypeDef,
    GetLaunchProfileResponseTypeDef,
    GetStreamingImageResponseTypeDef,
    GetStreamingSessionResponseTypeDef,
    GetStreamingSessionStreamResponseTypeDef,
    GetStudioComponentResponseTypeDef,
    GetStudioMemberResponseTypeDef,
    GetStudioResponseTypeDef,
    ListEulaAcceptancesResponseTypeDef,
    ListEulasResponseTypeDef,
    ListLaunchProfileMembersResponseTypeDef,
    ListLaunchProfilesResponseTypeDef,
    ListStreamingImagesResponseTypeDef,
    ListStreamingSessionsResponseTypeDef,
    ListStudioComponentsResponseTypeDef,
    ListStudioMembersResponseTypeDef,
    ListStudiosResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    NewLaunchProfileMemberTypeDef,
    NewStudioMemberTypeDef,
    ScriptParameterKeyValueTypeDef,
    StartStreamingSessionResponseTypeDef,
    StartStudioSSOConfigurationRepairResponseTypeDef,
    StopStreamingSessionResponseTypeDef,
    StreamConfigurationCreateTypeDef,
    StudioComponentConfigurationTypeDef,
    StudioComponentInitializationScriptTypeDef,
    StudioEncryptionConfigurationTypeDef,
    UpdateLaunchProfileMemberResponseTypeDef,
    UpdateLaunchProfileResponseTypeDef,
    UpdateStreamingImageResponseTypeDef,
    UpdateStudioComponentResponseTypeDef,
    UpdateStudioResponseTypeDef,
)
from .waiter import (
    LaunchProfileDeletedWaiter,
    LaunchProfileReadyWaiter,
    StreamingImageDeletedWaiter,
    StreamingImageReadyWaiter,
    StreamingSessionDeletedWaiter,
    StreamingSessionReadyWaiter,
    StreamingSessionStoppedWaiter,
    StreamingSessionStreamReadyWaiter,
    StudioComponentDeletedWaiter,
    StudioComponentReadyWaiter,
    StudioDeletedWaiter,
    StudioReadyWaiter,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("NimbleStudioClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class NimbleStudioClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        NimbleStudioClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#exceptions)
        """

    def accept_eulas(
        self, *, studioId: str, clientToken: str = ..., eulaIds: Sequence[str] = ...
    ) -> AcceptEulasResponseTypeDef:
        """
        Accept EULAs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.accept_eulas)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#accept_eulas)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#can_paginate)
        """

    def create_launch_profile(
        self,
        *,
        ec2SubnetIds: Sequence[str],
        launchProfileProtocolVersions: Sequence[str],
        name: str,
        streamConfiguration: StreamConfigurationCreateTypeDef,
        studioComponentIds: Sequence[str],
        studioId: str,
        clientToken: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateLaunchProfileResponseTypeDef:
        """
        Create a launch profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.create_launch_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#create_launch_profile)
        """

    def create_streaming_image(
        self,
        *,
        ec2ImageId: str,
        name: str,
        studioId: str,
        clientToken: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateStreamingImageResponseTypeDef:
        """
        Creates a streaming image resource in a studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.create_streaming_image)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#create_streaming_image)
        """

    def create_streaming_session(
        self,
        *,
        studioId: str,
        clientToken: str = ...,
        ec2InstanceType: StreamingInstanceTypeType = ...,
        launchProfileId: str = ...,
        ownedBy: str = ...,
        streamingImageId: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateStreamingSessionResponseTypeDef:
        """
        Creates a streaming session in a studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.create_streaming_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#create_streaming_session)
        """

    def create_streaming_session_stream(
        self,
        *,
        sessionId: str,
        studioId: str,
        clientToken: str = ...,
        expirationInSeconds: int = ...
    ) -> CreateStreamingSessionStreamResponseTypeDef:
        """
        Creates a streaming session stream for a streaming session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.create_streaming_session_stream)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#create_streaming_session_stream)
        """

    def create_studio(
        self,
        *,
        adminRoleArn: str,
        displayName: str,
        studioName: str,
        userRoleArn: str,
        clientToken: str = ...,
        studioEncryptionConfiguration: StudioEncryptionConfigurationTypeDef = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateStudioResponseTypeDef:
        """
        Create a new Studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.create_studio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#create_studio)
        """

    def create_studio_component(
        self,
        *,
        name: str,
        studioId: str,
        type: StudioComponentTypeType,
        clientToken: str = ...,
        configuration: StudioComponentConfigurationTypeDef = ...,
        description: str = ...,
        ec2SecurityGroupIds: Sequence[str] = ...,
        initializationScripts: Sequence[StudioComponentInitializationScriptTypeDef] = ...,
        scriptParameters: Sequence[ScriptParameterKeyValueTypeDef] = ...,
        subtype: StudioComponentSubtypeType = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateStudioComponentResponseTypeDef:
        """
        Creates a studio component resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.create_studio_component)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#create_studio_component)
        """

    def delete_launch_profile(
        self, *, launchProfileId: str, studioId: str, clientToken: str = ...
    ) -> DeleteLaunchProfileResponseTypeDef:
        """
        Permanently delete a launch profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.delete_launch_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#delete_launch_profile)
        """

    def delete_launch_profile_member(
        self, *, launchProfileId: str, principalId: str, studioId: str, clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Delete a user from launch profile membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.delete_launch_profile_member)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#delete_launch_profile_member)
        """

    def delete_streaming_image(
        self, *, streamingImageId: str, studioId: str, clientToken: str = ...
    ) -> DeleteStreamingImageResponseTypeDef:
        """
        Delete streaming image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.delete_streaming_image)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#delete_streaming_image)
        """

    def delete_streaming_session(
        self, *, sessionId: str, studioId: str, clientToken: str = ...
    ) -> DeleteStreamingSessionResponseTypeDef:
        """
        Deletes streaming session resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.delete_streaming_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#delete_streaming_session)
        """

    def delete_studio(
        self, *, studioId: str, clientToken: str = ...
    ) -> DeleteStudioResponseTypeDef:
        """
        Delete a studio resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.delete_studio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#delete_studio)
        """

    def delete_studio_component(
        self, *, studioComponentId: str, studioId: str, clientToken: str = ...
    ) -> DeleteStudioComponentResponseTypeDef:
        """
        Deletes a studio component resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.delete_studio_component)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#delete_studio_component)
        """

    def delete_studio_member(
        self, *, principalId: str, studioId: str, clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Delete a user from studio membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.delete_studio_member)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#delete_studio_member)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#generate_presigned_url)
        """

    def get_eula(self, *, eulaId: str) -> GetEulaResponseTypeDef:
        """
        Get Eula.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_eula)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_eula)
        """

    def get_launch_profile(
        self, *, launchProfileId: str, studioId: str
    ) -> GetLaunchProfileResponseTypeDef:
        """
        Get a launch profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_launch_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_launch_profile)
        """

    def get_launch_profile_details(
        self, *, launchProfileId: str, studioId: str
    ) -> GetLaunchProfileDetailsResponseTypeDef:
        """
        Launch profile details include the launch profile resource and summary
        information of resources that are used by, or available to, the launch profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_launch_profile_details)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_launch_profile_details)
        """

    def get_launch_profile_initialization(
        self,
        *,
        launchProfileId: str,
        launchProfileProtocolVersions: Sequence[str],
        launchPurpose: str,
        platform: str,
        studioId: str
    ) -> GetLaunchProfileInitializationResponseTypeDef:
        """
        Get a launch profile initialization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_launch_profile_initialization)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_launch_profile_initialization)
        """

    def get_launch_profile_member(
        self, *, launchProfileId: str, principalId: str, studioId: str
    ) -> GetLaunchProfileMemberResponseTypeDef:
        """
        Get a user persona in launch profile membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_launch_profile_member)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_launch_profile_member)
        """

    def get_streaming_image(
        self, *, streamingImageId: str, studioId: str
    ) -> GetStreamingImageResponseTypeDef:
        """
        Get streaming image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_streaming_image)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_streaming_image)
        """

    def get_streaming_session(
        self, *, sessionId: str, studioId: str
    ) -> GetStreamingSessionResponseTypeDef:
        """
        Gets StreamingSession resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_streaming_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_streaming_session)
        """

    def get_streaming_session_stream(
        self, *, sessionId: str, streamId: str, studioId: str
    ) -> GetStreamingSessionStreamResponseTypeDef:
        """
        Gets a StreamingSessionStream for a streaming session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_streaming_session_stream)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_streaming_session_stream)
        """

    def get_studio(self, *, studioId: str) -> GetStudioResponseTypeDef:
        """
        Get a Studio resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_studio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_studio)
        """

    def get_studio_component(
        self, *, studioComponentId: str, studioId: str
    ) -> GetStudioComponentResponseTypeDef:
        """
        Gets a studio component resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_studio_component)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_studio_component)
        """

    def get_studio_member(
        self, *, principalId: str, studioId: str
    ) -> GetStudioMemberResponseTypeDef:
        """
        Get a user's membership in a studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_studio_member)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_studio_member)
        """

    def list_eula_acceptances(
        self, *, studioId: str, eulaIds: Sequence[str] = ..., nextToken: str = ...
    ) -> ListEulaAcceptancesResponseTypeDef:
        """
        List Eula Acceptances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.list_eula_acceptances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#list_eula_acceptances)
        """

    def list_eulas(
        self, *, eulaIds: Sequence[str] = ..., nextToken: str = ...
    ) -> ListEulasResponseTypeDef:
        """
        List Eulas.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.list_eulas)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#list_eulas)
        """

    def list_launch_profile_members(
        self, *, launchProfileId: str, studioId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListLaunchProfileMembersResponseTypeDef:
        """
        Get all users in a given launch profile membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.list_launch_profile_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#list_launch_profile_members)
        """

    def list_launch_profiles(
        self,
        *,
        studioId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        principalId: str = ...,
        states: Sequence[LaunchProfileStateType] = ...
    ) -> ListLaunchProfilesResponseTypeDef:
        """
        List all the launch profiles a studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.list_launch_profiles)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#list_launch_profiles)
        """

    def list_streaming_images(
        self, *, studioId: str, nextToken: str = ..., owner: str = ...
    ) -> ListStreamingImagesResponseTypeDef:
        """
        List the streaming image resources available to this studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.list_streaming_images)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#list_streaming_images)
        """

    def list_streaming_sessions(
        self,
        *,
        studioId: str,
        createdBy: str = ...,
        nextToken: str = ...,
        ownedBy: str = ...,
        sessionIds: str = ...
    ) -> ListStreamingSessionsResponseTypeDef:
        """
        Lists the streaming image resources in a studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.list_streaming_sessions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#list_streaming_sessions)
        """

    def list_studio_components(
        self,
        *,
        studioId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        states: Sequence[StudioComponentStateType] = ...,
        types: Sequence[StudioComponentTypeType] = ...
    ) -> ListStudioComponentsResponseTypeDef:
        """
        Lists the StudioComponents in a studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.list_studio_components)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#list_studio_components)
        """

    def list_studio_members(
        self, *, studioId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListStudioMembersResponseTypeDef:
        """
        Get all users in a given studio membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.list_studio_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#list_studio_members)
        """

    def list_studios(self, *, nextToken: str = ...) -> ListStudiosResponseTypeDef:
        """
        List studios in your Amazon Web Services account in the requested Amazon Web
        Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.list_studios)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#list_studios)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Gets the tags for a resource, given its Amazon Resource Names (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#list_tags_for_resource)
        """

    def put_launch_profile_members(
        self,
        *,
        identityStoreId: str,
        launchProfileId: str,
        members: Sequence[NewLaunchProfileMemberTypeDef],
        studioId: str,
        clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Add/update users with given persona to launch profile membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.put_launch_profile_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#put_launch_profile_members)
        """

    def put_studio_members(
        self,
        *,
        identityStoreId: str,
        members: Sequence[NewStudioMemberTypeDef],
        studioId: str,
        clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Add/update users with given persona to studio membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.put_studio_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#put_studio_members)
        """

    def start_streaming_session(
        self, *, sessionId: str, studioId: str, clientToken: str = ...
    ) -> StartStreamingSessionResponseTypeDef:
        """
        Transitions sessions from the STOPPED state into the READY state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.start_streaming_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#start_streaming_session)
        """

    def start_studio_sso_configuration_repair(
        self, *, studioId: str, clientToken: str = ...
    ) -> StartStudioSSOConfigurationRepairResponseTypeDef:
        """
        Repairs the Amazon Web Services SSO configuration for a given studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.start_studio_sso_configuration_repair)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#start_studio_sso_configuration_repair)
        """

    def stop_streaming_session(
        self, *, sessionId: str, studioId: str, clientToken: str = ...
    ) -> StopStreamingSessionResponseTypeDef:
        """
        Transitions sessions from the READY state into the STOPPED state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.stop_streaming_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#stop_streaming_session)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str] = ...) -> Dict[str, Any]:
        """
        Creates tags for a resource, given its ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#untag_resource)
        """

    def update_launch_profile(
        self,
        *,
        launchProfileId: str,
        studioId: str,
        clientToken: str = ...,
        description: str = ...,
        launchProfileProtocolVersions: Sequence[str] = ...,
        name: str = ...,
        streamConfiguration: StreamConfigurationCreateTypeDef = ...,
        studioComponentIds: Sequence[str] = ...
    ) -> UpdateLaunchProfileResponseTypeDef:
        """
        Update a launch profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.update_launch_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#update_launch_profile)
        """

    def update_launch_profile_member(
        self,
        *,
        launchProfileId: str,
        persona: Literal["USER"],
        principalId: str,
        studioId: str,
        clientToken: str = ...
    ) -> UpdateLaunchProfileMemberResponseTypeDef:
        """
        Update a user persona in launch profile membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.update_launch_profile_member)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#update_launch_profile_member)
        """

    def update_streaming_image(
        self,
        *,
        streamingImageId: str,
        studioId: str,
        clientToken: str = ...,
        description: str = ...,
        name: str = ...
    ) -> UpdateStreamingImageResponseTypeDef:
        """
        Update streaming image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.update_streaming_image)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#update_streaming_image)
        """

    def update_studio(
        self,
        *,
        studioId: str,
        adminRoleArn: str = ...,
        clientToken: str = ...,
        displayName: str = ...,
        userRoleArn: str = ...
    ) -> UpdateStudioResponseTypeDef:
        """
        Update a Studio resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.update_studio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#update_studio)
        """

    def update_studio_component(
        self,
        *,
        studioComponentId: str,
        studioId: str,
        clientToken: str = ...,
        configuration: StudioComponentConfigurationTypeDef = ...,
        description: str = ...,
        ec2SecurityGroupIds: Sequence[str] = ...,
        initializationScripts: Sequence[StudioComponentInitializationScriptTypeDef] = ...,
        name: str = ...,
        scriptParameters: Sequence[ScriptParameterKeyValueTypeDef] = ...,
        subtype: StudioComponentSubtypeType = ...,
        type: StudioComponentTypeType = ...
    ) -> UpdateStudioComponentResponseTypeDef:
        """
        Updates a studio component resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.update_studio_component)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#update_studio_component)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_eula_acceptances"]
    ) -> ListEulaAcceptancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_eulas"]) -> ListEulasPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_launch_profile_members"]
    ) -> ListLaunchProfileMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_launch_profiles"]
    ) -> ListLaunchProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_streaming_images"]
    ) -> ListStreamingImagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_streaming_sessions"]
    ) -> ListStreamingSessionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_studio_components"]
    ) -> ListStudioComponentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_studio_members"]
    ) -> ListStudioMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_studios"]) -> ListStudiosPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["launch_profile_deleted"]
    ) -> LaunchProfileDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["launch_profile_ready"]) -> LaunchProfileReadyWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["streaming_image_deleted"]
    ) -> StreamingImageDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["streaming_image_ready"]
    ) -> StreamingImageReadyWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["streaming_session_deleted"]
    ) -> StreamingSessionDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["streaming_session_ready"]
    ) -> StreamingSessionReadyWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["streaming_session_stopped"]
    ) -> StreamingSessionStoppedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["streaming_session_stream_ready"]
    ) -> StreamingSessionStreamReadyWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["studio_component_deleted"]
    ) -> StudioComponentDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["studio_component_ready"]
    ) -> StudioComponentReadyWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["studio_deleted"]) -> StudioDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["studio_ready"]) -> StudioReadyWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/client/#get_waiter)
        """
