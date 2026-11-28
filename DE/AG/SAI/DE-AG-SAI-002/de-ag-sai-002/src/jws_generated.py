import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import json

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ISSUER = os.getenv("ISSUER")
AUDIENCE = os.getenv("AUDIENCE")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

def generate_jws(sub: str = "user",
                 roles: list[str] = ["user"],
                 min_time_validity: int = 30):
    
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": now,
        "exp": now + timedelta(minutes=int(min_time_validity)),
        "roles": roles,
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM,)
    return token

tokens = {
    "alice_user": generate_jws(
        sub="Alice",
        roles=["user"],
        min_time_validity=3000,
    ),
    "bob_admin": generate_jws(
        sub="Bob",
        roles=["admin"],
        min_time_validity=3000,
    ),
    "claude_user": generate_jws(
        sub="Claude",
        roles=["user"],
        min_time_validity=3000,
    ),
}

with open("tokens.json", "w", encoding="utf-8") as file:
    json.dump(tokens, file)