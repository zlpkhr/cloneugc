from notion_client import Client


class Database:
    def __init__(
        self, notion: Client, database_id: str, schema: dict[str, type] = None
    ):
        self.notion = notion
        self.database_id = database_id
        self.schema = schema or {}

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
