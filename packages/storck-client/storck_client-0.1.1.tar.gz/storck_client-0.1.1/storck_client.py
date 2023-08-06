import requests
import os


class StorckClient:
    def __init__(
        self,
        api_host: str = "http://localhost:8000",
        user_token: str = None,
        workspace_token: str = None,
    ):
        """
        The main class for creating connection to storck database.

        :param api_host: The adress of the storck instance
        :param user_token: the token of the user, if not defined, the environment variable STORCK_USER_TOKEN will be used
        :param user_token: the token of the workspace, if not defined, the environment variable STORCK_WORKSPACE_TOKEN will be used
        """
        self.api_host = os.getenv("STORCK_API_HOST", default=api_host)
        self.user_token = user_token or os.getenv("STORCK_USER_TOKEN")
        self.workspace_token = workspace_token or os.getenv("STORCK_WORKSPACE_TOKEN")

    def auth_verify(self) -> dict:
        """

        Check whether user exists in storck.
        """
        self._is_authorized()
        return self._post(
            "/api/auth", headers={"Authorization": "Token {}".format(self.user_token)}
        )

    def set_workspace_token(self, workspace_token: str):
        """
        Will override the current workspace_token, and also environment variable
        """
        self.workspace_token = workspace_token.token
        os.putenv("STORCK_WORKSPACE_TOKEN", self.workspace_token)

    def create_workspace(self, name:str) -> dict:
        """
        Will create a workspace with given name.
        """
        self._is_authorized()
        content = self._post(
            "/api/workspace",
            data={"name": name},
            headers={"Authorization": "Token {}".format(self.user_token)},
        )
        return content["data"]

    def get_workspaces(self) -> dict:
        """
        Gets the list of current workspaces


       :return: dict of workspaces
        """
        self._is_authorized()
        content = self._get(
            "/api/workspaces",
            headers={"Authorization": "Token {}".format(self.user_token)},
        )
        return content["data"]["workspaces"]

    def search(self, name_contains:str=None, meta_search:str=None) -> dict:
        """
        Searches for files. If name_contains will be provided, looks for a filename containig gie string.
        If meta_search is provided, will use it as the JSON encoded string query.

        :param name_contains: A string with a pattern
        :param meta_search: A stringified JSON containing relevant query https://docs.djangoproject.com/en/4.0/topics/db/queries/#querying-jsonfield. This json will be unpacked to python dict, which will be unpacked as arguments of filter function in django.
        :return: list of files matching the query
        """
        self._is_authorized()
        self._is_workspace_set()
        query = {"token": self.workspace_token}
        if name_contains is not None:
            query["filename_contains"] = name_contains
        if meta_search is not None:
            query["meta_search"] = meta_search
        content = self._get(
            "/api/search",
            query=query,
            headers={"Authorization": "Token {}".format(self.user_token)},
        )
        return content["files"]

    def get_info(self, file_id:int=None, path:str=None) -> dict:
        """
        Gets detailed information about the file.

        :param file_id: id of the file.
        :param path: database path of the file
        """
        self._is_authorized()
        self._is_workspace_set()
        content = self._get(
            "/api/info",
            query={
                "path": path,
                "id": file_id,
                "token": self.workspace_token,
            },
            headers={"Authorization": "Token {}".format(self.user_token)},
        )
        return content["file"]

    def upload_file(self, filename:str, path:str=None, metadata_str:str=None) -> dict:
        """
        Uploads the file to storck.

        :param filename: Path to the file on the client side.
        :param path: Optional database path to be used in storck. If not provided filename will be used instead.
        :param metadata_str: a metadata json string
        """

        self._is_authorized()
        self._is_workspace_set()
        data = {"path": path or filename}
        if metadata_str is not None:
            data["metadata"] = metadata_str
        return self._post(
            "/api/file",
            query={"token": self.workspace_token},
            data=data,
            files={"file": open(filename, "rb")},
            headers={"Authorization": "Token {}".format(self.user_token)},
        )

    def download_file(self, file_id: int) -> bytes:
        """
        Downloads the content of the file.

        :param file_id: Id of the file to downloaded.
        """
        self._is_authorized()
        self._is_workspace_set()
        return self._get_raw(
            "/api/file",
            query={"id": file_id, "token": self.workspace_token},
            headers={"Authorization": "Token {}".format(self.user_token)},
        )

    def add_user_to_workspace(self, user_id: int):
        """
        Adds users to workspace.

        :param user_id: the id of the user to be added to the workspace.
        """
        self._is_authorized()
        self._is_workspace_set()
        content = self._post(
            "/api/workspace/user",
            data={"user_id": user_id, "token": self.workspace_token},
            headers={"Authorization": "Token {}".format(self.user_token)},
        )
        return content["data"]

    def _is_authorized(self):
        if self.user_token is None:
            raise Exception("You need to provide user token")

    def _is_workspace_set(self):
        if self.workspace_token is None:
            raise Exception("You need to provide workspace token")

    def _post(self, path, query=None, data=None, files=None, headers=None):
        content = requests.post(
            "{}{}".format(self.api_host, path),
            data=data,
            files=files,
            params=query,
            headers=headers,
        )
        content.raise_for_status()
        return content.json()

    def _get(self, path, query=None, headers=None):
        content = requests.get(
            "{}{}".format(self.api_host, path), params=query, headers=headers
        )
        content.raise_for_status()
        return content.json()

    def _get_raw(self, path, query=None, headers=None):
        content = requests.get(
            "{}{}".format(self.api_host, path),
            params=query,
            headers=headers,
            stream=True,
        )
        content.raise_for_status()
        return content.raw.read()

