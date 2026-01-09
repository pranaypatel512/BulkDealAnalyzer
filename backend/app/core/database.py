"""
Database Connection and Client

Handles Supabase client initialization and database operations.
"""

from functools import lru_cache
from typing import Any

from supabase import Client, create_client

from app.core.config import get_settings


@lru_cache
def get_supabase_client() -> Client:
    """Get cached Supabase client instance."""
    settings = get_settings()
    return create_client(
        url=settings.supabase_url,
        key=settings.supabase_key,
    )


@lru_cache
def get_supabase_admin_client() -> Client:
    """Get Supabase admin client with service role key (bypasses RLS)."""
    settings = get_settings()
    if not settings.supabase_service_role_key:
        raise ValueError("SUPABASE_SERVICE_ROLE_KEY not configured")
    return create_client(
        url=settings.supabase_url,
        key=settings.supabase_service_role_key,
    )


class Database:
    """Database operations wrapper."""

    def __init__(self, client: Client | None = None):
        """Initialize database with optional client."""
        self.client = client or get_supabase_client()

    async def execute_query(
        self,
        table: str,
        operation: str = "select",
        filters: dict[str, Any] | None = None,
        data: dict[str, Any] | list[dict[str, Any]] | None = None,
    ) -> Any:
        """
        Execute a database query.

        Args:
            table: Table name
            operation: Operation type (select, insert, update, delete)
            filters: Query filters
            data: Data for insert/update operations

        Returns:
            Query result
        """
        query = self.client.table(table)

        # Apply filters
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        # Execute operation
        if operation == "select":
            result = query.select("*").execute()
        elif operation == "insert":
            if isinstance(data, list):
                result = query.insert(data).execute()
            else:
                result = query.insert(data).execute() if data else None
        elif operation == "update":
            result = query.update(data).execute() if data else None
        elif operation == "delete":
            result = query.delete().execute()
        else:
            raise ValueError(f"Unknown operation: {operation}")

        return result

    def get_table(self, table_name: str):
        """Get a table query builder."""
        return self.client.table(table_name)


# Global database instance
db = Database()

