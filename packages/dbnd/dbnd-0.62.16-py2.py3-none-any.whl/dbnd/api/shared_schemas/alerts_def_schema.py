from dbnd._core.tracking.schemas.base import ApiStrictSchema
from dbnd._vendor.marshmallow import fields, pre_load


class MLAlert(ApiStrictSchema):
    sensitivity = fields.Float()
    look_back = fields.Integer()


class AlertDefsSchema(ApiStrictSchema):
    severity = fields.Str(required=True)
    type = fields.Str(required=True)
    user_metric = fields.Str()
    operator = fields.Str()
    is_str_value = fields.Bool()

    created_at = fields.DateTime()
    scheduled_job_name = fields.Str(attribute="scheduled_job.name")
    source_instance_name = fields.Method("get_tracking_source_name")
    env = fields.Method("get_tracking_source_env")
    # TODO_CORE: API: Deprecate airflow_server_info
    airflow_instance_name = fields.Method("get_tracking_source_name")
    project_id = fields.Int(attribute="job.project_id")
    project_name = fields.Str(attribute="job.project.name")
    alert_on_historical_runs = fields.Bool()
    group_uid = fields.Str(allow_none=True, load_from="alert_group_uid")

    uid = fields.Str(allow_none=True)
    value = fields.Str(allow_none=True)
    job_id = fields.Int(allow_none=True)
    summary = fields.Str(allow_none=True)
    job_name = fields.Str(attribute="job.name", allow_none=True)
    task_repr = fields.Str(allow_none=True)
    task_name = fields.Str(allow_none=True)
    custom_name = fields.Str(allow_none=True)
    original_uid = fields.Str(allow_none=True)
    advanced_json = fields.Str(allow_none=True)
    scheduled_job_uid = fields.Str(allow_none=True)
    custom_description = fields.Str(allow_none=True)
    ml_alert = fields.Nested(MLAlert, allow_none=True)

    # Fields for DatasetSlaAlert/DatasetSlaAdvancedAlert alert
    # --------------------------------------
    seconds_delta = fields.Int(allow_none=True)  # Converts to datetime.timedelta
    dataset_partial_name = fields.Str(allow_none=True)
    datasets_uids = fields.List(fields.Str(), allow_none=True)

    # Fields for OperationColumnStatAdvancedAlert alert
    # --------------------------------------
    dataset_uid = fields.Str(allow_none=True)
    # Operation type (e.g. "read", "write", None=any) to filter stats by
    operation_type = fields.Str(allow_none=True)

    # Type of MetricRule, found in dbnd_web. Used to build advanced_json
    metrics_rules = fields.List(fields.Dict(), allow_none=True)

    # Used only used by the UI
    affected_datasets = fields.List(fields.Dict(), allow_none=True, dump_only=True)

    is_system = fields.Function(
        lambda alert_def: alert_def.owner == "system", dump_only=True,
    )

    def get_tracking_source_name(self, obj):
        return self._get_tracking_source_instance(obj).name

    def get_tracking_source_env(self, obj):
        return self._get_tracking_source_instance(obj).env

    def _get_tracking_source_instance(self, obj):
        if obj.job:
            return obj.job.tracking_source

        return obj.tracking_source

    @pre_load
    def prepere(self, data: dict, **kwargs):
        value = data.get("value", None)
        if value is not None:
            data["value"] = str(data["value"])
        return data
