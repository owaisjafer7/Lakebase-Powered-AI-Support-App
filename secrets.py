from databricks.sdk import WorkspaceClient
from databricks.sdk.service import workspace
import getpass


w = WorkspaceClient()

scope_name = "lakebase"

try:
    w.secrets.create_scope(
        scope=scope_name
    )
    print(f"Created secret scope: {scope_name}")

except Exception:
    print(f"Secret scope {scope_name} already exists")


secrets = {
    "host": getpass.getpass("Lakebase host: "),
    "port": "5432",
    "database": "databricks_postgres",
    "username": "student",
    "password": getpass.getpass("Lakebase password: "),
}


for key, value in secrets.items():

    w.secrets.put_secret(
        scope=scope_name,
        key=key,
        string_value=value
    )

    print(f"Stored secret: {key}")

w.secrets.put_acl(
    scope=scope_name,
    principal="users",
    permission=workspace.AclPermission.READ
)


print("Lakebase secrets setup complete.")