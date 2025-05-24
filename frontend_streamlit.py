import streamlit as st
import requests

st.title("Cadastro de Veículos")

# Cadastro de novo veículo
st.header("Cadastrar Novo Veículo")
with st.form("form_cadastro"):
    modelo = st.text_input("Modelo")
    valor = st.number_input("Valor")
    cor = st.text_input("Cor")
    ano = st.number_input("Ano", step=1)
    submitted = st.form_submit_button("Cadastrar")

    if submitted:
        dados = {"modelo": modelo, "valor": valor, "cor": cor, "ano": ano}
        response = requests.post("http://localhost:8000/veiculos", json=dados)
        if response.status_code == 200:
            st.success("Veículo cadastrado com sucesso!")
        else:
            st.error("Erro ao cadastrar veículo.")

# Listagem e ações dos veículos
st.header("Veículos Cadastrados")
response = requests.get("http://localhost:8000/veiculos")
if response.status_code == 200:
    veiculos = response.json()
    for veiculo in veiculos:
        with st.expander(f"{veiculo['modelo']} - {veiculo['ano']}"):
            st.write(f"Valor: R$ {veiculo['valor']}")
            st.write(f"Cor: {veiculo['cor']}")

            # Botão para deletar
            if st.button(f"Excluir {veiculo['id']}"):
                response = requests.delete(f"http://localhost:8000/veiculos/{veiculo['id']}")
                if response.status_code == 200:
                    st.success("Veículo excluído com sucesso!")
                else:
                    st.error("Erro ao excluir veículo.")

            # Formulário de edição
            with st.form(f"form_edit_{veiculo['id']}"):
                novo_modelo = st.text_input("Editar Modelo", value=veiculo["modelo"])
                novo_valor = st.number_input("Editar Valor", value=veiculo["valor"], key=f"valor_{veiculo['id']}")
                nova_cor = st.text_input("Editar Cor", value=veiculo["cor"])
                novo_ano = st.number_input("Editar Ano", value=veiculo["ano"], step=1, key=f"ano_{veiculo['id']}")

                submitted_edit = st.form_submit_button("Salvar alterações")
                if submitted_edit:
                    dados_atualizados = {
                        "modelo": novo_modelo,
                        "valor": novo_valor,
                        "cor": nova_cor,
                        "ano": novo_ano,
                    }
                    res = requests.put(f"http://localhost:8000/veiculos/{veiculo['id']}", json=dados_atualizados)
                    if res.status_code == 200:
                        st.success("Veículo atualizado com sucesso!")
                    else:
                        st.error("Erro ao atualizar veículo.")
else:
    st.error("Erro ao buscar veículos.")
