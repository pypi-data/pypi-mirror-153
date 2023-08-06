"""
Type annotations for elastictranscoder service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elastictranscoder.client import ElasticTranscoderClient
    from mypy_boto3_elastictranscoder.waiter import (
        JobCompleteWaiter,
    )

    session = Session()
    client: ElasticTranscoderClient = session.client("elastictranscoder")

    job_complete_waiter: JobCompleteWaiter = client.get_waiter("job_complete")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("JobCompleteWaiter",)


class JobCompleteWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Waiter.JobComplete)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/waiters/#jobcompletewaiter)
    """

    def wait(self, *, Id: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder.html#ElasticTranscoder.Waiter.JobComplete.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elastictranscoder/waiters/#jobcompletewaiter)
        """
