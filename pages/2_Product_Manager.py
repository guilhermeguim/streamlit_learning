from sqlalchemy import create_engine
import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Product Manager",
    layout='wide',
)

st.title("Product Manager")

conn = create_engine("mysql://umjvmq4d8kjetiuc:mowxpy13KGH1shBOvjxF@biapzcnvuo639g5rpxcn-mysql.services.clever-cloud.com:3306/biapzcnvuo639g5rpxcn?charset=utf8mb4")

st.header("Assign Tag")    

with st.form(key='tag_insert'):
    
    col1, col2, col3 = st.columns(3)
    
    SQL_Query = pd.read_sql('SELECT * FROM biapzcnvuo639g5rpxcn.produtos', conn)

    df = pd.DataFrame(SQL_Query)

    df.columns = ['Product ID','Name','Code','Description','Category','Manufacturing Cost ($)','Sales Value ($)','Creation Date']

    name_list = df['Name'].tolist()
    code_list = df['Code'].tolist()
    id_list = df['Product ID'].tolist()

    name_code_id = []

    for i in range(len(name_list)):
        name_code_un = 'ID: ' + str(id_list[i]) +  ' , Name: ' + str(name_list[i])+ ' , Code: ' +str(code_list[i])
        name_code_id.append(name_code_un)


    with col1:
        
        tag_read = st.text_input('RFID Tag Value:', '',placeholder='Scan Your RFID Tag')
        
    with col2:
        
        to_tag = st.selectbox('Select a Product:',name_code_id)

    with col3:
        
        lot  = st.number_input('Lot:',min_value=0,format='%i')
        
    if st.form_submit_button(label='Assign'):
        to_tag = to_tag.replace('ID:', '')
        to_tag = to_tag.replace(' , Name: ', ':')
        to_tag = to_tag.replace(' , Code: ', ':')
        selected = to_tag.split(':')
        id=conn.execute("INSERT INTO  biapzcnvuo639g5rpxcn.produtotag (id_tag, id_produto, lote) \
                        VALUES ({0}, {1}, {2})"
                        .format(tag_read,selected[0],lot))
        
    else:
        SQL_Query = pd.read_sql('SELECT * FROM biapzcnvuo639g5rpxcn.produtos', conn)

        df = pd.DataFrame(SQL_Query)

        df.columns = ['Product ID','Name','Code','Description','Category','Manufacturing Cost ($)','Sales Value ($)','Creation Date']

        name_list = df['Name'].tolist()
        code_list = df['Code'].tolist()

        name_code = []

        for i in range(len(name_list)):
            name_code_un = str(name_list[i])+':'+str(code_list[i])
            name_code.append(name_code_un)
        
st.header("Insert Product")    

with st.form(key='insert'):
    
    col1, col2, col3 = st.columns(3)

    with col1:
        nome = st.text_input('Name:', '',placeholder='Type Name')
        

    with col2:
        
        codigo = st.text_input('Code:', '',placeholder='Type Code')
        
    with col3: 
        
        categoria = st.selectbox('Category',('Carros', 'Motos', 'Caminhões', 'Outros'))
        
    descricao = st.text_input('Description:', '',placeholder='Type Description')

    col1, col2 = st.columns(2)
        
    with col1:

        custo = st.number_input('Manufacturing Cost',min_value=0.00)
        custo = round(custo,2)

        
    with col2:

        valor = st.number_input('Sales Value:',min_value=0.00)
        valor = round(valor,2)
        
    col1, col2 = st.columns(2)
    
    with col1:
        
        data  = st.date_input('Date:', datetime.today())
        
    with col2:
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        hora = st.text_input('Hour:', value=current_time ,max_chars=8)

        
    
    if st.form_submit_button(label='Submit'):
            date_time = str(data) + ' ' + str(hora)
            id=conn.execute("INSERT INTO  biapzcnvuo639g5rpxcn.produtos (nome_produto, code, descricao_produto, categoria, custo_fabricacao, valor_venda, created_at) \
                        VALUES ('{0}', '{1}', '{2}', '{3}', {4}, {5},'{6}')"
                        .format(nome,codigo,descricao,categoria,custo,valor,date_time))
    else:
        pass


st.header("Delete Product")

with st.form(key='delete'):
    
    SQL_Query = pd.read_sql('SELECT * FROM biapzcnvuo639g5rpxcn.produtos', conn)

    df = pd.DataFrame(SQL_Query)

    df.columns = ['Product ID','Name','Code','Description','Category','Manufacturing Cost ($)','Sales Value ($)','Creation Date']

    name_list = df['Name'].tolist()
    code_list = df['Code'].tolist()

    name_code = []

    for i in range(len(name_list)):
        name_code_un = str(name_list[i])+': '+str(code_list[i])
        name_code.append(name_code_un)

    to_delete = st.selectbox('Select a Product:',name_code)

    if st.form_submit_button(label='Delete'):
        selected = to_delete.split(': ')
        id=conn.execute("DELETE FROM biapzcnvuo639g5rpxcn.produtos WHERE nome_produto = '{0}' AND code = '{1}'"
                            .format(selected[0],selected[1]))
    else:
        SQL_Query = pd.read_sql('SELECT * FROM biapzcnvuo639g5rpxcn.produtos', conn)

        df = pd.DataFrame(SQL_Query)

        df.columns = ['Product ID','Name','Code','Description','Category','Manufacturing Cost ($)','Sales Value ($)','Creation Date']
        
        name_list = df['Name'].tolist()
        code_list = df['Code'].tolist()

        name_code = []

        for i in range(len(name_list)):
            name_code_un = str(name_list[i])+': '+str(code_list[i])
            name_code.append(name_code_un)

st.header("Product Viewer")

with st.form(key='view'):
    
    SQL_Query = pd.read_sql('SELECT * FROM biapzcnvuo639g5rpxcn.produtos', conn)

    df = pd.DataFrame(SQL_Query)

    df.columns = ['Product ID','Name','Code','Description','Category','Manufacturing Cost ($)','Sales Value ($)','Creation Date']

    nome_filtro = st.text_input('Filter By Name:', '',placeholder='Type Name')

    if st.form_submit_button(label='Search'):
        df = df[df['Name'].str.contains(str(nome_filtro))]
        st.dataframe(df,use_container_width = True)
    else:
        st.dataframe(df,use_container_width = True)
        

