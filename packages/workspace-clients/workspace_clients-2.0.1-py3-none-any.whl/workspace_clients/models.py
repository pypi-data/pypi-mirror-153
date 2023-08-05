from __future__ import annotations
import json
from uuid import UUID
from enum import Enum
from typing import TYPE_CHECKING
from datetime import datetime
from typing import Dict, Optional, List, Any
from pydantic import BaseModel as _BaseModel, PrivateAttr, validator, constr
from clients_core.exceptions import ClientException


if TYPE_CHECKING:
    from .assets_client import WorkspaceServiceAssetsClient
    from .containers_client import WorkspaceServiceContainersClient


class BaseModel(_BaseModel):
    def dump(self) -> dict:
        return json.loads(self.json(by_alias=True))

    class Config:
        use_enum_values = True


class LocationSearchType(Enum):
    SINGLE_LEVEL = "singleLevel"
    SUBTREE = "subtree"


class AssetType(Enum):
    ANALYTIC = "Analytic"
    ANALYTIC_DATASET = "Analytic Dataset"
    ANALYTIC_PACKAGE = "Analytic Package"
    ANALYTIC_WORKBENCH_PROJECT = "Analytics Workbench Project"
    CARD = "Card"
    COHORT = "Cohort"
    COHORT_PREVIEW = "Cohort Preview"
    CDM_9 = "Core Diabetes Model v9.0"
    CDM_9_5 = "Core Diabetes Model v9.5"
    COVARIATE_TEMPLATE = "Covariate Template"
    DASHBOARD = "Dashboard"
    DATA_ON_DEMAND = "Data on Demand"
    DATA_SLICE = "Data Slice"
    DATASET_DISTRIBUTION = "Dataset Distribution"
    DESCRIPTIVE_ANALYTIC = "Descriptive Analytic"
    DOCUMENT = "Document"
    EVIDENCE_PLANNER_ASSET = "Evidence Planner Asset"
    EXPORT = "Export"
    GENOMIC_QUERY = "Genomic Query"
    GENOMIC_VARIANT_LIST = "Genomic Variant List"
    GROUPED_CODELIST = "Grouped Codelist"
    INTERACTIVE_REPORT = "Interactive Report"
    LINK = "Link"
    NOTEBOOK = "Notebook"
    PUBLISHED_DASHBOARD = "Published Dashboard"
    PUBLISHED_INTERACTIVE_REPORT = "Published Interactive Report"
    RECRUITMENT = "Recruitment"
    REPORT = "Report"
    SCIENTIFIC_REPORT = "Scientific Report"
    VARIANT_LIST = "Variant List"
    VISUALIZATION = "Visualisation"


class ContainerEmbed(Enum):
    CHILDREN = "children"
    PARENT = "parent"
    SHARED_WITH = "sharedWith"


class AssetEmbed(Enum):
    PARENT = "parent"
    METADATA = "metadata"
    DATASET_INFO = "datasetInfo"


class AssetModel(BaseModel):
    type: AssetType
    name: Optional[constr(max_length=100)] = None  # type: ignore
    id: Optional[UUID] = None
    parent: Optional[dict] = None
    parentAssetId: Optional[str] = None
    subtype: Optional[str] = None
    isHidden: Optional[bool] = None
    sentByUserId: Optional[str] = None
    datasetInfo: Optional[List[dict]] = None
    metadata: Optional[Dict[str, str]] = None
    description: Optional[constr(max_length=500)] = None  # type: ignore
    isFavourite: Optional[bool] = None
    rights: Optional[dict] = None
    createdByUserId: Optional[str] = None
    isShared: Optional[bool] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    _client: Optional[WorkspaceServiceAssetsClient] = PrivateAttr(default=None)

    @validator("id")
    def _uuid_as_str(cls, value: Any) -> Optional[str]:
        if value:
            return str(value)
        return value

    def delete(self) -> bool:
        if self._client is None:  # type: ignore
            message = (
                "Can not perform AssetMode.delete operation."
                "No instance of WorkspaceServiceAssetsClient has been provided to this model."
                "Please use WorkspaceServiceAssetsClient.delete function instead"
            )

            raise ClientException(message)
        return self._client.delete(self.id)  # type: ignore


class ContainerModel(BaseModel):
    name: constr(max_length=100)  # type: ignore
    id: Optional[UUID] = None
    type: Optional[str] = "standard"
    description: Optional[constr(max_length=500)] = None  # type: ignore
    parent: Optional[dict] = None
    children: Optional[List[dict]] = None
    rights: Optional[dict] = None
    isFavourite: Optional[bool] = None
    isShared: Optional[bool] = None
    sharedWith: Optional[dict] = None
    totalDescendantAssets: Optional[int] = None
    createdByUserId: Optional[str] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    _client: Optional[WorkspaceServiceContainersClient] = PrivateAttr(default=None)

    @validator("id")
    def _uuid_as_str(cls, value: Any) -> Optional[str]:
        if value:
            return str(value)
        return value

    def delete(self) -> bool:
        if self._client is None:  # type: ignore
            message = (
                "Can not perform ContainerModel.delete operation. "
                "No instance of WorkspaceServiceContainersClient has been provided to this model."
                "Please use WorkspaceServiceContainersClient.delete function instead"
            )
            raise ClientException(message)
        return self._client.delete(self.id)  # type: ignore
