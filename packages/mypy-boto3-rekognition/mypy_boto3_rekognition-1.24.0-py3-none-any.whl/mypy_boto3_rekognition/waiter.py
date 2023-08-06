"""
Type annotations for rekognition service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_rekognition.client import RekognitionClient
    from mypy_boto3_rekognition.waiter import (
        ProjectVersionRunningWaiter,
        ProjectVersionTrainingCompletedWaiter,
    )

    session = Session()
    client: RekognitionClient = session.client("rekognition")

    project_version_running_waiter: ProjectVersionRunningWaiter = client.get_waiter("project_version_running")
    project_version_training_completed_waiter: ProjectVersionTrainingCompletedWaiter = client.get_waiter("project_version_training_completed")
    ```
"""
from typing import Sequence

from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("ProjectVersionRunningWaiter", "ProjectVersionTrainingCompletedWaiter")


class ProjectVersionRunningWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Waiter.ProjectVersionRunning)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/waiters/#projectversionrunningwaiter)
    """

    def wait(
        self,
        *,
        ProjectArn: str,
        VersionNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Waiter.ProjectVersionRunning.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/waiters/#projectversionrunningwaiter)
        """


class ProjectVersionTrainingCompletedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Waiter.ProjectVersionTrainingCompleted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/waiters/#projectversiontrainingcompletedwaiter)
    """

    def wait(
        self,
        *,
        ProjectArn: str,
        VersionNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Waiter.ProjectVersionTrainingCompleted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/waiters/#projectversiontrainingcompletedwaiter)
        """
