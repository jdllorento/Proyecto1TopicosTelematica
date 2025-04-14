import grpc
import redis
import json
from microservices import calculator_pb2
from microservices import calculator_pb2_grpc
from concurrent import futures


class SumService(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        result = request.num1 + request.num2
        print(f"Suma directa: {request.num1} + {request.num2} = {result}")
        return calculator_pb2.OperationResponse(result=result)


def process_pending_tasks():
    print("Buscando tareas pendientes en Redis...")
    r = redis.Redis(host='localhost', port=6379, db=0)

    while True:
        task = r.lpop("task_queue")  # Quita el primero de la cola
        if task is None:
            break  # No hay más tareas

        data = json.loads(task)
        if data["service"] == "add":
            nums = data["data"]
            result = nums["num1"] + nums["num2"]
            print(
                f"Procesando tarea pendiente de suma: {nums['num1']} + {nums['num2']} = {result}")
        else:
            # Si no es una tarea para este microservicio, volverla a poner al final de la cola
            r.rpush("task_queue", task)


def serve():

    process_pending_tasks()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(SumService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Sum Service running on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
