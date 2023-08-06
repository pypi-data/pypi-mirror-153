"""
Type annotations for location service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/type_defs/)

Usage::

    ```python
    from mypy_boto3_location.type_defs import AssociateTrackerConsumerRequestRequestTypeDef

    data: AssociateTrackerConsumerRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    BatchItemErrorCodeType,
    DimensionUnitType,
    DistanceUnitType,
    IntendedUseType,
    PositionFilteringType,
    PricingPlanType,
    RouteMatrixErrorCodeType,
    TravelModeType,
    VehicleWeightUnitType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AssociateTrackerConsumerRequestRequestTypeDef",
    "BatchItemErrorTypeDef",
    "BatchDeleteDevicePositionHistoryRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "BatchDeleteGeofenceRequestRequestTypeDef",
    "BatchGetDevicePositionRequestRequestTypeDef",
    "GeofenceGeometryTypeDef",
    "BatchPutGeofenceSuccessTypeDef",
    "CalculateRouteCarModeOptionsTypeDef",
    "CalculateRouteMatrixSummaryTypeDef",
    "CalculateRouteSummaryTypeDef",
    "TruckDimensionsTypeDef",
    "TruckWeightTypeDef",
    "CreateGeofenceCollectionRequestRequestTypeDef",
    "MapConfigurationTypeDef",
    "DataSourceConfigurationTypeDef",
    "CreateRouteCalculatorRequestRequestTypeDef",
    "CreateTrackerRequestRequestTypeDef",
    "DeleteGeofenceCollectionRequestRequestTypeDef",
    "DeleteMapRequestRequestTypeDef",
    "DeletePlaceIndexRequestRequestTypeDef",
    "DeleteRouteCalculatorRequestRequestTypeDef",
    "DeleteTrackerRequestRequestTypeDef",
    "DescribeGeofenceCollectionRequestRequestTypeDef",
    "DescribeMapRequestRequestTypeDef",
    "DescribePlaceIndexRequestRequestTypeDef",
    "DescribeRouteCalculatorRequestRequestTypeDef",
    "DescribeTrackerRequestRequestTypeDef",
    "PositionalAccuracyTypeDef",
    "DisassociateTrackerConsumerRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "GetDevicePositionHistoryRequestRequestTypeDef",
    "GetDevicePositionRequestRequestTypeDef",
    "GetGeofenceRequestRequestTypeDef",
    "GetMapGlyphsRequestRequestTypeDef",
    "GetMapSpritesRequestRequestTypeDef",
    "GetMapStyleDescriptorRequestRequestTypeDef",
    "GetMapTileRequestRequestTypeDef",
    "LegGeometryTypeDef",
    "StepTypeDef",
    "ListDevicePositionsRequestRequestTypeDef",
    "ListGeofenceCollectionsRequestRequestTypeDef",
    "ListGeofenceCollectionsResponseEntryTypeDef",
    "ListGeofencesRequestRequestTypeDef",
    "ListMapsRequestRequestTypeDef",
    "ListMapsResponseEntryTypeDef",
    "ListPlaceIndexesRequestRequestTypeDef",
    "ListPlaceIndexesResponseEntryTypeDef",
    "ListRouteCalculatorsRequestRequestTypeDef",
    "ListRouteCalculatorsResponseEntryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTrackerConsumersRequestRequestTypeDef",
    "ListTrackersRequestRequestTypeDef",
    "ListTrackersResponseEntryTypeDef",
    "PlaceGeometryTypeDef",
    "TimeZoneTypeDef",
    "RouteMatrixEntryErrorTypeDef",
    "SearchForSuggestionsResultTypeDef",
    "SearchPlaceIndexForPositionRequestRequestTypeDef",
    "SearchPlaceIndexForPositionSummaryTypeDef",
    "SearchPlaceIndexForSuggestionsRequestRequestTypeDef",
    "SearchPlaceIndexForSuggestionsSummaryTypeDef",
    "SearchPlaceIndexForTextRequestRequestTypeDef",
    "SearchPlaceIndexForTextSummaryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateGeofenceCollectionRequestRequestTypeDef",
    "UpdateMapRequestRequestTypeDef",
    "UpdateRouteCalculatorRequestRequestTypeDef",
    "UpdateTrackerRequestRequestTypeDef",
    "BatchDeleteDevicePositionHistoryErrorTypeDef",
    "BatchDeleteGeofenceErrorTypeDef",
    "BatchEvaluateGeofencesErrorTypeDef",
    "BatchGetDevicePositionErrorTypeDef",
    "BatchPutGeofenceErrorTypeDef",
    "BatchUpdateDevicePositionErrorTypeDef",
    "CreateGeofenceCollectionResponseTypeDef",
    "CreateMapResponseTypeDef",
    "CreatePlaceIndexResponseTypeDef",
    "CreateRouteCalculatorResponseTypeDef",
    "CreateTrackerResponseTypeDef",
    "DescribeGeofenceCollectionResponseTypeDef",
    "DescribeRouteCalculatorResponseTypeDef",
    "DescribeTrackerResponseTypeDef",
    "GetMapGlyphsResponseTypeDef",
    "GetMapSpritesResponseTypeDef",
    "GetMapStyleDescriptorResponseTypeDef",
    "GetMapTileResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTrackerConsumersResponseTypeDef",
    "PutGeofenceResponseTypeDef",
    "UpdateGeofenceCollectionResponseTypeDef",
    "UpdateMapResponseTypeDef",
    "UpdatePlaceIndexResponseTypeDef",
    "UpdateRouteCalculatorResponseTypeDef",
    "UpdateTrackerResponseTypeDef",
    "BatchPutGeofenceRequestEntryTypeDef",
    "GetGeofenceResponseTypeDef",
    "ListGeofenceResponseEntryTypeDef",
    "PutGeofenceRequestRequestTypeDef",
    "CalculateRouteTruckModeOptionsTypeDef",
    "CreateMapRequestRequestTypeDef",
    "DescribeMapResponseTypeDef",
    "CreatePlaceIndexRequestRequestTypeDef",
    "DescribePlaceIndexResponseTypeDef",
    "UpdatePlaceIndexRequestRequestTypeDef",
    "DevicePositionTypeDef",
    "DevicePositionUpdateTypeDef",
    "GetDevicePositionResponseTypeDef",
    "ListDevicePositionsResponseEntryTypeDef",
    "GetDevicePositionHistoryRequestGetDevicePositionHistoryPaginateTypeDef",
    "ListDevicePositionsRequestListDevicePositionsPaginateTypeDef",
    "ListGeofenceCollectionsRequestListGeofenceCollectionsPaginateTypeDef",
    "ListGeofencesRequestListGeofencesPaginateTypeDef",
    "ListMapsRequestListMapsPaginateTypeDef",
    "ListPlaceIndexesRequestListPlaceIndexesPaginateTypeDef",
    "ListRouteCalculatorsRequestListRouteCalculatorsPaginateTypeDef",
    "ListTrackerConsumersRequestListTrackerConsumersPaginateTypeDef",
    "ListTrackersRequestListTrackersPaginateTypeDef",
    "LegTypeDef",
    "ListGeofenceCollectionsResponseTypeDef",
    "ListMapsResponseTypeDef",
    "ListPlaceIndexesResponseTypeDef",
    "ListRouteCalculatorsResponseTypeDef",
    "ListTrackersResponseTypeDef",
    "PlaceTypeDef",
    "RouteMatrixEntryTypeDef",
    "SearchPlaceIndexForSuggestionsResponseTypeDef",
    "BatchDeleteDevicePositionHistoryResponseTypeDef",
    "BatchDeleteGeofenceResponseTypeDef",
    "BatchEvaluateGeofencesResponseTypeDef",
    "BatchPutGeofenceResponseTypeDef",
    "BatchUpdateDevicePositionResponseTypeDef",
    "BatchPutGeofenceRequestRequestTypeDef",
    "ListGeofencesResponseTypeDef",
    "CalculateRouteMatrixRequestRequestTypeDef",
    "CalculateRouteRequestRequestTypeDef",
    "BatchGetDevicePositionResponseTypeDef",
    "GetDevicePositionHistoryResponseTypeDef",
    "BatchEvaluateGeofencesRequestRequestTypeDef",
    "BatchUpdateDevicePositionRequestRequestTypeDef",
    "ListDevicePositionsResponseTypeDef",
    "CalculateRouteResponseTypeDef",
    "SearchForPositionResultTypeDef",
    "SearchForTextResultTypeDef",
    "CalculateRouteMatrixResponseTypeDef",
    "SearchPlaceIndexForPositionResponseTypeDef",
    "SearchPlaceIndexForTextResponseTypeDef",
)

AssociateTrackerConsumerRequestRequestTypeDef = TypedDict(
    "AssociateTrackerConsumerRequestRequestTypeDef",
    {
        "ConsumerArn": str,
        "TrackerName": str,
    },
)

BatchItemErrorTypeDef = TypedDict(
    "BatchItemErrorTypeDef",
    {
        "Code": BatchItemErrorCodeType,
        "Message": str,
    },
    total=False,
)

BatchDeleteDevicePositionHistoryRequestRequestTypeDef = TypedDict(
    "BatchDeleteDevicePositionHistoryRequestRequestTypeDef",
    {
        "DeviceIds": Sequence[str],
        "TrackerName": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

BatchDeleteGeofenceRequestRequestTypeDef = TypedDict(
    "BatchDeleteGeofenceRequestRequestTypeDef",
    {
        "CollectionName": str,
        "GeofenceIds": Sequence[str],
    },
)

BatchGetDevicePositionRequestRequestTypeDef = TypedDict(
    "BatchGetDevicePositionRequestRequestTypeDef",
    {
        "DeviceIds": Sequence[str],
        "TrackerName": str,
    },
)

GeofenceGeometryTypeDef = TypedDict(
    "GeofenceGeometryTypeDef",
    {
        "Polygon": Sequence[Sequence[Sequence[float]]],
    },
    total=False,
)

BatchPutGeofenceSuccessTypeDef = TypedDict(
    "BatchPutGeofenceSuccessTypeDef",
    {
        "CreateTime": datetime,
        "GeofenceId": str,
        "UpdateTime": datetime,
    },
)

CalculateRouteCarModeOptionsTypeDef = TypedDict(
    "CalculateRouteCarModeOptionsTypeDef",
    {
        "AvoidFerries": bool,
        "AvoidTolls": bool,
    },
    total=False,
)

CalculateRouteMatrixSummaryTypeDef = TypedDict(
    "CalculateRouteMatrixSummaryTypeDef",
    {
        "DataSource": str,
        "DistanceUnit": DistanceUnitType,
        "ErrorCount": int,
        "RouteCount": int,
    },
)

CalculateRouteSummaryTypeDef = TypedDict(
    "CalculateRouteSummaryTypeDef",
    {
        "DataSource": str,
        "Distance": float,
        "DistanceUnit": DistanceUnitType,
        "DurationSeconds": float,
        "RouteBBox": List[float],
    },
)

TruckDimensionsTypeDef = TypedDict(
    "TruckDimensionsTypeDef",
    {
        "Height": float,
        "Length": float,
        "Unit": DimensionUnitType,
        "Width": float,
    },
    total=False,
)

TruckWeightTypeDef = TypedDict(
    "TruckWeightTypeDef",
    {
        "Total": float,
        "Unit": VehicleWeightUnitType,
    },
    total=False,
)

_RequiredCreateGeofenceCollectionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGeofenceCollectionRequestRequestTypeDef",
    {
        "CollectionName": str,
    },
)
_OptionalCreateGeofenceCollectionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGeofenceCollectionRequestRequestTypeDef",
    {
        "Description": str,
        "KmsKeyId": str,
        "PricingPlan": PricingPlanType,
        "PricingPlanDataSource": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateGeofenceCollectionRequestRequestTypeDef(
    _RequiredCreateGeofenceCollectionRequestRequestTypeDef,
    _OptionalCreateGeofenceCollectionRequestRequestTypeDef,
):
    pass


MapConfigurationTypeDef = TypedDict(
    "MapConfigurationTypeDef",
    {
        "Style": str,
    },
)

DataSourceConfigurationTypeDef = TypedDict(
    "DataSourceConfigurationTypeDef",
    {
        "IntendedUse": IntendedUseType,
    },
    total=False,
)

_RequiredCreateRouteCalculatorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRouteCalculatorRequestRequestTypeDef",
    {
        "CalculatorName": str,
        "DataSource": str,
    },
)
_OptionalCreateRouteCalculatorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRouteCalculatorRequestRequestTypeDef",
    {
        "Description": str,
        "PricingPlan": PricingPlanType,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateRouteCalculatorRequestRequestTypeDef(
    _RequiredCreateRouteCalculatorRequestRequestTypeDef,
    _OptionalCreateRouteCalculatorRequestRequestTypeDef,
):
    pass


_RequiredCreateTrackerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTrackerRequestRequestTypeDef",
    {
        "TrackerName": str,
    },
)
_OptionalCreateTrackerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTrackerRequestRequestTypeDef",
    {
        "Description": str,
        "KmsKeyId": str,
        "PositionFiltering": PositionFilteringType,
        "PricingPlan": PricingPlanType,
        "PricingPlanDataSource": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateTrackerRequestRequestTypeDef(
    _RequiredCreateTrackerRequestRequestTypeDef, _OptionalCreateTrackerRequestRequestTypeDef
):
    pass


DeleteGeofenceCollectionRequestRequestTypeDef = TypedDict(
    "DeleteGeofenceCollectionRequestRequestTypeDef",
    {
        "CollectionName": str,
    },
)

DeleteMapRequestRequestTypeDef = TypedDict(
    "DeleteMapRequestRequestTypeDef",
    {
        "MapName": str,
    },
)

DeletePlaceIndexRequestRequestTypeDef = TypedDict(
    "DeletePlaceIndexRequestRequestTypeDef",
    {
        "IndexName": str,
    },
)

DeleteRouteCalculatorRequestRequestTypeDef = TypedDict(
    "DeleteRouteCalculatorRequestRequestTypeDef",
    {
        "CalculatorName": str,
    },
)

DeleteTrackerRequestRequestTypeDef = TypedDict(
    "DeleteTrackerRequestRequestTypeDef",
    {
        "TrackerName": str,
    },
)

DescribeGeofenceCollectionRequestRequestTypeDef = TypedDict(
    "DescribeGeofenceCollectionRequestRequestTypeDef",
    {
        "CollectionName": str,
    },
)

DescribeMapRequestRequestTypeDef = TypedDict(
    "DescribeMapRequestRequestTypeDef",
    {
        "MapName": str,
    },
)

DescribePlaceIndexRequestRequestTypeDef = TypedDict(
    "DescribePlaceIndexRequestRequestTypeDef",
    {
        "IndexName": str,
    },
)

DescribeRouteCalculatorRequestRequestTypeDef = TypedDict(
    "DescribeRouteCalculatorRequestRequestTypeDef",
    {
        "CalculatorName": str,
    },
)

DescribeTrackerRequestRequestTypeDef = TypedDict(
    "DescribeTrackerRequestRequestTypeDef",
    {
        "TrackerName": str,
    },
)

PositionalAccuracyTypeDef = TypedDict(
    "PositionalAccuracyTypeDef",
    {
        "Horizontal": float,
    },
)

DisassociateTrackerConsumerRequestRequestTypeDef = TypedDict(
    "DisassociateTrackerConsumerRequestRequestTypeDef",
    {
        "ConsumerArn": str,
        "TrackerName": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredGetDevicePositionHistoryRequestRequestTypeDef = TypedDict(
    "_RequiredGetDevicePositionHistoryRequestRequestTypeDef",
    {
        "DeviceId": str,
        "TrackerName": str,
    },
)
_OptionalGetDevicePositionHistoryRequestRequestTypeDef = TypedDict(
    "_OptionalGetDevicePositionHistoryRequestRequestTypeDef",
    {
        "EndTimeExclusive": Union[datetime, str],
        "MaxResults": int,
        "NextToken": str,
        "StartTimeInclusive": Union[datetime, str],
    },
    total=False,
)


class GetDevicePositionHistoryRequestRequestTypeDef(
    _RequiredGetDevicePositionHistoryRequestRequestTypeDef,
    _OptionalGetDevicePositionHistoryRequestRequestTypeDef,
):
    pass


GetDevicePositionRequestRequestTypeDef = TypedDict(
    "GetDevicePositionRequestRequestTypeDef",
    {
        "DeviceId": str,
        "TrackerName": str,
    },
)

GetGeofenceRequestRequestTypeDef = TypedDict(
    "GetGeofenceRequestRequestTypeDef",
    {
        "CollectionName": str,
        "GeofenceId": str,
    },
)

GetMapGlyphsRequestRequestTypeDef = TypedDict(
    "GetMapGlyphsRequestRequestTypeDef",
    {
        "FontStack": str,
        "FontUnicodeRange": str,
        "MapName": str,
    },
)

GetMapSpritesRequestRequestTypeDef = TypedDict(
    "GetMapSpritesRequestRequestTypeDef",
    {
        "FileName": str,
        "MapName": str,
    },
)

GetMapStyleDescriptorRequestRequestTypeDef = TypedDict(
    "GetMapStyleDescriptorRequestRequestTypeDef",
    {
        "MapName": str,
    },
)

GetMapTileRequestRequestTypeDef = TypedDict(
    "GetMapTileRequestRequestTypeDef",
    {
        "MapName": str,
        "X": str,
        "Y": str,
        "Z": str,
    },
)

LegGeometryTypeDef = TypedDict(
    "LegGeometryTypeDef",
    {
        "LineString": List[List[float]],
    },
    total=False,
)

_RequiredStepTypeDef = TypedDict(
    "_RequiredStepTypeDef",
    {
        "Distance": float,
        "DurationSeconds": float,
        "EndPosition": List[float],
        "StartPosition": List[float],
    },
)
_OptionalStepTypeDef = TypedDict(
    "_OptionalStepTypeDef",
    {
        "GeometryOffset": int,
    },
    total=False,
)


class StepTypeDef(_RequiredStepTypeDef, _OptionalStepTypeDef):
    pass


_RequiredListDevicePositionsRequestRequestTypeDef = TypedDict(
    "_RequiredListDevicePositionsRequestRequestTypeDef",
    {
        "TrackerName": str,
    },
)
_OptionalListDevicePositionsRequestRequestTypeDef = TypedDict(
    "_OptionalListDevicePositionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListDevicePositionsRequestRequestTypeDef(
    _RequiredListDevicePositionsRequestRequestTypeDef,
    _OptionalListDevicePositionsRequestRequestTypeDef,
):
    pass


ListGeofenceCollectionsRequestRequestTypeDef = TypedDict(
    "ListGeofenceCollectionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListGeofenceCollectionsResponseEntryTypeDef = TypedDict(
    "_RequiredListGeofenceCollectionsResponseEntryTypeDef",
    {
        "CollectionName": str,
        "CreateTime": datetime,
        "Description": str,
        "UpdateTime": datetime,
    },
)
_OptionalListGeofenceCollectionsResponseEntryTypeDef = TypedDict(
    "_OptionalListGeofenceCollectionsResponseEntryTypeDef",
    {
        "PricingPlan": PricingPlanType,
        "PricingPlanDataSource": str,
    },
    total=False,
)


class ListGeofenceCollectionsResponseEntryTypeDef(
    _RequiredListGeofenceCollectionsResponseEntryTypeDef,
    _OptionalListGeofenceCollectionsResponseEntryTypeDef,
):
    pass


_RequiredListGeofencesRequestRequestTypeDef = TypedDict(
    "_RequiredListGeofencesRequestRequestTypeDef",
    {
        "CollectionName": str,
    },
)
_OptionalListGeofencesRequestRequestTypeDef = TypedDict(
    "_OptionalListGeofencesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListGeofencesRequestRequestTypeDef(
    _RequiredListGeofencesRequestRequestTypeDef, _OptionalListGeofencesRequestRequestTypeDef
):
    pass


ListMapsRequestRequestTypeDef = TypedDict(
    "ListMapsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListMapsResponseEntryTypeDef = TypedDict(
    "_RequiredListMapsResponseEntryTypeDef",
    {
        "CreateTime": datetime,
        "DataSource": str,
        "Description": str,
        "MapName": str,
        "UpdateTime": datetime,
    },
)
_OptionalListMapsResponseEntryTypeDef = TypedDict(
    "_OptionalListMapsResponseEntryTypeDef",
    {
        "PricingPlan": PricingPlanType,
    },
    total=False,
)


class ListMapsResponseEntryTypeDef(
    _RequiredListMapsResponseEntryTypeDef, _OptionalListMapsResponseEntryTypeDef
):
    pass


ListPlaceIndexesRequestRequestTypeDef = TypedDict(
    "ListPlaceIndexesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListPlaceIndexesResponseEntryTypeDef = TypedDict(
    "_RequiredListPlaceIndexesResponseEntryTypeDef",
    {
        "CreateTime": datetime,
        "DataSource": str,
        "Description": str,
        "IndexName": str,
        "UpdateTime": datetime,
    },
)
_OptionalListPlaceIndexesResponseEntryTypeDef = TypedDict(
    "_OptionalListPlaceIndexesResponseEntryTypeDef",
    {
        "PricingPlan": PricingPlanType,
    },
    total=False,
)


class ListPlaceIndexesResponseEntryTypeDef(
    _RequiredListPlaceIndexesResponseEntryTypeDef, _OptionalListPlaceIndexesResponseEntryTypeDef
):
    pass


ListRouteCalculatorsRequestRequestTypeDef = TypedDict(
    "ListRouteCalculatorsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListRouteCalculatorsResponseEntryTypeDef = TypedDict(
    "_RequiredListRouteCalculatorsResponseEntryTypeDef",
    {
        "CalculatorName": str,
        "CreateTime": datetime,
        "DataSource": str,
        "Description": str,
        "UpdateTime": datetime,
    },
)
_OptionalListRouteCalculatorsResponseEntryTypeDef = TypedDict(
    "_OptionalListRouteCalculatorsResponseEntryTypeDef",
    {
        "PricingPlan": PricingPlanType,
    },
    total=False,
)


class ListRouteCalculatorsResponseEntryTypeDef(
    _RequiredListRouteCalculatorsResponseEntryTypeDef,
    _OptionalListRouteCalculatorsResponseEntryTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredListTrackerConsumersRequestRequestTypeDef = TypedDict(
    "_RequiredListTrackerConsumersRequestRequestTypeDef",
    {
        "TrackerName": str,
    },
)
_OptionalListTrackerConsumersRequestRequestTypeDef = TypedDict(
    "_OptionalListTrackerConsumersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListTrackerConsumersRequestRequestTypeDef(
    _RequiredListTrackerConsumersRequestRequestTypeDef,
    _OptionalListTrackerConsumersRequestRequestTypeDef,
):
    pass


ListTrackersRequestRequestTypeDef = TypedDict(
    "ListTrackersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListTrackersResponseEntryTypeDef = TypedDict(
    "_RequiredListTrackersResponseEntryTypeDef",
    {
        "CreateTime": datetime,
        "Description": str,
        "TrackerName": str,
        "UpdateTime": datetime,
    },
)
_OptionalListTrackersResponseEntryTypeDef = TypedDict(
    "_OptionalListTrackersResponseEntryTypeDef",
    {
        "PricingPlan": PricingPlanType,
        "PricingPlanDataSource": str,
    },
    total=False,
)


class ListTrackersResponseEntryTypeDef(
    _RequiredListTrackersResponseEntryTypeDef, _OptionalListTrackersResponseEntryTypeDef
):
    pass


PlaceGeometryTypeDef = TypedDict(
    "PlaceGeometryTypeDef",
    {
        "Point": List[float],
    },
    total=False,
)

_RequiredTimeZoneTypeDef = TypedDict(
    "_RequiredTimeZoneTypeDef",
    {
        "Name": str,
    },
)
_OptionalTimeZoneTypeDef = TypedDict(
    "_OptionalTimeZoneTypeDef",
    {
        "Offset": int,
    },
    total=False,
)


class TimeZoneTypeDef(_RequiredTimeZoneTypeDef, _OptionalTimeZoneTypeDef):
    pass


_RequiredRouteMatrixEntryErrorTypeDef = TypedDict(
    "_RequiredRouteMatrixEntryErrorTypeDef",
    {
        "Code": RouteMatrixErrorCodeType,
    },
)
_OptionalRouteMatrixEntryErrorTypeDef = TypedDict(
    "_OptionalRouteMatrixEntryErrorTypeDef",
    {
        "Message": str,
    },
    total=False,
)


class RouteMatrixEntryErrorTypeDef(
    _RequiredRouteMatrixEntryErrorTypeDef, _OptionalRouteMatrixEntryErrorTypeDef
):
    pass


SearchForSuggestionsResultTypeDef = TypedDict(
    "SearchForSuggestionsResultTypeDef",
    {
        "Text": str,
    },
)

_RequiredSearchPlaceIndexForPositionRequestRequestTypeDef = TypedDict(
    "_RequiredSearchPlaceIndexForPositionRequestRequestTypeDef",
    {
        "IndexName": str,
        "Position": Sequence[float],
    },
)
_OptionalSearchPlaceIndexForPositionRequestRequestTypeDef = TypedDict(
    "_OptionalSearchPlaceIndexForPositionRequestRequestTypeDef",
    {
        "Language": str,
        "MaxResults": int,
    },
    total=False,
)


class SearchPlaceIndexForPositionRequestRequestTypeDef(
    _RequiredSearchPlaceIndexForPositionRequestRequestTypeDef,
    _OptionalSearchPlaceIndexForPositionRequestRequestTypeDef,
):
    pass


_RequiredSearchPlaceIndexForPositionSummaryTypeDef = TypedDict(
    "_RequiredSearchPlaceIndexForPositionSummaryTypeDef",
    {
        "DataSource": str,
        "Position": List[float],
    },
)
_OptionalSearchPlaceIndexForPositionSummaryTypeDef = TypedDict(
    "_OptionalSearchPlaceIndexForPositionSummaryTypeDef",
    {
        "Language": str,
        "MaxResults": int,
    },
    total=False,
)


class SearchPlaceIndexForPositionSummaryTypeDef(
    _RequiredSearchPlaceIndexForPositionSummaryTypeDef,
    _OptionalSearchPlaceIndexForPositionSummaryTypeDef,
):
    pass


_RequiredSearchPlaceIndexForSuggestionsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchPlaceIndexForSuggestionsRequestRequestTypeDef",
    {
        "IndexName": str,
        "Text": str,
    },
)
_OptionalSearchPlaceIndexForSuggestionsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchPlaceIndexForSuggestionsRequestRequestTypeDef",
    {
        "BiasPosition": Sequence[float],
        "FilterBBox": Sequence[float],
        "FilterCountries": Sequence[str],
        "Language": str,
        "MaxResults": int,
    },
    total=False,
)


class SearchPlaceIndexForSuggestionsRequestRequestTypeDef(
    _RequiredSearchPlaceIndexForSuggestionsRequestRequestTypeDef,
    _OptionalSearchPlaceIndexForSuggestionsRequestRequestTypeDef,
):
    pass


_RequiredSearchPlaceIndexForSuggestionsSummaryTypeDef = TypedDict(
    "_RequiredSearchPlaceIndexForSuggestionsSummaryTypeDef",
    {
        "DataSource": str,
        "Text": str,
    },
)
_OptionalSearchPlaceIndexForSuggestionsSummaryTypeDef = TypedDict(
    "_OptionalSearchPlaceIndexForSuggestionsSummaryTypeDef",
    {
        "BiasPosition": List[float],
        "FilterBBox": List[float],
        "FilterCountries": List[str],
        "Language": str,
        "MaxResults": int,
    },
    total=False,
)


class SearchPlaceIndexForSuggestionsSummaryTypeDef(
    _RequiredSearchPlaceIndexForSuggestionsSummaryTypeDef,
    _OptionalSearchPlaceIndexForSuggestionsSummaryTypeDef,
):
    pass


_RequiredSearchPlaceIndexForTextRequestRequestTypeDef = TypedDict(
    "_RequiredSearchPlaceIndexForTextRequestRequestTypeDef",
    {
        "IndexName": str,
        "Text": str,
    },
)
_OptionalSearchPlaceIndexForTextRequestRequestTypeDef = TypedDict(
    "_OptionalSearchPlaceIndexForTextRequestRequestTypeDef",
    {
        "BiasPosition": Sequence[float],
        "FilterBBox": Sequence[float],
        "FilterCountries": Sequence[str],
        "Language": str,
        "MaxResults": int,
    },
    total=False,
)


class SearchPlaceIndexForTextRequestRequestTypeDef(
    _RequiredSearchPlaceIndexForTextRequestRequestTypeDef,
    _OptionalSearchPlaceIndexForTextRequestRequestTypeDef,
):
    pass


_RequiredSearchPlaceIndexForTextSummaryTypeDef = TypedDict(
    "_RequiredSearchPlaceIndexForTextSummaryTypeDef",
    {
        "DataSource": str,
        "Text": str,
    },
)
_OptionalSearchPlaceIndexForTextSummaryTypeDef = TypedDict(
    "_OptionalSearchPlaceIndexForTextSummaryTypeDef",
    {
        "BiasPosition": List[float],
        "FilterBBox": List[float],
        "FilterCountries": List[str],
        "Language": str,
        "MaxResults": int,
        "ResultBBox": List[float],
    },
    total=False,
)


class SearchPlaceIndexForTextSummaryTypeDef(
    _RequiredSearchPlaceIndexForTextSummaryTypeDef, _OptionalSearchPlaceIndexForTextSummaryTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateGeofenceCollectionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateGeofenceCollectionRequestRequestTypeDef",
    {
        "CollectionName": str,
    },
)
_OptionalUpdateGeofenceCollectionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateGeofenceCollectionRequestRequestTypeDef",
    {
        "Description": str,
        "PricingPlan": PricingPlanType,
        "PricingPlanDataSource": str,
    },
    total=False,
)


class UpdateGeofenceCollectionRequestRequestTypeDef(
    _RequiredUpdateGeofenceCollectionRequestRequestTypeDef,
    _OptionalUpdateGeofenceCollectionRequestRequestTypeDef,
):
    pass


_RequiredUpdateMapRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateMapRequestRequestTypeDef",
    {
        "MapName": str,
    },
)
_OptionalUpdateMapRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateMapRequestRequestTypeDef",
    {
        "Description": str,
        "PricingPlan": PricingPlanType,
    },
    total=False,
)


class UpdateMapRequestRequestTypeDef(
    _RequiredUpdateMapRequestRequestTypeDef, _OptionalUpdateMapRequestRequestTypeDef
):
    pass


_RequiredUpdateRouteCalculatorRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRouteCalculatorRequestRequestTypeDef",
    {
        "CalculatorName": str,
    },
)
_OptionalUpdateRouteCalculatorRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRouteCalculatorRequestRequestTypeDef",
    {
        "Description": str,
        "PricingPlan": PricingPlanType,
    },
    total=False,
)


class UpdateRouteCalculatorRequestRequestTypeDef(
    _RequiredUpdateRouteCalculatorRequestRequestTypeDef,
    _OptionalUpdateRouteCalculatorRequestRequestTypeDef,
):
    pass


_RequiredUpdateTrackerRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTrackerRequestRequestTypeDef",
    {
        "TrackerName": str,
    },
)
_OptionalUpdateTrackerRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTrackerRequestRequestTypeDef",
    {
        "Description": str,
        "PositionFiltering": PositionFilteringType,
        "PricingPlan": PricingPlanType,
        "PricingPlanDataSource": str,
    },
    total=False,
)


class UpdateTrackerRequestRequestTypeDef(
    _RequiredUpdateTrackerRequestRequestTypeDef, _OptionalUpdateTrackerRequestRequestTypeDef
):
    pass


BatchDeleteDevicePositionHistoryErrorTypeDef = TypedDict(
    "BatchDeleteDevicePositionHistoryErrorTypeDef",
    {
        "DeviceId": str,
        "Error": BatchItemErrorTypeDef,
    },
)

BatchDeleteGeofenceErrorTypeDef = TypedDict(
    "BatchDeleteGeofenceErrorTypeDef",
    {
        "Error": BatchItemErrorTypeDef,
        "GeofenceId": str,
    },
)

BatchEvaluateGeofencesErrorTypeDef = TypedDict(
    "BatchEvaluateGeofencesErrorTypeDef",
    {
        "DeviceId": str,
        "Error": BatchItemErrorTypeDef,
        "SampleTime": datetime,
    },
)

BatchGetDevicePositionErrorTypeDef = TypedDict(
    "BatchGetDevicePositionErrorTypeDef",
    {
        "DeviceId": str,
        "Error": BatchItemErrorTypeDef,
    },
)

BatchPutGeofenceErrorTypeDef = TypedDict(
    "BatchPutGeofenceErrorTypeDef",
    {
        "Error": BatchItemErrorTypeDef,
        "GeofenceId": str,
    },
)

BatchUpdateDevicePositionErrorTypeDef = TypedDict(
    "BatchUpdateDevicePositionErrorTypeDef",
    {
        "DeviceId": str,
        "Error": BatchItemErrorTypeDef,
        "SampleTime": datetime,
    },
)

CreateGeofenceCollectionResponseTypeDef = TypedDict(
    "CreateGeofenceCollectionResponseTypeDef",
    {
        "CollectionArn": str,
        "CollectionName": str,
        "CreateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMapResponseTypeDef = TypedDict(
    "CreateMapResponseTypeDef",
    {
        "CreateTime": datetime,
        "MapArn": str,
        "MapName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePlaceIndexResponseTypeDef = TypedDict(
    "CreatePlaceIndexResponseTypeDef",
    {
        "CreateTime": datetime,
        "IndexArn": str,
        "IndexName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRouteCalculatorResponseTypeDef = TypedDict(
    "CreateRouteCalculatorResponseTypeDef",
    {
        "CalculatorArn": str,
        "CalculatorName": str,
        "CreateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTrackerResponseTypeDef = TypedDict(
    "CreateTrackerResponseTypeDef",
    {
        "CreateTime": datetime,
        "TrackerArn": str,
        "TrackerName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGeofenceCollectionResponseTypeDef = TypedDict(
    "DescribeGeofenceCollectionResponseTypeDef",
    {
        "CollectionArn": str,
        "CollectionName": str,
        "CreateTime": datetime,
        "Description": str,
        "KmsKeyId": str,
        "PricingPlan": PricingPlanType,
        "PricingPlanDataSource": str,
        "Tags": Dict[str, str],
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRouteCalculatorResponseTypeDef = TypedDict(
    "DescribeRouteCalculatorResponseTypeDef",
    {
        "CalculatorArn": str,
        "CalculatorName": str,
        "CreateTime": datetime,
        "DataSource": str,
        "Description": str,
        "PricingPlan": PricingPlanType,
        "Tags": Dict[str, str],
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTrackerResponseTypeDef = TypedDict(
    "DescribeTrackerResponseTypeDef",
    {
        "CreateTime": datetime,
        "Description": str,
        "KmsKeyId": str,
        "PositionFiltering": PositionFilteringType,
        "PricingPlan": PricingPlanType,
        "PricingPlanDataSource": str,
        "Tags": Dict[str, str],
        "TrackerArn": str,
        "TrackerName": str,
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMapGlyphsResponseTypeDef = TypedDict(
    "GetMapGlyphsResponseTypeDef",
    {
        "Blob": StreamingBody,
        "ContentType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMapSpritesResponseTypeDef = TypedDict(
    "GetMapSpritesResponseTypeDef",
    {
        "Blob": StreamingBody,
        "ContentType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMapStyleDescriptorResponseTypeDef = TypedDict(
    "GetMapStyleDescriptorResponseTypeDef",
    {
        "Blob": StreamingBody,
        "ContentType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMapTileResponseTypeDef = TypedDict(
    "GetMapTileResponseTypeDef",
    {
        "Blob": StreamingBody,
        "ContentType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTrackerConsumersResponseTypeDef = TypedDict(
    "ListTrackerConsumersResponseTypeDef",
    {
        "ConsumerArns": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutGeofenceResponseTypeDef = TypedDict(
    "PutGeofenceResponseTypeDef",
    {
        "CreateTime": datetime,
        "GeofenceId": str,
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGeofenceCollectionResponseTypeDef = TypedDict(
    "UpdateGeofenceCollectionResponseTypeDef",
    {
        "CollectionArn": str,
        "CollectionName": str,
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateMapResponseTypeDef = TypedDict(
    "UpdateMapResponseTypeDef",
    {
        "MapArn": str,
        "MapName": str,
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePlaceIndexResponseTypeDef = TypedDict(
    "UpdatePlaceIndexResponseTypeDef",
    {
        "IndexArn": str,
        "IndexName": str,
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRouteCalculatorResponseTypeDef = TypedDict(
    "UpdateRouteCalculatorResponseTypeDef",
    {
        "CalculatorArn": str,
        "CalculatorName": str,
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTrackerResponseTypeDef = TypedDict(
    "UpdateTrackerResponseTypeDef",
    {
        "TrackerArn": str,
        "TrackerName": str,
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutGeofenceRequestEntryTypeDef = TypedDict(
    "BatchPutGeofenceRequestEntryTypeDef",
    {
        "GeofenceId": str,
        "Geometry": GeofenceGeometryTypeDef,
    },
)

GetGeofenceResponseTypeDef = TypedDict(
    "GetGeofenceResponseTypeDef",
    {
        "CreateTime": datetime,
        "GeofenceId": str,
        "Geometry": GeofenceGeometryTypeDef,
        "Status": str,
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGeofenceResponseEntryTypeDef = TypedDict(
    "ListGeofenceResponseEntryTypeDef",
    {
        "CreateTime": datetime,
        "GeofenceId": str,
        "Geometry": GeofenceGeometryTypeDef,
        "Status": str,
        "UpdateTime": datetime,
    },
)

PutGeofenceRequestRequestTypeDef = TypedDict(
    "PutGeofenceRequestRequestTypeDef",
    {
        "CollectionName": str,
        "GeofenceId": str,
        "Geometry": GeofenceGeometryTypeDef,
    },
)

CalculateRouteTruckModeOptionsTypeDef = TypedDict(
    "CalculateRouteTruckModeOptionsTypeDef",
    {
        "AvoidFerries": bool,
        "AvoidTolls": bool,
        "Dimensions": TruckDimensionsTypeDef,
        "Weight": TruckWeightTypeDef,
    },
    total=False,
)

_RequiredCreateMapRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMapRequestRequestTypeDef",
    {
        "Configuration": MapConfigurationTypeDef,
        "MapName": str,
    },
)
_OptionalCreateMapRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMapRequestRequestTypeDef",
    {
        "Description": str,
        "PricingPlan": PricingPlanType,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateMapRequestRequestTypeDef(
    _RequiredCreateMapRequestRequestTypeDef, _OptionalCreateMapRequestRequestTypeDef
):
    pass


DescribeMapResponseTypeDef = TypedDict(
    "DescribeMapResponseTypeDef",
    {
        "Configuration": MapConfigurationTypeDef,
        "CreateTime": datetime,
        "DataSource": str,
        "Description": str,
        "MapArn": str,
        "MapName": str,
        "PricingPlan": PricingPlanType,
        "Tags": Dict[str, str],
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreatePlaceIndexRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePlaceIndexRequestRequestTypeDef",
    {
        "DataSource": str,
        "IndexName": str,
    },
)
_OptionalCreatePlaceIndexRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePlaceIndexRequestRequestTypeDef",
    {
        "DataSourceConfiguration": DataSourceConfigurationTypeDef,
        "Description": str,
        "PricingPlan": PricingPlanType,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreatePlaceIndexRequestRequestTypeDef(
    _RequiredCreatePlaceIndexRequestRequestTypeDef, _OptionalCreatePlaceIndexRequestRequestTypeDef
):
    pass


DescribePlaceIndexResponseTypeDef = TypedDict(
    "DescribePlaceIndexResponseTypeDef",
    {
        "CreateTime": datetime,
        "DataSource": str,
        "DataSourceConfiguration": DataSourceConfigurationTypeDef,
        "Description": str,
        "IndexArn": str,
        "IndexName": str,
        "PricingPlan": PricingPlanType,
        "Tags": Dict[str, str],
        "UpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdatePlaceIndexRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePlaceIndexRequestRequestTypeDef",
    {
        "IndexName": str,
    },
)
_OptionalUpdatePlaceIndexRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePlaceIndexRequestRequestTypeDef",
    {
        "DataSourceConfiguration": DataSourceConfigurationTypeDef,
        "Description": str,
        "PricingPlan": PricingPlanType,
    },
    total=False,
)


class UpdatePlaceIndexRequestRequestTypeDef(
    _RequiredUpdatePlaceIndexRequestRequestTypeDef, _OptionalUpdatePlaceIndexRequestRequestTypeDef
):
    pass


_RequiredDevicePositionTypeDef = TypedDict(
    "_RequiredDevicePositionTypeDef",
    {
        "Position": List[float],
        "ReceivedTime": datetime,
        "SampleTime": datetime,
    },
)
_OptionalDevicePositionTypeDef = TypedDict(
    "_OptionalDevicePositionTypeDef",
    {
        "Accuracy": PositionalAccuracyTypeDef,
        "DeviceId": str,
        "PositionProperties": Dict[str, str],
    },
    total=False,
)


class DevicePositionTypeDef(_RequiredDevicePositionTypeDef, _OptionalDevicePositionTypeDef):
    pass


_RequiredDevicePositionUpdateTypeDef = TypedDict(
    "_RequiredDevicePositionUpdateTypeDef",
    {
        "DeviceId": str,
        "Position": Sequence[float],
        "SampleTime": Union[datetime, str],
    },
)
_OptionalDevicePositionUpdateTypeDef = TypedDict(
    "_OptionalDevicePositionUpdateTypeDef",
    {
        "Accuracy": PositionalAccuracyTypeDef,
        "PositionProperties": Mapping[str, str],
    },
    total=False,
)


class DevicePositionUpdateTypeDef(
    _RequiredDevicePositionUpdateTypeDef, _OptionalDevicePositionUpdateTypeDef
):
    pass


GetDevicePositionResponseTypeDef = TypedDict(
    "GetDevicePositionResponseTypeDef",
    {
        "Accuracy": PositionalAccuracyTypeDef,
        "DeviceId": str,
        "Position": List[float],
        "PositionProperties": Dict[str, str],
        "ReceivedTime": datetime,
        "SampleTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListDevicePositionsResponseEntryTypeDef = TypedDict(
    "_RequiredListDevicePositionsResponseEntryTypeDef",
    {
        "DeviceId": str,
        "Position": List[float],
        "SampleTime": datetime,
    },
)
_OptionalListDevicePositionsResponseEntryTypeDef = TypedDict(
    "_OptionalListDevicePositionsResponseEntryTypeDef",
    {
        "Accuracy": PositionalAccuracyTypeDef,
        "PositionProperties": Dict[str, str],
    },
    total=False,
)


class ListDevicePositionsResponseEntryTypeDef(
    _RequiredListDevicePositionsResponseEntryTypeDef,
    _OptionalListDevicePositionsResponseEntryTypeDef,
):
    pass


_RequiredGetDevicePositionHistoryRequestGetDevicePositionHistoryPaginateTypeDef = TypedDict(
    "_RequiredGetDevicePositionHistoryRequestGetDevicePositionHistoryPaginateTypeDef",
    {
        "DeviceId": str,
        "TrackerName": str,
    },
)
_OptionalGetDevicePositionHistoryRequestGetDevicePositionHistoryPaginateTypeDef = TypedDict(
    "_OptionalGetDevicePositionHistoryRequestGetDevicePositionHistoryPaginateTypeDef",
    {
        "EndTimeExclusive": Union[datetime, str],
        "StartTimeInclusive": Union[datetime, str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetDevicePositionHistoryRequestGetDevicePositionHistoryPaginateTypeDef(
    _RequiredGetDevicePositionHistoryRequestGetDevicePositionHistoryPaginateTypeDef,
    _OptionalGetDevicePositionHistoryRequestGetDevicePositionHistoryPaginateTypeDef,
):
    pass


_RequiredListDevicePositionsRequestListDevicePositionsPaginateTypeDef = TypedDict(
    "_RequiredListDevicePositionsRequestListDevicePositionsPaginateTypeDef",
    {
        "TrackerName": str,
    },
)
_OptionalListDevicePositionsRequestListDevicePositionsPaginateTypeDef = TypedDict(
    "_OptionalListDevicePositionsRequestListDevicePositionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDevicePositionsRequestListDevicePositionsPaginateTypeDef(
    _RequiredListDevicePositionsRequestListDevicePositionsPaginateTypeDef,
    _OptionalListDevicePositionsRequestListDevicePositionsPaginateTypeDef,
):
    pass


ListGeofenceCollectionsRequestListGeofenceCollectionsPaginateTypeDef = TypedDict(
    "ListGeofenceCollectionsRequestListGeofenceCollectionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListGeofencesRequestListGeofencesPaginateTypeDef = TypedDict(
    "_RequiredListGeofencesRequestListGeofencesPaginateTypeDef",
    {
        "CollectionName": str,
    },
)
_OptionalListGeofencesRequestListGeofencesPaginateTypeDef = TypedDict(
    "_OptionalListGeofencesRequestListGeofencesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListGeofencesRequestListGeofencesPaginateTypeDef(
    _RequiredListGeofencesRequestListGeofencesPaginateTypeDef,
    _OptionalListGeofencesRequestListGeofencesPaginateTypeDef,
):
    pass


ListMapsRequestListMapsPaginateTypeDef = TypedDict(
    "ListMapsRequestListMapsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListPlaceIndexesRequestListPlaceIndexesPaginateTypeDef = TypedDict(
    "ListPlaceIndexesRequestListPlaceIndexesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListRouteCalculatorsRequestListRouteCalculatorsPaginateTypeDef = TypedDict(
    "ListRouteCalculatorsRequestListRouteCalculatorsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListTrackerConsumersRequestListTrackerConsumersPaginateTypeDef = TypedDict(
    "_RequiredListTrackerConsumersRequestListTrackerConsumersPaginateTypeDef",
    {
        "TrackerName": str,
    },
)
_OptionalListTrackerConsumersRequestListTrackerConsumersPaginateTypeDef = TypedDict(
    "_OptionalListTrackerConsumersRequestListTrackerConsumersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTrackerConsumersRequestListTrackerConsumersPaginateTypeDef(
    _RequiredListTrackerConsumersRequestListTrackerConsumersPaginateTypeDef,
    _OptionalListTrackerConsumersRequestListTrackerConsumersPaginateTypeDef,
):
    pass


ListTrackersRequestListTrackersPaginateTypeDef = TypedDict(
    "ListTrackersRequestListTrackersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredLegTypeDef = TypedDict(
    "_RequiredLegTypeDef",
    {
        "Distance": float,
        "DurationSeconds": float,
        "EndPosition": List[float],
        "StartPosition": List[float],
        "Steps": List[StepTypeDef],
    },
)
_OptionalLegTypeDef = TypedDict(
    "_OptionalLegTypeDef",
    {
        "Geometry": LegGeometryTypeDef,
    },
    total=False,
)


class LegTypeDef(_RequiredLegTypeDef, _OptionalLegTypeDef):
    pass


ListGeofenceCollectionsResponseTypeDef = TypedDict(
    "ListGeofenceCollectionsResponseTypeDef",
    {
        "Entries": List[ListGeofenceCollectionsResponseEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMapsResponseTypeDef = TypedDict(
    "ListMapsResponseTypeDef",
    {
        "Entries": List[ListMapsResponseEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPlaceIndexesResponseTypeDef = TypedDict(
    "ListPlaceIndexesResponseTypeDef",
    {
        "Entries": List[ListPlaceIndexesResponseEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRouteCalculatorsResponseTypeDef = TypedDict(
    "ListRouteCalculatorsResponseTypeDef",
    {
        "Entries": List[ListRouteCalculatorsResponseEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTrackersResponseTypeDef = TypedDict(
    "ListTrackersResponseTypeDef",
    {
        "Entries": List[ListTrackersResponseEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPlaceTypeDef = TypedDict(
    "_RequiredPlaceTypeDef",
    {
        "Geometry": PlaceGeometryTypeDef,
    },
)
_OptionalPlaceTypeDef = TypedDict(
    "_OptionalPlaceTypeDef",
    {
        "AddressNumber": str,
        "Country": str,
        "Interpolated": bool,
        "Label": str,
        "Municipality": str,
        "Neighborhood": str,
        "PostalCode": str,
        "Region": str,
        "Street": str,
        "SubRegion": str,
        "TimeZone": TimeZoneTypeDef,
    },
    total=False,
)


class PlaceTypeDef(_RequiredPlaceTypeDef, _OptionalPlaceTypeDef):
    pass


RouteMatrixEntryTypeDef = TypedDict(
    "RouteMatrixEntryTypeDef",
    {
        "Distance": float,
        "DurationSeconds": float,
        "Error": RouteMatrixEntryErrorTypeDef,
    },
    total=False,
)

SearchPlaceIndexForSuggestionsResponseTypeDef = TypedDict(
    "SearchPlaceIndexForSuggestionsResponseTypeDef",
    {
        "Results": List[SearchForSuggestionsResultTypeDef],
        "Summary": SearchPlaceIndexForSuggestionsSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDeleteDevicePositionHistoryResponseTypeDef = TypedDict(
    "BatchDeleteDevicePositionHistoryResponseTypeDef",
    {
        "Errors": List[BatchDeleteDevicePositionHistoryErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDeleteGeofenceResponseTypeDef = TypedDict(
    "BatchDeleteGeofenceResponseTypeDef",
    {
        "Errors": List[BatchDeleteGeofenceErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchEvaluateGeofencesResponseTypeDef = TypedDict(
    "BatchEvaluateGeofencesResponseTypeDef",
    {
        "Errors": List[BatchEvaluateGeofencesErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutGeofenceResponseTypeDef = TypedDict(
    "BatchPutGeofenceResponseTypeDef",
    {
        "Errors": List[BatchPutGeofenceErrorTypeDef],
        "Successes": List[BatchPutGeofenceSuccessTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchUpdateDevicePositionResponseTypeDef = TypedDict(
    "BatchUpdateDevicePositionResponseTypeDef",
    {
        "Errors": List[BatchUpdateDevicePositionErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutGeofenceRequestRequestTypeDef = TypedDict(
    "BatchPutGeofenceRequestRequestTypeDef",
    {
        "CollectionName": str,
        "Entries": Sequence[BatchPutGeofenceRequestEntryTypeDef],
    },
)

ListGeofencesResponseTypeDef = TypedDict(
    "ListGeofencesResponseTypeDef",
    {
        "Entries": List[ListGeofenceResponseEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCalculateRouteMatrixRequestRequestTypeDef = TypedDict(
    "_RequiredCalculateRouteMatrixRequestRequestTypeDef",
    {
        "CalculatorName": str,
        "DeparturePositions": Sequence[Sequence[float]],
        "DestinationPositions": Sequence[Sequence[float]],
    },
)
_OptionalCalculateRouteMatrixRequestRequestTypeDef = TypedDict(
    "_OptionalCalculateRouteMatrixRequestRequestTypeDef",
    {
        "CarModeOptions": CalculateRouteCarModeOptionsTypeDef,
        "DepartNow": bool,
        "DepartureTime": Union[datetime, str],
        "DistanceUnit": DistanceUnitType,
        "TravelMode": TravelModeType,
        "TruckModeOptions": CalculateRouteTruckModeOptionsTypeDef,
    },
    total=False,
)


class CalculateRouteMatrixRequestRequestTypeDef(
    _RequiredCalculateRouteMatrixRequestRequestTypeDef,
    _OptionalCalculateRouteMatrixRequestRequestTypeDef,
):
    pass


_RequiredCalculateRouteRequestRequestTypeDef = TypedDict(
    "_RequiredCalculateRouteRequestRequestTypeDef",
    {
        "CalculatorName": str,
        "DeparturePosition": Sequence[float],
        "DestinationPosition": Sequence[float],
    },
)
_OptionalCalculateRouteRequestRequestTypeDef = TypedDict(
    "_OptionalCalculateRouteRequestRequestTypeDef",
    {
        "CarModeOptions": CalculateRouteCarModeOptionsTypeDef,
        "DepartNow": bool,
        "DepartureTime": Union[datetime, str],
        "DistanceUnit": DistanceUnitType,
        "IncludeLegGeometry": bool,
        "TravelMode": TravelModeType,
        "TruckModeOptions": CalculateRouteTruckModeOptionsTypeDef,
        "WaypointPositions": Sequence[Sequence[float]],
    },
    total=False,
)


class CalculateRouteRequestRequestTypeDef(
    _RequiredCalculateRouteRequestRequestTypeDef, _OptionalCalculateRouteRequestRequestTypeDef
):
    pass


BatchGetDevicePositionResponseTypeDef = TypedDict(
    "BatchGetDevicePositionResponseTypeDef",
    {
        "DevicePositions": List[DevicePositionTypeDef],
        "Errors": List[BatchGetDevicePositionErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDevicePositionHistoryResponseTypeDef = TypedDict(
    "GetDevicePositionHistoryResponseTypeDef",
    {
        "DevicePositions": List[DevicePositionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchEvaluateGeofencesRequestRequestTypeDef = TypedDict(
    "BatchEvaluateGeofencesRequestRequestTypeDef",
    {
        "CollectionName": str,
        "DevicePositionUpdates": Sequence[DevicePositionUpdateTypeDef],
    },
)

BatchUpdateDevicePositionRequestRequestTypeDef = TypedDict(
    "BatchUpdateDevicePositionRequestRequestTypeDef",
    {
        "TrackerName": str,
        "Updates": Sequence[DevicePositionUpdateTypeDef],
    },
)

ListDevicePositionsResponseTypeDef = TypedDict(
    "ListDevicePositionsResponseTypeDef",
    {
        "Entries": List[ListDevicePositionsResponseEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CalculateRouteResponseTypeDef = TypedDict(
    "CalculateRouteResponseTypeDef",
    {
        "Legs": List[LegTypeDef],
        "Summary": CalculateRouteSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchForPositionResultTypeDef = TypedDict(
    "SearchForPositionResultTypeDef",
    {
        "Distance": float,
        "Place": PlaceTypeDef,
    },
)

_RequiredSearchForTextResultTypeDef = TypedDict(
    "_RequiredSearchForTextResultTypeDef",
    {
        "Place": PlaceTypeDef,
    },
)
_OptionalSearchForTextResultTypeDef = TypedDict(
    "_OptionalSearchForTextResultTypeDef",
    {
        "Distance": float,
        "Relevance": float,
    },
    total=False,
)


class SearchForTextResultTypeDef(
    _RequiredSearchForTextResultTypeDef, _OptionalSearchForTextResultTypeDef
):
    pass


CalculateRouteMatrixResponseTypeDef = TypedDict(
    "CalculateRouteMatrixResponseTypeDef",
    {
        "RouteMatrix": List[List[RouteMatrixEntryTypeDef]],
        "SnappedDeparturePositions": List[List[float]],
        "SnappedDestinationPositions": List[List[float]],
        "Summary": CalculateRouteMatrixSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchPlaceIndexForPositionResponseTypeDef = TypedDict(
    "SearchPlaceIndexForPositionResponseTypeDef",
    {
        "Results": List[SearchForPositionResultTypeDef],
        "Summary": SearchPlaceIndexForPositionSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchPlaceIndexForTextResponseTypeDef = TypedDict(
    "SearchPlaceIndexForTextResponseTypeDef",
    {
        "Results": List[SearchForTextResultTypeDef],
        "Summary": SearchPlaceIndexForTextSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
