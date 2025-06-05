from loguru import logger


def add_custom_fields(record):
    record["extra"]["app_name"] = "rockapp-api"
    return True


logger.add("/app/logs/app.json", format="{time:MMMM D, YYYY > HH:mm:ss!UTC} | {level} | {message}", serialize=True, rotation="500 MB", filter=add_custom_fields)

