"""
Type annotations for codeartifact service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codeartifact.client import CodeArtifactClient
    from mypy_boto3_codeartifact.paginator import (
        ListDomainsPaginator,
        ListPackageVersionAssetsPaginator,
        ListPackageVersionsPaginator,
        ListPackagesPaginator,
        ListRepositoriesPaginator,
        ListRepositoriesInDomainPaginator,
    )

    session = Session()
    client: CodeArtifactClient = session.client("codeartifact")

    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_package_version_assets_paginator: ListPackageVersionAssetsPaginator = client.get_paginator("list_package_version_assets")
    list_package_versions_paginator: ListPackageVersionsPaginator = client.get_paginator("list_package_versions")
    list_packages_paginator: ListPackagesPaginator = client.get_paginator("list_packages")
    list_repositories_paginator: ListRepositoriesPaginator = client.get_paginator("list_repositories")
    list_repositories_in_domain_paginator: ListRepositoriesInDomainPaginator = client.get_paginator("list_repositories_in_domain")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import PackageFormatType, PackageVersionStatusType
from .type_defs import (
    ListDomainsResultTypeDef,
    ListPackagesResultTypeDef,
    ListPackageVersionAssetsResultTypeDef,
    ListPackageVersionsResultTypeDef,
    ListRepositoriesInDomainResultTypeDef,
    ListRepositoriesResultTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ListDomainsPaginator",
    "ListPackageVersionAssetsPaginator",
    "ListPackageVersionsPaginator",
    "ListPackagesPaginator",
    "ListRepositoriesPaginator",
    "ListRepositoriesInDomainPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDomainsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Paginator.ListDomains)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators/#listdomainspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDomainsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Paginator.ListDomains.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators/#listdomainspaginator)
        """

class ListPackageVersionAssetsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Paginator.ListPackageVersionAssets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators/#listpackageversionassetspaginator)
    """

    def paginate(
        self,
        *,
        domain: str,
        repository: str,
        format: PackageFormatType,
        package: str,
        packageVersion: str,
        domainOwner: str = ...,
        namespace: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPackageVersionAssetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Paginator.ListPackageVersionAssets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators/#listpackageversionassetspaginator)
        """

class ListPackageVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Paginator.ListPackageVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators/#listpackageversionspaginator)
    """

    def paginate(
        self,
        *,
        domain: str,
        repository: str,
        format: PackageFormatType,
        package: str,
        domainOwner: str = ...,
        namespace: str = ...,
        status: PackageVersionStatusType = ...,
        sortBy: Literal["PUBLISHED_TIME"] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPackageVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Paginator.ListPackageVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators/#listpackageversionspaginator)
        """

class ListPackagesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Paginator.ListPackages)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators/#listpackagespaginator)
    """

    def paginate(
        self,
        *,
        domain: str,
        repository: str,
        domainOwner: str = ...,
        format: PackageFormatType = ...,
        namespace: str = ...,
        packagePrefix: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPackagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Paginator.ListPackages.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators/#listpackagespaginator)
        """

class ListRepositoriesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Paginator.ListRepositories)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators/#listrepositoriespaginator)
    """

    def paginate(
        self, *, repositoryPrefix: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRepositoriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Paginator.ListRepositories.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators/#listrepositoriespaginator)
        """

class ListRepositoriesInDomainPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Paginator.ListRepositoriesInDomain)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators/#listrepositoriesindomainpaginator)
    """

    def paginate(
        self,
        *,
        domain: str,
        domainOwner: str = ...,
        administratorAccount: str = ...,
        repositoryPrefix: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRepositoriesInDomainResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact.html#CodeArtifact.Paginator.ListRepositoriesInDomain.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeartifact/paginators/#listrepositoriesindomainpaginator)
        """
