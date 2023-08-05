__version__ = "2.0.1"
__all__ = [
    "WorkspaceServiceAssetsClient",
    "WorkspaceServiceContainersClient",
    "AssetModel",
    "ContainerModel",
]

try:
    # Attempts to import the client class
    # Allowed to fail importing so the package metadata can be read for building
    from .assets_client import WorkspaceServiceAssetsClient
    from .containers_client import WorkspaceServiceContainersClient
    from .models import AssetModel, ContainerModel
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass  # pragma: no cover
