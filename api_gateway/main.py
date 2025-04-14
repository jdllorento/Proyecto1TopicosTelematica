
import setup_paths
from microservices import calculator_pb2
from microservices import calculator_pb2_grpc
from .redis_mom import send_to_queue
from fastapi import FastAPI
import grpc

app = FastAPI()

# Crear conexiones gRPC con los microservicios
sum_channel = grpc.insecure_channel("localhost:50051")
sum_stub = calculator_pb2_grpc.CalculatorStub(sum_channel)

sub_channel = grpc.insecure_channel("localhost:50052")
sub_stub = calculator_pb2_grpc.CalculatorStub(sub_channel)

mul_channel = grpc.insecure_channel("localhost:50053")
mul_stub = calculator_pb2_grpc.CalculatorStub(mul_channel)


@app.get("/add/{num1}/{num2}")
def add_numbers(num1: float, num2: float):
    request = calculator_pb2.OperationRequest(num1=num1, num2=num2)
    try:
        response = sum_stub.Add(request)
        return {"operation": "add", "result": response.result}
    except grpc.RpcError:
        send_to_queue("add", {"num1": num1, "num2": num2})
        return {"message": "Servicio de suma no disponible, operación encolada."}


@app.get("/subtract/{num1}/{num2}")
def subtract_numbers(num1: float, num2: float):
    request = calculator_pb2.OperationRequest(num1=num1, num2=num2)
    try:
        response = sub_stub.Subtract(request)
        return {"operation": "subtract", "result": response.result}
    except grpc.RpcError:
        send_to_queue("subtract", {"num1": num1, "num2": num2})
        return {"message": "Servicio de resta no disponible, operación encolada."}


@app.get("/multiply/{num1}/{num2}")
def multiply_numbers(num1: float, num2: float):
    request = calculator_pb2.OperationRequest(num1=num1, num2=num2)
    try:
        response = mul_stub.Multiply(request)
        return {"operation": "multiply", "result": response.result}
    except grpc.RpcError:
        send_to_queue("multiply", {"num1": num1, "num2": num2})
        return {"message": "Servicio de multiplicación no disponible, operación encolada."}
