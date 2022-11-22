from sqlalchemy import create_engine
import streamlit as st
import pandas as pd
import datetime

st.markdown("# Cadastro de Produtos")

ID_Tag = st.text_input('ID Tag:', '',placeholder='Scan Your Tag')

descricao = st.text_input('Descrição do Produto:', '',placeholder='Type Description')

data  = st.date_input('Date:', placeholder=datetime.date.today())