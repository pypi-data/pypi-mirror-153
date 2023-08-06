"""
Type annotations for greengrassv2 service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_greengrassv2.client import GreengrassV2Client
    from mypy_boto3_greengrassv2.paginator import (
        ListClientDevicesAssociatedWithCoreDevicePaginator,
        ListComponentVersionsPaginator,
        ListComponentsPaginator,
        ListCoreDevicesPaginator,
        ListDeploymentsPaginator,
        ListEffectiveDeploymentsPaginator,
        ListInstalledComponentsPaginator,
    )

    session = Session()
    client: GreengrassV2Client = session.client("greengrassv2")

    list_client_devices_associated_with_core_device_paginator: ListClientDevicesAssociatedWithCoreDevicePaginator = client.get_paginator("list_client_devices_associated_with_core_device")
    list_component_versions_paginator: ListComponentVersionsPaginator = client.get_paginator("list_component_versions")
    list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
    list_core_devices_paginator: ListCoreDevicesPaginator = client.get_paginator("list_core_devices")
    list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
    list_effective_deployments_paginator: ListEffectiveDeploymentsPaginator = client.get_paginator("list_effective_deployments")
    list_installed_components_paginator: ListInstalledComponentsPaginator = client.get_paginator("list_installed_components")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    ComponentVisibilityScopeType,
    CoreDeviceStatusType,
    DeploymentHistoryFilterType,
)
from .type_defs import (
    ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef,
    ListComponentsResponseTypeDef,
    ListComponentVersionsResponseTypeDef,
    ListCoreDevicesResponseTypeDef,
    ListDeploymentsResponseTypeDef,
    ListEffectiveDeploymentsResponseTypeDef,
    ListInstalledComponentsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListClientDevicesAssociatedWithCoreDevicePaginator",
    "ListComponentVersionsPaginator",
    "ListComponentsPaginator",
    "ListCoreDevicesPaginator",
    "ListDeploymentsPaginator",
    "ListEffectiveDeploymentsPaginator",
    "ListInstalledComponentsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListClientDevicesAssociatedWithCoreDevicePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListClientDevicesAssociatedWithCoreDevice)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listclientdevicesassociatedwithcoredevicepaginator)
    """

    def paginate(
        self, *, coreDeviceThingName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListClientDevicesAssociatedWithCoreDevice.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listclientdevicesassociatedwithcoredevicepaginator)
        """

class ListComponentVersionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListComponentVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listcomponentversionspaginator)
    """

    def paginate(
        self, *, arn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListComponentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListComponentVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listcomponentversionspaginator)
        """

class ListComponentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListComponents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listcomponentspaginator)
    """

    def paginate(
        self,
        *,
        scope: ComponentVisibilityScopeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListComponents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listcomponentspaginator)
        """

class ListCoreDevicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListCoreDevices)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listcoredevicespaginator)
    """

    def paginate(
        self,
        *,
        thingGroupArn: str = ...,
        status: CoreDeviceStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCoreDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListCoreDevices.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listcoredevicespaginator)
        """

class ListDeploymentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListDeployments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listdeploymentspaginator)
    """

    def paginate(
        self,
        *,
        targetArn: str = ...,
        historyFilter: DeploymentHistoryFilterType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListDeployments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listdeploymentspaginator)
        """

class ListEffectiveDeploymentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListEffectiveDeployments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listeffectivedeploymentspaginator)
    """

    def paginate(
        self, *, coreDeviceThingName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEffectiveDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListEffectiveDeployments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listeffectivedeploymentspaginator)
        """

class ListInstalledComponentsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListInstalledComponents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listinstalledcomponentspaginator)
    """

    def paginate(
        self, *, coreDeviceThingName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListInstalledComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListInstalledComponents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/paginators/#listinstalledcomponentspaginator)
        """
