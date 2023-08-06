"""
Kelvin API Client.
"""

from __future__ import annotations

from functools import wraps
from types import FunctionType, MethodType
from typing import Any, Generic, List, Mapping, Type, TypeVar

from .base_client import BaseClient
from .data_model import DataModel
from .model import responses

MODELS: Mapping[str, Type[DataModel]] = {
    "acp": responses.ACP,  # type: ignore
    "acp_edge_app_version": responses.ACPEdgeAppVersion,  # type: ignore
    "acp_item": responses.ACPItem,  # type: ignore
    "acp_meta_data_item": responses.ACPMetaDataItem,  # type: ignore
    "acp_metadata": responses.ACPMetadata,  # type: ignore
    "acp_status": responses.ACPStatus,  # type: ignore
    "acp_status_count": responses.ACPStatusCount,  # type: ignore
    "acp_telemetry": responses.ACPTelemetry,  # type: ignore
    "acp_workload_manifests": responses.ACPWorkloadManifests,  # type: ignore
    "alarm": responses.Alarm,  # type: ignore
    "alarm_assets_statistics": responses.AlarmAssetsStatistics,  # type: ignore
    "alarm_class": responses.AlarmClass,  # type: ignore
    "alarm_filter": responses.AlarmFilter,  # type: ignore
    "alarm_statistics": responses.AlarmStatistics,  # type: ignore
    "alarm_type": responses.AlarmType,  # type: ignore
    "app": responses.App,  # type: ignore
    "app_version": responses.AppVersion,  # type: ignore
    "asset": responses.Asset,  # type: ignore
    "asset_class": responses.AssetClass,  # type: ignore
    "asset_hierarchies": responses.AssetHierarchies,  # type: ignore
    "asset_hierarchy_list": responses.AssetHierarchyList,  # type: ignore
    "asset_item": responses.AssetItem,  # type: ignore
    "asset_oee": responses.AssetOEE,  # type: ignore
    "asset_shift": responses.AssetShift,  # type: ignore
    "asset_statistics_item": responses.AssetStatisticsItem,  # type: ignore
    "asset_status": responses.AssetStatus,  # type: ignore
    "asset_status_count": responses.AssetStatusCount,  # type: ignore
    "asset_template": responses.AssetTemplate,  # type: ignore
    "asset_type": responses.AssetType,  # type: ignore
    "asset_type_metadata": responses.AssetTypeMetadata,  # type: ignore
    "audit_logger": responses.AuditLogger,  # type: ignore
    "bridge": responses.Bridge,  # type: ignore
    "bridge_data_stream_item": responses.BridgeDataStreamItem,  # type: ignore
    "cluster": responses.Cluster,  # type: ignore
    "cluster_cidr_item": responses.ClusterCIDRItem,  # type: ignore
    "cluster_manifest_list": responses.ClusterManifestList,  # type: ignore
    "control_change": responses.ControlChange,  # type: ignore
    "data_label": responses.DataLabel,  # type: ignore
    "data_label_cluster": responses.DataLabelCluster,  # type: ignore
    "data_type": responses.DataType,  # type: ignore
    "data_type_schema": responses.DataTypeSchema,  # type: ignore
    "failure_class": responses.FailureClass,  # type: ignore
    "failure_event_item": responses.FailureEventItem,  # type: ignore
    "failure_list": responses.FailureList,  # type: ignore
    "instance_health_status": responses.InstanceHealthStatus,  # type: ignore
    "instance_setting_item": responses.InstanceSettingItem,  # type: ignore
    "integration": responses.Integration,  # type: ignore
    "integration_aws_region": responses.IntegrationAwsRegion,  # type: ignore
    "integration_aws_region_list": responses.IntegrationAwsRegionList,  # type: ignore
    "integration_list": responses.IntegrationList,  # type: ignore
    "label": responses.Label,  # type: ignore
    "label_metadata": responses.LabelMetadata,  # type: ignore
    "mqtt_topic_list": responses.MQTTTopicList,  # type: ignore
    "map_item": responses.MapItem,  # type: ignore
    "map_model": responses.MapModel,  # type: ignore
    "map_version_item": responses.MapVersionItem,  # type: ignore
    "metric": responses.Metric,  # type: ignore
    "orchestration_provision": responses.OrchestrationProvision,  # type: ignore
    "secret": responses.Secret,  # type: ignore
    "semantic_type_list": responses.SemanticTypeList,  # type: ignore
    "site_hierarchy_overview_item": responses.SiteHierarchyOverviewItem,  # type: ignore
    "storage": responses.Storage,  # type: ignore
    "symbol": responses.Symbol,  # type: ignore
    "thread": responses.Thread,  # type: ignore
    "user": responses.User,  # type: ignore
    "user_setting_item": responses.UserSettingItem,  # type: ignore
    "user_with_permissions": responses.UserWithPermissions,  # type: ignore
    "wireguard_peer": responses.WireguardPeer,  # type: ignore
    "wireguard_tunnel": responses.WireguardTunnel,  # type: ignore
    "workload": responses.Workload,  # type: ignore
    "workload_logs": responses.WorkloadLogs,  # type: ignore
    "workload_telemetry": responses.WorkloadTelemetry,  # type: ignore
}


T = TypeVar("T", bound=DataModel)


class DataModelProxy(Generic[T]):
    """Proxy client to data models."""

    def __init__(self, model: Type[T], client: Client) -> None:
        """Initialise resource adaptor."""

        self._model = model
        self._client = client

    def new(self, **kwargs: Any) -> T:
        """New instance."""

        return self._model(self._client, **kwargs)

    def __getattr__(self, name: str) -> Any:
        """Map name to method."""

        if name.startswith("_"):
            return super().__getattribute__(name)

        try:
            f = getattr(self._model, name)
        except AttributeError:
            return super().__getattribute__(name)

        if isinstance(f, (FunctionType, MethodType)):

            @wraps(f)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return f(*args, **kwargs, _client=self._client)

            return wrapper

        return super().__getattribute__(name)

    def __dir__(self) -> List[str]:
        """List methods for model."""

        return sorted(
            k
            for k in vars(self._model)
            if not k.startswith("_")
            and isinstance(getattr(self._model, k), (FunctionType, MethodType))
        )

    def __str__(self) -> str:
        """Return str(self)."""

        return str(self._model)

    def __repr__(self) -> str:
        """Return repr(self)."""

        return repr(self._model)


class Client(BaseClient):
    """
    Kelvin API Client.

    Parameters
    ----------
    config : :obj:`ClientConfiguration`, optional
        Configuration object
    password : :obj:`str`, optional
        Password for obtaining access token
    totp : :obj:`str`, optional
        Time-based one-time password
    verbose : :obj:`bool`, optional
        Log requests/responses
    use_keychain : :obj:`bool`, optional
        Store credentials securely in system keychain
    store_token : :obj:`bool`, optional
        Store access token
    login : :obj:`bool`, optional
        Login to API
    mirror : :obj:`str`, optional
        Directory to use for caching mirrored responses (created if not existing)
    mirror_mode : :obj:`MirrorMode`, :obj:`str` or :obj:`list`, optional
        Mode of response mirroring:
            - ``dump``: Save responses in mirror cache
            - ``load``: Load responses from mirror cache (if available)
            - ``both``: Both dump and load
            - ``none``: Do not dump or load
    _adapter : :obj:`requests.adapters.BaseAdapter`, optional
        Optional requests adapter instance (e.g. :obj:`requests.adapters.HTTPAdapter`).
        Useful for testing.

    """

    acp: Type[responses.ACP]
    acp_edge_app_version: Type[responses.ACPEdgeAppVersion]
    acp_item: Type[responses.ACPItem]
    acp_meta_data_item: Type[responses.ACPMetaDataItem]
    acp_metadata: Type[responses.ACPMetadata]
    acp_status: Type[responses.ACPStatus]
    acp_status_count: Type[responses.ACPStatusCount]
    acp_telemetry: Type[responses.ACPTelemetry]
    acp_workload_manifests: Type[responses.ACPWorkloadManifests]
    alarm: Type[responses.Alarm]
    alarm_assets_statistics: Type[responses.AlarmAssetsStatistics]
    alarm_class: Type[responses.AlarmClass]
    alarm_filter: Type[responses.AlarmFilter]
    alarm_statistics: Type[responses.AlarmStatistics]
    alarm_type: Type[responses.AlarmType]
    app: Type[responses.App]
    app_version: Type[responses.AppVersion]
    asset: Type[responses.Asset]
    asset_class: Type[responses.AssetClass]
    asset_hierarchies: Type[responses.AssetHierarchies]
    asset_hierarchy_list: Type[responses.AssetHierarchyList]
    asset_item: Type[responses.AssetItem]
    asset_oee: Type[responses.AssetOEE]
    asset_shift: Type[responses.AssetShift]
    asset_statistics_item: Type[responses.AssetStatisticsItem]
    asset_status: Type[responses.AssetStatus]
    asset_status_count: Type[responses.AssetStatusCount]
    asset_template: Type[responses.AssetTemplate]
    asset_type: Type[responses.AssetType]
    asset_type_metadata: Type[responses.AssetTypeMetadata]
    audit_logger: Type[responses.AuditLogger]
    bridge: Type[responses.Bridge]
    bridge_data_stream_item: Type[responses.BridgeDataStreamItem]
    cluster: Type[responses.Cluster]
    cluster_cidr_item: Type[responses.ClusterCIDRItem]
    cluster_manifest_list: Type[responses.ClusterManifestList]
    control_change: Type[responses.ControlChange]
    data_label: Type[responses.DataLabel]
    data_label_cluster: Type[responses.DataLabelCluster]
    data_type: Type[responses.DataType]
    data_type_schema: Type[responses.DataTypeSchema]
    failure_class: Type[responses.FailureClass]
    failure_event_item: Type[responses.FailureEventItem]
    failure_list: Type[responses.FailureList]
    instance_health_status: Type[responses.InstanceHealthStatus]
    instance_setting_item: Type[responses.InstanceSettingItem]
    integration: Type[responses.Integration]
    integration_aws_region: Type[responses.IntegrationAwsRegion]
    integration_aws_region_list: Type[responses.IntegrationAwsRegionList]
    integration_list: Type[responses.IntegrationList]
    label: Type[responses.Label]
    label_metadata: Type[responses.LabelMetadata]
    mqtt_topic_list: Type[responses.MQTTTopicList]
    map_item: Type[responses.MapItem]
    map_model: Type[responses.MapModel]
    map_version_item: Type[responses.MapVersionItem]
    metric: Type[responses.Metric]
    orchestration_provision: Type[responses.OrchestrationProvision]
    secret: Type[responses.Secret]
    semantic_type_list: Type[responses.SemanticTypeList]
    site_hierarchy_overview_item: Type[responses.SiteHierarchyOverviewItem]
    storage: Type[responses.Storage]
    symbol: Type[responses.Symbol]
    thread: Type[responses.Thread]
    user: Type[responses.User]
    user_setting_item: Type[responses.UserSettingItem]
    user_with_permissions: Type[responses.UserWithPermissions]
    wireguard_peer: Type[responses.WireguardPeer]
    wireguard_tunnel: Type[responses.WireguardTunnel]
    workload: Type[responses.Workload]
    workload_logs: Type[responses.WorkloadLogs]
    workload_telemetry: Type[responses.WorkloadTelemetry]

    def __dir__(self) -> List[str]:
        """Return list of names of the object items/attributes."""

        return [*super().__dir__(), *MODELS]

    def __getattr__(self, name: str) -> Any:
        """Get attribute."""

        if name.startswith("_") or name in super().__dir__():
            return super().__getattribute__(name)  # pragma: no cover

        try:
            model = MODELS[name]
        except KeyError:
            return super().__getattribute__(name)

        return DataModelProxy(model, self)
