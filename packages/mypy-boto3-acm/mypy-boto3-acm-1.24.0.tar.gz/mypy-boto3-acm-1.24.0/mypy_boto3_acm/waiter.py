"""
Type annotations for acm service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_acm.client import ACMClient
    from mypy_boto3_acm.waiter import (
        CertificateValidatedWaiter,
    )

    session = Session()
    client: ACMClient = session.client("acm")

    certificate_validated_waiter: CertificateValidatedWaiter = client.get_waiter("certificate_validated")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("CertificateValidatedWaiter",)


class CertificateValidatedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Waiter.CertificateValidated)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/waiters/#certificatevalidatedwaiter)
    """

    def wait(self, *, CertificateArn: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Waiter.CertificateValidated.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/waiters/#certificatevalidatedwaiter)
        """
