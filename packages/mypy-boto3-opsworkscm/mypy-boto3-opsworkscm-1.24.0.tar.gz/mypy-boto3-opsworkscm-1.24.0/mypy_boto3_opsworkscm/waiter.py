"""
Type annotations for opsworkscm service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworkscm/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_opsworkscm.client import OpsWorksCMClient
    from mypy_boto3_opsworkscm.waiter import (
        NodeAssociatedWaiter,
    )

    session = Session()
    client: OpsWorksCMClient = session.client("opsworkscm")

    node_associated_waiter: NodeAssociatedWaiter = client.get_waiter("node_associated")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("NodeAssociatedWaiter",)


class NodeAssociatedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm.html#OpsWorksCM.Waiter.NodeAssociated)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworkscm/waiters/#nodeassociatedwaiter)
    """

    def wait(
        self,
        *,
        NodeAssociationStatusToken: str,
        ServerName: str,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworkscm.html#OpsWorksCM.Waiter.NodeAssociated.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworkscm/waiters/#nodeassociatedwaiter)
        """
