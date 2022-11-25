from sqlalchemy import create_engine
import streamlit as st
import pandas as pd

conn = create_engine("mysql://umjvmq4d8kjetiuc:mowxpy13KGH1shBOvjxF@biapzcnvuo639g5rpxcn-mysql.services.clever-cloud.com:3306/biapzcnvuo639g5rpxcn?charset=utf8mb4")

@st.experimental_memo
def get_data() -> pd.DataFrame:
    SQL_Query = pd.read_sql('SELECT * FROM biapzcnvuo639g5rpxcn.produtos', conn)
    data = pd.DataFrame(SQL_Query)
    
    return data

df = get_data()



