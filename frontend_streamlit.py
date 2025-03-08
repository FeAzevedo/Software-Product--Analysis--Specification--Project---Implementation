import streamlit as st
import requests

# Definir a URL da API FastAPI
API_URL = "http://127.0.0.1:8000"

st.title("Cadastro de Veículos")

# Criar o formulário para cadastro de veículos
with st.form("cadastro_veiculo"):
    st.subheader("Cadastrar Novo Veículo")
    
    
    modelo = st.text_input('Modelo')
    valor = st.number_input('Valor', min_value=0.0, format="%.2f")
    cor = st.selectbox('Cor', ['vermelho', 'azul', 'verde', 'preto', 'prata', 'branco'])
    ano = st.number_input('Ano', min_value=2000, max_value=2100, step=1)

    submit_button = st.form_submit_button("Cadastrar")

    if submit_button:
        if modelo and valor and ano:
            veiculo = {
                "modelo": modelo,
                "valor": valor,
                "cor": cor,
                "ano": ano
            }

            response = requests.post(f"{API_URL}/veiculos", json=veiculo)

            if response.status_code == 200:
                st.success("Veículo cadastrado com sucesso!")
             
            else:
                st.error("Erro ao cadastrar veículo.")
        else:
            st.warning("Preencha todos os campos antes de enviar.")            
        

# Exibir a lista de veículos cadastrados
st.subheader("Veículos Cadastrados")

response = requests.get(f"{API_URL}/veiculos")

if response.status_code == 200:
    veiculos = response.json()
    
    if veiculos:
        for veiculo in veiculos:
            st.write(f"📌 **{veiculo['modelo']}** - {veiculo['cor']} - {veiculo['ano']} - R$ {veiculo['valor']:.2f}")
    else:
        st.info("Nenhum veículo cadastrado ainda.")
else:
    st.error("Erro ao carregar os veículos cadastrados.")
