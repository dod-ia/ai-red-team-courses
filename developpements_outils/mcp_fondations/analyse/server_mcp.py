from mcp.server import MCPServer
from mcp import MCPError
from mcp.types import INVALID_PARAMS
from mcp.server.request_state import RequestStateSecurity
from mcp.server import ServerRequestContext
from mcp.server.context import CallNext, HandlerResult
from mcp.server.mcpserver.context import Context
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.mcpserver import AcceptedElicitation, CancelledElicitation, DeclinedElicitation, Elicit, ElicitationResult, Resolve
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from typing import Annotated
from database import init_database
from pydantic import BaseModel, Field
import sqlite3
import logging
import os
import time

# RequestState key used for horizontal scaling 
# DANGER: Don't use this key in production. By the way, don't use this code in production too...
REQUEST_STATE_KEY = b'\xf0\xcb+jm\xef\x94\xc5\xf1\xe5M\x97\xe7\xe1\x0f\xdaJ\xb9q\x14\xc9\xd0Sn6\xb8\x99\x1cS\x99\xa70'

class Confirm(BaseModel):
    """Elicitation data"""
    confirmed: bool
    reason: str | None = None

# class DeleteReason(BaseModel):
#     reason: str = Field(description="Reason for deleting the order")

class Order(BaseModel):
    """An order associated with a user"""

    id: int = Field(description="Unique identifier of the order")
    name: str = Field(description="Name of the user who placed the order")
    product: str = Field(description="Name of the product ordered")


async def confirm_delete(order_id: int) -> Elicit[Confirm]:
    """Resolver: ask for confirmation for removing data."""
    return Elicit(f"Are you sure to delete the order {order_id}", Confirm)

async def get_request_logging(ctx:  ServerRequestContext, call_next: CallNext) -> HandlerResult:
    """Middleware - Logging PID processus, method called and durated time"""
    start = time.perf_counter()
    logger.info(f"[MCP] PID={os.getpid()} method={ctx.method} function={ctx.params.get("name")}")
    try:
        return await call_next(ctx)
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info("%s took %.1f ms", ctx.method, elapsed_ms)

async def get_request_control(ctx:  ServerRequestContext, call_next: CallNext) -> HandlerResult:
    """Middleware - Block all interaction with Mortarion customer"""
    if ctx.method == "tools/call":
        if (await ctx.request.json())["params"]["arguments"].get("name") == "Mortarion":
            logger.warning(f"Unauthorized access to protected customer - Refused request")
            raise MCPError(code=INVALID_PARAMS, message=f"Mortarion is a protected customer ! - Refused request") 
    return await call_next(ctx)

# Init telemetry and store data in a file in the current repertory
log_file = open("./telemetry.log", "a", encoding="utf-8")
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter(out=log_file)))
trace.set_tracer_provider(provider)


logger = logging.getLogger(__name__)
database_name = init_database()

mcp = MCPServer(name="Enterprise Database MCP",
                description="MCP server permetting to get/update informations about customer's orders",
                instructions=("MCP server connected to a SQLite enterprise test database. "
                              "Use tools to query users and orders."
                              ),
                log_level="INFO",
                request_state_security=RequestStateSecurity(keys=[REQUEST_STATE_KEY]))

# Add middleware to the MCP server
mcp.middleware.append(get_request_logging)
mcp.middleware.append(get_request_control)

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
async def delete_order(order_id: Annotated[int, Field(description="ID of the order")], 
                       confirm: Annotated[ElicitationResult[Confirm], Resolve(confirm_delete)],
                       ctx: Context) -> Annotated[bool, Field(description="Indicate if the order has been deleted or not")]:
    """
    Permanently deletes an order from the database.

    This operation modifies the database. Use this tool only when the user
    explicitly requests that an order be deleted.
    """

    # Refuse to apply except if the user has accepted explicitly
    match confirm:
        case AcceptedElicitation(data=Confirm(confirmed=False)):
            logger.info(f"Deletion refused for order {order_id}")
            return False
        
        case DeclinedElicitation():
            logger.info(f"Deletion declined for order {order_id}")
            return False

        case CancelledElicitation():
            logger.info(f"Deletion cancelled for order {order_id}")
            return False
        
        case AcceptedElicitation(data=Confirm(confirmed=True)):
            logger.warning(f"Deletion confirmed for order: {order_id} - reason: {confirm.data.reason}")
            connection = sqlite3.connect(database_name)
            connection.row_factory = sqlite3.Row

            try:
                cursor = connection.cursor()
                cursor.execute("SELECT name FROM orders WHERE id = ?", (order_id,))
                row = cursor.fetchone()

                if row is None:
                    raise ToolError(f"Order with id {order_id} does not exist.")
                
                name = row["name"]
                cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
                connection.commit()

                logger.warning(f"Deleting order: {order_id}")

                # Notify that the user's order count has changed
                await ctx.notify_resource_updated(uri=f"orders://{name}/count")
                logger.info(f"Notifying update to user: orders://{name}/count")

                return True

            finally:
                connection.close()

@mcp.resource("orders://{name}/count")
def user_orders_count_resource(name: Annotated[str, Field(description="Name of the user")]) -> Annotated[str, Field(description="Number of orders")]:
    """
    Current order count for a user.

    Read this resource when you need to know how many orders a user has.
    """
    connection = sqlite3.connect(database_name)
    try:
        cursor = connection.cursor()

        cursor.execute("""SELECT COUNT(*) FROM orders WHERE name = ?""", (name,))
        return str(cursor.fetchone()[0])

    finally:
        connection.close()

@mcp.tool()
async def add_order(name: Annotated[str, Field(description="Name of the user")],
                    product: Annotated[str, Field(description="Product affiliated to the order")], 
                    ctx: Context) -> Order:
    """
    Create a new order for a user.

    Use this tool when an order must be added to the database.
    After the order is created, the user's order-count resource is
    notified so clients subscribed to that resource can refresh it.

    This operation modifies the database.
    """

    connection = sqlite3.connect(database_name)
    try:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO orders (name, product) VALUES (?, ?)""",(name, product),)
        order_id = cursor.lastrowid
        connection.commit()
        logger.info(f"Adding order: {name}:{product}")

        # Notify that the resource count of the <name> customer has changed
        await ctx.notify_resource_updated(uri=f"orders://{name}/count")
        logger.info(f"Notifying update to user: orders://{name}/count")

        return Order(id=order_id, name=name, product=product)

    finally:
        connection.close()

@mcp.prompt()
def audit_user_orders(name: Annotated[str, Field(description="Name of the user")]) -> Annotated[str, Field(description="Prompt for an audit workflow of user's orders")]:
    """
    Create a read-only audit workflow for a user's orders.

    The workflow compares the complete order list with the user's
    order-count resource and requires the model to report any mismatch.
    It is intended for consistency checks and must not modify the database.
    """
        
    return f"""
You are auditing the order data for the user "{name}".

Perform a read-only audit.

Use both:
- the get_user_orders tool;
- the orders://{name}/count resource.

Your objectives are:
1. Determine the total number of orders.
2. List every order and its product.
3. Verify that the number of orders returned by the tool matches the resource count.
4. If the values differ, clearly report the discrepancy.
5. Do not modify the database.

Return a structured audit containing:
- User
- Resource count
- Tool result count
- Orders
- Consistency status
- Observations

Never invent missing orders or data.
"""

app = mcp.streamable_http_app()
# if __name__ == "__main__":
#     mcp.run(transport="streamable-http")