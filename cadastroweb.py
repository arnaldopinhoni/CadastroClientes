import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

#display title
st.title("cadastro medicar web")
st.markdown("**Cadastro de pacientes**")

#establishing a google sheet connection
conn = st.connection("gsheets", type=GSheetsConnection)

 # Fetch existing vendors data
existing_data = conn.read(worksheet="pagina1", usecols=list(range(3)), ttl=5)
existing_data = existing_data.dropna(how='all')  # Remove rows where all elements are NaN

#Formulario de cadastro
st.subheader("Novo cadastro")
with st.form(key="form_cadastro"):
    nome = st.text_input("Nome")
    cpf = st.text_input("CPF")
    idade = st.number_input("Idade", min_value=0, max_value=150, step=1)

    submitted = st.form_submit_button("Cadastrar")

    if submitted:
        # Validação simples
        if not nome or not cpf or not idade:
            st.warning("Preencha todos os campos!")
        # Verifica se o CPF já existe
        elif cpf in existing_data['CPF'].astype(str).values:
            st.warning("CPF já cadastrado!")
        else:
            # Cria novo registro
            novo_paciente = pd.DataFrame([[nome, cpf, int(idade)]], columns=["Nome", "CPF", "Idade"])
            df_final = pd.concat([existing_data, novo_paciente], ignore_index=True)
            # Atualiza a planilha
            conn.update(worksheet="cadastrodeclientes", data=df_final)
            st.success("Cadastro realizado com sucesso!")
            st.experimental_rerun()  # Atualiza exibição
