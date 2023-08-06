"""
Type annotations for glacier service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_glacier.client import GlacierClient
    from mypy_boto3_glacier.waiter import (
        VaultExistsWaiter,
        VaultNotExistsWaiter,
    )

    session = Session()
    client: GlacierClient = session.client("glacier")

    vault_exists_waiter: VaultExistsWaiter = client.get_waiter("vault_exists")
    vault_not_exists_waiter: VaultNotExistsWaiter = client.get_waiter("vault_not_exists")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("VaultExistsWaiter", "VaultNotExistsWaiter")


class VaultExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Waiter.VaultExists)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/waiters/#vaultexistswaiter)
    """

    def wait(
        self, *, accountId: str, vaultName: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Waiter.VaultExists.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/waiters/#vaultexistswaiter)
        """


class VaultNotExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Waiter.VaultNotExists)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/waiters/#vaultnotexistswaiter)
    """

    def wait(
        self, *, accountId: str, vaultName: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Waiter.VaultNotExists.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/waiters/#vaultnotexistswaiter)
        """
