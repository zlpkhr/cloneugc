from logging import getLogger

import requests


class Notion:
    """
    Simple Notion API wrapper for interacting with Notion databases.
    """

    def __init__(self, integration_token: str, notion_version: str = "2022-06-28"):
        self.token = integration_token
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": notion_version,
            "Content-Type": "application/json",
        }
        self.logger = getLogger(__name__)


class Database:
    def __init__(
        self, notion: Notion, database_id: str, schema: dict[str, type] = None
    ):
        self.notion = notion
        self.database_id = database_id
        self.logger = notion.logger
        self.schema = schema or {}

    def insert(self, data: dict[str, object]) -> str:
        """
        Insert a row (page) into this Notion database.
        Args:
            data: A dict mapping property names to raw values (str for Text/Email).
        Returns:
            The 'id' of the created page object as a string.
        Raises:
            requests.RequestException: If the request fails, with error details from Notion.
        """
        properties = {}
        for key, value in data.items():
            if key not in self.schema:
                raise ValueError(f"Property '{key}' not in schema.")
            value_obj = self.schema[key](value)
            properties[key] = value_obj.serialize()
        try:
            response = requests.post(
                f"{self.notion.base_url}/pages",
                headers=self.notion.headers,
                json={
                    "parent": {"database_id": self.database_id},
                    "properties": properties,
                },
            )
            response.raise_for_status()
            return response.json()["id"]
        except requests.RequestException as e:
            error_text = str(e)
            self.logger.error(
                f"Failed to insert row into Notion database: {error_text}"
            )
            raise requests.RequestException(f"Notion API error: {error_text}") from e
