"""
Type annotations for location service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_location.client import LocationServiceClient

    session = Session()
    client: LocationServiceClient = session.client("location")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import DistanceUnitType, PositionFilteringType, PricingPlanType, TravelModeType
from .paginator import (
    GetDevicePositionHistoryPaginator,
    ListDevicePositionsPaginator,
    ListGeofenceCollectionsPaginator,
    ListGeofencesPaginator,
    ListMapsPaginator,
    ListPlaceIndexesPaginator,
    ListRouteCalculatorsPaginator,
    ListTrackerConsumersPaginator,
    ListTrackersPaginator,
)
from .type_defs import (
    BatchDeleteDevicePositionHistoryResponseTypeDef,
    BatchDeleteGeofenceResponseTypeDef,
    BatchEvaluateGeofencesResponseTypeDef,
    BatchGetDevicePositionResponseTypeDef,
    BatchPutGeofenceRequestEntryTypeDef,
    BatchPutGeofenceResponseTypeDef,
    BatchUpdateDevicePositionResponseTypeDef,
    CalculateRouteCarModeOptionsTypeDef,
    CalculateRouteMatrixResponseTypeDef,
    CalculateRouteResponseTypeDef,
    CalculateRouteTruckModeOptionsTypeDef,
    CreateGeofenceCollectionResponseTypeDef,
    CreateMapResponseTypeDef,
    CreatePlaceIndexResponseTypeDef,
    CreateRouteCalculatorResponseTypeDef,
    CreateTrackerResponseTypeDef,
    DataSourceConfigurationTypeDef,
    DescribeGeofenceCollectionResponseTypeDef,
    DescribeMapResponseTypeDef,
    DescribePlaceIndexResponseTypeDef,
    DescribeRouteCalculatorResponseTypeDef,
    DescribeTrackerResponseTypeDef,
    DevicePositionUpdateTypeDef,
    GeofenceGeometryTypeDef,
    GetDevicePositionHistoryResponseTypeDef,
    GetDevicePositionResponseTypeDef,
    GetGeofenceResponseTypeDef,
    GetMapGlyphsResponseTypeDef,
    GetMapSpritesResponseTypeDef,
    GetMapStyleDescriptorResponseTypeDef,
    GetMapTileResponseTypeDef,
    ListDevicePositionsResponseTypeDef,
    ListGeofenceCollectionsResponseTypeDef,
    ListGeofencesResponseTypeDef,
    ListMapsResponseTypeDef,
    ListPlaceIndexesResponseTypeDef,
    ListRouteCalculatorsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrackerConsumersResponseTypeDef,
    ListTrackersResponseTypeDef,
    MapConfigurationTypeDef,
    PutGeofenceResponseTypeDef,
    SearchPlaceIndexForPositionResponseTypeDef,
    SearchPlaceIndexForSuggestionsResponseTypeDef,
    SearchPlaceIndexForTextResponseTypeDef,
    UpdateGeofenceCollectionResponseTypeDef,
    UpdateMapResponseTypeDef,
    UpdatePlaceIndexResponseTypeDef,
    UpdateRouteCalculatorResponseTypeDef,
    UpdateTrackerResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("LocationServiceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LocationServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LocationServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#exceptions)
        """

    def associate_tracker_consumer(self, *, ConsumerArn: str, TrackerName: str) -> Dict[str, Any]:
        """
        Creates an association between a geofence collection and a tracker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.associate_tracker_consumer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#associate_tracker_consumer)
        """

    def batch_delete_device_position_history(
        self, *, DeviceIds: Sequence[str], TrackerName: str
    ) -> BatchDeleteDevicePositionHistoryResponseTypeDef:
        """
        Deletes the position history of one or more devices from a tracker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_delete_device_position_history)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#batch_delete_device_position_history)
        """

    def batch_delete_geofence(
        self, *, CollectionName: str, GeofenceIds: Sequence[str]
    ) -> BatchDeleteGeofenceResponseTypeDef:
        """
        Deletes a batch of geofences from a geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_delete_geofence)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#batch_delete_geofence)
        """

    def batch_evaluate_geofences(
        self, *, CollectionName: str, DevicePositionUpdates: Sequence[DevicePositionUpdateTypeDef]
    ) -> BatchEvaluateGeofencesResponseTypeDef:
        """
        Evaluates device positions against the geofence geometries from a given geofence
        collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_evaluate_geofences)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#batch_evaluate_geofences)
        """

    def batch_get_device_position(
        self, *, DeviceIds: Sequence[str], TrackerName: str
    ) -> BatchGetDevicePositionResponseTypeDef:
        """
        Lists the latest device positions for requested devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_get_device_position)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#batch_get_device_position)
        """

    def batch_put_geofence(
        self, *, CollectionName: str, Entries: Sequence[BatchPutGeofenceRequestEntryTypeDef]
    ) -> BatchPutGeofenceResponseTypeDef:
        """
        A batch request for storing geofence geometries into a given geofence
        collection, or updates the geometry of an existing geofence if a geofence ID is
        included in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_put_geofence)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#batch_put_geofence)
        """

    def batch_update_device_position(
        self, *, TrackerName: str, Updates: Sequence[DevicePositionUpdateTypeDef]
    ) -> BatchUpdateDevicePositionResponseTypeDef:
        """
        Uploads position update data for one or more devices to a tracker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_update_device_position)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#batch_update_device_position)
        """

    def calculate_route(
        self,
        *,
        CalculatorName: str,
        DeparturePosition: Sequence[float],
        DestinationPosition: Sequence[float],
        CarModeOptions: CalculateRouteCarModeOptionsTypeDef = ...,
        DepartNow: bool = ...,
        DepartureTime: Union[datetime, str] = ...,
        DistanceUnit: DistanceUnitType = ...,
        IncludeLegGeometry: bool = ...,
        TravelMode: TravelModeType = ...,
        TruckModeOptions: CalculateRouteTruckModeOptionsTypeDef = ...,
        WaypointPositions: Sequence[Sequence[float]] = ...
    ) -> CalculateRouteResponseTypeDef:
        """
        [Calculates a
        route](https://docs.aws.amazon.com/location/latest/developerguide/calculate-
        route.html)_ given the following required parameters: `DeparturePosition` and
        `DestinationPosition`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.calculate_route)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#calculate_route)
        """

    def calculate_route_matrix(
        self,
        *,
        CalculatorName: str,
        DeparturePositions: Sequence[Sequence[float]],
        DestinationPositions: Sequence[Sequence[float]],
        CarModeOptions: CalculateRouteCarModeOptionsTypeDef = ...,
        DepartNow: bool = ...,
        DepartureTime: Union[datetime, str] = ...,
        DistanceUnit: DistanceUnitType = ...,
        TravelMode: TravelModeType = ...,
        TruckModeOptions: CalculateRouteTruckModeOptionsTypeDef = ...
    ) -> CalculateRouteMatrixResponseTypeDef:
        """
        [Calculates a route
        matrix](https://docs.aws.amazon.com/location/latest/developerguide/calculate-
        route-matrix.html)_ given the following required parameters:
        `DeparturePositions` and `DestinationPositions`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.calculate_route_matrix)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#calculate_route_matrix)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#can_paginate)
        """

    def create_geofence_collection(
        self,
        *,
        CollectionName: str,
        Description: str = ...,
        KmsKeyId: str = ...,
        PricingPlan: PricingPlanType = ...,
        PricingPlanDataSource: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateGeofenceCollectionResponseTypeDef:
        """
        Creates a geofence collection, which manages and stores geofences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_geofence_collection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#create_geofence_collection)
        """

    def create_map(
        self,
        *,
        Configuration: MapConfigurationTypeDef,
        MapName: str,
        Description: str = ...,
        PricingPlan: PricingPlanType = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateMapResponseTypeDef:
        """
        Creates a map resource in your AWS account, which provides map tiles of
        different styles sourced from global location data providers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_map)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#create_map)
        """

    def create_place_index(
        self,
        *,
        DataSource: str,
        IndexName: str,
        DataSourceConfiguration: DataSourceConfigurationTypeDef = ...,
        Description: str = ...,
        PricingPlan: PricingPlanType = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreatePlaceIndexResponseTypeDef:
        """
        Creates a place index resource in your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_place_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#create_place_index)
        """

    def create_route_calculator(
        self,
        *,
        CalculatorName: str,
        DataSource: str,
        Description: str = ...,
        PricingPlan: PricingPlanType = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateRouteCalculatorResponseTypeDef:
        """
        Creates a route calculator resource in your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_route_calculator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#create_route_calculator)
        """

    def create_tracker(
        self,
        *,
        TrackerName: str,
        Description: str = ...,
        KmsKeyId: str = ...,
        PositionFiltering: PositionFilteringType = ...,
        PricingPlan: PricingPlanType = ...,
        PricingPlanDataSource: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateTrackerResponseTypeDef:
        """
        Creates a tracker resource in your AWS account, which lets you retrieve current
        and historical location of devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_tracker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#create_tracker)
        """

    def delete_geofence_collection(self, *, CollectionName: str) -> Dict[str, Any]:
        """
        Deletes a geofence collection from your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_geofence_collection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#delete_geofence_collection)
        """

    def delete_map(self, *, MapName: str) -> Dict[str, Any]:
        """
        Deletes a map resource from your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_map)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#delete_map)
        """

    def delete_place_index(self, *, IndexName: str) -> Dict[str, Any]:
        """
        Deletes a place index resource from your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_place_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#delete_place_index)
        """

    def delete_route_calculator(self, *, CalculatorName: str) -> Dict[str, Any]:
        """
        Deletes a route calculator resource from your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_route_calculator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#delete_route_calculator)
        """

    def delete_tracker(self, *, TrackerName: str) -> Dict[str, Any]:
        """
        Deletes a tracker resource from your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_tracker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#delete_tracker)
        """

    def describe_geofence_collection(
        self, *, CollectionName: str
    ) -> DescribeGeofenceCollectionResponseTypeDef:
        """
        Retrieves the geofence collection details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_geofence_collection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#describe_geofence_collection)
        """

    def describe_map(self, *, MapName: str) -> DescribeMapResponseTypeDef:
        """
        Retrieves the map resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_map)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#describe_map)
        """

    def describe_place_index(self, *, IndexName: str) -> DescribePlaceIndexResponseTypeDef:
        """
        Retrieves the place index resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_place_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#describe_place_index)
        """

    def describe_route_calculator(
        self, *, CalculatorName: str
    ) -> DescribeRouteCalculatorResponseTypeDef:
        """
        Retrieves the route calculator resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_route_calculator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#describe_route_calculator)
        """

    def describe_tracker(self, *, TrackerName: str) -> DescribeTrackerResponseTypeDef:
        """
        Retrieves the tracker resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_tracker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#describe_tracker)
        """

    def disassociate_tracker_consumer(
        self, *, ConsumerArn: str, TrackerName: str
    ) -> Dict[str, Any]:
        """
        Removes the association between a tracker resource and a geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.disassociate_tracker_consumer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#disassociate_tracker_consumer)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#generate_presigned_url)
        """

    def get_device_position(
        self, *, DeviceId: str, TrackerName: str
    ) -> GetDevicePositionResponseTypeDef:
        """
        Retrieves a device's most recent position according to its sample time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_device_position)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_device_position)
        """

    def get_device_position_history(
        self,
        *,
        DeviceId: str,
        TrackerName: str,
        EndTimeExclusive: Union[datetime, str] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        StartTimeInclusive: Union[datetime, str] = ...
    ) -> GetDevicePositionHistoryResponseTypeDef:
        """
        Retrieves the device position history from a tracker resource within a specified
        range of time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_device_position_history)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_device_position_history)
        """

    def get_geofence(self, *, CollectionName: str, GeofenceId: str) -> GetGeofenceResponseTypeDef:
        """
        Retrieves the geofence details from a geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_geofence)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_geofence)
        """

    def get_map_glyphs(
        self, *, FontStack: str, FontUnicodeRange: str, MapName: str
    ) -> GetMapGlyphsResponseTypeDef:
        """
        Retrieves glyphs used to display labels on a map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_map_glyphs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_map_glyphs)
        """

    def get_map_sprites(self, *, FileName: str, MapName: str) -> GetMapSpritesResponseTypeDef:
        """
        Retrieves the sprite sheet corresponding to a map resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_map_sprites)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_map_sprites)
        """

    def get_map_style_descriptor(self, *, MapName: str) -> GetMapStyleDescriptorResponseTypeDef:
        """
        Retrieves the map style descriptor from a map resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_map_style_descriptor)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_map_style_descriptor)
        """

    def get_map_tile(self, *, MapName: str, X: str, Y: str, Z: str) -> GetMapTileResponseTypeDef:
        """
        Retrieves a vector data tile from the map resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_map_tile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_map_tile)
        """

    def list_device_positions(
        self, *, TrackerName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListDevicePositionsResponseTypeDef:
        """
        A batch request to retrieve all device positions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_device_positions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#list_device_positions)
        """

    def list_geofence_collections(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListGeofenceCollectionsResponseTypeDef:
        """
        Lists geofence collections in your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_geofence_collections)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#list_geofence_collections)
        """

    def list_geofences(
        self, *, CollectionName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListGeofencesResponseTypeDef:
        """
        Lists geofences stored in a given geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_geofences)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#list_geofences)
        """

    def list_maps(self, *, MaxResults: int = ..., NextToken: str = ...) -> ListMapsResponseTypeDef:
        """
        Lists map resources in your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_maps)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#list_maps)
        """

    def list_place_indexes(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListPlaceIndexesResponseTypeDef:
        """
        Lists place index resources in your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_place_indexes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#list_place_indexes)
        """

    def list_route_calculators(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListRouteCalculatorsResponseTypeDef:
        """
        Lists route calculator resources in your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_route_calculators)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#list_route_calculators)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags that are applied to the specified Amazon Location
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#list_tags_for_resource)
        """

    def list_tracker_consumers(
        self, *, TrackerName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListTrackerConsumersResponseTypeDef:
        """
        Lists geofence collections currently associated to the given tracker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_tracker_consumers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#list_tracker_consumers)
        """

    def list_trackers(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListTrackersResponseTypeDef:
        """
        Lists tracker resources in your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_trackers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#list_trackers)
        """

    def put_geofence(
        self, *, CollectionName: str, GeofenceId: str, Geometry: GeofenceGeometryTypeDef
    ) -> PutGeofenceResponseTypeDef:
        """
        Stores a geofence geometry in a given geofence collection, or updates the
        geometry of an existing geofence if a geofence ID is included in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.put_geofence)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#put_geofence)
        """

    def search_place_index_for_position(
        self,
        *,
        IndexName: str,
        Position: Sequence[float],
        Language: str = ...,
        MaxResults: int = ...
    ) -> SearchPlaceIndexForPositionResponseTypeDef:
        """
        Reverse geocodes a given coordinate and returns a legible address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.search_place_index_for_position)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#search_place_index_for_position)
        """

    def search_place_index_for_suggestions(
        self,
        *,
        IndexName: str,
        Text: str,
        BiasPosition: Sequence[float] = ...,
        FilterBBox: Sequence[float] = ...,
        FilterCountries: Sequence[str] = ...,
        Language: str = ...,
        MaxResults: int = ...
    ) -> SearchPlaceIndexForSuggestionsResponseTypeDef:
        """
        Generates suggestions for addresses and points of interest based on partial or
        misspelled free-form text.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.search_place_index_for_suggestions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#search_place_index_for_suggestions)
        """

    def search_place_index_for_text(
        self,
        *,
        IndexName: str,
        Text: str,
        BiasPosition: Sequence[float] = ...,
        FilterBBox: Sequence[float] = ...,
        FilterCountries: Sequence[str] = ...,
        Language: str = ...,
        MaxResults: int = ...
    ) -> SearchPlaceIndexForTextResponseTypeDef:
        """
        Geocodes free-form text, such as an address, name, city, or region to allow you
        to search for Places or points of interest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.search_place_index_for_text)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#search_place_index_for_text)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified Amazon Location
        Service resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified Amazon Location resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#untag_resource)
        """

    def update_geofence_collection(
        self,
        *,
        CollectionName: str,
        Description: str = ...,
        PricingPlan: PricingPlanType = ...,
        PricingPlanDataSource: str = ...
    ) -> UpdateGeofenceCollectionResponseTypeDef:
        """
        Updates the specified properties of a given geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_geofence_collection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#update_geofence_collection)
        """

    def update_map(
        self, *, MapName: str, Description: str = ..., PricingPlan: PricingPlanType = ...
    ) -> UpdateMapResponseTypeDef:
        """
        Updates the specified properties of a given map resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_map)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#update_map)
        """

    def update_place_index(
        self,
        *,
        IndexName: str,
        DataSourceConfiguration: DataSourceConfigurationTypeDef = ...,
        Description: str = ...,
        PricingPlan: PricingPlanType = ...
    ) -> UpdatePlaceIndexResponseTypeDef:
        """
        Updates the specified properties of a given place index resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_place_index)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#update_place_index)
        """

    def update_route_calculator(
        self, *, CalculatorName: str, Description: str = ..., PricingPlan: PricingPlanType = ...
    ) -> UpdateRouteCalculatorResponseTypeDef:
        """
        Updates the specified properties for a given route calculator resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_route_calculator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#update_route_calculator)
        """

    def update_tracker(
        self,
        *,
        TrackerName: str,
        Description: str = ...,
        PositionFiltering: PositionFilteringType = ...,
        PricingPlan: PricingPlanType = ...,
        PricingPlanDataSource: str = ...
    ) -> UpdateTrackerResponseTypeDef:
        """
        Updates the specified properties of a given tracker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_tracker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#update_tracker)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_device_position_history"]
    ) -> GetDevicePositionHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_positions"]
    ) -> ListDevicePositionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_geofence_collections"]
    ) -> ListGeofenceCollectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_geofences"]) -> ListGeofencesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_maps"]) -> ListMapsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_place_indexes"]
    ) -> ListPlaceIndexesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_route_calculators"]
    ) -> ListRouteCalculatorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tracker_consumers"]
    ) -> ListTrackerConsumersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_trackers"]) -> ListTrackersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/client/#get_paginator)
        """
