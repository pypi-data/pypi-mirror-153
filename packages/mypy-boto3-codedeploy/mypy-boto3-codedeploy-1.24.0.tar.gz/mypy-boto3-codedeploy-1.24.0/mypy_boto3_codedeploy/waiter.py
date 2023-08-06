"""
Type annotations for codedeploy service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codedeploy.client import CodeDeployClient
    from mypy_boto3_codedeploy.waiter import (
        DeploymentSuccessfulWaiter,
    )

    session = Session()
    client: CodeDeployClient = session.client("codedeploy")

    deployment_successful_waiter: DeploymentSuccessfulWaiter = client.get_waiter("deployment_successful")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("DeploymentSuccessfulWaiter",)


class DeploymentSuccessfulWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Waiter.DeploymentSuccessful)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/waiters/#deploymentsuccessfulwaiter)
    """

    def wait(self, *, deploymentId: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Waiter.DeploymentSuccessful.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codedeploy/waiters/#deploymentsuccessfulwaiter)
        """
