# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = metadata_change_event_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, Callable, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class AspectType(Enum):
    ASSET_CONTACTS = "ASSET_CONTACTS"
    ASSET_FOLLOWERS = "ASSET_FOLLOWERS"
    DASHBOARD_INFO = "DASHBOARD_INFO"
    DASHBOARD_UPSTREAM = "DASHBOARD_UPSTREAM"
    DATASET_DOCUMENTATION = "DATASET_DOCUMENTATION"
    DATASET_FIELD_STATISTICS = "DATASET_FIELD_STATISTICS"
    DATASET_QUERY_HISTORY = "DATASET_QUERY_HISTORY"
    DATASET_SCHEMA = "DATASET_SCHEMA"
    DATASET_SODA_DATA_QUALITY = "DATASET_SODA_DATA_QUALITY"
    DATASET_STATISTICS = "DATASET_STATISTICS"
    DATASET_UPSTREAM = "DATASET_UPSTREAM"
    DATASET_USAGE = "DATASET_USAGE"
    DBT_METRIC = "DBT_METRIC"
    DBT_MODEL = "DBT_MODEL"
    KNOWLEDGE_CARD_INFO = "KNOWLEDGE_CARD_INFO"
    KNOWLEDGE_CARD_VALIDATION = "KNOWLEDGE_CARD_VALIDATION"
    LOOKER_EXPLORE = "LOOKER_EXPLORE"
    LOOKER_VIEW = "LOOKER_VIEW"
    NAMESPACE_ASSETS = "NAMESPACE_ASSETS"
    NAMESPACE_INFO = "NAMESPACE_INFO"
    PERSON_ACTIVITY = "PERSON_ACTIVITY"
    PERSON_ORGANIZATION = "PERSON_ORGANIZATION"
    PERSON_PROPERTIES = "PERSON_PROPERTIES"
    PERSON_SLACK_PROFILE = "PERSON_SLACK_PROFILE"
    POWER_BI_DATASET = "POWER_BI_DATASET"
    PROPERTIES = "PROPERTIES"
    SOURCE_INFO = "SOURCE_INFO"
    SUPPORT_INFO = "SUPPORT_INFO"
    THOUGHT_SPOT = "THOUGHT_SPOT"
    USER_DEFINED_RESOURCE_INFO = "USER_DEFINED_RESOURCE_INFO"


class ValueType(Enum):
    EMAIL = "EMAIL"
    PERSON = "PERSON"
    SLACK = "SLACK"
    UNKNOWN = "UNKNOWN"


@dataclass
class DesignatedContact:
    designation: Optional[str] = None
    value: Optional[str] = None
    value_type: Optional[ValueType] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DesignatedContact':
        assert isinstance(obj, dict)
        designation = from_union([from_str, from_none], obj.get("designation"))
        value = from_union([from_str, from_none], obj.get("value"))
        value_type = from_union([ValueType, from_none], obj.get("valueType"))
        return DesignatedContact(designation, value, value_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["designation"] = from_union([from_str, from_none], self.designation)
        result["value"] = from_union([from_str, from_none], self.value)
        result["valueType"] = from_union([lambda x: to_enum(ValueType, x), from_none], self.value_type)
        return result


@dataclass
class AuditStamp:
    """Model only archival status i.e. not exposed to GraphQL Mutations
    isArchived flag is used by client to update, application logic will transform to
    AuditStamp or undefined as needed
    
    Model only publish status i.e. not exposed to GraphQL Mutations
    isPublished flag is used by client to update, application logic will transform to
    AuditStamp or undefined as needed
    """
    actor: Optional[str] = None
    time: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AuditStamp':
        assert isinstance(obj, dict)
        actor = from_union([from_str, from_none], obj.get("actor"))
        time = from_union([from_datetime, from_none], obj.get("time"))
        return AuditStamp(actor, time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["actor"] = from_union([from_str, from_none], self.actor)
        result["time"] = from_union([lambda x: x.isoformat(), from_none], self.time)
        return result


@dataclass
class ObjectID:
    """A class representation of the BSON ObjectId type."""
    """The generation time of this ObjectId instance"""
    generation_time: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ObjectID':
        assert isinstance(obj, dict)
        generation_time = from_union([from_float, from_none], obj.get("generationTime"))
        return ObjectID(generation_time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["generationTime"] = from_union([to_float, from_none], self.generation_time)
        return result


@dataclass
class AssetContacts:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    contacts: Optional[List[DesignatedContact]] = None
    created: Optional[AuditStamp] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    asset_contacts_id: Optional[str] = None
    last_modified: Optional[AuditStamp] = None
    latest: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AssetContacts':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        contacts = from_union([lambda x: from_list(DesignatedContact.from_dict, x), from_none], obj.get("contacts"))
        created = from_union([AuditStamp.from_dict, from_none], obj.get("created"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        asset_contacts_id = from_union([from_str, from_none], obj.get("id"))
        last_modified = from_union([AuditStamp.from_dict, from_none], obj.get("lastModified"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        return AssetContacts(id, aspect_type, contacts, created, created_at, entity_id, asset_contacts_id, last_modified, latest)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["contacts"] = from_union([lambda x: from_list(lambda x: to_class(DesignatedContact, x), x), from_none], self.contacts)
        result["created"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.created)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.asset_contacts_id)
        result["lastModified"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.last_modified)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        return result


class ChartType(Enum):
    AREA = "AREA"
    BAR = "BAR"
    BOX_PLOT = "BOX_PLOT"
    COLUMN = "COLUMN"
    DONUT = "DONUT"
    FUNNEL = "FUNNEL"
    LINE = "LINE"
    MAP = "MAP"
    OTHER = "OTHER"
    PIE = "PIE"
    SCATTER = "SCATTER"
    TABLE = "TABLE"
    TEXT = "TEXT"
    TIMELINE = "TIMELINE"
    UNKNOWN = "UNKNOWN"
    WATERFALL = "WATERFALL"


@dataclass
class Chart:
    chart_type: Optional[ChartType] = None
    description: Optional[str] = None
    preview: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Chart':
        assert isinstance(obj, dict)
        chart_type = from_union([ChartType, from_none], obj.get("chartType"))
        description = from_union([from_str, from_none], obj.get("description"))
        preview = from_union([from_str, from_none], obj.get("preview"))
        title = from_union([from_str, from_none], obj.get("title"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Chart(chart_type, description, preview, title, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["chartType"] = from_union([lambda x: to_enum(ChartType, x), from_none], self.chart_type)
        result["description"] = from_union([from_str, from_none], self.description)
        result["preview"] = from_union([from_str, from_none], self.preview)
        result["title"] = from_union([from_str, from_none], self.title)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


class PowerBIDashboardType(Enum):
    DASHBOARD = "DASHBOARD"
    REPORT = "REPORT"


@dataclass
class DashboardInfo:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    charts: Optional[List[Chart]] = None
    created_at: Optional[datetime] = None
    description: Optional[str] = None
    entity_id: Optional[str] = None
    dashboard_info_id: Optional[str] = None
    latest: Optional[bool] = None
    power_bi_dashboard_type: Optional[PowerBIDashboardType] = None
    title: Optional[str] = None
    url: Optional[str] = None
    view_count: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DashboardInfo':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        charts = from_union([lambda x: from_list(Chart.from_dict, x), from_none], obj.get("charts"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        description = from_union([from_str, from_none], obj.get("description"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        dashboard_info_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        power_bi_dashboard_type = from_union([PowerBIDashboardType, from_none], obj.get("powerBiDashboardType"))
        title = from_union([from_str, from_none], obj.get("title"))
        url = from_union([from_str, from_none], obj.get("url"))
        view_count = from_union([from_float, from_none], obj.get("viewCount"))
        return DashboardInfo(id, aspect_type, charts, created_at, description, entity_id, dashboard_info_id, latest, power_bi_dashboard_type, title, url, view_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["charts"] = from_union([lambda x: from_list(lambda x: to_class(Chart, x), x), from_none], self.charts)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["description"] = from_union([from_str, from_none], self.description)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.dashboard_info_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["powerBiDashboardType"] = from_union([lambda x: to_enum(PowerBIDashboardType, x), from_none], self.power_bi_dashboard_type)
        result["title"] = from_union([from_str, from_none], self.title)
        result["url"] = from_union([from_str, from_none], self.url)
        result["viewCount"] = from_union([to_float, from_none], self.view_count)
        return result


class EntityType(Enum):
    DASHBOARD = "DASHBOARD"
    DATASET = "DATASET"
    KNOWLEDGE_CARD = "KNOWLEDGE_CARD"
    METRIC = "METRIC"
    NAMESPACE = "NAMESPACE"
    PERSON = "PERSON"
    USER_DEFINED_RESOURCE = "USER_DEFINED_RESOURCE"
    VIRTUAL_VIEW = "VIRTUAL_VIEW"


class DashboardPlatform(Enum):
    LOOKER = "LOOKER"
    METABASE = "METABASE"
    POWER_BI = "POWER_BI"
    TABLEAU = "TABLEAU"
    THOUGHT_SPOT = "THOUGHT_SPOT"
    UNKNOWN = "UNKNOWN"


@dataclass
class DashboardLogicalID:
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    dashboard_id: Optional[str] = None
    platform: Optional[DashboardPlatform] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DashboardLogicalID':
        assert isinstance(obj, dict)
        dashboard_id = from_union([from_str, from_none], obj.get("dashboardId"))
        platform = from_union([DashboardPlatform, from_none], obj.get("platform"))
        return DashboardLogicalID(dashboard_id, platform)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dashboardId"] = from_union([from_str, from_none], self.dashboard_id)
        result["platform"] = from_union([lambda x: to_enum(DashboardPlatform, x), from_none], self.platform)
        return result


@dataclass
class SourceInfo:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    source_info_id: Optional[str] = None
    latest: Optional[bool] = None
    main_url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SourceInfo':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        source_info_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        main_url = from_union([from_str, from_none], obj.get("mainUrl"))
        return SourceInfo(id, aspect_type, created_at, entity_id, source_info_id, latest, main_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.source_info_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["mainUrl"] = from_union([from_str, from_none], self.main_url)
        return result


@dataclass
class DashboardUpstream:
    """DashboardUpstream captures upstream lineages from data sources to this dashboard"""
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    dashboard_upstream_id: Optional[str] = None
    latest: Optional[bool] = None
    source_datasets: Optional[List[str]] = None
    source_virtual_views: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DashboardUpstream':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        dashboard_upstream_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        source_datasets = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sourceDatasets"))
        source_virtual_views = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sourceVirtualViews"))
        return DashboardUpstream(id, aspect_type, created_at, entity_id, dashboard_upstream_id, latest, source_datasets, source_virtual_views)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.dashboard_upstream_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["sourceDatasets"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_datasets)
        result["sourceVirtualViews"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_virtual_views)
        return result


@dataclass
class Dashboard:
    """Backing store for an optionally provided creation date"""
    created_at: Optional[datetime] = None
    """A class representation of the BSON ObjectId type."""
    id: Optional[ObjectID] = None
    asset_contacts: Optional[AssetContacts] = None
    dashboard_created_at: Optional[datetime] = None
    dashboard_info: Optional[DashboardInfo] = None
    deleted_at: Optional[datetime] = None
    entity_type: Optional[EntityType] = None
    """A getter for the id property that's directly generated from the
    entity type & logical ID.
    """
    dashboard_id: Optional[str] = None
    last_modified_at: Optional[datetime] = None
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    logical_id: Optional[DashboardLogicalID] = None
    source_info: Optional[SourceInfo] = None
    """DashboardUpstream captures upstream lineages from data sources to this dashboard"""
    upstream: Optional[DashboardUpstream] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Dashboard':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("_createdAt"))
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        asset_contacts = from_union([AssetContacts.from_dict, from_none], obj.get("assetContacts"))
        dashboard_created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        dashboard_info = from_union([DashboardInfo.from_dict, from_none], obj.get("dashboardInfo"))
        deleted_at = from_union([from_datetime, from_none], obj.get("deletedAt"))
        entity_type = from_union([EntityType, from_none], obj.get("entityType"))
        dashboard_id = from_union([from_str, from_none], obj.get("id"))
        last_modified_at = from_union([from_datetime, from_none], obj.get("lastModifiedAt"))
        logical_id = from_union([DashboardLogicalID.from_dict, from_none], obj.get("logicalId"))
        source_info = from_union([SourceInfo.from_dict, from_none], obj.get("sourceInfo"))
        upstream = from_union([DashboardUpstream.from_dict, from_none], obj.get("upstream"))
        return Dashboard(created_at, id, asset_contacts, dashboard_created_at, dashboard_info, deleted_at, entity_type, dashboard_id, last_modified_at, logical_id, source_info, upstream)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["assetContacts"] = from_union([lambda x: to_class(AssetContacts, x), from_none], self.asset_contacts)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.dashboard_created_at)
        result["dashboardInfo"] = from_union([lambda x: to_class(DashboardInfo, x), from_none], self.dashboard_info)
        result["deletedAt"] = from_union([lambda x: x.isoformat(), from_none], self.deleted_at)
        result["entityType"] = from_union([lambda x: to_enum(EntityType, x), from_none], self.entity_type)
        result["id"] = from_union([from_str, from_none], self.dashboard_id)
        result["lastModifiedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_modified_at)
        result["logicalId"] = from_union([lambda x: to_class(DashboardLogicalID, x), from_none], self.logical_id)
        result["sourceInfo"] = from_union([lambda x: to_class(SourceInfo, x), from_none], self.source_info)
        result["upstream"] = from_union([lambda x: to_class(DashboardUpstream, x), from_none], self.upstream)
        return result


@dataclass
class FieldDocumentation:
    documentation: Optional[str] = None
    field_path: Optional[str] = None
    tests: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FieldDocumentation':
        assert isinstance(obj, dict)
        documentation = from_union([from_str, from_none], obj.get("documentation"))
        field_path = from_union([from_str, from_none], obj.get("fieldPath"))
        tests = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tests"))
        return FieldDocumentation(documentation, field_path, tests)

    def to_dict(self) -> dict:
        result: dict = {}
        result["documentation"] = from_union([from_str, from_none], self.documentation)
        result["fieldPath"] = from_union([from_str, from_none], self.field_path)
        result["tests"] = from_union([lambda x: from_list(from_str, x), from_none], self.tests)
        return result


@dataclass
class DatasetDocumentation:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    dataset_documentations: Optional[List[str]] = None
    entity_id: Optional[str] = None
    field_documentations: Optional[List[FieldDocumentation]] = None
    dataset_documentation_id: Optional[str] = None
    latest: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetDocumentation':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        dataset_documentations = from_union([lambda x: from_list(from_str, x), from_none], obj.get("datasetDocumentations"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        field_documentations = from_union([lambda x: from_list(FieldDocumentation.from_dict, x), from_none], obj.get("fieldDocumentations"))
        dataset_documentation_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        return DatasetDocumentation(id, aspect_type, created_at, dataset_documentations, entity_id, field_documentations, dataset_documentation_id, latest)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["datasetDocumentations"] = from_union([lambda x: from_list(from_str, x), from_none], self.dataset_documentations)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["fieldDocumentations"] = from_union([lambda x: from_list(lambda x: to_class(FieldDocumentation, x), x), from_none], self.field_documentations)
        result["id"] = from_union([from_str, from_none], self.dataset_documentation_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        return result


@dataclass
class FieldStatistics:
    """The statistics of a field/column, e.g. values count, min/max/avg, etc',"""
    average: Optional[float] = None
    distinct_value_count: Optional[float] = None
    field_path: Optional[str] = None
    max_value: Optional[float] = None
    min_value: Optional[float] = None
    nonnull_value_count: Optional[float] = None
    null_value_count: Optional[float] = None
    std_dev: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FieldStatistics':
        assert isinstance(obj, dict)
        average = from_union([from_float, from_none], obj.get("average"))
        distinct_value_count = from_union([from_float, from_none], obj.get("distinctValueCount"))
        field_path = from_union([from_str, from_none], obj.get("fieldPath"))
        max_value = from_union([from_float, from_none], obj.get("maxValue"))
        min_value = from_union([from_float, from_none], obj.get("minValue"))
        nonnull_value_count = from_union([from_float, from_none], obj.get("nonnullValueCount"))
        null_value_count = from_union([from_float, from_none], obj.get("nullValueCount"))
        std_dev = from_union([from_float, from_none], obj.get("stdDev"))
        return FieldStatistics(average, distinct_value_count, field_path, max_value, min_value, nonnull_value_count, null_value_count, std_dev)

    def to_dict(self) -> dict:
        result: dict = {}
        result["average"] = from_union([to_float, from_none], self.average)
        result["distinctValueCount"] = from_union([to_float, from_none], self.distinct_value_count)
        result["fieldPath"] = from_union([from_str, from_none], self.field_path)
        result["maxValue"] = from_union([to_float, from_none], self.max_value)
        result["minValue"] = from_union([to_float, from_none], self.min_value)
        result["nonnullValueCount"] = from_union([to_float, from_none], self.nonnull_value_count)
        result["nullValueCount"] = from_union([to_float, from_none], self.null_value_count)
        result["stdDev"] = from_union([to_float, from_none], self.std_dev)
        return result


@dataclass
class DatasetFieldStatistics:
    """DatasetStatistics captures operational information about the dataset, e.g. the number of
    records or the last refresh time.
    """
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    field_statistics: Optional[List[FieldStatistics]] = None
    dataset_field_statistics_id: Optional[str] = None
    latest: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetFieldStatistics':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        field_statistics = from_union([lambda x: from_list(FieldStatistics.from_dict, x), from_none], obj.get("fieldStatistics"))
        dataset_field_statistics_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        return DatasetFieldStatistics(id, aspect_type, created_at, entity_id, field_statistics, dataset_field_statistics_id, latest)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["fieldStatistics"] = from_union([lambda x: from_list(lambda x: to_class(FieldStatistics, x), x), from_none], self.field_statistics)
        result["id"] = from_union([from_str, from_none], self.dataset_field_statistics_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        return result


class DataPlatform(Enum):
    BIGQUERY = "BIGQUERY"
    DOCUMENTDB = "DOCUMENTDB"
    DYNAMODB = "DYNAMODB"
    ELASTICSEARCH = "ELASTICSEARCH"
    EXTERNAL = "EXTERNAL"
    MYSQL = "MYSQL"
    POSTGRESQL = "POSTGRESQL"
    RDS = "RDS"
    REDIS = "REDIS"
    REDSHIFT = "REDSHIFT"
    S3 = "S3"
    SNOWFLAKE = "SNOWFLAKE"
    UNKNOWN = "UNKNOWN"


@dataclass
class DatasetLogicalID:
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    account: Optional[str] = None
    name: Optional[str] = None
    platform: Optional[DataPlatform] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetLogicalID':
        assert isinstance(obj, dict)
        account = from_union([from_str, from_none], obj.get("account"))
        name = from_union([from_str, from_none], obj.get("name"))
        platform = from_union([DataPlatform, from_none], obj.get("platform"))
        return DatasetLogicalID(account, name, platform)

    def to_dict(self) -> dict:
        result: dict = {}
        result["account"] = from_union([from_str, from_none], self.account)
        result["name"] = from_union([from_str, from_none], self.name)
        result["platform"] = from_union([lambda x: to_enum(DataPlatform, x), from_none], self.platform)
        return result


@dataclass
class Deprecation:
    deprecated_by: Optional[AuditStamp] = None
    reason: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Deprecation':
        assert isinstance(obj, dict)
        deprecated_by = from_union([AuditStamp.from_dict, from_none], obj.get("deprecatedBy"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        return Deprecation(deprecated_by, reason)

    def to_dict(self) -> dict:
        result: dict = {}
        result["deprecatedBy"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.deprecated_by)
        result["reason"] = from_union([from_str, from_none], self.reason)
        return result


@dataclass
class Properties:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    deprecated: Optional[Deprecation] = None
    description: Optional[str] = None
    entity_id: Optional[str] = None
    properties_id: Optional[str] = None
    latest: Optional[bool] = None
    tags: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Properties':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deprecated = from_union([Deprecation.from_dict, from_none], obj.get("deprecated"))
        description = from_union([from_str, from_none], obj.get("description"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        properties_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        return Properties(id, aspect_type, created_at, deprecated, description, entity_id, properties_id, latest, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["deprecated"] = from_union([lambda x: to_class(Deprecation, x), from_none], self.deprecated)
        result["description"] = from_union([from_str, from_none], self.description)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.properties_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        return result


@dataclass
class QueryInfo:
    """Captures the information associated with a specific query."""
    issued_at: Optional[datetime] = None
    issued_by: Optional[str] = None
    query: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'QueryInfo':
        assert isinstance(obj, dict)
        issued_at = from_union([from_datetime, from_none], obj.get("issuedAt"))
        issued_by = from_union([from_str, from_none], obj.get("issuedBy"))
        query = from_union([from_str, from_none], obj.get("query"))
        return QueryInfo(issued_at, issued_by, query)

    def to_dict(self) -> dict:
        result: dict = {}
        result["issuedAt"] = from_union([lambda x: x.isoformat(), from_none], self.issued_at)
        result["issuedBy"] = from_union([from_str, from_none], self.issued_by)
        result["query"] = from_union([from_str, from_none], self.query)
        return result


@dataclass
class DatasetQueryHistory:
    """A dataset's query history"""
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    dataset_query_history_id: Optional[str] = None
    latest: Optional[bool] = None
    recent_queries: Optional[List[QueryInfo]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetQueryHistory':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        dataset_query_history_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        recent_queries = from_union([lambda x: from_list(QueryInfo.from_dict, x), from_none], obj.get("recentQueries"))
        return DatasetQueryHistory(id, aspect_type, created_at, entity_id, dataset_query_history_id, latest, recent_queries)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.dataset_query_history_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["recentQueries"] = from_union([lambda x: from_list(lambda x: to_class(QueryInfo, x), x), from_none], self.recent_queries)
        return result


@dataclass
class SchemaField:
    description: Optional[str] = None
    field_path: Optional[str] = None
    is_unique: Optional[bool] = None
    max_length: Optional[float] = None
    native_type: Optional[str] = None
    nullable: Optional[bool] = None
    precision: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SchemaField':
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        field_path = from_union([from_str, from_none], obj.get("fieldPath"))
        is_unique = from_union([from_bool, from_none], obj.get("isUnique"))
        max_length = from_union([from_float, from_none], obj.get("maxLength"))
        native_type = from_union([from_str, from_none], obj.get("nativeType"))
        nullable = from_union([from_bool, from_none], obj.get("nullable"))
        precision = from_union([from_float, from_none], obj.get("precision"))
        return SchemaField(description, field_path, is_unique, max_length, native_type, nullable, precision)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([from_str, from_none], self.description)
        result["fieldPath"] = from_union([from_str, from_none], self.field_path)
        result["isUnique"] = from_union([from_bool, from_none], self.is_unique)
        result["maxLength"] = from_union([to_float, from_none], self.max_length)
        result["nativeType"] = from_union([from_str, from_none], self.native_type)
        result["nullable"] = from_union([from_bool, from_none], self.nullable)
        result["precision"] = from_union([to_float, from_none], self.precision)
        return result


class SchemaType(Enum):
    AVRO = "AVRO"
    DYNAMODB = "DYNAMODB"
    JSON = "JSON"
    ORC = "ORC"
    PARQUET = "PARQUET"
    PROTOBUF = "PROTOBUF"
    SCHEMALESS = "SCHEMALESS"
    SQL = "SQL"


@dataclass
class ForeignKey:
    field_path: Optional[str] = None
    parent: Optional[DatasetLogicalID] = None
    parent_field: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ForeignKey':
        assert isinstance(obj, dict)
        field_path = from_union([from_str, from_none], obj.get("fieldPath"))
        parent = from_union([DatasetLogicalID.from_dict, from_none], obj.get("parent"))
        parent_field = from_union([from_str, from_none], obj.get("parentField"))
        return ForeignKey(field_path, parent, parent_field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fieldPath"] = from_union([from_str, from_none], self.field_path)
        result["parent"] = from_union([lambda x: to_class(DatasetLogicalID, x), from_none], self.parent)
        result["parentField"] = from_union([from_str, from_none], self.parent_field)
        return result


class MaterializationType(Enum):
    EXTERNAL = "EXTERNAL"
    MATERIALIZED_VIEW = "MATERIALIZED_VIEW"
    TABLE = "TABLE"
    VIEW = "VIEW"


@dataclass
class SQLSchema:
    foreign_key: Optional[List[ForeignKey]] = None
    materialization: Optional[MaterializationType] = None
    primary_key: Optional[List[str]] = None
    table_schema: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SQLSchema':
        assert isinstance(obj, dict)
        foreign_key = from_union([lambda x: from_list(ForeignKey.from_dict, x), from_none], obj.get("foreignKey"))
        materialization = from_union([MaterializationType, from_none], obj.get("materialization"))
        primary_key = from_union([lambda x: from_list(from_str, x), from_none], obj.get("primaryKey"))
        table_schema = from_union([from_str, from_none], obj.get("tableSchema"))
        return SQLSchema(foreign_key, materialization, primary_key, table_schema)

    def to_dict(self) -> dict:
        result: dict = {}
        result["foreignKey"] = from_union([lambda x: from_list(lambda x: to_class(ForeignKey, x), x), from_none], self.foreign_key)
        result["materialization"] = from_union([lambda x: to_enum(MaterializationType, x), from_none], self.materialization)
        result["primaryKey"] = from_union([lambda x: from_list(from_str, x), from_none], self.primary_key)
        result["tableSchema"] = from_union([from_str, from_none], self.table_schema)
        return result


@dataclass
class DatasetSchema:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    description: Optional[str] = None
    entity_id: Optional[str] = None
    fields: Optional[List[SchemaField]] = None
    dataset_schema_id: Optional[str] = None
    last_modified: Optional[AuditStamp] = None
    latest: Optional[bool] = None
    schema_type: Optional[SchemaType] = None
    sql_schema: Optional[SQLSchema] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetSchema':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        description = from_union([from_str, from_none], obj.get("description"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        fields = from_union([lambda x: from_list(SchemaField.from_dict, x), from_none], obj.get("fields"))
        dataset_schema_id = from_union([from_str, from_none], obj.get("id"))
        last_modified = from_union([AuditStamp.from_dict, from_none], obj.get("lastModified"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        schema_type = from_union([SchemaType, from_none], obj.get("schemaType"))
        sql_schema = from_union([SQLSchema.from_dict, from_none], obj.get("sqlSchema"))
        return DatasetSchema(id, aspect_type, created_at, description, entity_id, fields, dataset_schema_id, last_modified, latest, schema_type, sql_schema)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["description"] = from_union([from_str, from_none], self.description)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["fields"] = from_union([lambda x: from_list(lambda x: to_class(SchemaField, x), x), from_none], self.fields)
        result["id"] = from_union([from_str, from_none], self.dataset_schema_id)
        result["lastModified"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.last_modified)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["schemaType"] = from_union([lambda x: to_enum(SchemaType, x), from_none], self.schema_type)
        result["sqlSchema"] = from_union([lambda x: to_class(SQLSchema, x), from_none], self.sql_schema)
        return result


class SodaDataMonitorStatus(Enum):
    ERROR = "ERROR"
    PASSED = "PASSED"
    UNKNOWN = "UNKNOWN"
    WARNING = "WARNING"


@dataclass
class SodaDataMonitorTarget:
    column: Optional[str] = None
    dataset: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SodaDataMonitorTarget':
        assert isinstance(obj, dict)
        column = from_union([from_str, from_none], obj.get("column"))
        dataset = from_union([from_str, from_none], obj.get("dataset"))
        return SodaDataMonitorTarget(column, dataset)

    def to_dict(self) -> dict:
        result: dict = {}
        result["column"] = from_union([from_str, from_none], self.column)
        result["dataset"] = from_union([from_str, from_none], self.dataset)
        return result


@dataclass
class SodaDataMonitor:
    last_run: Optional[datetime] = None
    owner: Optional[str] = None
    status: Optional[SodaDataMonitorStatus] = None
    targets: Optional[List[SodaDataMonitorTarget]] = None
    title: Optional[str] = None
    value: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SodaDataMonitor':
        assert isinstance(obj, dict)
        last_run = from_union([from_datetime, from_none], obj.get("lastRun"))
        owner = from_union([from_str, from_none], obj.get("owner"))
        status = from_union([SodaDataMonitorStatus, from_none], obj.get("status"))
        targets = from_union([lambda x: from_list(SodaDataMonitorTarget.from_dict, x), from_none], obj.get("targets"))
        title = from_union([from_str, from_none], obj.get("title"))
        value = from_union([from_float, from_none], obj.get("value"))
        return SodaDataMonitor(last_run, owner, status, targets, title, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["lastRun"] = from_union([lambda x: x.isoformat(), from_none], self.last_run)
        result["owner"] = from_union([from_str, from_none], self.owner)
        result["status"] = from_union([lambda x: to_enum(SodaDataMonitorStatus, x), from_none], self.status)
        result["targets"] = from_union([lambda x: from_list(lambda x: to_class(SodaDataMonitorTarget, x), x), from_none], self.targets)
        result["title"] = from_union([from_str, from_none], self.title)
        result["value"] = from_union([to_float, from_none], self.value)
        return result


@dataclass
class SodaDataProfileMetrics:
    distinct: Optional[float] = None
    invalid: Optional[float] = None
    maximum: Optional[float] = None
    mean: Optional[float] = None
    minimum: Optional[float] = None
    missing: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SodaDataProfileMetrics':
        assert isinstance(obj, dict)
        distinct = from_union([from_float, from_none], obj.get("distinct"))
        invalid = from_union([from_float, from_none], obj.get("invalid"))
        maximum = from_union([from_float, from_none], obj.get("maximum"))
        mean = from_union([from_float, from_none], obj.get("mean"))
        minimum = from_union([from_float, from_none], obj.get("minimum"))
        missing = from_union([from_float, from_none], obj.get("missing"))
        return SodaDataProfileMetrics(distinct, invalid, maximum, mean, minimum, missing)

    def to_dict(self) -> dict:
        result: dict = {}
        result["distinct"] = from_union([to_float, from_none], self.distinct)
        result["invalid"] = from_union([to_float, from_none], self.invalid)
        result["maximum"] = from_union([to_float, from_none], self.maximum)
        result["mean"] = from_union([to_float, from_none], self.mean)
        result["minimum"] = from_union([to_float, from_none], self.minimum)
        result["missing"] = from_union([to_float, from_none], self.missing)
        return result


@dataclass
class SodaDataProfile:
    column: Optional[str] = None
    last_run: Optional[datetime] = None
    metrics: Optional[SodaDataProfileMetrics] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SodaDataProfile':
        assert isinstance(obj, dict)
        column = from_union([from_str, from_none], obj.get("column"))
        last_run = from_union([from_datetime, from_none], obj.get("lastRun"))
        metrics = from_union([SodaDataProfileMetrics.from_dict, from_none], obj.get("metrics"))
        return SodaDataProfile(column, last_run, metrics)

    def to_dict(self) -> dict:
        result: dict = {}
        result["column"] = from_union([from_str, from_none], self.column)
        result["lastRun"] = from_union([lambda x: x.isoformat(), from_none], self.last_run)
        result["metrics"] = from_union([lambda x: to_class(SodaDataProfileMetrics, x), from_none], self.metrics)
        return result


@dataclass
class DatasetSodaDataQuality:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    dataset_soda_data_quality_id: Optional[str] = None
    latest: Optional[bool] = None
    monitors: Optional[List[SodaDataMonitor]] = None
    profiles: Optional[List[SodaDataProfile]] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetSodaDataQuality':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        dataset_soda_data_quality_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        monitors = from_union([lambda x: from_list(SodaDataMonitor.from_dict, x), from_none], obj.get("monitors"))
        profiles = from_union([lambda x: from_list(SodaDataProfile.from_dict, x), from_none], obj.get("profiles"))
        url = from_union([from_str, from_none], obj.get("url"))
        return DatasetSodaDataQuality(id, aspect_type, created_at, entity_id, dataset_soda_data_quality_id, latest, monitors, profiles, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.dataset_soda_data_quality_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["monitors"] = from_union([lambda x: from_list(lambda x: to_class(SodaDataMonitor, x), x), from_none], self.monitors)
        result["profiles"] = from_union([lambda x: from_list(lambda x: to_class(SodaDataProfile, x), x), from_none], self.profiles)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class DatasetStatistics:
    """DatasetStatistics captures operational information about the dataset, e.g. the number of
    records or the last refresh time.
    """
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    data_size: Optional[float] = None
    entity_id: Optional[str] = None
    field_statistics: Optional[List[FieldStatistics]] = None
    dataset_statistics_id: Optional[str] = None
    last_updated: Optional[datetime] = None
    latest: Optional[bool] = None
    record_count: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetStatistics':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        data_size = from_union([from_float, from_none], obj.get("dataSize"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        field_statistics = from_union([lambda x: from_list(FieldStatistics.from_dict, x), from_none], obj.get("fieldStatistics"))
        dataset_statistics_id = from_union([from_str, from_none], obj.get("id"))
        last_updated = from_union([from_datetime, from_none], obj.get("lastUpdated"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        record_count = from_union([from_float, from_none], obj.get("recordCount"))
        return DatasetStatistics(id, aspect_type, created_at, data_size, entity_id, field_statistics, dataset_statistics_id, last_updated, latest, record_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["dataSize"] = from_union([to_float, from_none], self.data_size)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["fieldStatistics"] = from_union([lambda x: from_list(lambda x: to_class(FieldStatistics, x), x), from_none], self.field_statistics)
        result["id"] = from_union([from_str, from_none], self.dataset_statistics_id)
        result["lastUpdated"] = from_union([lambda x: x.isoformat(), from_none], self.last_updated)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["recordCount"] = from_union([to_float, from_none], self.record_count)
        return result


@dataclass
class ChannelSlackInfo:
    channel_id: Optional[str] = None
    is_archived: Optional[bool] = None
    name: Optional[str] = None
    purpose: Optional[str] = None
    team_id: Optional[str] = None
    topic: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ChannelSlackInfo':
        assert isinstance(obj, dict)
        channel_id = from_union([from_str, from_none], obj.get("channelId"))
        is_archived = from_union([from_bool, from_none], obj.get("isArchived"))
        name = from_union([from_str, from_none], obj.get("name"))
        purpose = from_union([from_str, from_none], obj.get("purpose"))
        team_id = from_union([from_str, from_none], obj.get("teamId"))
        topic = from_union([from_str, from_none], obj.get("topic"))
        return ChannelSlackInfo(channel_id, is_archived, name, purpose, team_id, topic)

    def to_dict(self) -> dict:
        result: dict = {}
        result["channelId"] = from_union([from_str, from_none], self.channel_id)
        result["isArchived"] = from_union([from_bool, from_none], self.is_archived)
        result["name"] = from_union([from_str, from_none], self.name)
        result["purpose"] = from_union([from_str, from_none], self.purpose)
        result["teamId"] = from_union([from_str, from_none], self.team_id)
        result["topic"] = from_union([from_str, from_none], self.topic)
        return result


@dataclass
class SupportInfo:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    group_email: Optional[str] = None
    support_info_id: Optional[str] = None
    latest: Optional[bool] = None
    people_emails: Optional[List[str]] = None
    slack_info: Optional[ChannelSlackInfo] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SupportInfo':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        group_email = from_union([from_str, from_none], obj.get("groupEmail"))
        support_info_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        people_emails = from_union([lambda x: from_list(from_str, x), from_none], obj.get("peopleEmails"))
        slack_info = from_union([ChannelSlackInfo.from_dict, from_none], obj.get("slackInfo"))
        return SupportInfo(id, aspect_type, created_at, entity_id, group_email, support_info_id, latest, people_emails, slack_info)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["groupEmail"] = from_union([from_str, from_none], self.group_email)
        result["id"] = from_union([from_str, from_none], self.support_info_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["peopleEmails"] = from_union([lambda x: from_list(from_str, x), from_none], self.people_emails)
        result["slackInfo"] = from_union([lambda x: to_class(ChannelSlackInfo, x), from_none], self.slack_info)
        return result


@dataclass
class DatasetField:
    dataset: Optional[DatasetLogicalID] = None
    field: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetField':
        assert isinstance(obj, dict)
        dataset = from_union([DatasetLogicalID.from_dict, from_none], obj.get("dataset"))
        field = from_union([from_str, from_none], obj.get("field"))
        return DatasetField(dataset, field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dataset"] = from_union([lambda x: to_class(DatasetLogicalID, x), from_none], self.dataset)
        result["field"] = from_union([from_str, from_none], self.field)
        return result


@dataclass
class FieldMapping:
    destination: Optional[str] = None
    sources: Optional[List[DatasetField]] = None
    transformation: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FieldMapping':
        assert isinstance(obj, dict)
        destination = from_union([from_str, from_none], obj.get("destination"))
        sources = from_union([lambda x: from_list(DatasetField.from_dict, x), from_none], obj.get("sources"))
        transformation = from_union([from_str, from_none], obj.get("transformation"))
        return FieldMapping(destination, sources, transformation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["destination"] = from_union([from_str, from_none], self.destination)
        result["sources"] = from_union([lambda x: from_list(lambda x: to_class(DatasetField, x), x), from_none], self.sources)
        result["transformation"] = from_union([from_str, from_none], self.transformation)
        return result


@dataclass
class DatasetUpstream:
    """DatasetUpstream captures upstream lineages from data sources to this dataset"""
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    executor_url: Optional[str] = None
    field_mappings: Optional[List[FieldMapping]] = None
    dataset_upstream_id: Optional[str] = None
    latest: Optional[bool] = None
    source_code_url: Optional[str] = None
    source_datasets: Optional[List[str]] = None
    transformation: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetUpstream':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        executor_url = from_union([from_str, from_none], obj.get("executorUrl"))
        field_mappings = from_union([lambda x: from_list(FieldMapping.from_dict, x), from_none], obj.get("fieldMappings"))
        dataset_upstream_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        source_code_url = from_union([from_str, from_none], obj.get("sourceCodeUrl"))
        source_datasets = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sourceDatasets"))
        transformation = from_union([from_str, from_none], obj.get("transformation"))
        return DatasetUpstream(id, aspect_type, created_at, entity_id, executor_url, field_mappings, dataset_upstream_id, latest, source_code_url, source_datasets, transformation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["executorUrl"] = from_union([from_str, from_none], self.executor_url)
        result["fieldMappings"] = from_union([lambda x: from_list(lambda x: to_class(FieldMapping, x), x), from_none], self.field_mappings)
        result["id"] = from_union([from_str, from_none], self.dataset_upstream_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["sourceCodeUrl"] = from_union([from_str, from_none], self.source_code_url)
        result["sourceDatasets"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_datasets)
        result["transformation"] = from_union([from_str, from_none], self.transformation)
        return result


@dataclass
class FieldQueryCount:
    """Query count number and statistics of a dataset field"""
    count: Optional[float] = None
    field: Optional[str] = None
    percentile: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FieldQueryCount':
        assert isinstance(obj, dict)
        count = from_union([from_float, from_none], obj.get("count"))
        field = from_union([from_str, from_none], obj.get("field"))
        percentile = from_union([from_float, from_none], obj.get("percentile"))
        return FieldQueryCount(count, field, percentile)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_union([to_float, from_none], self.count)
        result["field"] = from_union([from_str, from_none], self.field)
        result["percentile"] = from_union([to_float, from_none], self.percentile)
        return result


@dataclass
class FieldQueryCounts:
    """Captures field/column query counts in last day/week/month/year."""
    last24_hours: Optional[List[FieldQueryCount]] = None
    last30_days: Optional[List[FieldQueryCount]] = None
    last365_days: Optional[List[FieldQueryCount]] = None
    last7_days: Optional[List[FieldQueryCount]] = None
    last90_days: Optional[List[FieldQueryCount]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'FieldQueryCounts':
        assert isinstance(obj, dict)
        last24_hours = from_union([lambda x: from_list(FieldQueryCount.from_dict, x), from_none], obj.get("last24Hours"))
        last30_days = from_union([lambda x: from_list(FieldQueryCount.from_dict, x), from_none], obj.get("last30Days"))
        last365_days = from_union([lambda x: from_list(FieldQueryCount.from_dict, x), from_none], obj.get("last365Days"))
        last7_days = from_union([lambda x: from_list(FieldQueryCount.from_dict, x), from_none], obj.get("last7Days"))
        last90_days = from_union([lambda x: from_list(FieldQueryCount.from_dict, x), from_none], obj.get("last90Days"))
        return FieldQueryCounts(last24_hours, last30_days, last365_days, last7_days, last90_days)

    def to_dict(self) -> dict:
        result: dict = {}
        result["last24Hours"] = from_union([lambda x: from_list(lambda x: to_class(FieldQueryCount, x), x), from_none], self.last24_hours)
        result["last30Days"] = from_union([lambda x: from_list(lambda x: to_class(FieldQueryCount, x), x), from_none], self.last30_days)
        result["last365Days"] = from_union([lambda x: from_list(lambda x: to_class(FieldQueryCount, x), x), from_none], self.last365_days)
        result["last7Days"] = from_union([lambda x: from_list(lambda x: to_class(FieldQueryCount, x), x), from_none], self.last7_days)
        result["last90Days"] = from_union([lambda x: from_list(lambda x: to_class(FieldQueryCount, x), x), from_none], self.last90_days)
        return result


@dataclass
class QueryCount:
    """Query count number and statistics
    
    The dataset query count within the history date
    """
    count: Optional[float] = None
    percentile: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'QueryCount':
        assert isinstance(obj, dict)
        count = from_union([from_float, from_none], obj.get("count"))
        percentile = from_union([from_float, from_none], obj.get("percentile"))
        return QueryCount(count, percentile)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_union([to_float, from_none], self.count)
        result["percentile"] = from_union([to_float, from_none], self.percentile)
        return result


@dataclass
class QueryCounts:
    """Captures query counts in last day/week/month/year."""
    """Query count number and statistics"""
    last24_hours: Optional[QueryCount] = None
    """Query count number and statistics"""
    last30_days: Optional[QueryCount] = None
    """Query count number and statistics"""
    last365_days: Optional[QueryCount] = None
    """Query count number and statistics"""
    last7_days: Optional[QueryCount] = None
    """Query count number and statistics"""
    last90_days: Optional[QueryCount] = None

    @staticmethod
    def from_dict(obj: Any) -> 'QueryCounts':
        assert isinstance(obj, dict)
        last24_hours = from_union([QueryCount.from_dict, from_none], obj.get("last24Hours"))
        last30_days = from_union([QueryCount.from_dict, from_none], obj.get("last30Days"))
        last365_days = from_union([QueryCount.from_dict, from_none], obj.get("last365Days"))
        last7_days = from_union([QueryCount.from_dict, from_none], obj.get("last7Days"))
        last90_days = from_union([QueryCount.from_dict, from_none], obj.get("last90Days"))
        return QueryCounts(last24_hours, last30_days, last365_days, last7_days, last90_days)

    def to_dict(self) -> dict:
        result: dict = {}
        result["last24Hours"] = from_union([lambda x: to_class(QueryCount, x), from_none], self.last24_hours)
        result["last30Days"] = from_union([lambda x: to_class(QueryCount, x), from_none], self.last30_days)
        result["last365Days"] = from_union([lambda x: to_class(QueryCount, x), from_none], self.last365_days)
        result["last7Days"] = from_union([lambda x: to_class(QueryCount, x), from_none], self.last7_days)
        result["last90Days"] = from_union([lambda x: to_class(QueryCount, x), from_none], self.last90_days)
        return result


@dataclass
class TableColumnsUsage:
    """The columns used in the table join, either in join criteria or filter criteria."""
    columns: Optional[List[str]] = None
    count: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TableColumnsUsage':
        assert isinstance(obj, dict)
        columns = from_union([lambda x: from_list(from_str, x), from_none], obj.get("columns"))
        count = from_union([from_float, from_none], obj.get("count"))
        return TableColumnsUsage(columns, count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["columns"] = from_union([lambda x: from_list(from_str, x), from_none], self.columns)
        result["count"] = from_union([to_float, from_none], self.count)
        return result


@dataclass
class TableJoinScenario:
    """Table join scenario, including the tables involved, joining columns, filtering columns,
    etc.
    """
    count: Optional[float] = None
    datasets: Optional[List[str]] = None
    filtering_columns: Optional[List[TableColumnsUsage]] = None
    joining_columns: Optional[List[TableColumnsUsage]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TableJoinScenario':
        assert isinstance(obj, dict)
        count = from_union([from_float, from_none], obj.get("count"))
        datasets = from_union([lambda x: from_list(from_str, x), from_none], obj.get("datasets"))
        filtering_columns = from_union([lambda x: from_list(TableColumnsUsage.from_dict, x), from_none], obj.get("filteringColumns"))
        joining_columns = from_union([lambda x: from_list(TableColumnsUsage.from_dict, x), from_none], obj.get("joiningColumns"))
        return TableJoinScenario(count, datasets, filtering_columns, joining_columns)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_union([to_float, from_none], self.count)
        result["datasets"] = from_union([lambda x: from_list(from_str, x), from_none], self.datasets)
        result["filteringColumns"] = from_union([lambda x: from_list(lambda x: to_class(TableColumnsUsage, x), x), from_none], self.filtering_columns)
        result["joiningColumns"] = from_union([lambda x: from_list(lambda x: to_class(TableColumnsUsage, x), x), from_none], self.joining_columns)
        return result


@dataclass
class TableJoin:
    """Table join usage statistics"""
    scenarios: Optional[List[TableJoinScenario]] = None
    total_join_count: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TableJoin':
        assert isinstance(obj, dict)
        scenarios = from_union([lambda x: from_list(TableJoinScenario.from_dict, x), from_none], obj.get("scenarios"))
        total_join_count = from_union([from_float, from_none], obj.get("totalJoinCount"))
        return TableJoin(scenarios, total_join_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["scenarios"] = from_union([lambda x: from_list(lambda x: to_class(TableJoinScenario, x), x), from_none], self.scenarios)
        result["totalJoinCount"] = from_union([to_float, from_none], self.total_join_count)
        return result


@dataclass
class TableJoins:
    """Captures table join usage info in last day/week/month/year."""
    """Table join usage statistics"""
    last24_hours: Optional[TableJoin] = None
    """Table join usage statistics"""
    last30_days: Optional[TableJoin] = None
    """Table join usage statistics"""
    last365_days: Optional[TableJoin] = None
    """Table join usage statistics"""
    last7_days: Optional[TableJoin] = None
    """Table join usage statistics"""
    last90_days: Optional[TableJoin] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TableJoins':
        assert isinstance(obj, dict)
        last24_hours = from_union([TableJoin.from_dict, from_none], obj.get("last24Hours"))
        last30_days = from_union([TableJoin.from_dict, from_none], obj.get("last30Days"))
        last365_days = from_union([TableJoin.from_dict, from_none], obj.get("last365Days"))
        last7_days = from_union([TableJoin.from_dict, from_none], obj.get("last7Days"))
        last90_days = from_union([TableJoin.from_dict, from_none], obj.get("last90Days"))
        return TableJoins(last24_hours, last30_days, last365_days, last7_days, last90_days)

    def to_dict(self) -> dict:
        result: dict = {}
        result["last24Hours"] = from_union([lambda x: to_class(TableJoin, x), from_none], self.last24_hours)
        result["last30Days"] = from_union([lambda x: to_class(TableJoin, x), from_none], self.last30_days)
        result["last365Days"] = from_union([lambda x: to_class(TableJoin, x), from_none], self.last365_days)
        result["last7Days"] = from_union([lambda x: to_class(TableJoin, x), from_none], self.last7_days)
        result["last90Days"] = from_union([lambda x: to_class(TableJoin, x), from_none], self.last90_days)
        return result


@dataclass
class UserQueryCount:
    """Query count number and statistics from a user/account"""
    count: Optional[float] = None
    user: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'UserQueryCount':
        assert isinstance(obj, dict)
        count = from_union([from_float, from_none], obj.get("count"))
        user = from_union([from_str, from_none], obj.get("user"))
        return UserQueryCount(count, user)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_union([to_float, from_none], self.count)
        result["user"] = from_union([from_str, from_none], self.user)
        return result


@dataclass
class UserQueryCounts:
    """Captures user query counts in last day/week/month/year."""
    last24_hours: Optional[List[UserQueryCount]] = None
    last24_hours_queried_by_count: Optional[float] = None
    last30_days: Optional[List[UserQueryCount]] = None
    last30_days_queried_by_count: Optional[float] = None
    last365_days: Optional[List[UserQueryCount]] = None
    last365_days_queried_by_count: Optional[float] = None
    last7_days: Optional[List[UserQueryCount]] = None
    last7_days_queried_by_count: Optional[float] = None
    last90_days: Optional[List[UserQueryCount]] = None
    last90_days_queried_by_count: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'UserQueryCounts':
        assert isinstance(obj, dict)
        last24_hours = from_union([lambda x: from_list(UserQueryCount.from_dict, x), from_none], obj.get("last24Hours"))
        last24_hours_queried_by_count = from_union([from_float, from_none], obj.get("last24HoursQueriedByCount"))
        last30_days = from_union([lambda x: from_list(UserQueryCount.from_dict, x), from_none], obj.get("last30Days"))
        last30_days_queried_by_count = from_union([from_float, from_none], obj.get("last30DaysQueriedByCount"))
        last365_days = from_union([lambda x: from_list(UserQueryCount.from_dict, x), from_none], obj.get("last365Days"))
        last365_days_queried_by_count = from_union([from_float, from_none], obj.get("last365DaysQueriedByCount"))
        last7_days = from_union([lambda x: from_list(UserQueryCount.from_dict, x), from_none], obj.get("last7Days"))
        last7_days_queried_by_count = from_union([from_float, from_none], obj.get("last7DaysQueriedByCount"))
        last90_days = from_union([lambda x: from_list(UserQueryCount.from_dict, x), from_none], obj.get("last90Days"))
        last90_days_queried_by_count = from_union([from_float, from_none], obj.get("last90DaysQueriedByCount"))
        return UserQueryCounts(last24_hours, last24_hours_queried_by_count, last30_days, last30_days_queried_by_count, last365_days, last365_days_queried_by_count, last7_days, last7_days_queried_by_count, last90_days, last90_days_queried_by_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["last24Hours"] = from_union([lambda x: from_list(lambda x: to_class(UserQueryCount, x), x), from_none], self.last24_hours)
        result["last24HoursQueriedByCount"] = from_union([to_float, from_none], self.last24_hours_queried_by_count)
        result["last30Days"] = from_union([lambda x: from_list(lambda x: to_class(UserQueryCount, x), x), from_none], self.last30_days)
        result["last30DaysQueriedByCount"] = from_union([to_float, from_none], self.last30_days_queried_by_count)
        result["last365Days"] = from_union([lambda x: from_list(lambda x: to_class(UserQueryCount, x), x), from_none], self.last365_days)
        result["last365DaysQueriedByCount"] = from_union([to_float, from_none], self.last365_days_queried_by_count)
        result["last7Days"] = from_union([lambda x: from_list(lambda x: to_class(UserQueryCount, x), x), from_none], self.last7_days)
        result["last7DaysQueriedByCount"] = from_union([to_float, from_none], self.last7_days_queried_by_count)
        result["last90Days"] = from_union([lambda x: from_list(lambda x: to_class(UserQueryCount, x), x), from_none], self.last90_days)
        result["last90DaysQueriedByCount"] = from_union([to_float, from_none], self.last90_days_queried_by_count)
        return result


@dataclass
class DatasetUsage:
    """Captures dataset usage statistic, e.g. the query counts."""
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    field_query_counts: Optional[FieldQueryCounts] = None
    dataset_usage_id: Optional[str] = None
    latest: Optional[bool] = None
    query_counts: Optional[QueryCounts] = None
    table_joins: Optional[TableJoins] = None
    user_query_counts: Optional[UserQueryCounts] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetUsage':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        field_query_counts = from_union([FieldQueryCounts.from_dict, from_none], obj.get("fieldQueryCounts"))
        dataset_usage_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        query_counts = from_union([QueryCounts.from_dict, from_none], obj.get("queryCounts"))
        table_joins = from_union([TableJoins.from_dict, from_none], obj.get("tableJoins"))
        user_query_counts = from_union([UserQueryCounts.from_dict, from_none], obj.get("userQueryCounts"))
        return DatasetUsage(id, aspect_type, created_at, entity_id, field_query_counts, dataset_usage_id, latest, query_counts, table_joins, user_query_counts)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["fieldQueryCounts"] = from_union([lambda x: to_class(FieldQueryCounts, x), from_none], self.field_query_counts)
        result["id"] = from_union([from_str, from_none], self.dataset_usage_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["queryCounts"] = from_union([lambda x: to_class(QueryCounts, x), from_none], self.query_counts)
        result["tableJoins"] = from_union([lambda x: to_class(TableJoins, x), from_none], self.table_joins)
        result["userQueryCounts"] = from_union([lambda x: to_class(UserQueryCounts, x), from_none], self.user_query_counts)
        return result


class HistoryType(Enum):
    DATASET_USAGE_HISTORY = "DATASET_USAGE_HISTORY"


@dataclass
class DatasetUsageHistory:
    id: Optional[ObjectID] = None
    entity_id: Optional[str] = None
    """The dataset field query counts within the history date"""
    field_query_counts: Optional[List[FieldQueryCount]] = None
    history_date: Optional[datetime] = None
    history_type: Optional[HistoryType] = None
    dataset_usage_history_id: Optional[str] = None
    """The dataset query count within the history date"""
    query_count: Optional[QueryCount] = None
    """The user query counts of the dataset within the history date"""
    user_query_counts: Optional[List[UserQueryCount]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetUsageHistory':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        field_query_counts = from_union([lambda x: from_list(FieldQueryCount.from_dict, x), from_none], obj.get("fieldQueryCounts"))
        history_date = from_union([from_datetime, from_none], obj.get("historyDate"))
        history_type = from_union([HistoryType, from_none], obj.get("historyType"))
        dataset_usage_history_id = from_union([from_str, from_none], obj.get("id"))
        query_count = from_union([QueryCount.from_dict, from_none], obj.get("queryCount"))
        user_query_counts = from_union([lambda x: from_list(UserQueryCount.from_dict, x), from_none], obj.get("userQueryCounts"))
        return DatasetUsageHistory(id, entity_id, field_query_counts, history_date, history_type, dataset_usage_history_id, query_count, user_query_counts)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["fieldQueryCounts"] = from_union([lambda x: from_list(lambda x: to_class(FieldQueryCount, x), x), from_none], self.field_query_counts)
        result["historyDate"] = from_union([lambda x: x.isoformat(), from_none], self.history_date)
        result["historyType"] = from_union([lambda x: to_enum(HistoryType, x), from_none], self.history_type)
        result["id"] = from_union([from_str, from_none], self.dataset_usage_history_id)
        result["queryCount"] = from_union([lambda x: to_class(QueryCount, x), from_none], self.query_count)
        result["userQueryCounts"] = from_union([lambda x: from_list(lambda x: to_class(UserQueryCount, x), x), from_none], self.user_query_counts)
        return result


@dataclass
class Dataset:
    """Backing store for an optionally provided creation date"""
    created_at: Optional[datetime] = None
    """A class representation of the BSON ObjectId type."""
    id: Optional[ObjectID] = None
    asset_contacts: Optional[AssetContacts] = None
    dataset_created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    documentation: Optional[DatasetDocumentation] = None
    entity_type: Optional[EntityType] = None
    """DatasetStatistics captures operational information about the dataset, e.g. the number of
    records or the last refresh time.
    """
    field_statistics: Optional[DatasetFieldStatistics] = None
    """A getter for the id property that's directly generated from the
    entity type & logical ID.
    """
    dataset_id: Optional[str] = None
    last_modified_at: Optional[datetime] = None
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    logical_id: Optional[DatasetLogicalID] = None
    properties: Optional[Properties] = None
    """A dataset's query history"""
    query_history: Optional[DatasetQueryHistory] = None
    schema: Optional[DatasetSchema] = None
    soda_data_quality: Optional[DatasetSodaDataQuality] = None
    source_info: Optional[SourceInfo] = None
    """DatasetStatistics captures operational information about the dataset, e.g. the number of
    records or the last refresh time.
    """
    statistics: Optional[DatasetStatistics] = None
    support_info: Optional[SupportInfo] = None
    """DatasetUpstream captures upstream lineages from data sources to this dataset"""
    upstream: Optional[DatasetUpstream] = None
    """Captures dataset usage statistic, e.g. the query counts."""
    usage: Optional[DatasetUsage] = None
    usage_history: Optional[DatasetUsageHistory] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Dataset':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("_createdAt"))
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        asset_contacts = from_union([AssetContacts.from_dict, from_none], obj.get("assetContacts"))
        dataset_created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deleted_at = from_union([from_datetime, from_none], obj.get("deletedAt"))
        documentation = from_union([DatasetDocumentation.from_dict, from_none], obj.get("documentation"))
        entity_type = from_union([EntityType, from_none], obj.get("entityType"))
        field_statistics = from_union([DatasetFieldStatistics.from_dict, from_none], obj.get("fieldStatistics"))
        dataset_id = from_union([from_str, from_none], obj.get("id"))
        last_modified_at = from_union([from_datetime, from_none], obj.get("lastModifiedAt"))
        logical_id = from_union([DatasetLogicalID.from_dict, from_none], obj.get("logicalId"))
        properties = from_union([Properties.from_dict, from_none], obj.get("properties"))
        query_history = from_union([DatasetQueryHistory.from_dict, from_none], obj.get("queryHistory"))
        schema = from_union([DatasetSchema.from_dict, from_none], obj.get("schema"))
        soda_data_quality = from_union([DatasetSodaDataQuality.from_dict, from_none], obj.get("sodaDataQuality"))
        source_info = from_union([SourceInfo.from_dict, from_none], obj.get("sourceInfo"))
        statistics = from_union([DatasetStatistics.from_dict, from_none], obj.get("statistics"))
        support_info = from_union([SupportInfo.from_dict, from_none], obj.get("supportInfo"))
        upstream = from_union([DatasetUpstream.from_dict, from_none], obj.get("upstream"))
        usage = from_union([DatasetUsage.from_dict, from_none], obj.get("usage"))
        usage_history = from_union([DatasetUsageHistory.from_dict, from_none], obj.get("usageHistory"))
        return Dataset(created_at, id, asset_contacts, dataset_created_at, deleted_at, documentation, entity_type, field_statistics, dataset_id, last_modified_at, logical_id, properties, query_history, schema, soda_data_quality, source_info, statistics, support_info, upstream, usage, usage_history)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["assetContacts"] = from_union([lambda x: to_class(AssetContacts, x), from_none], self.asset_contacts)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.dataset_created_at)
        result["deletedAt"] = from_union([lambda x: x.isoformat(), from_none], self.deleted_at)
        result["documentation"] = from_union([lambda x: to_class(DatasetDocumentation, x), from_none], self.documentation)
        result["entityType"] = from_union([lambda x: to_enum(EntityType, x), from_none], self.entity_type)
        result["fieldStatistics"] = from_union([lambda x: to_class(DatasetFieldStatistics, x), from_none], self.field_statistics)
        result["id"] = from_union([from_str, from_none], self.dataset_id)
        result["lastModifiedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_modified_at)
        result["logicalId"] = from_union([lambda x: to_class(DatasetLogicalID, x), from_none], self.logical_id)
        result["properties"] = from_union([lambda x: to_class(Properties, x), from_none], self.properties)
        result["queryHistory"] = from_union([lambda x: to_class(DatasetQueryHistory, x), from_none], self.query_history)
        result["schema"] = from_union([lambda x: to_class(DatasetSchema, x), from_none], self.schema)
        result["sodaDataQuality"] = from_union([lambda x: to_class(DatasetSodaDataQuality, x), from_none], self.soda_data_quality)
        result["sourceInfo"] = from_union([lambda x: to_class(SourceInfo, x), from_none], self.source_info)
        result["statistics"] = from_union([lambda x: to_class(DatasetStatistics, x), from_none], self.statistics)
        result["supportInfo"] = from_union([lambda x: to_class(SupportInfo, x), from_none], self.support_info)
        result["upstream"] = from_union([lambda x: to_class(DatasetUpstream, x), from_none], self.upstream)
        result["usage"] = from_union([lambda x: to_class(DatasetUsage, x), from_none], self.usage)
        result["usageHistory"] = from_union([lambda x: to_class(DatasetUsageHistory, x), from_none], self.usage_history)
        return result


@dataclass
class EventHeader:
    app_name: Optional[str] = None
    server: Optional[str] = None
    time: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'EventHeader':
        assert isinstance(obj, dict)
        app_name = from_union([from_str, from_none], obj.get("appName"))
        server = from_union([from_str, from_none], obj.get("server"))
        time = from_union([from_datetime, from_none], obj.get("time"))
        return EventHeader(app_name, server, time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["appName"] = from_union([from_str, from_none], self.app_name)
        result["server"] = from_union([from_str, from_none], self.server)
        result["time"] = from_union([lambda x: x.isoformat(), from_none], self.time)
        return result


@dataclass
class AssetDescriptionTokenizedContent:
    description: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AssetDescriptionTokenizedContent':
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        return AssetDescriptionTokenizedContent(description)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([from_str, from_none], self.description)
        return result


@dataclass
class AssetDescriptionKnowledgeCard:
    description: Optional[str] = None
    title: Optional[str] = None
    tokenized_content: Optional[AssetDescriptionTokenizedContent] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AssetDescriptionKnowledgeCard':
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        title = from_union([from_str, from_none], obj.get("title"))
        tokenized_content = from_union([AssetDescriptionTokenizedContent.from_dict, from_none], obj.get("tokenizedContent"))
        return AssetDescriptionKnowledgeCard(description, title, tokenized_content)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([from_str, from_none], self.description)
        result["title"] = from_union([from_str, from_none], self.title)
        result["tokenizedContent"] = from_union([lambda x: to_class(AssetDescriptionTokenizedContent, x), from_none], self.tokenized_content)
        return result


@dataclass
class BusinessCriticalTokenizedContent:
    justification: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'BusinessCriticalTokenizedContent':
        assert isinstance(obj, dict)
        justification = from_union([from_str, from_none], obj.get("justification"))
        return BusinessCriticalTokenizedContent(justification)

    def to_dict(self) -> dict:
        result: dict = {}
        result["justification"] = from_union([from_str, from_none], self.justification)
        return result


@dataclass
class BusinessCriticalKnowledgeCard:
    justification: Optional[str] = None
    title: Optional[str] = None
    tokenized_content: Optional[BusinessCriticalTokenizedContent] = None

    @staticmethod
    def from_dict(obj: Any) -> 'BusinessCriticalKnowledgeCard':
        assert isinstance(obj, dict)
        justification = from_union([from_str, from_none], obj.get("justification"))
        title = from_union([from_str, from_none], obj.get("title"))
        tokenized_content = from_union([BusinessCriticalTokenizedContent.from_dict, from_none], obj.get("tokenizedContent"))
        return BusinessCriticalKnowledgeCard(justification, title, tokenized_content)

    def to_dict(self) -> dict:
        result: dict = {}
        result["justification"] = from_union([from_str, from_none], self.justification)
        result["title"] = from_union([from_str, from_none], self.title)
        result["tokenizedContent"] = from_union([lambda x: to_class(BusinessCriticalTokenizedContent, x), from_none], self.tokenized_content)
        return result


@dataclass
class BusinessTermTokenizedContent:
    definition: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'BusinessTermTokenizedContent':
        assert isinstance(obj, dict)
        definition = from_union([from_str, from_none], obj.get("definition"))
        return BusinessTermTokenizedContent(definition)

    def to_dict(self) -> dict:
        result: dict = {}
        result["definition"] = from_union([from_str, from_none], self.definition)
        return result


@dataclass
class BusinessTermKnowledgeCard:
    definition: Optional[str] = None
    title: Optional[str] = None
    tokenized_content: Optional[BusinessTermTokenizedContent] = None

    @staticmethod
    def from_dict(obj: Any) -> 'BusinessTermKnowledgeCard':
        assert isinstance(obj, dict)
        definition = from_union([from_str, from_none], obj.get("definition"))
        title = from_union([from_str, from_none], obj.get("title"))
        tokenized_content = from_union([BusinessTermTokenizedContent.from_dict, from_none], obj.get("tokenizedContent"))
        return BusinessTermKnowledgeCard(definition, title, tokenized_content)

    def to_dict(self) -> dict:
        result: dict = {}
        result["definition"] = from_union([from_str, from_none], self.definition)
        result["title"] = from_union([from_str, from_none], self.title)
        result["tokenizedContent"] = from_union([lambda x: to_class(BusinessTermTokenizedContent, x), from_none], self.tokenized_content)
        return result


@dataclass
class ColumnDescriptionKnowledgeCard:
    description: Optional[str] = None
    field_path: Optional[str] = None
    title: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ColumnDescriptionKnowledgeCard':
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        field_path = from_union([from_str, from_none], obj.get("fieldPath"))
        title = from_union([from_str, from_none], obj.get("title"))
        return ColumnDescriptionKnowledgeCard(description, field_path, title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([from_str, from_none], self.description)
        result["fieldPath"] = from_union([from_str, from_none], self.field_path)
        result["title"] = from_union([from_str, from_none], self.title)
        return result


@dataclass
class DataDocumentTokenizedContent:
    content: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DataDocumentTokenizedContent':
        assert isinstance(obj, dict)
        content = from_union([from_str, from_none], obj.get("content"))
        return DataDocumentTokenizedContent(content)

    def to_dict(self) -> dict:
        result: dict = {}
        result["content"] = from_union([from_str, from_none], self.content)
        return result


@dataclass
class DataDocument:
    content: Optional[str] = None
    title: Optional[str] = None
    tokenized_content: Optional[DataDocumentTokenizedContent] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DataDocument':
        assert isinstance(obj, dict)
        content = from_union([from_str, from_none], obj.get("content"))
        title = from_union([from_str, from_none], obj.get("title"))
        tokenized_content = from_union([DataDocumentTokenizedContent.from_dict, from_none], obj.get("tokenizedContent"))
        return DataDocument(content, title, tokenized_content)

    def to_dict(self) -> dict:
        result: dict = {}
        result["content"] = from_union([from_str, from_none], self.content)
        result["title"] = from_union([from_str, from_none], self.title)
        result["tokenizedContent"] = from_union([lambda x: to_class(DataDocumentTokenizedContent, x), from_none], self.tokenized_content)
        return result


@dataclass
class DeprecationTokenizedContent:
    detail: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DeprecationTokenizedContent':
        assert isinstance(obj, dict)
        detail = from_union([from_str, from_none], obj.get("detail"))
        return DeprecationTokenizedContent(detail)

    def to_dict(self) -> dict:
        result: dict = {}
        result["detail"] = from_union([from_str, from_none], self.detail)
        return result


@dataclass
class DeprecationKnowledgeCard:
    detail: Optional[str] = None
    planned_date: Optional[datetime] = None
    title: Optional[str] = None
    tokenized_content: Optional[DeprecationTokenizedContent] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DeprecationKnowledgeCard':
        assert isinstance(obj, dict)
        detail = from_union([from_str, from_none], obj.get("detail"))
        planned_date = from_union([from_datetime, from_none], obj.get("plannedDate"))
        title = from_union([from_str, from_none], obj.get("title"))
        tokenized_content = from_union([DeprecationTokenizedContent.from_dict, from_none], obj.get("tokenizedContent"))
        return DeprecationKnowledgeCard(detail, planned_date, title, tokenized_content)

    def to_dict(self) -> dict:
        result: dict = {}
        result["detail"] = from_union([from_str, from_none], self.detail)
        result["plannedDate"] = from_union([lambda x: x.isoformat(), from_none], self.planned_date)
        result["title"] = from_union([from_str, from_none], self.title)
        result["tokenizedContent"] = from_union([lambda x: to_class(DeprecationTokenizedContent, x), from_none], self.tokenized_content)
        return result


@dataclass
class IncidentTokenizedContent:
    detail: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'IncidentTokenizedContent':
        assert isinstance(obj, dict)
        detail = from_union([from_str, from_none], obj.get("detail"))
        return IncidentTokenizedContent(detail)

    def to_dict(self) -> dict:
        result: dict = {}
        result["detail"] = from_union([from_str, from_none], self.detail)
        return result


@dataclass
class IncidentKnowledgeCard:
    detail: Optional[str] = None
    title: Optional[str] = None
    tokenized_content: Optional[IncidentTokenizedContent] = None

    @staticmethod
    def from_dict(obj: Any) -> 'IncidentKnowledgeCard':
        assert isinstance(obj, dict)
        detail = from_union([from_str, from_none], obj.get("detail"))
        title = from_union([from_str, from_none], obj.get("title"))
        tokenized_content = from_union([IncidentTokenizedContent.from_dict, from_none], obj.get("tokenizedContent"))
        return IncidentKnowledgeCard(detail, title, tokenized_content)

    def to_dict(self) -> dict:
        result: dict = {}
        result["detail"] = from_union([from_str, from_none], self.detail)
        result["title"] = from_union([from_str, from_none], self.title)
        result["tokenizedContent"] = from_union([lambda x: to_class(IncidentTokenizedContent, x), from_none], self.tokenized_content)
        return result


class KnowledgeCardType(Enum):
    ASSET_DESCRIPTION = "ASSET_DESCRIPTION"
    BUSINESS_CRITICAL = "BUSINESS_CRITICAL"
    BUSINESS_TERM = "BUSINESS_TERM"
    COLUMN_DESCRIPTION = "COLUMN_DESCRIPTION"
    DATA_DOCUMENT = "DATA_DOCUMENT"
    DEPRECATION = "DEPRECATION"
    HOW_TO_USE = "HOW_TO_USE"
    INCIDENT = "INCIDENT"
    UNKNOWN = "UNKNOWN"


@dataclass
class HowToUseTokenizedContent:
    detail: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'HowToUseTokenizedContent':
        assert isinstance(obj, dict)
        detail = from_union([from_str, from_none], obj.get("detail"))
        return HowToUseTokenizedContent(detail)

    def to_dict(self) -> dict:
        result: dict = {}
        result["detail"] = from_union([from_str, from_none], self.detail)
        return result


@dataclass
class UsageKnowledgeCard:
    detail: Optional[str] = None
    example: Optional[str] = None
    title: Optional[str] = None
    tokenized_content: Optional[HowToUseTokenizedContent] = None

    @staticmethod
    def from_dict(obj: Any) -> 'UsageKnowledgeCard':
        assert isinstance(obj, dict)
        detail = from_union([from_str, from_none], obj.get("detail"))
        example = from_union([from_str, from_none], obj.get("example"))
        title = from_union([from_str, from_none], obj.get("title"))
        tokenized_content = from_union([HowToUseTokenizedContent.from_dict, from_none], obj.get("tokenizedContent"))
        return UsageKnowledgeCard(detail, example, title, tokenized_content)

    def to_dict(self) -> dict:
        result: dict = {}
        result["detail"] = from_union([from_str, from_none], self.detail)
        result["example"] = from_union([from_str, from_none], self.example)
        result["title"] = from_union([from_str, from_none], self.title)
        result["tokenizedContent"] = from_union([lambda x: to_class(HowToUseTokenizedContent, x), from_none], self.tokenized_content)
        return result


@dataclass
class KnowledgeCardDetail:
    """Collection of possible knowledge card types"""
    asset_description: Optional[AssetDescriptionKnowledgeCard] = None
    business_critical: Optional[BusinessCriticalKnowledgeCard] = None
    business_term: Optional[BusinessTermKnowledgeCard] = None
    column_description: Optional[ColumnDescriptionKnowledgeCard] = None
    data_document: Optional[DataDocument] = None
    deprecation: Optional[DeprecationKnowledgeCard] = None
    incident: Optional[IncidentKnowledgeCard] = None
    type: Optional[KnowledgeCardType] = None
    usage: Optional[UsageKnowledgeCard] = None

    @staticmethod
    def from_dict(obj: Any) -> 'KnowledgeCardDetail':
        assert isinstance(obj, dict)
        asset_description = from_union([AssetDescriptionKnowledgeCard.from_dict, from_none], obj.get("assetDescription"))
        business_critical = from_union([BusinessCriticalKnowledgeCard.from_dict, from_none], obj.get("businessCritical"))
        business_term = from_union([BusinessTermKnowledgeCard.from_dict, from_none], obj.get("businessTerm"))
        column_description = from_union([ColumnDescriptionKnowledgeCard.from_dict, from_none], obj.get("columnDescription"))
        data_document = from_union([DataDocument.from_dict, from_none], obj.get("dataDocument"))
        deprecation = from_union([DeprecationKnowledgeCard.from_dict, from_none], obj.get("deprecation"))
        incident = from_union([IncidentKnowledgeCard.from_dict, from_none], obj.get("incident"))
        type = from_union([KnowledgeCardType, from_none], obj.get("type"))
        usage = from_union([UsageKnowledgeCard.from_dict, from_none], obj.get("usage"))
        return KnowledgeCardDetail(asset_description, business_critical, business_term, column_description, data_document, deprecation, incident, type, usage)

    def to_dict(self) -> dict:
        result: dict = {}
        result["assetDescription"] = from_union([lambda x: to_class(AssetDescriptionKnowledgeCard, x), from_none], self.asset_description)
        result["businessCritical"] = from_union([lambda x: to_class(BusinessCriticalKnowledgeCard, x), from_none], self.business_critical)
        result["businessTerm"] = from_union([lambda x: to_class(BusinessTermKnowledgeCard, x), from_none], self.business_term)
        result["columnDescription"] = from_union([lambda x: to_class(ColumnDescriptionKnowledgeCard, x), from_none], self.column_description)
        result["dataDocument"] = from_union([lambda x: to_class(DataDocument, x), from_none], self.data_document)
        result["deprecation"] = from_union([lambda x: to_class(DeprecationKnowledgeCard, x), from_none], self.deprecation)
        result["incident"] = from_union([lambda x: to_class(IncidentKnowledgeCard, x), from_none], self.incident)
        result["type"] = from_union([lambda x: to_enum(KnowledgeCardType, x), from_none], self.type)
        result["usage"] = from_union([lambda x: to_class(UsageKnowledgeCard, x), from_none], self.usage)
        return result


@dataclass
class Hashtag:
    value: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Hashtag':
        assert isinstance(obj, dict)
        value = from_union([from_str, from_none], obj.get("value"))
        return Hashtag(value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["value"] = from_union([from_str, from_none], self.value)
        return result


@dataclass
class KnowledgeCardInfo:
    id: Optional[ObjectID] = None
    """backing store for related Entities which contains
    related entity ids excluding the anchor Entity id
    Note: Cannot be a native private field since it's shared between input and output
    """
    non_anchoring_ids_backing_store: Optional[List[str]] = None
    """The global id for the Entity the associated Knowledge Card was created for. Must be
    provided on Knowledge Card creation for cards that are anchored to an Entity
    Specified on the Input Type KnowledgeCardInfoInput
    """
    anchor_entity_id: Optional[str] = None
    """Model only archival status i.e. not exposed to GraphQL Mutations
    isArchived flag is used by client to update, application logic will transform to
    AuditStamp or undefined as needed
    """
    archived: Optional[AuditStamp] = None
    aspect_type: Optional[AspectType] = None
    created: Optional[AuditStamp] = None
    created_at: Optional[datetime] = None
    detail: Optional[KnowledgeCardDetail] = None
    entity_id: Optional[str] = None
    hashtags: Optional[List[Hashtag]] = None
    knowledge_card_info_id: Optional[str] = None
    is_draft: Optional[bool] = None
    last_modified: Optional[AuditStamp] = None
    latest: Optional[bool] = None
    """Model only publish status i.e. not exposed to GraphQL Mutations
    isPublished flag is used by client to update, application logic will transform to
    AuditStamp or undefined as needed
    """
    published: Optional[AuditStamp] = None
    """Getter and setter interface to protected _nonAnchoringIdsBackingStore
    Includes the non-empty anchorEntityId as the first item in the list
    of relatedEntityIds
    """
    related_entity_ids: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'KnowledgeCardInfo':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        non_anchoring_ids_backing_store = from_union([lambda x: from_list(from_str, x), from_none], obj.get("_nonAnchoringIdsBackingStore"))
        anchor_entity_id = from_union([from_str, from_none], obj.get("anchorEntityId"))
        archived = from_union([AuditStamp.from_dict, from_none], obj.get("archived"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created = from_union([AuditStamp.from_dict, from_none], obj.get("created"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        detail = from_union([KnowledgeCardDetail.from_dict, from_none], obj.get("detail"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        hashtags = from_union([lambda x: from_list(Hashtag.from_dict, x), from_none], obj.get("hashtags"))
        knowledge_card_info_id = from_union([from_str, from_none], obj.get("id"))
        is_draft = from_union([from_bool, from_none], obj.get("isDraft"))
        last_modified = from_union([AuditStamp.from_dict, from_none], obj.get("lastModified"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        published = from_union([AuditStamp.from_dict, from_none], obj.get("published"))
        related_entity_ids = from_union([lambda x: from_list(from_str, x), from_none], obj.get("relatedEntityIds"))
        return KnowledgeCardInfo(id, non_anchoring_ids_backing_store, anchor_entity_id, archived, aspect_type, created, created_at, detail, entity_id, hashtags, knowledge_card_info_id, is_draft, last_modified, latest, published, related_entity_ids)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["_nonAnchoringIdsBackingStore"] = from_union([lambda x: from_list(from_str, x), from_none], self.non_anchoring_ids_backing_store)
        result["anchorEntityId"] = from_union([from_str, from_none], self.anchor_entity_id)
        result["archived"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.archived)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["created"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.created)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["detail"] = from_union([lambda x: to_class(KnowledgeCardDetail, x), from_none], self.detail)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["hashtags"] = from_union([lambda x: from_list(lambda x: to_class(Hashtag, x), x), from_none], self.hashtags)
        result["id"] = from_union([from_str, from_none], self.knowledge_card_info_id)
        result["isDraft"] = from_union([from_bool, from_none], self.is_draft)
        result["lastModified"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.last_modified)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["published"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.published)
        result["relatedEntityIds"] = from_union([lambda x: from_list(from_str, x), from_none], self.related_entity_ids)
        return result


@dataclass
class ValidationConfirmation:
    confirmed_by: Optional[AuditStamp] = None
    knowledge_card_id: Optional[str] = None
    message: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ValidationConfirmation':
        assert isinstance(obj, dict)
        confirmed_by = from_union([AuditStamp.from_dict, from_none], obj.get("confirmedBy"))
        knowledge_card_id = from_union([from_str, from_none], obj.get("knowledgeCardId"))
        message = from_union([from_str, from_none], obj.get("message"))
        return ValidationConfirmation(confirmed_by, knowledge_card_id, message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["confirmedBy"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.confirmed_by)
        result["knowledgeCardId"] = from_union([from_str, from_none], self.knowledge_card_id)
        result["message"] = from_union([from_str, from_none], self.message)
        return result


@dataclass
class ValidationRequest:
    knowledge_card_id: Optional[str] = None
    message: Optional[str] = None
    recipient_id: Optional[str] = None
    requested_by: Optional[AuditStamp] = None
    requester_id: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ValidationRequest':
        assert isinstance(obj, dict)
        knowledge_card_id = from_union([from_str, from_none], obj.get("knowledgeCardId"))
        message = from_union([from_str, from_none], obj.get("message"))
        recipient_id = from_union([from_str, from_none], obj.get("recipientId"))
        requested_by = from_union([AuditStamp.from_dict, from_none], obj.get("requestedBy"))
        requester_id = from_union([from_str, from_none], obj.get("requesterId"))
        return ValidationRequest(knowledge_card_id, message, recipient_id, requested_by, requester_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["knowledgeCardId"] = from_union([from_str, from_none], self.knowledge_card_id)
        result["message"] = from_union([from_str, from_none], self.message)
        result["recipientId"] = from_union([from_str, from_none], self.recipient_id)
        result["requestedBy"] = from_union([lambda x: to_class(AuditStamp, x), from_none], self.requested_by)
        result["requesterId"] = from_union([from_str, from_none], self.requester_id)
        return result


@dataclass
class KnowledgeCardValidation:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    confirmation: Optional[ValidationConfirmation] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    knowledge_card_validation_id: Optional[str] = None
    latest: Optional[bool] = None
    request: Optional[ValidationRequest] = None

    @staticmethod
    def from_dict(obj: Any) -> 'KnowledgeCardValidation':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        confirmation = from_union([ValidationConfirmation.from_dict, from_none], obj.get("confirmation"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        knowledge_card_validation_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        request = from_union([ValidationRequest.from_dict, from_none], obj.get("request"))
        return KnowledgeCardValidation(id, aspect_type, confirmation, created_at, entity_id, knowledge_card_validation_id, latest, request)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["confirmation"] = from_union([lambda x: to_class(ValidationConfirmation, x), from_none], self.confirmation)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.knowledge_card_validation_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["request"] = from_union([lambda x: to_class(ValidationRequest, x), from_none], self.request)
        return result


@dataclass
class KnowledgeCardLogicalID:
    """Implemented in {@link KnowledgeCard} output type
    Definite assignment assertion is safe since it is defined in output subtype.
    This is due to unresolved TypeScript bug preventing this class from being defined as an
    abstract class, and
    then being used in a mixin {@see https://github.com/microsoft/TypeScript/issues/37142}
    """
    id: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'KnowledgeCardLogicalID':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("id"))
        return KnowledgeCardLogicalID(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_str, from_none], self.id)
        return result


@dataclass
class KnowledgeCard:
    """Backing store for an optionally provided creation date"""
    created_at: Optional[datetime] = None
    """A class representation of the BSON ObjectId type."""
    id: Optional[ObjectID] = None
    asset_contacts: Optional[AssetContacts] = None
    knowledge_card_created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    entity_type: Optional[EntityType] = None
    """A getter for the id property that's directly generated from the
    entity type & logical ID.
    """
    knowledge_card_id: Optional[str] = None
    knowledge_card_info: Optional[KnowledgeCardInfo] = None
    knowledge_card_validation: Optional[KnowledgeCardValidation] = None
    last_modified_at: Optional[datetime] = None
    """Implemented in {@link KnowledgeCard} output type
    Definite assignment assertion is safe since it is defined in output subtype.
    This is due to unresolved TypeScript bug preventing this class from being defined as an
    abstract class, and
    then being used in a mixin {@see https://github.com/microsoft/TypeScript/issues/37142}
    """
    logical_id: Optional[KnowledgeCardLogicalID] = None

    @staticmethod
    def from_dict(obj: Any) -> 'KnowledgeCard':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("_createdAt"))
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        asset_contacts = from_union([AssetContacts.from_dict, from_none], obj.get("assetContacts"))
        knowledge_card_created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deleted_at = from_union([from_datetime, from_none], obj.get("deletedAt"))
        entity_type = from_union([EntityType, from_none], obj.get("entityType"))
        knowledge_card_id = from_union([from_str, from_none], obj.get("id"))
        knowledge_card_info = from_union([KnowledgeCardInfo.from_dict, from_none], obj.get("knowledgeCardInfo"))
        knowledge_card_validation = from_union([KnowledgeCardValidation.from_dict, from_none], obj.get("knowledgeCardValidation"))
        last_modified_at = from_union([from_datetime, from_none], obj.get("lastModifiedAt"))
        logical_id = from_union([KnowledgeCardLogicalID.from_dict, from_none], obj.get("logicalId"))
        return KnowledgeCard(created_at, id, asset_contacts, knowledge_card_created_at, deleted_at, entity_type, knowledge_card_id, knowledge_card_info, knowledge_card_validation, last_modified_at, logical_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["assetContacts"] = from_union([lambda x: to_class(AssetContacts, x), from_none], self.asset_contacts)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.knowledge_card_created_at)
        result["deletedAt"] = from_union([lambda x: x.isoformat(), from_none], self.deleted_at)
        result["entityType"] = from_union([lambda x: to_enum(EntityType, x), from_none], self.entity_type)
        result["id"] = from_union([from_str, from_none], self.knowledge_card_id)
        result["knowledgeCardInfo"] = from_union([lambda x: to_class(KnowledgeCardInfo, x), from_none], self.knowledge_card_info)
        result["knowledgeCardValidation"] = from_union([lambda x: to_class(KnowledgeCardValidation, x), from_none], self.knowledge_card_validation)
        result["lastModifiedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_modified_at)
        result["logicalId"] = from_union([lambda x: to_class(KnowledgeCardLogicalID, x), from_none], self.logical_id)
        return result


@dataclass
class MetricFilter:
    field: Optional[str] = None
    operator: Optional[str] = None
    value: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MetricFilter':
        assert isinstance(obj, dict)
        field = from_union([from_str, from_none], obj.get("field"))
        operator = from_union([from_str, from_none], obj.get("operator"))
        value = from_union([from_str, from_none], obj.get("value"))
        return MetricFilter(field, operator, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["field"] = from_union([from_str, from_none], self.field)
        result["operator"] = from_union([from_str, from_none], self.operator)
        result["value"] = from_union([from_str, from_none], self.value)
        return result


@dataclass
class DbtMetric:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    description: Optional[str] = None
    dimensions: Optional[List[str]] = None
    entity_id: Optional[str] = None
    filters: Optional[List[MetricFilter]] = None
    dbt_metric_id: Optional[str] = None
    label: Optional[str] = None
    latest: Optional[bool] = None
    package_name: Optional[str] = None
    source_datasets: Optional[List[str]] = None
    source_models: Optional[List[str]] = None
    sql: Optional[str] = None
    tags: Optional[List[str]] = None
    time_grains: Optional[List[str]] = None
    timestamp: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DbtMetric':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        description = from_union([from_str, from_none], obj.get("description"))
        dimensions = from_union([lambda x: from_list(from_str, x), from_none], obj.get("dimensions"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        filters = from_union([lambda x: from_list(MetricFilter.from_dict, x), from_none], obj.get("filters"))
        dbt_metric_id = from_union([from_str, from_none], obj.get("id"))
        label = from_union([from_str, from_none], obj.get("label"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        package_name = from_union([from_str, from_none], obj.get("packageName"))
        source_datasets = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sourceDatasets"))
        source_models = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sourceModels"))
        sql = from_union([from_str, from_none], obj.get("sql"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        time_grains = from_union([lambda x: from_list(from_str, x), from_none], obj.get("timeGrains"))
        timestamp = from_union([from_str, from_none], obj.get("timestamp"))
        type = from_union([from_str, from_none], obj.get("type"))
        url = from_union([from_str, from_none], obj.get("url"))
        return DbtMetric(id, aspect_type, created_at, description, dimensions, entity_id, filters, dbt_metric_id, label, latest, package_name, source_datasets, source_models, sql, tags, time_grains, timestamp, type, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["description"] = from_union([from_str, from_none], self.description)
        result["dimensions"] = from_union([lambda x: from_list(from_str, x), from_none], self.dimensions)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["filters"] = from_union([lambda x: from_list(lambda x: to_class(MetricFilter, x), x), from_none], self.filters)
        result["id"] = from_union([from_str, from_none], self.dbt_metric_id)
        result["label"] = from_union([from_str, from_none], self.label)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["packageName"] = from_union([from_str, from_none], self.package_name)
        result["sourceDatasets"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_datasets)
        result["sourceModels"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_models)
        result["sql"] = from_union([from_str, from_none], self.sql)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        result["timeGrains"] = from_union([lambda x: from_list(from_str, x), from_none], self.time_grains)
        result["timestamp"] = from_union([from_str, from_none], self.timestamp)
        result["type"] = from_union([from_str, from_none], self.type)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


class MetricType(Enum):
    DBT_METRIC = "DBT_METRIC"
    UNKNOWN = "UNKNOWN"


@dataclass
class MetricLogicalID:
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    name: Optional[str] = None
    type: Optional[MetricType] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MetricLogicalID':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        type = from_union([MetricType, from_none], obj.get("type"))
        return MetricLogicalID(name, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["type"] = from_union([lambda x: to_enum(MetricType, x), from_none], self.type)
        return result


@dataclass
class Metric:
    """Backing store for an optionally provided creation date"""
    created_at: Optional[datetime] = None
    """A class representation of the BSON ObjectId type."""
    id: Optional[ObjectID] = None
    metric_created_at: Optional[datetime] = None
    dbt_metric: Optional[DbtMetric] = None
    deleted_at: Optional[datetime] = None
    entity_type: Optional[EntityType] = None
    """A getter for the id property that's directly generated from the
    entity type & logical ID.
    """
    metric_id: Optional[str] = None
    last_modified_at: Optional[datetime] = None
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    logical_id: Optional[MetricLogicalID] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Metric':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("_createdAt"))
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        metric_created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        dbt_metric = from_union([DbtMetric.from_dict, from_none], obj.get("dbtMetric"))
        deleted_at = from_union([from_datetime, from_none], obj.get("deletedAt"))
        entity_type = from_union([EntityType, from_none], obj.get("entityType"))
        metric_id = from_union([from_str, from_none], obj.get("id"))
        last_modified_at = from_union([from_datetime, from_none], obj.get("lastModifiedAt"))
        logical_id = from_union([MetricLogicalID.from_dict, from_none], obj.get("logicalId"))
        return Metric(created_at, id, metric_created_at, dbt_metric, deleted_at, entity_type, metric_id, last_modified_at, logical_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.metric_created_at)
        result["dbtMetric"] = from_union([lambda x: to_class(DbtMetric, x), from_none], self.dbt_metric)
        result["deletedAt"] = from_union([lambda x: x.isoformat(), from_none], self.deleted_at)
        result["entityType"] = from_union([lambda x: to_enum(EntityType, x), from_none], self.entity_type)
        result["id"] = from_union([from_str, from_none], self.metric_id)
        result["lastModifiedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_modified_at)
        result["logicalId"] = from_union([lambda x: to_class(MetricLogicalID, x), from_none], self.logical_id)
        return result


class Context(Enum):
    """Easily extract the type of a given object's values"""
    BUSINESS_TERMS = "BUSINESS_TERMS"
    DASHBOARDS = "dashboards"
    DATASETS = "datasets"
    DATA_DOCUMENT = "DATA_DOCUMENT"
    DBT_MODEL = "DBT_MODEL"
    KNOWLEDGE_CARDS = "knowledge_cards"
    LOOKER_EXPLORE = "LOOKER_EXPLORE"
    LOOKER_VIEW = "LOOKER_VIEW"
    PERSONS = "persons"
    POWER_BI_DATASET = "POWER_BI_DATASET"
    THOUGHT_SPOT_DATA_OBJECT = "THOUGHT_SPOT_DATA_OBJECT"


@dataclass
class SearchQuery:
    """Easily extract the type of a given object's values"""
    context: Optional[Context] = None
    keyword: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SearchQuery':
        assert isinstance(obj, dict)
        context = from_union([Context, from_none], obj.get("context"))
        keyword = from_union([from_str, from_none], obj.get("keyword"))
        return SearchQuery(context, keyword)

    def to_dict(self) -> dict:
        result: dict = {}
        result["context"] = from_union([lambda x: to_enum(Context, x), from_none], self.context)
        result["keyword"] = from_union([from_str, from_none], self.keyword)
        return result


@dataclass
class ViewedEntityHistory:
    date: Optional[datetime] = None
    entity_id: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ViewedEntityHistory':
        assert isinstance(obj, dict)
        date = from_union([from_datetime, from_none], obj.get("date"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        return ViewedEntityHistory(date, entity_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["date"] = from_union([lambda x: x.isoformat(), from_none], self.date)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        return result


@dataclass
class PersonActivity:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    person_activity_id: Optional[str] = None
    latest: Optional[bool] = None
    recently_viewed_history: Optional[List[ViewedEntityHistory]] = None
    recent_searches: Optional[List[SearchQuery]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonActivity':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        person_activity_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        recently_viewed_history = from_union([lambda x: from_list(ViewedEntityHistory.from_dict, x), from_none], obj.get("recentlyViewedHistory"))
        recent_searches = from_union([lambda x: from_list(SearchQuery.from_dict, x), from_none], obj.get("recentSearches"))
        return PersonActivity(id, aspect_type, created_at, entity_id, person_activity_id, latest, recently_viewed_history, recent_searches)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.person_activity_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["recentlyViewedHistory"] = from_union([lambda x: from_list(lambda x: to_class(ViewedEntityHistory, x), x), from_none], self.recently_viewed_history)
        result["recentSearches"] = from_union([lambda x: from_list(lambda x: to_class(SearchQuery, x), x), from_none], self.recent_searches)
        return result


@dataclass
class PersonLogicalID:
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    email: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonLogicalID':
        assert isinstance(obj, dict)
        email = from_union([from_str, from_none], obj.get("email"))
        return PersonLogicalID(email)

    def to_dict(self) -> dict:
        result: dict = {}
        result["email"] = from_union([from_str, from_none], self.email)
        return result


@dataclass
class GroupID:
    group_name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GroupID':
        assert isinstance(obj, dict)
        group_name = from_union([from_str, from_none], obj.get("groupName"))
        return GroupID(group_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["groupName"] = from_union([from_str, from_none], self.group_name)
        return result


@dataclass
class PersonOrganization:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    department: Optional[str] = None
    division: Optional[str] = None
    employee_number: Optional[str] = None
    entity_id: Optional[str] = None
    groups: Optional[List[GroupID]] = None
    person_organization_id: Optional[str] = None
    latest: Optional[bool] = None
    manager: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonOrganization':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        department = from_union([from_str, from_none], obj.get("department"))
        division = from_union([from_str, from_none], obj.get("division"))
        employee_number = from_union([from_str, from_none], obj.get("employeeNumber"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        groups = from_union([lambda x: from_list(GroupID.from_dict, x), from_none], obj.get("groups"))
        person_organization_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        manager = from_union([from_str, from_none], obj.get("manager"))
        name = from_union([from_str, from_none], obj.get("name"))
        title = from_union([from_str, from_none], obj.get("title"))
        return PersonOrganization(id, aspect_type, created_at, department, division, employee_number, entity_id, groups, person_organization_id, latest, manager, name, title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["department"] = from_union([from_str, from_none], self.department)
        result["division"] = from_union([from_str, from_none], self.division)
        result["employeeNumber"] = from_union([from_str, from_none], self.employee_number)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["groups"] = from_union([lambda x: from_list(lambda x: to_class(GroupID, x), x), from_none], self.groups)
        result["id"] = from_union([from_str, from_none], self.person_organization_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["manager"] = from_union([from_str, from_none], self.manager)
        result["name"] = from_union([from_str, from_none], self.name)
        result["title"] = from_union([from_str, from_none], self.title)
        return result


class Role(Enum):
    ADMIN = "ADMIN"
    CONTRIBUTOR = "CONTRIBUTOR"
    DATA_ADMIN = "DATA_ADMIN"


@dataclass
class PersonProperties:
    """Object / output type for PersonProperties aspect contains the full aspect fields
    
    Input type for PersonProperties aspect, contains just the common fields across input and
    output
    """
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None
    display_name: Optional[str] = None
    entity_id: Optional[str] = None
    first_name: Optional[str] = None
    full_name: Optional[str] = None
    person_properties_id: Optional[str] = None
    issuer: Optional[str] = None
    last_login: Optional[str] = None
    last_name: Optional[str] = None
    latest: Optional[bool] = None
    mobile_phone: Optional[str] = None
    occupation: Optional[str] = None
    primary_phone: Optional[str] = None
    provider_name: Optional[str] = None
    role: Optional[Role] = None
    status: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonProperties':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        avatar_url = from_union([from_str, from_none], obj.get("avatarUrl"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        display_name = from_union([from_str, from_none], obj.get("displayName"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        first_name = from_union([from_str, from_none], obj.get("firstName"))
        full_name = from_union([from_str, from_none], obj.get("fullName"))
        person_properties_id = from_union([from_str, from_none], obj.get("id"))
        issuer = from_union([from_str, from_none], obj.get("issuer"))
        last_login = from_union([from_str, from_none], obj.get("lastLogin"))
        last_name = from_union([from_str, from_none], obj.get("lastName"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        mobile_phone = from_union([from_str, from_none], obj.get("mobilePhone"))
        occupation = from_union([from_str, from_none], obj.get("occupation"))
        primary_phone = from_union([from_str, from_none], obj.get("primaryPhone"))
        provider_name = from_union([from_str, from_none], obj.get("providerName"))
        role = from_union([Role, from_none], obj.get("role"))
        status = from_union([from_str, from_none], obj.get("status"))
        return PersonProperties(id, aspect_type, avatar_url, created_at, display_name, entity_id, first_name, full_name, person_properties_id, issuer, last_login, last_name, latest, mobile_phone, occupation, primary_phone, provider_name, role, status)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["avatarUrl"] = from_union([from_str, from_none], self.avatar_url)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["displayName"] = from_union([from_str, from_none], self.display_name)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["firstName"] = from_union([from_str, from_none], self.first_name)
        result["fullName"] = from_union([from_str, from_none], self.full_name)
        result["id"] = from_union([from_str, from_none], self.person_properties_id)
        result["issuer"] = from_union([from_str, from_none], self.issuer)
        result["lastLogin"] = from_union([from_str, from_none], self.last_login)
        result["lastName"] = from_union([from_str, from_none], self.last_name)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["mobilePhone"] = from_union([from_str, from_none], self.mobile_phone)
        result["occupation"] = from_union([from_str, from_none], self.occupation)
        result["primaryPhone"] = from_union([from_str, from_none], self.primary_phone)
        result["providerName"] = from_union([from_str, from_none], self.provider_name)
        result["role"] = from_union([lambda x: to_enum(Role, x), from_none], self.role)
        result["status"] = from_union([from_str, from_none], self.status)
        return result


@dataclass
class PersonSlackProfile:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    deleted: Optional[bool] = None
    entity_id: Optional[str] = None
    person_slack_profile_id: Optional[str] = None
    latest: Optional[bool] = None
    slack_id: Optional[str] = None
    team_id: Optional[str] = None
    username: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PersonSlackProfile':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deleted = from_union([from_bool, from_none], obj.get("deleted"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        person_slack_profile_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        slack_id = from_union([from_str, from_none], obj.get("slackId"))
        team_id = from_union([from_str, from_none], obj.get("teamId"))
        username = from_union([from_str, from_none], obj.get("username"))
        return PersonSlackProfile(id, aspect_type, created_at, deleted, entity_id, person_slack_profile_id, latest, slack_id, team_id, username)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["deleted"] = from_union([from_bool, from_none], self.deleted)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.person_slack_profile_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["slackId"] = from_union([from_str, from_none], self.slack_id)
        result["teamId"] = from_union([from_str, from_none], self.team_id)
        result["username"] = from_union([from_str, from_none], self.username)
        return result


@dataclass
class Person:
    """A person entity represents any individual who is a member of the organization (or beyond)
    and can
    potentially have some relation to the other entities in our application
    """
    """Backing store for an optionally provided creation date"""
    created_at: Optional[datetime] = None
    """A class representation of the BSON ObjectId type."""
    id: Optional[ObjectID] = None
    activity: Optional[PersonActivity] = None
    person_created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    entity_type: Optional[EntityType] = None
    """A getter for the id property that's directly generated from the
    entity type & logical ID.
    """
    person_id: Optional[str] = None
    last_modified_at: Optional[datetime] = None
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    logical_id: Optional[PersonLogicalID] = None
    organization: Optional[PersonOrganization] = None
    properties: Optional[PersonProperties] = None
    slack_profile: Optional[PersonSlackProfile] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Person':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("_createdAt"))
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        activity = from_union([PersonActivity.from_dict, from_none], obj.get("activity"))
        person_created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        deleted_at = from_union([from_datetime, from_none], obj.get("deletedAt"))
        entity_type = from_union([EntityType, from_none], obj.get("entityType"))
        person_id = from_union([from_str, from_none], obj.get("id"))
        last_modified_at = from_union([from_datetime, from_none], obj.get("lastModifiedAt"))
        logical_id = from_union([PersonLogicalID.from_dict, from_none], obj.get("logicalId"))
        organization = from_union([PersonOrganization.from_dict, from_none], obj.get("organization"))
        properties = from_union([PersonProperties.from_dict, from_none], obj.get("properties"))
        slack_profile = from_union([PersonSlackProfile.from_dict, from_none], obj.get("slackProfile"))
        return Person(created_at, id, activity, person_created_at, deleted_at, entity_type, person_id, last_modified_at, logical_id, organization, properties, slack_profile)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["activity"] = from_union([lambda x: to_class(PersonActivity, x), from_none], self.activity)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.person_created_at)
        result["deletedAt"] = from_union([lambda x: x.isoformat(), from_none], self.deleted_at)
        result["entityType"] = from_union([lambda x: to_enum(EntityType, x), from_none], self.entity_type)
        result["id"] = from_union([from_str, from_none], self.person_id)
        result["lastModifiedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_modified_at)
        result["logicalId"] = from_union([lambda x: to_class(PersonLogicalID, x), from_none], self.logical_id)
        result["organization"] = from_union([lambda x: to_class(PersonOrganization, x), from_none], self.organization)
        result["properties"] = from_union([lambda x: to_class(PersonProperties, x), from_none], self.properties)
        result["slackProfile"] = from_union([lambda x: to_class(PersonSlackProfile, x), from_none], self.slack_profile)
        return result


@dataclass
class DbtMacroArgument:
    description: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DbtMacroArgument':
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        name = from_union([from_str, from_none], obj.get("name"))
        type = from_union([from_str, from_none], obj.get("type"))
        return DbtMacroArgument(description, name, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([from_str, from_none], self.description)
        result["name"] = from_union([from_str, from_none], self.name)
        result["type"] = from_union([from_str, from_none], self.type)
        return result


@dataclass
class DbtMacro:
    arguments: Optional[List[DbtMacroArgument]] = None
    depends_on_macros: Optional[List[str]] = None
    description: Optional[str] = None
    name: Optional[str] = None
    package_name: Optional[str] = None
    sql: Optional[str] = None
    unique_id: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DbtMacro':
        assert isinstance(obj, dict)
        arguments = from_union([lambda x: from_list(DbtMacroArgument.from_dict, x), from_none], obj.get("arguments"))
        depends_on_macros = from_union([lambda x: from_list(from_str, x), from_none], obj.get("dependsOnMacros"))
        description = from_union([from_str, from_none], obj.get("description"))
        name = from_union([from_str, from_none], obj.get("name"))
        package_name = from_union([from_str, from_none], obj.get("packageName"))
        sql = from_union([from_str, from_none], obj.get("sql"))
        unique_id = from_union([from_str, from_none], obj.get("uniqueId"))
        return DbtMacro(arguments, depends_on_macros, description, name, package_name, sql, unique_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["arguments"] = from_union([lambda x: from_list(lambda x: to_class(DbtMacroArgument, x), x), from_none], self.arguments)
        result["dependsOnMacros"] = from_union([lambda x: from_list(from_str, x), from_none], self.depends_on_macros)
        result["description"] = from_union([from_str, from_none], self.description)
        result["name"] = from_union([from_str, from_none], self.name)
        result["packageName"] = from_union([from_str, from_none], self.package_name)
        result["sql"] = from_union([from_str, from_none], self.sql)
        result["uniqueId"] = from_union([from_str, from_none], self.unique_id)
        return result


class DbtMaterializationType(Enum):
    EPHEMERAL = "EPHEMERAL"
    INCREMENTAL = "INCREMENTAL"
    OTHER = "OTHER"
    TABLE = "TABLE"
    VIEW = "VIEW"


@dataclass
class DbtMaterialization:
    target_dataset: Optional[str] = None
    type: Optional[DbtMaterializationType] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DbtMaterialization':
        assert isinstance(obj, dict)
        target_dataset = from_union([from_str, from_none], obj.get("targetDataset"))
        type = from_union([DbtMaterializationType, from_none], obj.get("type"))
        return DbtMaterialization(target_dataset, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["targetDataset"] = from_union([from_str, from_none], self.target_dataset)
        result["type"] = from_union([lambda x: to_enum(DbtMaterializationType, x), from_none], self.type)
        return result


@dataclass
class DbtTest:
    columns: Optional[List[str]] = None
    depends_on_macros: Optional[List[str]] = None
    name: Optional[str] = None
    sql: Optional[str] = None
    unique_id: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DbtTest':
        assert isinstance(obj, dict)
        columns = from_union([lambda x: from_list(from_str, x), from_none], obj.get("columns"))
        depends_on_macros = from_union([lambda x: from_list(from_str, x), from_none], obj.get("dependsOnMacros"))
        name = from_union([from_str, from_none], obj.get("name"))
        sql = from_union([from_str, from_none], obj.get("sql"))
        unique_id = from_union([from_str, from_none], obj.get("uniqueId"))
        return DbtTest(columns, depends_on_macros, name, sql, unique_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["columns"] = from_union([lambda x: from_list(from_str, x), from_none], self.columns)
        result["dependsOnMacros"] = from_union([lambda x: from_list(from_str, x), from_none], self.depends_on_macros)
        result["name"] = from_union([from_str, from_none], self.name)
        result["sql"] = from_union([from_str, from_none], self.sql)
        result["uniqueId"] = from_union([from_str, from_none], self.unique_id)
        return result


@dataclass
class DbtModel:
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    compiled_sql: Optional[str] = None
    created_at: Optional[datetime] = None
    description: Optional[str] = None
    docs_url: Optional[str] = None
    entity_id: Optional[str] = None
    fields: Optional[List[SchemaField]] = None
    dbt_model_id: Optional[str] = None
    latest: Optional[bool] = None
    macros: Optional[List[DbtMacro]] = None
    materialization: Optional[DbtMaterialization] = None
    owners: Optional[List[str]] = None
    package_name: Optional[str] = None
    raw_sql: Optional[str] = None
    source_datasets: Optional[List[str]] = None
    source_models: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    tests: Optional[List[DbtTest]] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DbtModel':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        compiled_sql = from_union([from_str, from_none], obj.get("compiledSql"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        description = from_union([from_str, from_none], obj.get("description"))
        docs_url = from_union([from_str, from_none], obj.get("docsUrl"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        fields = from_union([lambda x: from_list(SchemaField.from_dict, x), from_none], obj.get("fields"))
        dbt_model_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        macros = from_union([lambda x: from_list(DbtMacro.from_dict, x), from_none], obj.get("macros"))
        materialization = from_union([DbtMaterialization.from_dict, from_none], obj.get("materialization"))
        owners = from_union([lambda x: from_list(from_str, x), from_none], obj.get("owners"))
        package_name = from_union([from_str, from_none], obj.get("packageName"))
        raw_sql = from_union([from_str, from_none], obj.get("rawSql"))
        source_datasets = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sourceDatasets"))
        source_models = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sourceModels"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        tests = from_union([lambda x: from_list(DbtTest.from_dict, x), from_none], obj.get("tests"))
        url = from_union([from_str, from_none], obj.get("url"))
        return DbtModel(id, aspect_type, compiled_sql, created_at, description, docs_url, entity_id, fields, dbt_model_id, latest, macros, materialization, owners, package_name, raw_sql, source_datasets, source_models, tags, tests, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["compiledSql"] = from_union([from_str, from_none], self.compiled_sql)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["description"] = from_union([from_str, from_none], self.description)
        result["docsUrl"] = from_union([from_str, from_none], self.docs_url)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["fields"] = from_union([lambda x: from_list(lambda x: to_class(SchemaField, x), x), from_none], self.fields)
        result["id"] = from_union([from_str, from_none], self.dbt_model_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["macros"] = from_union([lambda x: from_list(lambda x: to_class(DbtMacro, x), x), from_none], self.macros)
        result["materialization"] = from_union([lambda x: to_class(DbtMaterialization, x), from_none], self.materialization)
        result["owners"] = from_union([lambda x: from_list(from_str, x), from_none], self.owners)
        result["packageName"] = from_union([from_str, from_none], self.package_name)
        result["rawSql"] = from_union([from_str, from_none], self.raw_sql)
        result["sourceDatasets"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_datasets)
        result["sourceModels"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_models)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        result["tests"] = from_union([lambda x: from_list(lambda x: to_class(DbtTest, x), x), from_none], self.tests)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


class VirtualViewType(Enum):
    DBT_MODEL = "DBT_MODEL"
    LOOKER_EXPLORE = "LOOKER_EXPLORE"
    LOOKER_VIEW = "LOOKER_VIEW"
    POWER_BI_DATASET = "POWER_BI_DATASET"
    THOUGHT_SPOT_DATA_OBJECT = "THOUGHT_SPOT_DATA_OBJECT"
    UNKNOWN = "UNKNOWN"


@dataclass
class VirtualViewLogicalID:
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    directory: Optional[str] = None
    name: Optional[str] = None
    type: Optional[VirtualViewType] = None

    @staticmethod
    def from_dict(obj: Any) -> 'VirtualViewLogicalID':
        assert isinstance(obj, dict)
        directory = from_union([from_str, from_none], obj.get("directory"))
        name = from_union([from_str, from_none], obj.get("name"))
        type = from_union([VirtualViewType, from_none], obj.get("type"))
        return VirtualViewLogicalID(directory, name, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["directory"] = from_union([from_str, from_none], self.directory)
        result["name"] = from_union([from_str, from_none], self.name)
        result["type"] = from_union([lambda x: to_enum(VirtualViewType, x), from_none], self.type)
        return result


@dataclass
class LookerExploreFilter:
    allowed_values: Optional[str] = None
    field: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LookerExploreFilter':
        assert isinstance(obj, dict)
        allowed_values = from_union([from_str, from_none], obj.get("allowedValues"))
        field = from_union([from_str, from_none], obj.get("field"))
        return LookerExploreFilter(allowed_values, field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["allowedValues"] = from_union([from_str, from_none], self.allowed_values)
        result["field"] = from_union([from_str, from_none], self.field)
        return result


@dataclass
class LookerExploreJoin:
    fields: Optional[List[str]] = None
    on_clause: Optional[str] = None
    relationship: Optional[str] = None
    type: Optional[str] = None
    """The Looker View that is joined in the Explore"""
    view: Optional[str] = None
    where_clause: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LookerExploreJoin':
        assert isinstance(obj, dict)
        fields = from_union([lambda x: from_list(from_str, x), from_none], obj.get("fields"))
        on_clause = from_union([from_str, from_none], obj.get("onClause"))
        relationship = from_union([from_str, from_none], obj.get("relationship"))
        type = from_union([from_str, from_none], obj.get("type"))
        view = from_union([from_str, from_none], obj.get("view"))
        where_clause = from_union([from_str, from_none], obj.get("whereClause"))
        return LookerExploreJoin(fields, on_clause, relationship, type, view, where_clause)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fields"] = from_union([lambda x: from_list(from_str, x), from_none], self.fields)
        result["onClause"] = from_union([from_str, from_none], self.on_clause)
        result["relationship"] = from_union([from_str, from_none], self.relationship)
        result["type"] = from_union([from_str, from_none], self.type)
        result["view"] = from_union([from_str, from_none], self.view)
        result["whereClause"] = from_union([from_str, from_none], self.where_clause)
        return result


@dataclass
class LookerExplore:
    """Captures information of a Looker Explore,
    https://docs.looker.com/reference/explore-reference
    """
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    """The Looker View which the Explore is based on"""
    base_view: Optional[str] = None
    created_at: Optional[datetime] = None
    description: Optional[str] = None
    entity_id: Optional[str] = None
    extends: Optional[List[str]] = None
    fields: Optional[List[str]] = None
    filters: Optional[List[LookerExploreFilter]] = None
    looker_explore_id: Optional[str] = None
    joins: Optional[List[LookerExploreJoin]] = None
    label: Optional[str] = None
    latest: Optional[bool] = None
    model_name: Optional[str] = None
    tags: Optional[List[str]] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LookerExplore':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        base_view = from_union([from_str, from_none], obj.get("baseView"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        description = from_union([from_str, from_none], obj.get("description"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        extends = from_union([lambda x: from_list(from_str, x), from_none], obj.get("extends"))
        fields = from_union([lambda x: from_list(from_str, x), from_none], obj.get("fields"))
        filters = from_union([lambda x: from_list(LookerExploreFilter.from_dict, x), from_none], obj.get("filters"))
        looker_explore_id = from_union([from_str, from_none], obj.get("id"))
        joins = from_union([lambda x: from_list(LookerExploreJoin.from_dict, x), from_none], obj.get("joins"))
        label = from_union([from_str, from_none], obj.get("label"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        model_name = from_union([from_str, from_none], obj.get("modelName"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        url = from_union([from_str, from_none], obj.get("url"))
        return LookerExplore(id, aspect_type, base_view, created_at, description, entity_id, extends, fields, filters, looker_explore_id, joins, label, latest, model_name, tags, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["baseView"] = from_union([from_str, from_none], self.base_view)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["description"] = from_union([from_str, from_none], self.description)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["extends"] = from_union([lambda x: from_list(from_str, x), from_none], self.extends)
        result["fields"] = from_union([lambda x: from_list(from_str, x), from_none], self.fields)
        result["filters"] = from_union([lambda x: from_list(lambda x: to_class(LookerExploreFilter, x), x), from_none], self.filters)
        result["id"] = from_union([from_str, from_none], self.looker_explore_id)
        result["joins"] = from_union([lambda x: from_list(lambda x: to_class(LookerExploreJoin, x), x), from_none], self.joins)
        result["label"] = from_union([from_str, from_none], self.label)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["modelName"] = from_union([from_str, from_none], self.model_name)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class LookerViewDimension:
    data_type: Optional[str] = None
    field: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LookerViewDimension':
        assert isinstance(obj, dict)
        data_type = from_union([from_str, from_none], obj.get("dataType"))
        field = from_union([from_str, from_none], obj.get("field"))
        return LookerViewDimension(data_type, field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dataType"] = from_union([from_str, from_none], self.data_type)
        result["field"] = from_union([from_str, from_none], self.field)
        return result


@dataclass
class LookerViewFilter:
    field: Optional[str] = None
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LookerViewFilter':
        assert isinstance(obj, dict)
        field = from_union([from_str, from_none], obj.get("field"))
        type = from_union([from_str, from_none], obj.get("type"))
        return LookerViewFilter(field, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["field"] = from_union([from_str, from_none], self.field)
        result["type"] = from_union([from_str, from_none], self.type)
        return result


@dataclass
class LookerViewMeasure:
    field: Optional[str] = None
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LookerViewMeasure':
        assert isinstance(obj, dict)
        field = from_union([from_str, from_none], obj.get("field"))
        type = from_union([from_str, from_none], obj.get("type"))
        return LookerViewMeasure(field, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["field"] = from_union([from_str, from_none], self.field)
        result["type"] = from_union([from_str, from_none], self.type)
        return result


@dataclass
class LookerView:
    """Captures information of a Looker View, https://docs.looker.com/reference/view-reference"""
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    dimensions: Optional[List[LookerViewDimension]] = None
    entity_id: Optional[str] = None
    extends: Optional[List[str]] = None
    filters: Optional[List[LookerViewFilter]] = None
    looker_view_id: Optional[str] = None
    label: Optional[str] = None
    latest: Optional[bool] = None
    measures: Optional[List[LookerViewMeasure]] = None
    source_datasets: Optional[List[str]] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LookerView':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        dimensions = from_union([lambda x: from_list(LookerViewDimension.from_dict, x), from_none], obj.get("dimensions"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        extends = from_union([lambda x: from_list(from_str, x), from_none], obj.get("extends"))
        filters = from_union([lambda x: from_list(LookerViewFilter.from_dict, x), from_none], obj.get("filters"))
        looker_view_id = from_union([from_str, from_none], obj.get("id"))
        label = from_union([from_str, from_none], obj.get("label"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        measures = from_union([lambda x: from_list(LookerViewMeasure.from_dict, x), from_none], obj.get("measures"))
        source_datasets = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sourceDatasets"))
        url = from_union([from_str, from_none], obj.get("url"))
        return LookerView(id, aspect_type, created_at, dimensions, entity_id, extends, filters, looker_view_id, label, latest, measures, source_datasets, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["dimensions"] = from_union([lambda x: from_list(lambda x: to_class(LookerViewDimension, x), x), from_none], self.dimensions)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["extends"] = from_union([lambda x: from_list(from_str, x), from_none], self.extends)
        result["filters"] = from_union([lambda x: from_list(lambda x: to_class(LookerViewFilter, x), x), from_none], self.filters)
        result["id"] = from_union([from_str, from_none], self.looker_view_id)
        result["label"] = from_union([from_str, from_none], self.label)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["measures"] = from_union([lambda x: from_list(lambda x: to_class(LookerViewMeasure, x), x), from_none], self.measures)
        result["sourceDatasets"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_datasets)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class PowerBIColumn:
    """Captures column name of a dataset table,
    https://docs.microsoft.com/en-us/rest/api/power-bi/admin/workspace-info-get-scan-result#column
    """
    field: Optional[str] = None
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PowerBIColumn':
        assert isinstance(obj, dict)
        field = from_union([from_str, from_none], obj.get("field"))
        type = from_union([from_str, from_none], obj.get("type"))
        return PowerBIColumn(field, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["field"] = from_union([from_str, from_none], self.field)
        result["type"] = from_union([from_str, from_none], self.type)
        return result


@dataclass
class PowerBIMeasure:
    """Captures Power BI measure of a dataset table,
    https://docs.microsoft.com/en-us/rest/api/power-bi/admin/workspace-info-get-scan-result#measure
    """
    expression: Optional[str] = None
    field: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PowerBIMeasure':
        assert isinstance(obj, dict)
        expression = from_union([from_str, from_none], obj.get("expression"))
        field = from_union([from_str, from_none], obj.get("field"))
        return PowerBIMeasure(expression, field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["expression"] = from_union([from_str, from_none], self.expression)
        result["field"] = from_union([from_str, from_none], self.field)
        return result


@dataclass
class PowerBIDatasetTable:
    """Captures dataset table information of a Power BI Dataset,
    https://docs.microsoft.com/en-us/rest/api/power-bi/admin/workspace-info-get-scan-result#table
    """
    columns: Optional[List[PowerBIColumn]] = None
    measures: Optional[List[PowerBIMeasure]] = None
    name: Optional[str] = None
    sources: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PowerBIDatasetTable':
        assert isinstance(obj, dict)
        columns = from_union([lambda x: from_list(PowerBIColumn.from_dict, x), from_none], obj.get("columns"))
        measures = from_union([lambda x: from_list(PowerBIMeasure.from_dict, x), from_none], obj.get("measures"))
        name = from_union([from_str, from_none], obj.get("name"))
        sources = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sources"))
        return PowerBIDatasetTable(columns, measures, name, sources)

    def to_dict(self) -> dict:
        result: dict = {}
        result["columns"] = from_union([lambda x: from_list(lambda x: to_class(PowerBIColumn, x), x), from_none], self.columns)
        result["measures"] = from_union([lambda x: from_list(lambda x: to_class(PowerBIMeasure, x), x), from_none], self.measures)
        result["name"] = from_union([from_str, from_none], self.name)
        result["sources"] = from_union([lambda x: from_list(from_str, x), from_none], self.sources)
        return result


@dataclass
class PowerBIDataset:
    """Captures information of a Power BI Dataset using admin API,
    https://docs.microsoft.com/en-us/rest/api/power-bi/admin/workspace-info-get-scan-result#workspaceinfodataset
    """
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    created_at: Optional[datetime] = None
    description: Optional[str] = None
    entity_id: Optional[str] = None
    power_bi_dataset_id: Optional[str] = None
    latest: Optional[bool] = None
    name: Optional[str] = None
    source_datasets: Optional[List[str]] = None
    tables: Optional[List[PowerBIDatasetTable]] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PowerBIDataset':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        description = from_union([from_str, from_none], obj.get("description"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        power_bi_dataset_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        name = from_union([from_str, from_none], obj.get("name"))
        source_datasets = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sourceDatasets"))
        tables = from_union([lambda x: from_list(PowerBIDatasetTable.from_dict, x), from_none], obj.get("tables"))
        url = from_union([from_str, from_none], obj.get("url"))
        return PowerBIDataset(id, aspect_type, created_at, description, entity_id, power_bi_dataset_id, latest, name, source_datasets, tables, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["description"] = from_union([from_str, from_none], self.description)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.power_bi_dataset_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["name"] = from_union([from_str, from_none], self.name)
        result["sourceDatasets"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_datasets)
        result["tables"] = from_union([lambda x: from_list(lambda x: to_class(PowerBIDatasetTable, x), x), from_none], self.tables)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class ThoughtSpotColumn:
    description: Optional[str] = None
    field: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ThoughtSpotColumn':
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        field = from_union([from_str, from_none], obj.get("field"))
        name = from_union([from_str, from_none], obj.get("name"))
        type = from_union([from_str, from_none], obj.get("type"))
        return ThoughtSpotColumn(description, field, name, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([from_str, from_none], self.description)
        result["field"] = from_union([from_str, from_none], self.field)
        result["name"] = from_union([from_str, from_none], self.name)
        result["type"] = from_union([from_str, from_none], self.type)
        return result


class ThoughtSpotDataObjectType(Enum):
    TABLE = "TABLE"
    UNKNOWN = "UNKNOWN"
    VIEW = "VIEW"
    WORKSHEET = "WORKSHEET"


@dataclass
class ThoughtSpotDataObject:
    """Modeling ThoughtSpot DataSource or DataObject in the API into a virtual view.
    DataSource: https://docs.thoughtspot.com/software/latest/data-sources
    """
    id: Optional[ObjectID] = None
    aspect_type: Optional[AspectType] = None
    columns: Optional[List[ThoughtSpotColumn]] = None
    created_at: Optional[datetime] = None
    description: Optional[str] = None
    entity_id: Optional[str] = None
    thought_spot_data_object_id: Optional[str] = None
    latest: Optional[bool] = None
    name: Optional[str] = None
    source_datasets: Optional[List[str]] = None
    source_virtual_views: Optional[List[str]] = None
    type: Optional[ThoughtSpotDataObjectType] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ThoughtSpotDataObject':
        assert isinstance(obj, dict)
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        aspect_type = from_union([AspectType, from_none], obj.get("aspectType"))
        columns = from_union([lambda x: from_list(ThoughtSpotColumn.from_dict, x), from_none], obj.get("columns"))
        created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        description = from_union([from_str, from_none], obj.get("description"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        thought_spot_data_object_id = from_union([from_str, from_none], obj.get("id"))
        latest = from_union([from_bool, from_none], obj.get("latest"))
        name = from_union([from_str, from_none], obj.get("name"))
        source_datasets = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sourceDatasets"))
        source_virtual_views = from_union([lambda x: from_list(from_str, x), from_none], obj.get("sourceVirtualViews"))
        type = from_union([ThoughtSpotDataObjectType, from_none], obj.get("type"))
        url = from_union([from_str, from_none], obj.get("url"))
        return ThoughtSpotDataObject(id, aspect_type, columns, created_at, description, entity_id, thought_spot_data_object_id, latest, name, source_datasets, source_virtual_views, type, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["aspectType"] = from_union([lambda x: to_enum(AspectType, x), from_none], self.aspect_type)
        result["columns"] = from_union([lambda x: from_list(lambda x: to_class(ThoughtSpotColumn, x), x), from_none], self.columns)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["description"] = from_union([from_str, from_none], self.description)
        result["entityId"] = from_union([from_str, from_none], self.entity_id)
        result["id"] = from_union([from_str, from_none], self.thought_spot_data_object_id)
        result["latest"] = from_union([from_bool, from_none], self.latest)
        result["name"] = from_union([from_str, from_none], self.name)
        result["sourceDatasets"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_datasets)
        result["sourceVirtualViews"] = from_union([lambda x: from_list(from_str, x), from_none], self.source_virtual_views)
        result["type"] = from_union([lambda x: to_enum(ThoughtSpotDataObjectType, x), from_none], self.type)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class VirtualView:
    """Backing store for an optionally provided creation date"""
    created_at: Optional[datetime] = None
    """A class representation of the BSON ObjectId type."""
    id: Optional[ObjectID] = None
    virtual_view_created_at: Optional[datetime] = None
    dbt_model: Optional[DbtModel] = None
    deleted_at: Optional[datetime] = None
    entity_type: Optional[EntityType] = None
    """A getter for the id property that's directly generated from the
    entity type & logical ID.
    """
    virtual_view_id: Optional[str] = None
    last_modified_at: Optional[datetime] = None
    """Identify an entity "logically".
    Each entity must have a logicalId to be ingested.
    A compelling use-case is that this allows a producer to create an
    instance of the Entity without requiring an entity ID to be
    obtained prior to instantiation, potentially resulting in two round-trips
    """
    logical_id: Optional[VirtualViewLogicalID] = None
    """Captures information of a Looker Explore,
    https://docs.looker.com/reference/explore-reference
    """
    looker_explore: Optional[LookerExplore] = None
    """Captures information of a Looker View, https://docs.looker.com/reference/view-reference"""
    looker_view: Optional[LookerView] = None
    """Captures information of a Power BI Dataset using admin API,
    https://docs.microsoft.com/en-us/rest/api/power-bi/admin/workspace-info-get-scan-result#workspaceinfodataset
    """
    power_bi_dataset: Optional[PowerBIDataset] = None
    """Modeling ThoughtSpot DataSource or DataObject in the API into a virtual view.
    DataSource: https://docs.thoughtspot.com/software/latest/data-sources
    """
    thought_spot: Optional[ThoughtSpotDataObject] = None

    @staticmethod
    def from_dict(obj: Any) -> 'VirtualView':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("_createdAt"))
        id = from_union([ObjectID.from_dict, from_none], obj.get("_id"))
        virtual_view_created_at = from_union([from_datetime, from_none], obj.get("createdAt"))
        dbt_model = from_union([DbtModel.from_dict, from_none], obj.get("dbtModel"))
        deleted_at = from_union([from_datetime, from_none], obj.get("deletedAt"))
        entity_type = from_union([EntityType, from_none], obj.get("entityType"))
        virtual_view_id = from_union([from_str, from_none], obj.get("id"))
        last_modified_at = from_union([from_datetime, from_none], obj.get("lastModifiedAt"))
        logical_id = from_union([VirtualViewLogicalID.from_dict, from_none], obj.get("logicalId"))
        looker_explore = from_union([LookerExplore.from_dict, from_none], obj.get("lookerExplore"))
        looker_view = from_union([LookerView.from_dict, from_none], obj.get("lookerView"))
        power_bi_dataset = from_union([PowerBIDataset.from_dict, from_none], obj.get("powerBIDataset"))
        thought_spot = from_union([ThoughtSpotDataObject.from_dict, from_none], obj.get("thoughtSpot"))
        return VirtualView(created_at, id, virtual_view_created_at, dbt_model, deleted_at, entity_type, virtual_view_id, last_modified_at, logical_id, looker_explore, looker_view, power_bi_dataset, thought_spot)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        result["_id"] = from_union([lambda x: to_class(ObjectID, x), from_none], self.id)
        result["createdAt"] = from_union([lambda x: x.isoformat(), from_none], self.virtual_view_created_at)
        result["dbtModel"] = from_union([lambda x: to_class(DbtModel, x), from_none], self.dbt_model)
        result["deletedAt"] = from_union([lambda x: x.isoformat(), from_none], self.deleted_at)
        result["entityType"] = from_union([lambda x: to_enum(EntityType, x), from_none], self.entity_type)
        result["id"] = from_union([from_str, from_none], self.virtual_view_id)
        result["lastModifiedAt"] = from_union([lambda x: x.isoformat(), from_none], self.last_modified_at)
        result["logicalId"] = from_union([lambda x: to_class(VirtualViewLogicalID, x), from_none], self.logical_id)
        result["lookerExplore"] = from_union([lambda x: to_class(LookerExplore, x), from_none], self.looker_explore)
        result["lookerView"] = from_union([lambda x: to_class(LookerView, x), from_none], self.looker_view)
        result["powerBIDataset"] = from_union([lambda x: to_class(PowerBIDataset, x), from_none], self.power_bi_dataset)
        result["thoughtSpot"] = from_union([lambda x: to_class(ThoughtSpotDataObject, x), from_none], self.thought_spot)
        return result


@dataclass
class MetadataChangeEvent:
    dashboard: Optional[Dashboard] = None
    dataset: Optional[Dataset] = None
    event_header: Optional[EventHeader] = None
    knowledge_card: Optional[KnowledgeCard] = None
    metric: Optional[Metric] = None
    """A person entity represents any individual who is a member of the organization (or beyond)
    and can
    potentially have some relation to the other entities in our application
    """
    person: Optional[Person] = None
    virtual_view: Optional[VirtualView] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MetadataChangeEvent':
        assert isinstance(obj, dict)
        dashboard = from_union([Dashboard.from_dict, from_none], obj.get("dashboard"))
        dataset = from_union([Dataset.from_dict, from_none], obj.get("dataset"))
        event_header = from_union([EventHeader.from_dict, from_none], obj.get("eventHeader"))
        knowledge_card = from_union([KnowledgeCard.from_dict, from_none], obj.get("knowledgeCard"))
        metric = from_union([Metric.from_dict, from_none], obj.get("metric"))
        person = from_union([Person.from_dict, from_none], obj.get("person"))
        virtual_view = from_union([VirtualView.from_dict, from_none], obj.get("virtualView"))
        return MetadataChangeEvent(dashboard, dataset, event_header, knowledge_card, metric, person, virtual_view)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dashboard"] = from_union([lambda x: to_class(Dashboard, x), from_none], self.dashboard)
        result["dataset"] = from_union([lambda x: to_class(Dataset, x), from_none], self.dataset)
        result["eventHeader"] = from_union([lambda x: to_class(EventHeader, x), from_none], self.event_header)
        result["knowledgeCard"] = from_union([lambda x: to_class(KnowledgeCard, x), from_none], self.knowledge_card)
        result["metric"] = from_union([lambda x: to_class(Metric, x), from_none], self.metric)
        result["person"] = from_union([lambda x: to_class(Person, x), from_none], self.person)
        result["virtualView"] = from_union([lambda x: to_class(VirtualView, x), from_none], self.virtual_view)
        return result


def metadata_change_event_from_dict(s: Any) -> MetadataChangeEvent:
    return MetadataChangeEvent.from_dict(s)


def metadata_change_event_to_dict(x: MetadataChangeEvent) -> Any:
    return to_class(MetadataChangeEvent, x)
