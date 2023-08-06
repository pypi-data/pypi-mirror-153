import asyncio
import json
import os

import grpc

import kubefox_pb2 as kf
import kubefox_pb2_grpc as kf_rpc


class ComponentService(kf_rpc.ComponentServiceServicer):
    async def CallFunction(self, req: kf.KubeFoxData, ctx: grpc.aio.ServicerContext) -> kf.KubeFoxData:
        # if req.type == "io.kubefox.http.v1":
        #     res = handler.entry_point(sdk.HttpMsg(broker_msg=req))
        # else:
        # res = handler.entry_point(req)
        print(req.values)
        
        res = "Hellow"

        return kf.KubeFoxData(content=bytes(res, "utf-8"), content_type="text/plain")

        # if res is None:
        #     return kf.UnitMsg()
        # if isinstance(res, kf.UnitMsg):
        #     return res
        # if isinstance(res, bytes):
        #     return kf.UnitMsg(content=res, content_type="application/octet-stream")
        # if isinstance(res, dict):
        #     return kf.UnitMsg(content=json.dumps(res), content_type="application/json")

        # try:
        #     return kf.UnitMsg(content=json.dumps(res.__dict__), content_type="application/json")
        # except AttributeError:
        #     pass

        # return kf.UnitMsg(content=bytes(str(res), "utf-8"), content_type="text/plain")

    async def GetTelemetry(self, req: kf.TelemetryRequest, ctx: grpc.aio.ServicerContext) -> kf.TelemetryResponse:
        return kf.TelemetryResponse(healthy=True)


async def serve() -> None:
    server = grpc.aio.server()
    kf_rpc.add_ComponentServiceServicer_to_server(ComponentService(), server)

    runtime_addr = os.getenv("RUNTIME_ADDR", "localhost:6060")
    server.add_insecure_port(runtime_addr)

    print(f"Starting gRPC server on {runtime_addr}")

    await server.start()
    await server.wait_for_termination()


def start() -> None:
    # TODO: This isn't quite right, should use `asyncio.run(serve())`
    #       https://github.com/grpc/grpc/issues/26123
    asyncio.new_event_loop().run_until_complete(serve())


if __name__ == "__main__":
    # TODO: If this script run as main should search for all functions with annotations
    start()
