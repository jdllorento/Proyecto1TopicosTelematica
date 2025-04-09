
import setup_paths
from microservices import calculator_pb2
from microservices import calculator_pb2_grpc
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
    response = sum_stub.Add(request)
    return {"operation": "add", "result": response.result}


@app.get("/subtract/{num1}/{num2}")
def subtract_numbers(num1: float, num2: float):
    request = calculator_pb2.OperationRequest(num1=num1, num2=num2)
    response = sub_stub.Subtract(request)
    return {"operation": "subtract", "result": response.result}


@app.get("/multiply/{num1}/{num2}")
def multiply_numbers(num1: float, num2: float):
    request = calculator_pb2.OperationRequest(num1=num1, num2=num2)
    response = mul_stub.Multiply(request)
    return {"operation": "multiply", "result": response.result}
