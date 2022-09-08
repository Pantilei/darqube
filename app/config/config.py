import os


class Configs:

    app_configs = {
        "db_url": os.environ.get("MONGODB_URL") or "mongodb://localhost:27017/darqube",
        "db_name": os.environ.get("DB_NAME") or "darqube",

        "api_v1": "/api/v1"
    }
