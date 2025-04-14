import grpc
import redis
import json
import threading
from microservices import calculator_pb2
from microservices import calculator_pb2_grpc
from concurrent import futures


class SubtractService(calculator_pb2_grpc.CalculatorServicer):
    def Subtract(self, request, context):
        result = request.num1 - request.num2
        print(f"Resta directa: {request.num1} - {request.num2} = {result}")
        return calculator_pb2.OperationResponse(result=result)


def process_pending_tasks():
    print("Buscando tareas pendientes en Redis para resta...")
    r = redis.Redis(host='localhost', port=6379, db=0)

    while True:
        task = r.lpop("task_queue")
        if task is None:
            break

        data = json.loads(task)
        if data["service"] == "subtract":
            nums = data["data"]
            result = nums["num1"] - nums["num2"]
            print(
                f"Procesando tarea pendiente de resta: {nums['num1']} - {nums['num2']} = {result}")

            processed = {
                "operation": "Subtraction",
                "num1": nums["num1"],
                "num2": nums["num2"],
                "result": result
            }

            r.rpush("processed_results", json.dumps(processed))

        else:
            r.rpush("task_queue", task)


def serve():
    threading.Thread(target=process_pending_tasks, daemon=True).start()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        SubtractService(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("Subtract Service running on port 50052...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
