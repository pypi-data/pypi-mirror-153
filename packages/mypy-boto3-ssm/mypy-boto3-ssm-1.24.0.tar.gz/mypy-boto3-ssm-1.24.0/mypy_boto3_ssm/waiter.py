"""
Type annotations for ssm service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_ssm.client import SSMClient
    from mypy_boto3_ssm.waiter import (
        CommandExecutedWaiter,
    )

    session = Session()
    client: SSMClient = session.client("ssm")

    command_executed_waiter: CommandExecutedWaiter = client.get_waiter("command_executed")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("CommandExecutedWaiter",)


class CommandExecutedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Waiter.CommandExecuted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/waiters/#commandexecutedwaiter)
    """

    def wait(
        self,
        *,
        CommandId: str,
        InstanceId: str,
        PluginName: str = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Waiter.CommandExecuted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm/waiters/#commandexecutedwaiter)
        """
