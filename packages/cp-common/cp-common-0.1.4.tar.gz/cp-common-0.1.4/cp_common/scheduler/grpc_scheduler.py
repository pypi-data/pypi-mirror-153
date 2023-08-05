import uuid
from concurrent import futures

import grpc

from cp_common.log import logger
from cp_common.scheduler.protos.agent_pb2 import (
    CurrencyResponse,
    GetTaskRequest,
    GetTaskResponse,
    HeartBeatRequest,
    PingRequest,
    PongResponse,
    TaskResultRequest,
)
from cp_common.scheduler.protos.agent_pb2_grpc import (
    AgentService,
    add_AgentServiceServicer_to_server,
)


class MyAgentService(AgentService):
    def Ping(self, request, context):
        return PongResponse(msg="pong")

    def HeartBeat(self, request, context):
        return CurrencyResponse(msg="heartbeat ok!", code=200)

    def Task(self, request, context):
        _worker_name = request.worker_name
        logger.info(request)

        logger.info(f"{_worker_name} is online!")
        # while True:
        #     _task_queue, _task_info = REDIS_CONN.brpop(
        #         "worker:" + _worker_name + ":task"
        #     )
        #     logger.info(_task_info)
        #     yield GetTaskResponse(
        #         msg="send task",
        #         code=201,
        #         msg_type="task",
        #         task_id=uuid.uuid4().hex,
        #         task_info={"task_args": _task_info},
        #     )


def run_server() -> None:
    logger.info("grpc server runing ....")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_AgentServiceServicer_to_server(MyAgentService(), server)
    server.add_insecure_port("[::]:9002")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logger.info("start grpc server ...")
    run_server()
