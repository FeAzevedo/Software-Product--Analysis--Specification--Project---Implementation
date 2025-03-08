from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

#Aqui defino a classe do meu objeto

class Veiculo(BaseModel):
    modelo: str
    valor: float
    cor: str
    ano: int
    
banco_de_dados_provisorio = []    
    

@app.get("/")
def read_root():
    return {"Hello": "World"}


#Cadastro de veículos

@app.post("/veiculos")
async def cadastra_veiculos(veiculo:Veiculo):
    print("Vou cadastrar um veículo")
    print(f"Modelo: {veiculo.modelo}")
    print(f"Valor: {veiculo.valor}")
    print(f"Cor: {veiculo.cor}")
    print(f"Ano: {veiculo.ano}")
    
    banco_de_dados_provisorio.append(veiculo)
   
    return veiculo


@app.get("/veiculos")
async def lista_veiculos():
    return banco_de_dados_provisorio
    



