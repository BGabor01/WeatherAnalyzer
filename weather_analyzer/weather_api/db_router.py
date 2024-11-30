class DatabaseRouter:
    def db_for_read(self, model, **hints):
        """Point all read operations to the replica."""
        return "replica"

    def db_for_write(self, model, **hints):
        """Point all write operations to the default database."""
        return "default"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure migrations only apply to the default database."""
        return db == "default"
