"""
Type annotations for route53 service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_route53.client import Route53Client
    from mypy_boto3_route53.waiter import (
        ResourceRecordSetsChangedWaiter,
    )

    session = Session()
    client: Route53Client = session.client("route53")

    resource_record_sets_changed_waiter: ResourceRecordSetsChangedWaiter = client.get_waiter("resource_record_sets_changed")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("ResourceRecordSetsChangedWaiter",)


class ResourceRecordSetsChangedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Waiter.ResourceRecordSetsChanged)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/waiters/#resourcerecordsetschangedwaiter)
    """

    def wait(self, *, Id: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Waiter.ResourceRecordSetsChanged.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/waiters/#resourcerecordsetschangedwaiter)
        """
