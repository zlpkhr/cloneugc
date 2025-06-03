from functools import cached_property

from notion_client import Client

from .schema import schema as notion_schema


class Database:
    def __init__(self, notion: Client, database_id: str):
        self.notion = notion
        self.database_id = database_id

    @cached_property
    def schema(self) -> dict[str, type]:
        try:
            response = self.notion.databases.retrieve(self.database_id)
            properties = response.get("properties", {})

            schema = {}
            for name, property in properties.items():
                schema[name] = notion_schema[property["type"]]

            if not schema:
                self.notion.logger.warning(
                    f"Schema for database {self.database_id} is empty."
                )

            return schema
        except Exception as e:
            self.notion.logger.error(f"Error retrieving database schema: {e}")
            return None

    def insert(self, props: dict[str, object]) -> str:
        """
        Insert a row (page) into this Notion database.

        Args:
            props: A dict mapping property names to raw values. The keys must match the schema.
                The values are raw data (e.g., str for Text/Email) that will be converted using the schema's type.
        Returns:
            The 'id' of the created page object as a string.
        """
        properties = {}
        for key, value in props.items():
            if key not in self.schema:
                raise ValueError(f"Property '{key}' not in schema.")
            value_obj = self.schema[key](value)
            properties[key] = value_obj.serialize()

        response = self.notion.pages.create(
            parent={"database_id": self.database_id},
            properties=properties,
        )

        return response["id"]
