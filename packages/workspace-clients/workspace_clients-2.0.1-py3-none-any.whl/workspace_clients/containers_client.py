from typing import Dict, List, Any
from requests import Response
from pydantic import parse_obj_as
from clients_core.service_clients import E360ServiceClient
from .models import ContainerModel, LocationSearchType, ContainerEmbed


class WorkspaceServiceContainersClient(E360ServiceClient):
    """
    A client for the containers endpoint of workspace service
    Subclasses dataclass `clients_core.service_clients.E360ServiceClient`.

    Args:
        client (clients_core.rest_client.RestClient): an instance of a rest client
        user_id (str): the user_id guid
        correlation_id (str): the correlation-id to be passed on the request headers

    """

    service_endpoint: str = ""
    extra_headers: Dict = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    def create(self, model: ContainerModel, **kwargs: Any) -> ContainerModel:
        """
        Creates a POST request for the containers endpoint, to allow the creation of a new container.

        Returns:
            ContainerModel: the newly created Container instance
        Raises:
            clients_core.exceptions.HttpResponseError: on server response errors.
        """

        response = self.client.post(
            "", json=model.dump(), headers=self.service_headers, raises=True, **kwargs
        )
        return self._response_to_model(response)

    def delete(self, id: str, **kwargs: Any) -> bool:
        """
        Delete the specified container, if it exists

        Returns:
            bool: True / False for successful / failed requests

        Raises:
            clients_core.exceptions.HttpResponseError: on server response errors.
        """
        response = self.client.delete(
            id, headers=self.service_headers, raises=True, **kwargs
        )
        return response.ok

    def get_by_id(
        self,
        id_: str,
        all_ancestors: bool = False,
        all_descendants: bool = False,
        embed: List[ContainerEmbed] = None,
        params: dict = {},
        **kwargs: Any,
    ) -> ContainerModel:
        """
        Retrieve a single container using its id. Can specify which fields should be returned using embed, and whether to include ancestors or descedants

        Returns:
            ContainerModel: The container matching the id provided

        Raises:
            clients_core.exceptions.HttpResponseError: on server response errors.
        """
        if embed:
            params["embed"] = ",".join(e.value for e in embed)
        if all_ancestors:
            params["allAncestors"] = all_ancestors
        if all_descendants:
            params["allDescendants"] = all_descendants
        response = self.client.get(
            id_, params=params, headers=self.service_headers, raises=True, **kwargs
        )
        return self._response_to_model(response)

    def get(
        self,
        name: str = None,
        location_search_type: LocationSearchType = LocationSearchType.SINGLE_LEVEL,
        embed: List[ContainerEmbed] = None,
        sort: List[str] = ["-created"],
        params: dict = {},
        **kwargs: Any,
    ) -> List[ContainerModel]:
        params["sort"] = ",".join(s for s in sort)
        """
        Creates a get request for the containers endpoint, returning the containers of the current user.
        By default all the containers will be returned without any pagination.

        Returns:
            list: a list of containers for the user that matched the provided filters

        Raises:
            clients_core.exceptions.HttpResponseError: on server response errors.
        """

        if name:
            params["name"] = name
        if location_search_type:
            params["locationSearchType"] = location_search_type.value
        if embed:
            params["embed"] = ",".join(e.value for e in embed)

        response = self.client.get(
            "", params=params, headers=self.service_headers, raises=True, **kwargs
        )
        return self._response_to_models(response)

    def _response_to_models(self, response: Response) -> List[ContainerModel]:
        response_json = response.json()["resources"]
        instances = parse_obj_as(List[ContainerModel], response_json)
        for instance in instances:
            instance._client = self
        return instances

    def _response_to_model(self, response: Response) -> ContainerModel:
        response_json = response.json()
        instance = ContainerModel.parse_obj(response_json)
        instance._client = self
        return instance
