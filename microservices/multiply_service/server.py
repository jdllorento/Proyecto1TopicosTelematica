import grpc
import redis
import json
from microservices import calculator_pb2
from microservices import calculator_pb2_grpc
from concurrent import futures


class MultiplyService(calculator_pb2_grpc.CalculatorServicer):
    def Multiply(self, request, context):
        result = request.num1 * request.num2
        print(
            f"Multiplicación directa: {request.num1} * {request.num2} = {result}")
        return calculator_pb2.OperationResponse(result=result)


def process_pending_tasks():
    print("Buscando tareas pendientes en Redis para multiplicación...")
    r = redis.Redis(host='localhost', port=6379, db=0)

    while True:
        task = r.lpop("task_queue")
        if task is None:
            break

        data = json.loads(task)
        if data["service"] == "multiply":
            nums = data["data"]
            result = nums["num1"] * nums["num2"]
            print(
                f"Procesando tarea pendiente de multiplicación: {nums['num1']} * {nums['num2']} = {result}")

            processed = {
                "operation": "Multiplication",
                "num1": nums["num1"],
                "num2": nums["num2"],
                "result": result
            }

            r.rpush("processed_results", json.dumps(processed))

        else:
            r.rpush("task_queue", task)


def serve():
    process_pending_tasks()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        MultiplyService(), server)
    server.add_insecure_port("[::]:50053")
    server.start()
    print("Multiply Service running on port 50053...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
