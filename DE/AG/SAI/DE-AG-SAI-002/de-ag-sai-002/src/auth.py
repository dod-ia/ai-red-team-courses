import os
import jwt
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from langgraph_sdk import Auth

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ISSUER = os.getenv("ISSUER")
AUDIENCE = os.getenv("AUDIENCE")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

if not all([JWT_SECRET_KEY, ISSUER, AUDIENCE, JWT_ALGORITHM]):
    raise RuntimeError("JWT configuration is incomplete")

# ============================================================
# 2. Define permissions for each role
# ============================================================

# Each role is associated with a list of permissions.
#
# The admin role has access to all permissions through "*".
#
# The user role has limited permissions to manage threads
# and assistants.
#
# Delete permissions are intentionally disabled for users.

ROLE_PERMISSIONS = {
    "admin": ["*"],
    "user": [
        "threads:create",
        "threads:read",
        "threads:run",
        "threads:update",
        "threads:search",
       # "threads:delete",
        "assistants:read",
        "assistants:search",
        "assistants:create",
        "assistants:update",
       # "assistants:delete"
    ],
}

# ============================================================
# 3. Initialize LangGraph authentication
# ============================================================

# Create the Auth object.
# It is used to define authentication and authorization
# policies for incoming LangGraph requests.

auth = Auth()

# ============================================================
# 4. Authenticate users using JWT tokens
# ============================================================

@auth.authenticate
async def authenticate(authorization: str | None,) -> Auth.types.MinimalUserDict:

    # If no authorization header...
    if not authorization:
        raise Auth.exceptions.HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    try:
        # Expected format:
        # Authorization: Bearer <TOKEN>
        scheme, token = authorization.split(" ", 1)

        if scheme.lower() != "bearer":
            raise ValueError("Invalid authorization scheme")

        # ----------------------------------------------------
        # Validate the JWT token
        # ----------------------------------------------------

        # Decode and validate the JWT.
        #
        # The following checks are performed:
        # - Token signature
        # - Token expiration
        # - Token issuer
        # - Token audience
        # - Presence of required claims
        #
        # The token must contain:
        # exp, iat, sub, iss, aud, and roles.

        payload = jwt.decode(
            jwt=token,
            key=JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_aud": True,
                "verify_iss": True,
                "require": [
                    "exp",
                    "iat",
                    "sub",
                    "iss",
                    "aud",
                    "roles",
                ]
            },
        )

        # ----------------------------------------------------
        # Extract user identity and roles
        # ----------------------------------------------------

        # The "sub" claim identifies the authenticated user.
        user_id = payload["sub"]
        # Retrieve the roles assigned to the user.
        roles = payload.get("roles", [])
        # Roles must be provided as a list.
        # Example: ["user"] or ["admin"].
        if not isinstance(roles, list):
            raise ValueError("Invalid roles format")

        # Use a set to avoid duplicate permissions.
        permissions = set()

        # For each role:
        # - Retrieve its associated permissions.
        # - Add a specific permission representing the role.
        #
        # Example:
        # "user" role -> "threads:read" permission
        # "user" role -> "role:user" permission
        for role in roles:
            permissions.update(ROLE_PERMISSIONS.get(role, []))
            # Roles are defined as permissions in `role:<role>` format
            permissions.add(f"role:{role}")

        # LangGraph uses this information to identify the user
        # and evaluate their permissions.
        return {
            "identity": user_id,
            "is_authenticated": True,
            "permissions": list(permissions),
        }

    except (ValueError, InvalidTokenError, KeyError) as e:
        print(e)
        raise Auth.exceptions.HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )


# ============================================================
# 5. Default security policy
# ============================================================

# This handler is called when no specific authorization
# rule matches the requested action.
#
# It implements the security principle:
# "Deny by default".
#
# Any action that is not explicitly authorized is forbidden.
#
# Note:
# CRON and STORE permissions are not defined.
# Therefore, they are denied by this default policy.
@auth.on
async def deny_all(
    ctx: Auth.types.AuthContext,
    value: dict,
):
    """
   We refuse all requests with no specific policy defined.
    """
    raise Auth.exceptions.HTTPException(
        status_code=403,
        detail="Access forbidden",
    )

# ============================================================
# 6. Permission verification
# ============================================================

# Check whether the authenticated user has the required
# permission to perform a specific action.
#
# Administrators have unrestricted access because their
# permissions include the wildcard "*".
def require_permission(
    ctx: Auth.types.AuthContext,
    permission: str,
):
    if "*" in ctx.user.permissions:
        return
    
    if permission not in ctx.user.permissions:
        raise Auth.exceptions.HTTPException(
            status_code=403,
            detail=f"Permission required: {permission}",
        )


# ============================================================
# 7. Assign resource ownership
# ============================================================

# Assign the authenticated user's identity as the owner
# of a newly created resource.
#
# The owner is stored in the resource metadata.
#
# This allows the application to associate each resource
# with the user who created it.

def set_owner(
    ctx: Auth.types.AuthContext,
    value: dict,
):
    metadata = value.setdefault("metadata", {})
    metadata["owner"] = ctx.user.identity

# ============================================================
# 8. Filter resources based on ownership
# ============================================================

# Administrators can access all resources.
#
# Regular users can only access resources whose owner
# matches their own identity.
#
# The returned dictionary is used as a resource filter.
def owner_filter(ctx: Auth.types.AuthContext):
    if "role:admin" in ctx.user.permissions:
        return {}
    return {"owner": ctx.user.identity}

# ============================================================
# 9. Create reusable authorization handlers
# ============================================================

# This factory generates authorization handlers
# for different LangGraph actions.
#
# Parameters:
# - permission: the permission required for the action
# - create: whether the action creates a new resource
#
# The generated handler:
# 1. Checks the required permission.
# 2. Assigns ownership if the resource is created.
# 3. Returns the ownership filter.
def make_handler(
    permission: str,
    *,
    create: bool = False,
):
    async def handler(
        ctx: Auth.types.AuthContext,
        value: dict,
    ):
        require_permission(ctx, permission)

        if create:
            set_owner(ctx, value)

        return owner_filter(ctx)

    return handler

# ============================================================
# 10. Authorization for thread execution
# ============================================================

# This handler defines the authorization rules
# for creating and executing a thread run.
#
# It also prevents regular users from modifying
# the system prompt through the run context.
@auth.on.threads.create_run
async def on_create_run(
    ctx: Auth.types.AuthContext,
    value: Auth.types.on.threads.create_run.value,
):
    # Vérification des permissions
    permissions = ctx.user.permissions
    kwargs = value.get("kwargs") or {}
    run_context = kwargs.get("context") or {}


    # ----------------------------------------------------
    # Protect the system prompt
    # ----------------------------------------------------

    # If the request attempts to modify the system prompt,
    # only administrators are allowed to do so.
    #
    # Regular users cannot override the system prompt.
    if "system_prompt" in run_context:
        if "*" not in permissions and "role:admin" not in permissions:
            raise Auth.exceptions.HTTPException(
                status_code=403,
                detail="Modification du system_prompt interdite.",
            )

    require_permission(ctx, "threads:run")

    # ----------------------------------------------------
    # Apply ownership restrictions
    # ----------------------------------------------------

    # If the run is associated with an existing thread,
    # apply the ownership filter.
    #
    # Regular users can only execute runs on their own threads.
    # Administrators can execute runs on any thread.
    if value.get("thread_id"):
        return owner_filter(ctx)
    # If the run has no thread ID, it is stateless.
    # No thread ownership filter is required.
    return None

# ============================================================
# 11. Thread authorization rules
# ============================================================

# Define the permissions required for each thread operation.

# Threads
auth.on.threads.create(make_handler("threads:create", create=True))
auth.on.threads.read(make_handler("threads:read"))
#auth.on.threads.create_run(make_handler("threads:run"))
auth.on.threads.search(make_handler("threads:search"))
auth.on.threads.update(make_handler("threads:update"))
auth.on.threads.delete(make_handler("threads:delete"))

# ============================================================
# 12. Assistant authorization rules
# ============================================================

# Define the permissions required for each assistant operation.

# Assistants
auth.on.assistants.create(make_handler("assistants:create", create=True))
auth.on.assistants.read(make_handler("assistants:read"))
auth.on.assistants.update(make_handler("assistants:update"))
auth.on.assistants.delete(make_handler("assistants:delete"))
auth.on.assistants.search(make_handler("assistants:search"))
