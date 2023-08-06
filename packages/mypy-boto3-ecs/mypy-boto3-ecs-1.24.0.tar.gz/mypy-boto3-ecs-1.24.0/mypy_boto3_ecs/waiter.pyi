"""
Type annotations for ecs service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ecs.client import ECSClient
    from mypy_boto3_ecs.waiter import (
        ServicesInactiveWaiter,
        ServicesStableWaiter,
        TasksRunningWaiter,
        TasksStoppedWaiter,
    )

    session = Session()
    client: ECSClient = session.client("ecs")

    services_inactive_waiter: ServicesInactiveWaiter = client.get_waiter("services_inactive")
    services_stable_waiter: ServicesStableWaiter = client.get_waiter("services_stable")
    tasks_running_waiter: TasksRunningWaiter = client.get_waiter("tasks_running")
    tasks_stopped_waiter: TasksStoppedWaiter = client.get_waiter("tasks_stopped")
    ```
"""
import sys
from typing import Sequence

from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ServicesInactiveWaiter",
    "ServicesStableWaiter",
    "TasksRunningWaiter",
    "TasksStoppedWaiter",
)

class ServicesInactiveWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Waiter.ServicesInactive)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#servicesinactivewaiter)
    """

    def wait(
        self,
        *,
        services: Sequence[str],
        cluster: str = ...,
        include: Sequence[Literal["TAGS"]] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Waiter.ServicesInactive.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#servicesinactivewaiter)
        """

class ServicesStableWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Waiter.ServicesStable)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#servicesstablewaiter)
    """

    def wait(
        self,
        *,
        services: Sequence[str],
        cluster: str = ...,
        include: Sequence[Literal["TAGS"]] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Waiter.ServicesStable.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#servicesstablewaiter)
        """

class TasksRunningWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Waiter.TasksRunning)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#tasksrunningwaiter)
    """

    def wait(
        self,
        *,
        tasks: Sequence[str],
        cluster: str = ...,
        include: Sequence[Literal["TAGS"]] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Waiter.TasksRunning.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#tasksrunningwaiter)
        """

class TasksStoppedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Waiter.TasksStopped)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#tasksstoppedwaiter)
    """

    def wait(
        self,
        *,
        tasks: Sequence[str],
        cluster: str = ...,
        include: Sequence[Literal["TAGS"]] = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Waiter.TasksStopped.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ecs/waiters/#tasksstoppedwaiter)
        """
