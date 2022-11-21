from sqlalchemy import create_engine
import streamlit as st
import pandas as pd

user = 'umjvmq4d8kjetiuc'
password = 'mowxpy13KGH1shBOvjxF'
host = 'biapzcnvuo639g5rpxcn-mysql.services.clever-cloud.com'
port = 3306
database = 'biapzcnvuo639g5rpxcn'

conn = create_engine("mysql://umjvmq4d8kjetiuc:mowxpy13KGH1shBOvjxF@biapzcnvuo639g5rpxcn-mysql.services.clever-cloud.com:3306/biapzcnvuo639g5rpxcn?charset=utf8mb4")

SQL_Query = pd.read_sql('SELECT custo_fabricacao,valor_venda FROM biapzcnvuo639g5rpxcn.produtos', conn)

st.write("Dashboard Test")

df = pd.DataFrame(SQL_Query,columns=['custo_fabricacao','valor_venda'])

st.line_chart(df)

if st.button('TESTE'):
    id=conn.execute("INSERT INTO  biapzcnvuo639g5rpxcn.produtos (descricao_produto, nome_produto, lote, id_tag, custo_fabricacao, valor_venda, status,created_at) \
                  VALUES ('Teste4', 'Teste4', 5, 4, 20.0, 15.0,'E','2022-11-21 00:00:00')")
else:
    pass
