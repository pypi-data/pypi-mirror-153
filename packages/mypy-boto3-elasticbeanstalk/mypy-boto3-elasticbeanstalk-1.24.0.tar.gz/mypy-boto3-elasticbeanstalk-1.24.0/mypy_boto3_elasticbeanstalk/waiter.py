"""
Type annotations for elasticbeanstalk service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elasticbeanstalk.client import ElasticBeanstalkClient
    from mypy_boto3_elasticbeanstalk.waiter import (
        EnvironmentExistsWaiter,
        EnvironmentTerminatedWaiter,
        EnvironmentUpdatedWaiter,
    )

    session = Session()
    client: ElasticBeanstalkClient = session.client("elasticbeanstalk")

    environment_exists_waiter: EnvironmentExistsWaiter = client.get_waiter("environment_exists")
    environment_terminated_waiter: EnvironmentTerminatedWaiter = client.get_waiter("environment_terminated")
    environment_updated_waiter: EnvironmentUpdatedWaiter = client.get_waiter("environment_updated")
    ```
"""
from datetime import datetime
from typing import Sequence, Union

from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("EnvironmentExistsWaiter", "EnvironmentTerminatedWaiter", "EnvironmentUpdatedWaiter")


class EnvironmentExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Waiter.EnvironmentExists)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/#environmentexistswaiter)
    """

    def wait(
        self,
        *,
        ApplicationName: str = ...,
        VersionLabel: str = ...,
        EnvironmentIds: Sequence[str] = ...,
        EnvironmentNames: Sequence[str] = ...,
        IncludeDeleted: bool = ...,
        IncludedDeletedBackTo: Union[datetime, str] = ...,
        MaxRecords: int = ...,
        NextToken: str = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Waiter.EnvironmentExists.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/#environmentexistswaiter)
        """


class EnvironmentTerminatedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Waiter.EnvironmentTerminated)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/#environmentterminatedwaiter)
    """

    def wait(
        self,
        *,
        ApplicationName: str = ...,
        VersionLabel: str = ...,
        EnvironmentIds: Sequence[str] = ...,
        EnvironmentNames: Sequence[str] = ...,
        IncludeDeleted: bool = ...,
        IncludedDeletedBackTo: Union[datetime, str] = ...,
        MaxRecords: int = ...,
        NextToken: str = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Waiter.EnvironmentTerminated.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/#environmentterminatedwaiter)
        """


class EnvironmentUpdatedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Waiter.EnvironmentUpdated)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/#environmentupdatedwaiter)
    """

    def wait(
        self,
        *,
        ApplicationName: str = ...,
        VersionLabel: str = ...,
        EnvironmentIds: Sequence[str] = ...,
        EnvironmentNames: Sequence[str] = ...,
        IncludeDeleted: bool = ...,
        IncludedDeletedBackTo: Union[datetime, str] = ...,
        MaxRecords: int = ...,
        NextToken: str = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Waiter.EnvironmentUpdated.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elasticbeanstalk/waiters/#environmentupdatedwaiter)
        """
