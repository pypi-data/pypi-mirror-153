import asyncio
import logging
import os
from typing import Callable

import grpc

from . import kubefox_pb2 as kf
from . import kubefox_pb2_grpc as kf_rpc


logging.basicConfig(level=logging.INFO)


class ComponentService(kf_rpc.ComponentServiceServicer):

    entrypoint: Callable = None

    def __init__(self, entrypoint: Callable) -> None:
        self.entrypoint = entrypoint

    async def CallFunction(self, req: kf.KubeFoxData, ctx: grpc.aio.ServicerContext) -> kf.KubeFoxData:
        kit = Kit(req)
        self.entrypoint(kit)
        return kit.res

    async def GetTelemetry(self, req: kf.TelemetryRequest, ctx: grpc.aio.ServicerContext) -> kf.TelemetryResponse:
        return kf.TelemetryResponse(healthy=True)


class KubeFox:

    entrypoint: Callable = None

    def entrypoint(self, func: Callable):
        self.entrypoint = func
        return func

    def start(self) -> None:
        # TODO: This isn't quite right, should use `asyncio.run(serve())`
        #       https://github.com/grpc/grpc/issues/26123
        asyncio.new_event_loop().run_until_complete(self._serve())

    async def _serve(self) -> None:
        server = grpc.aio.server()
        kf_rpc.add_ComponentServiceServicer_to_server(ComponentService(self.entrypoint), server)

        runtime_addr = os.getenv("RUNTIME_ADDR", "localhost:6060")
        server.add_insecure_port(runtime_addr)

        print(f"Starting gRPC server on {runtime_addr}")

        await server.start()
        await server.wait_for_termination()


class Kit:

    log: logging.Logger = logging.getLogger("kit")
    req: kf.KubeFoxData = None
    res: kf.KubeFoxData = kf.KubeFoxData()

    def __init__(self, req: kf.KubeFoxData) -> None:
        self.req = req

        h = logging.StreamHandler()
        h.setLevel(logging.INFO)
        self.log.addHandler(h)
