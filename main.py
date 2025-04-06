from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


# Aqui defino a classe do meu objeto
class Veiculo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    modelo: str
    valor: float
    cor: str
    ano: int
    

sqlite_file_name = "database_local.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()  


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Cadastro de veículos
@app.post("/veiculos")
def cadastra_veiculos(veiculo: Veiculo, session: SessionDep) -> Veiculo: 
    session.add(veiculo)
    session.commit()
    session.refresh(veiculo)
    return veiculo


@app.get("/veiculos")
def lista_veiculos(session: SessionDep) -> list[Veiculo]:
    veiculos = session.exec(select(Veiculo)).all()
    return veiculos


# Rota DELETE para excluir um veículo
@app.delete("/veiculos/{veiculo_id}")
def excluir_veiculo(veiculo_id: int, session: SessionDep):
    veiculo = session.get(Veiculo, veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    
    session.delete(veiculo)
    session.commit()
    return {"message": "Veículo excluído com sucesso"}
