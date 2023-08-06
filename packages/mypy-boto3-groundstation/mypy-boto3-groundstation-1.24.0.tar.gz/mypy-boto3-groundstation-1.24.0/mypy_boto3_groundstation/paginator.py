"""
Type annotations for groundstation service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_groundstation.client import GroundStationClient
    from mypy_boto3_groundstation.paginator import (
        ListConfigsPaginator,
        ListContactsPaginator,
        ListDataflowEndpointGroupsPaginator,
        ListGroundStationsPaginator,
        ListMissionProfilesPaginator,
        ListSatellitesPaginator,
    )

    session = Session()
    client: GroundStationClient = session.client("groundstation")

    list_configs_paginator: ListConfigsPaginator = client.get_paginator("list_configs")
    list_contacts_paginator: ListContactsPaginator = client.get_paginator("list_contacts")
    list_dataflow_endpoint_groups_paginator: ListDataflowEndpointGroupsPaginator = client.get_paginator("list_dataflow_endpoint_groups")
    list_ground_stations_paginator: ListGroundStationsPaginator = client.get_paginator("list_ground_stations")
    list_mission_profiles_paginator: ListMissionProfilesPaginator = client.get_paginator("list_mission_profiles")
    list_satellites_paginator: ListSatellitesPaginator = client.get_paginator("list_satellites")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .literals import ContactStatusType
from .type_defs import (
    ListConfigsResponseTypeDef,
    ListContactsResponseTypeDef,
    ListDataflowEndpointGroupsResponseTypeDef,
    ListGroundStationsResponseTypeDef,
    ListMissionProfilesResponseTypeDef,
    ListSatellitesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListConfigsPaginator",
    "ListContactsPaginator",
    "ListDataflowEndpointGroupsPaginator",
    "ListGroundStationsPaginator",
    "ListMissionProfilesPaginator",
    "ListSatellitesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListConfigsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Paginator.ListConfigs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listconfigspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Paginator.ListConfigs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listconfigspaginator)
        """


class ListContactsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Paginator.ListContacts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listcontactspaginator)
    """

    def paginate(
        self,
        *,
        endTime: Union[datetime, str],
        startTime: Union[datetime, str],
        statusList: Sequence[ContactStatusType],
        groundStation: str = ...,
        missionProfileArn: str = ...,
        satelliteArn: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListContactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Paginator.ListContacts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listcontactspaginator)
        """


class ListDataflowEndpointGroupsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Paginator.ListDataflowEndpointGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listdataflowendpointgroupspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDataflowEndpointGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Paginator.ListDataflowEndpointGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listdataflowendpointgroupspaginator)
        """


class ListGroundStationsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Paginator.ListGroundStations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listgroundstationspaginator)
    """

    def paginate(
        self, *, satelliteId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListGroundStationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Paginator.ListGroundStations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listgroundstationspaginator)
        """


class ListMissionProfilesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Paginator.ListMissionProfiles)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listmissionprofilespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMissionProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Paginator.ListMissionProfiles.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listmissionprofilespaginator)
        """


class ListSatellitesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Paginator.ListSatellites)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listsatellitespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSatellitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/groundstation.html#GroundStation.Paginator.ListSatellites.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_groundstation/paginators/#listsatellitespaginator)
        """
