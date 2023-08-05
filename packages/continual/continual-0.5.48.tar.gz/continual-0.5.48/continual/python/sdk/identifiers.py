from __future__ import annotations

from continual.python.sdk.exceptions import InvalidArgumentError


class ProjectEnvironmentIdentifer:
    """Utility class to handle project and environment names and identifers."""

    production_environment_ids = ["production", "prod"]
    default_environment_id = "production"

    def __init__(self, project_name_or_id="", environment_name_or_id=""):
        self.__project_name = ""
        self.__project_id = ""
        self.__environment_name = ""
        self.__environment_id = ""
        self.__environment_id_alias = ""
        self.__environment_is_default = False
        self.__environment_is_production = False
        self.__url_path = ""
        self.__parse(project_name_or_id, environment_name_or_id)

    def __parse(self, project_name_or_id: str, environment_name_or_id: str):
        project_part = ""
        environment_part = ""

        if project_name_or_id:
            if "@" in project_name_or_id:
                project_part = project_name_or_id.split("@")[0]
                environment_part = project_name_or_id.split("@")[1]
            else:
                project_part = project_name_or_id

        if environment_name_or_id:
            if "@" in environment_name_or_id:
                project_part = environment_name_or_id.split("@")[0]
                environment_part = environment_name_or_id.split("@")[1]
            else:
                environment_part = environment_name_or_id

        if not project_part:
            raise InvalidArgumentError(
                f"A project name or ID is required. Received: '{project_name_or_id}', '{environment_name_or_id}'"
            )
        elif project_part.startswith("projects/"):
            self.__project_id = project_part.split("projects/")[1]
            self.__project_name = project_part
        else:
            self.__project_id = project_part
            self.__project_name = f"projects/{self.__project_id}"

        if not environment_part:
            if self.__project_name:
                self.__environment_id = self.__project_name
                self.__environment_id_alias = self.default_environment_id
                self.__environment_name = (
                    f"{self.__project_name}@{self.__environment_id_alias}"
                )
                self.__environment_is_default = True
                self.__environment_is_production = True
            else:
                raise InvalidArgumentError(
                    f"A project name or ID is required. Received: '{project_name_or_id}', '{environment_name_or_id}'"
                )
        elif environment_part.startswith("projects/"):
            if environment_part == self.__project_name:
                self.__environment_id = environment_part
                self.__environment_id_alias = self.default_environment_id
                self.__environment_name = (
                    f"{environment_part}@{self.__environment_id_alias}"
                )
                self.__environment_is_default = True
                self.__environment_is_production = True
            else:
                raise InvalidArgumentError(
                    f"Default environment name does not match project name. Received: '{project_name_or_id}', '{environment_name_or_id}'"
                )
        elif environment_part in self.production_environment_ids:
            if self.__project_name:
                self.__environment_id = self.__project_name
                self.__environment_id_alias = self.default_environment_id
                self.__environment_name = (
                    f"{self.__project_name}@{self.__environment_id_alias}"
                )
                self.__environment_is_default = True
                self.__environment_is_production = True
            else:
                raise InvalidArgumentError(
                    f"A project name or ID is required. Received: '{project_name_or_id}', '{environment_name_or_id}'"
                )
        else:
            self.__environment_id = environment_part
            self.__environment_id_alias = environment_part
            self.__environment_is_default = False
            self.__environment_is_production = False
            self.__environment_name = f"{self.__project_name}@{self.__environment_id}"

        if self.__environment_is_default:
            self.__url_path = self.__project_name
        else:
            self.__url_path = self.__environment_name

    @property
    def project_name(self) -> str:
        """Project name `projects/[project_id]`."""
        return self.__project_name

    @property
    def project_id(self) -> str:
        """Project ID `[project_id]`."""
        return self.__project_id

    @property
    def environment_name(self) -> str:
        """Environment name `projects/[project_id]@[environment_id]`."""
        return self.__environment_name

    @property
    def environment_name_short(self) -> str:
        """Shortened environment name `[project_id]@[environment_id]`."""
        return self.__environment_name.replace("projects/", "")

    @property
    def environment_id(self) -> str:
        """Environment ID: `[environment_id]` when non-default, `[project_name]` when default."""
        return self.__environment_id

    @property
    def environment_id_alias(self) -> str:
        """Environment ID alias: `[environment_id]` when non-default, `[default_environment_id]` when default."""
        return self.__environment_id_alias

    @property
    def environment_is_default(self) -> str:
        """Whether the environment is the default environment."""
        return self.__environment_is_default

    @property
    def environment_is_production(self) -> str:
        """Whether the environment is the production environment."""
        return self.__environment_is_production

    @property
    def url_path(self) -> str:
        """The URL path for the project and environment: `projects/[project_id]` for projects and default environments, `projects/[project_id]@[environment_id]` for non-default environments."""
        return self.__url_path

    def __getitem__(self, key):
        return getattr(self, key)
