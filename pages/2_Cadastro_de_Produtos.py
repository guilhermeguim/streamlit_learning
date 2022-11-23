from sqlalchemy import create_engine
import streamlit as st
from datetime import datetime

st.title("Cadastro de Produtos")

conn = create_engine("mysql://umjvmq4d8kjetiuc:mowxpy13KGH1shBOvjxF@biapzcnvuo639g5rpxcn-mysql.services.clever-cloud.com:3306/biapzcnvuo639g5rpxcn?charset=utf8mb4")

with st.form(key='cadastro'):

    col1, col2, col3 = st.columns(3)

    with col1:

        tag = st.text_input('ID Tag:', '',placeholder='Scan Your Tag')

        lote = st.number_input('Lote:',min_value=0,format='%i')
        
        data  = st.date_input('Date:', datetime.today())

    with col2:

        nome = st.text_input('Nome do Produto:', '',placeholder='Type Name')

        custo = st.number_input('Custo de Fabricação:',min_value=0.00)
        custo = round(custo,2)

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        hora = st.text_input('Time:', value=current_time ,placeholder='Type Description',max_chars=8)

    with col3:

        descricao = st.text_input('Descrição do Produto:', '',placeholder='Type Description')

        valor = st.number_input('Valor de Venda:',min_value=0.00)
        valor = round(valor,2)

    if st.form_submit_button(label='Cadastrar'):
            date_time = str(data) + ' ' + str(hora)
            id=conn.execute("INSERT INTO  biapzcnvuo639g5rpxcn.produtos (descricao_produto, nome_produto, lote, id_tag, custo_fabricacao, valor_venda, status,created_at) \
                        VALUES ('{1}', '{3}', {4}, {0}, {5}, {6},'{7}','{2}')".format(tag,descricao,date_time,nome,lote,custo,valor,'E'))
    else:
        pass

        

        

    