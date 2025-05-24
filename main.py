from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List

# Inicialização do FastAPI
app = FastAPI()

# Definição do modelo de dados
class Veiculo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    modelo: str
    valor: float
    cor: str
    ano: int

# Configuração do banco de dados
sqlite_file_name = "database_local.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=False)

def criar_db():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    criar_db()

# Rota para cadastrar um novo veículo
@app.post("/veiculos")
def cadastrar_veiculo(veiculo: Veiculo):
    with Session(engine) as session:
        session.add(veiculo)
        session.commit()
        session.refresh(veiculo)
        return veiculo

# Rota para listar todos os veículos
@app.get("/veiculos", response_model=List[Veiculo])
def listar_veiculos():
    with Session(engine) as session:
        veiculos = session.exec(select(Veiculo)).all()
        return veiculos

# Rota para deletar um veículo
@app.delete("/veiculos/{veiculo_id}")
def deletar_veiculo(veiculo_id: int):
    with Session(engine) as session:
        veiculo = session.get(Veiculo, veiculo_id)
        if not veiculo:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        session.delete(veiculo)
        session.commit()
        return {"ok": True}

# Rota para atualizar os dados de um veículo
@app.put("/veiculos/{veiculo_id}")
def atualizar_veiculo(veiculo_id: int, veiculo_atualizado: Veiculo):
    with Session(engine) as session:
        veiculo = session.get(Veiculo, veiculo_id)
        if not veiculo:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")

        veiculo.modelo = veiculo_atualizado.modelo
        veiculo.valor = veiculo_atualizado.valor
        veiculo.cor = veiculo_atualizado.cor
        veiculo.ano = veiculo_atualizado.ano

        session.add(veiculo)
        session.commit()
        session.refresh(veiculo)
        return veiculo
