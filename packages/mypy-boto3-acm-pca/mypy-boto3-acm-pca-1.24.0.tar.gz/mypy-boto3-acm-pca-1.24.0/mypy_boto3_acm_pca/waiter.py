"""
Type annotations for acm-pca service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_acm_pca.client import ACMPCAClient
    from mypy_boto3_acm_pca.waiter import (
        AuditReportCreatedWaiter,
        CertificateAuthorityCSRCreatedWaiter,
        CertificateIssuedWaiter,
    )

    session = Session()
    client: ACMPCAClient = session.client("acm-pca")

    audit_report_created_waiter: AuditReportCreatedWaiter = client.get_waiter("audit_report_created")
    certificate_authority_csr_created_waiter: CertificateAuthorityCSRCreatedWaiter = client.get_waiter("certificate_authority_csr_created")
    certificate_issued_waiter: CertificateIssuedWaiter = client.get_waiter("certificate_issued")
    ```
"""
from botocore.waiter import Waiter as Boto3Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "AuditReportCreatedWaiter",
    "CertificateAuthorityCSRCreatedWaiter",
    "CertificateIssuedWaiter",
)


class AuditReportCreatedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Waiter.AuditReportCreated)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/#auditreportcreatedwaiter)
    """

    def wait(
        self,
        *,
        CertificateAuthorityArn: str,
        AuditReportId: str,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Waiter.AuditReportCreated.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/#auditreportcreatedwaiter)
        """


class CertificateAuthorityCSRCreatedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Waiter.CertificateAuthorityCSRCreated)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/#certificateauthoritycsrcreatedwaiter)
    """

    def wait(
        self, *, CertificateAuthorityArn: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Waiter.CertificateAuthorityCSRCreated.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/#certificateauthoritycsrcreatedwaiter)
        """


class CertificateIssuedWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Waiter.CertificateIssued)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/#certificateissuedwaiter)
    """

    def wait(
        self,
        *,
        CertificateAuthorityArn: str,
        CertificateArn: str,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca.html#ACMPCA.Waiter.CertificateIssued.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm_pca/waiters/#certificateissuedwaiter)
        """
