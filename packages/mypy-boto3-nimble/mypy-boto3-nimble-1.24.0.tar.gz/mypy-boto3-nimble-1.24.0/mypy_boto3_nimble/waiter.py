"""
Type annotations for nimble service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_nimble.client import NimbleStudioClient
    from mypy_boto3_nimble.waiter import (
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

    session = Session()
    client: NimbleStudioClient = session.client("nimble")

    launch_profile_deleted_waiter: LaunchProfileDeletedWaiter = client.get_waiter("launch_profile_deleted")
    launch_profile_ready_waiter: LaunchProfileReadyWaiter = client.get_waiter("launch_profile_ready")
    streaming_image_deleted_waiter: StreamingImageDeletedWaiter = client.get_waiter("streaming_image_deleted")
    streaming_image_ready_waiter: StreamingImageReadyWaiter = client.get_waiter("streaming_image_ready")
    streaming_session_deleted_waiter: StreamingSessionDeletedWaiter = client.get_waiter("streaming_session_deleted")
    streaming_session_ready_waiter: StreamingSessionReadyWaiter = client.get_waiter("streaming_session_ready")
    streaming_session_stopped_waiter: StreamingSessionStoppedWaiter = client.get_waiter("streaming_session_stopped")
    streaming_session_stream_ready_waiter: StreamingSessionStreamReadyWaiter = client.get_waiter("streaming_session_stream_ready")
    studio_component_deleted_waiter: StudioComponentDeletedWaiter = client.get_waiter("studio_component_deleted")
    studio_component_ready_waiter: StudioComponentReadyWaiter = client.get_waiter("studio_component_ready")
    studio_deleted_waiter: StudioDeletedWaiter = client.get_waiter("studio_deleted")
    studio_ready_waiter: StudioReadyWaiter = client.get_waiter("studio_ready")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "LaunchProfileDeletedWaiter",
    "LaunchProfileReadyWaiter",
    "StreamingImageDeletedWaiter",
    "StreamingImageReadyWaiter",
    "StreamingSessionDeletedWaiter",
    "StreamingSessionReadyWaiter",
    "StreamingSessionStoppedWaiter",
    "StreamingSessionStreamReadyWaiter",
    "StudioComponentDeletedWaiter",
    "StudioComponentReadyWaiter",
    "StudioDeletedWaiter",
    "StudioReadyWaiter",
)


class LaunchProfileDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.LaunchProfileDeleted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#launchprofiledeletedwaiter)
    """

    def wait(
        self, *, launchProfileId: str, studioId: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.LaunchProfileDeleted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#launchprofiledeletedwaiter)
        """


class LaunchProfileReadyWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.LaunchProfileReady)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#launchprofilereadywaiter)
    """

    def wait(
        self, *, launchProfileId: str, studioId: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.LaunchProfileReady.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#launchprofilereadywaiter)
        """


class StreamingImageDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingImageDeleted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#streamingimagedeletedwaiter)
    """

    def wait(
        self, *, streamingImageId: str, studioId: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingImageDeleted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#streamingimagedeletedwaiter)
        """


class StreamingImageReadyWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingImageReady)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#streamingimagereadywaiter)
    """

    def wait(
        self, *, streamingImageId: str, studioId: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingImageReady.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#streamingimagereadywaiter)
        """


class StreamingSessionDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionDeleted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#streamingsessiondeletedwaiter)
    """

    def wait(
        self, *, sessionId: str, studioId: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionDeleted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#streamingsessiondeletedwaiter)
        """


class StreamingSessionReadyWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionReady)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#streamingsessionreadywaiter)
    """

    def wait(
        self, *, sessionId: str, studioId: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionReady.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#streamingsessionreadywaiter)
        """


class StreamingSessionStoppedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionStopped)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#streamingsessionstoppedwaiter)
    """

    def wait(
        self, *, sessionId: str, studioId: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionStopped.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#streamingsessionstoppedwaiter)
        """


class StreamingSessionStreamReadyWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionStreamReady)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#streamingsessionstreamreadywaiter)
    """

    def wait(
        self,
        *,
        sessionId: str,
        streamId: str,
        studioId: str,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionStreamReady.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#streamingsessionstreamreadywaiter)
        """


class StudioComponentDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioComponentDeleted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#studiocomponentdeletedwaiter)
    """

    def wait(
        self, *, studioComponentId: str, studioId: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioComponentDeleted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#studiocomponentdeletedwaiter)
        """


class StudioComponentReadyWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioComponentReady)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#studiocomponentreadywaiter)
    """

    def wait(
        self, *, studioComponentId: str, studioId: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioComponentReady.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#studiocomponentreadywaiter)
        """


class StudioDeletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioDeleted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#studiodeletedwaiter)
    """

    def wait(self, *, studioId: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioDeleted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#studiodeletedwaiter)
        """


class StudioReadyWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioReady)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#studioreadywaiter)
    """

    def wait(self, *, studioId: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioReady.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/waiters/#studioreadywaiter)
        """
