from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from database import init_database
from pydantic import BaseModel, Field
from typing import Annotated

import logging
import sqlite3
import subprocess

class Order(BaseModel):
    """An order associated with a user"""

    id: int = Field(description="Unique identifier of the order")
    name: str = Field(description="Name of the user who placed the order")
    product: str = Field(description="Name of the product ordered")


logger = logging.getLogger(__name__)
database_name = init_database()

mcp = MCPServer(name="Enterprise Database MCP",
                description="MCP server providing access to customer order information",
                log_level="INFO")


@mcp.tool()
def get_user_orders(name: Annotated[str, Field(description="Name of the user")]) -> list[Order]:
    """
    Retrieve the complete order history for a user.

    Use for read-only queries about which orders a user has placed.
    Returns all matching orders in order ID order.
    """

    connection = sqlite3.connect(database_name)
    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        #######################
        # DANGER: SQLI threat #
        #######################

        cursor.execute(f"""SELECT id, name, product FROM orders WHERE name = '{name}' ORDER BY id""")
        return [Order(id=row["id"], name=row["name"], product=row["product"]) for row in cursor.fetchall()]
    finally:
        connection.close()

@mcp.tool()
def safe_get_user_orders(name: Annotated[str, Field(description="Name of the user")]) -> list[Order]:
    """
    Retrieve the complete order history for a user.

    Use for read-only queries about which orders a user has placed.
    Returns all matching orders in order ID order.
    """

    connection = sqlite3.connect(database_name)
    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""SELECT id, name, product FROM orders WHERE name = ? ORDER BY id""",(name,)) 
        return [Order(id=row["id"], name=row["name"], product=row["product"]) for row in cursor.fetchall()]
    finally:
        connection.close()

# ╔══════════════════════════════════════════════════════════════════════╗
# ║                                                                      ║
# ║                   ⚠️  SPOILER WARNING  ⚠️                            ║
# ║                                                                      ║
# ║                  🚫  DO NOT LOOK BELOW!  🚫                          ║
# ║                                                                      ║
# ║                  🔐  QUIZ SOLUTIONS AHEAD  🔐                        ║
# ║                                                                      ║
# ║                    You've been warned... 👀                          ║
# ║                                                                      ║
# ╚══════════════════════════════════════════════════════════════════════╝

@mcp.tool()
def check_ping(host: str) -> str:
    """Ping an IP to check if the service is up."""
    command = f"ping -c 1 {host}"

    ##########################
    # DANGER: Code Injection #
    ##########################

    result = subprocess.run(
        command,
        shell=True,
        executable="/bin/bash",
        capture_output=True,
        text=True,
        timeout=5
    )

    return result.stdout + result.stderr

@mcp.tool()
def safe_check_ping(host: str) -> str:
    """Ping an IP to check if the service is up."""

    ip = host

    # Check if host is a valid IPv4 or IPv6 address
    import ipaddress
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        raise ToolError("Adresse IP invalide")

    command = ["ping", "-c", "1", str(ip)]

    result = subprocess.run(
        command,
        shell=False,
        capture_output=True,
        text=True,
        timeout=5,
        check=False
    )

    if result.returncode != 0:
        raise ToolError(f"{result.stderr}")
    else:
        return result.stdout

app = mcp.streamable_http_app()