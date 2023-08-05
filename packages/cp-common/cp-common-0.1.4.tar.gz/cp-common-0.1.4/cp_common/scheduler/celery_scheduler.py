from celery import Celery, Task

from cp_common.log import logger


class Config:
    broker_url = "redis://:123456@177.17.0.3:6379/0"
    result_backend = "redis://:123456@177.17.0.3:6379/0"
    task_serializer = "json"
    result_expires = 60 * 60 * 24
    accept_content = ["json"]
    task_default_queue = "default"
    timezone = "Asia/Shanghai"


app = Celery("cp_common")
app.config_from_object(Config)


class CustomTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        logger.info("task done: {0}".format(retval))
        return super(CustomTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.warning("task fail, reason: {0}".format(exc))
        return super(CustomTask, self).on_failure(exc, task_id, args, kwargs, einfo)
