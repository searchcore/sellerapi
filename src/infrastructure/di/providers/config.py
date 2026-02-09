from dishka import Provider, Scope

from src.core.config import Config, DatabaseConfig, load_config


def setup_provider(provider: Provider):
    provider.provide(lambda: load_config(Config, "app"), scope=Scope.APP, provides=Config)
    provider.provide(lambda: load_config(DatabaseConfig, "db"), scope=Scope.APP, provides=DatabaseConfig)
