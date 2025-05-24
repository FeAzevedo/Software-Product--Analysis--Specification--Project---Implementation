from typing import Annotated, Optional, List
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Modelo do banco
class Veiculo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    modelo: str
    valor: float
    cor: str
    ano: int

# Configuração do banco SQLite
sqlite_file_name = "database_local.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Criação da tabela
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Sessão do banco
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Inicialização FastAPI
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# POST - Cadastrar veículo
@app.post("/veiculos", response_model=Veiculo)
def cadastrar_veiculo(veiculo: Veiculo, session: SessionDep):
    session.add(veiculo)
    session.commit()
    session.refresh(veiculo)
    return veiculo

# GET - Listar todos os veículos
@app.get("/veiculos", response_model=List[Veiculo])
def listar_veiculos(session: SessionDep):
    return session.exec(select(Veiculo)).all()

# PUT - Alterar veículo
@app.put("/veiculos/{veiculo_id}", response_model=Veiculo)
def alterar_veiculo(veiculo_id: int, veiculo: Veiculo, session: SessionDep):
    db_veiculo = session.get(Veiculo, veiculo_id)
    if not db_veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    db_veiculo.modelo = veiculo.modelo
    db_veiculo.valor = veiculo.valor
    db_veiculo.cor = veiculo.cor
    db_veiculo.ano = veiculo.ano

    session.add(db_veiculo)
    session.commit()
    session.refresh(db_veiculo)
    return db_veiculo
