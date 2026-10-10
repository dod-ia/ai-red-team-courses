import asyncio

from mcp import Client
from mcp.client import ClientRequestContext
from mcp.types import ElicitRequestParams, ElicitResult

# IMPORTANT: `Mortarion` is a protected customer (hard coded). Don't use it
NAME_USER = "Sanguinius"
PRODUCT = "Rhino"

async def handle_elicitation(context: ClientRequestContext, 
                             params: ElicitRequestParams) -> ElicitResult:
    """
    Ask human confirmation when an elicitation is aked by the MCP server.
    """
    answer = None
    print("\n" + "!" * 50)
    print("CONFIRMATION REQUISE")
    print("!" * 50)
    print(params.message)

    while answer not in ("y", "n"):
        answer = input("Confirmer ? [y/n] (response must be <y> or <n> only) ").strip().lower()

    if answer == "y":
        reason = input("Give a reason: ").strip()
        return ElicitResult(action="accept", content={"confirmed": True, "reason": reason})
    else:
        return ElicitResult(action="decline")

def display_orders(name: str, orders: list[dict]) -> None:
    """
    Just a beautiful print of client orders
    """

    print(f"\n📦 Commandes de {name}")
    print("─" * 45)

    if not orders:
        print("Aucune commande.")
        return

    for order in orders:
        print(
            f"  #{order['id']:<4} │ "
            f"{order['product']}"
        )

    print("─" * 45)
    print(f"Total : {len(orders)} commande(s)")

async def listen_sub(client: Client, state) -> None:
    """
    Client subscription to a resource updated. 
    It tracks all updated of the resource orders://{NAME_USER}/count according to a specific name.
    """

    async with client.listen(resource_subscriptions=[f"orders://{NAME_USER}/count"]) as subscription:
        print("Listening for resource updates...")
        print("Listener ready")

        # The subscription is done, we can continue the interaction withe the MCP server
        state.set()

        async for event in subscription:
            print(f"Notification received: {event}")

            # The resource has changed so we read the data again
            result = await client.read_resource(f"orders://{NAME_USER}/count")
            print("New number of orders:", result.contents[0].text)

async def main() -> None:
    async with Client("http://localhost:8000/mcp",
                      elicitation_callback=handle_elicitation) as client:
        
        print(client.server_capabilities.model_dump(exclude_none=True))

        # We subscribe to a resource update tracking
        # We launch the function in a different task because the function is blocking.
        # We are in asynchronous mode, to be sure that the subscription is operational before continuing, we create a trigger to wait until it is done
        ready = asyncio.Event()
        listener_task = asyncio.create_task(listen_sub(client, ready))

        try:
            # Wait until the subscription is done
            await ready.wait()

            # Tool call of `get_user_orders`
            print("\n" + "#" * 50)
            print("# GET_USER_ORDERS TOOL CALL")
            print("#" * 50 + "\n")
            result = await client.call_tool("get_user_orders", {"name": NAME_USER})
            display_orders(name=NAME_USER, orders=result.structured_content["result"])

            #  Read `orders://{name}/count`
            print("\n" + "#" * 50)
            print(f"# RESSOURCES READING orders://{NAME_USER}/count")
            print("#" * 50 + "\n")
            result = await client.read_resource(f"orders://{NAME_USER}/count")
            print(f"Number of orders of {NAME_USER}: {result.contents[0].text}")

            # Tool call of `add_orders` (protected customer)
            # Mortarion is a protected customer.
            # This action will raise an error because Mortarion data can't be modified
            print("\n" + "#" * 50)
            print("# ADD_ORDERS TOOL CALL")
            print("#" * 50 + "\n")
            try:
                result = await client.call_tool("add_order", {"name": "Mortarion", "product": PRODUCT})
            except Exception as e:
                print(e)

            # Tool call of`add_orders` (basic customer)
            print("\n" + "#" * 50)
            print("# ADD_ORDERS TOOL CALL")
            print("#" * 50 + "\n")
            result = await client.call_tool("add_order", {"name": NAME_USER, "product": PRODUCT})
            print(f"Command of {NAME_USER}: {result.structured_content}")

            # Tool call of `delete_order`
            print("\n" + "#" * 50)
            print(f"# DELETE_ORDERS TOOL CALL {result.structured_content["id"]}")
            print("#" * 50 + "\n")
            result = await client.call_tool("delete_order", {"order_id": result.structured_content["id"]})
            print(f"Order {"deleted" if result.structured_content["result"] else "NOT DELETED"}")

            # Prompt of ̀`audit_user_orders`
            print("\n" + "#" * 50)
            print(f"# AUNDIT_USER_ORDERS PROMPT CALL")
            print("#" * 50 + "\n")
            result = await client.get_prompt("audit_user_orders", {"name": NAME_USER})
            print(result.messages[0].content.text)   
            # await asyncio.sleep(1)

        finally:
            # Stop the subscription listener task
            listener_task.cancel()

            # Wait until is is done
            try:
                await listener_task
            except asyncio.CancelledError:
                # The error is normal when the task is stopped
                pass   

if __name__ == "__main__":
    asyncio.run(main())