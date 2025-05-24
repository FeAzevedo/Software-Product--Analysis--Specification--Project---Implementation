import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Cadastro de Veículos")

# Formulário para cadastrar novo veículo
with st.form("form_cadastro"):
    st.subheader("Cadastrar Novo Veículo")

    modelo = st.text_input("Modelo")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")
    cor = st.selectbox("Cor", ["vermelho", "azul", "verde", "preto", "prata", "branco"])
    ano = st.number_input("Ano", min_value=2000, max_value=2100, step=1)
    placa = st.text_input("Placa do veículo")

    submitted = st.form_submit_button("Cadastrar")

    if submitted:
        if modelo and valor and ano:
            novo_veiculo = {
                "modelo": modelo,
                "valor": valor,
                "cor": cor,
                "ano": ano
                # a placa não será enviada
            }
            response = requests.post(f"{API_URL}/veiculos", json=novo_veiculo)
            if response.status_code == 200:
                st.success(f"Veículo cadastrado com sucesso! [Placa: {placa}]")
            else:
                st.error("Erro ao cadastrar veículo.")
        else:
            st.warning("Preencha todos os campos!")

st.markdown("---")
st.subheader("Veículos Cadastrados")

# Buscar veículos
response = requests.get(f"{API_URL}/veiculos")

if response.status_code == 200:
    veiculos = response.json()
    if veiculos:
        for veiculo in veiculos:
            st.write(f"📌 **{veiculo['modelo']}** - {veiculo['cor']} - {veiculo['ano']} - R$ {veiculo['valor']:.2f}")
            
            with st.expander(f"Editar {veiculo['modelo']}"):
                novo_modelo = st.text_input(f"Modelo - {veiculo['id']}", value=veiculo["modelo"])
                novo_valor = st.number_input(f"Valor - {veiculo['id']}", value=veiculo["valor"], format="%.2f")
                nova_cor = st.selectbox(f"Cor - {veiculo['id']}", ["vermelho", "azul", "verde", "preto", "prata", "branco"], index=["vermelho", "azul", "verde", "preto", "prata", "branco"].index(veiculo["cor"]))
                novo_ano = st.number_input(f"Ano - {veiculo['id']}", value=veiculo["ano"], min_value=2000, max_value=2100, step=1)
                nova_placa = st.text_input(f"Placa- {veiculo['id']}")

                if st.button(f"Alterar - ID {veiculo['id']}"):
                    dados_alterados = {
                        "modelo": novo_modelo,
                        "valor": novo_valor,
                        "cor": nova_cor,
                        "ano": novo_ano
                        # placa não é enviada
                    }
                    update_response = requests.put(f"{API_URL}/veiculos/{veiculo['id']}", json=dados_alterados)
                    if update_response.status_code == 200:
                        st.success(f"Veículo alterado com sucesso! [Placa informada: {nova_placa}]")
                    else:
                        st.error("Erro ao alterar o veículo.")
    else:
        st.info("Nenhum veículo cadastrado.")
else:
    st.error("Erro ao buscar veículos.")
