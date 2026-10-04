
CLICKHOUSE_MODELS = {"workvolumerecord"}


class DatabaseRouter:
    """WorkVolumeRecord -> ClickHouse, всё остальное -> PostgreSQL."""

    def db_for_read(self, model, **hints):
        if model._meta.model_name in CLICKHOUSE_MODELS:
            return "clickhouse"
        return "default"

    db_for_write = db_for_read

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name is None:
            return db == "default"
        return (db == "clickhouse") == (model_name in CLICKHOUSE_MODELS)