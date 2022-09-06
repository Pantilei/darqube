import os


class Configs:

    app_configs = {
        "db_url": os.environ.get("MONGODB_URL")
    }
