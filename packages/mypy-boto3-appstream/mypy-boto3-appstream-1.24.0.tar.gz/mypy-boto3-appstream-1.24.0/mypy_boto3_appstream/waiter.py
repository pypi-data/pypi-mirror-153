"""
Type annotations for appstream service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_appstream.client import AppStreamClient
    from mypy_boto3_appstream.waiter import (
        FleetStartedWaiter,
        FleetStoppedWaiter,
    )

    session = Session()
    client: AppStreamClient = session.client("appstream")

    fleet_started_waiter: FleetStartedWaiter = client.get_waiter("fleet_started")
    fleet_stopped_waiter: FleetStoppedWaiter = client.get_waiter("fleet_stopped")
    ```
"""
from typing import Sequence

from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("FleetStartedWaiter", "FleetStoppedWaiter")


class FleetStartedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Waiter.FleetStarted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/waiters/#fleetstartedwaiter)
    """

    def wait(
        self,
        *,
        Names: Sequence[str] = ...,
        NextToken: str = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Waiter.FleetStarted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/waiters/#fleetstartedwaiter)
        """


class FleetStoppedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Waiter.FleetStopped)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/waiters/#fleetstoppedwaiter)
    """

    def wait(
        self,
        *,
        Names: Sequence[str] = ...,
        NextToken: str = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Waiter.FleetStopped.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appstream/waiters/#fleetstoppedwaiter)
        """
