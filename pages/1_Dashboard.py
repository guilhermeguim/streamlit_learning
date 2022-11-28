from sqlalchemy import create_engine
import streamlit as st
import plotly.express as px 
import pandas as pd
from time import sleep
from datetime import datetime
from PIL import Image


#page configuration
st.set_page_config(
    page_title="Production Dashboard",
    layout="wide",
)

image = Image.open('fho_png2.png')

with st.sidebar:
    st.image(image)

st.title("Production Dashboard")

#import datasets from MySQL
conn = create_engine("mysql://umjvmq4d8kjetiuc:mowxpy13KGH1shBOvjxF@biapzcnvuo639g5rpxcn-mysql.services.clever-cloud.com:3306/biapzcnvuo639g5rpxcn?charset=utf8mb4")

SQL_Query_prod = pd.read_sql('SELECT * FROM biapzcnvuo639g5rpxcn.produtos', conn)
df_prod = pd.DataFrame(SQL_Query_prod)
df_prod.columns = ['Product ID','Name','Code','Description','Category','Manufacturing Cost ($)','Sales Value ($)','Creation Date','Target']


SQL_Query_in = pd.read_sql('SELECT he.id_entrada, he.data_entrada, p.id_tag, p2.nome_produto, p2.meta FROM hist_entrada he INNER JOIN produtotag p ON p.id_tag = he.id_tag INNER JOIN produtos p2 ON p2.id_produto = p.id_produto', conn)
df_in = pd.DataFrame(SQL_Query_in)
#df_in.columns = ['Input ID','Datetime','Tag ID']

SQL_Query_out = pd.read_sql('SELECT hs.id_saida, hs.data_saida,p.id_tag, p2.nome_produto, p2.meta FROM hist_saida hs INNER JOIN produtotag p ON p.id_tag = hs.id_tag INNER JOIN produtos p2 ON p2.id_produto = p.id_produto', conn)
df_out = pd.DataFrame(SQL_Query_out)
#df_out.columns = ['Output ID','Datetime','Tag ID']

#Managing data
#get current date and time
data  = datetime.today()
current_date = str(data)[:10]
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
date_time = str(current_date) + ' ' + str(current_time)


selected_date = current_date
selected_hour = date_time[:13]

print('data: ',selected_date)
print('hora: ',selected_hour)

#df filtered by hour and date
df_in['data_entrada'] = df_in['data_entrada'].astype(str)
df_out['data_saida'] = df_out['data_saida'].astype(str)

df_in_hour = df_in[df_in['data_entrada'].str.contains(str(selected_hour))]
df_in_date = df_in[df_in['data_entrada'].str.contains(str(selected_date))]

df_out_hour = df_out[df_out['data_saida'].str.contains(str(selected_hour))]
df_out_date = df_out[df_out['data_saida'].str.contains(str(selected_date))]

name_list = df_prod['Name'].tolist()
code_list = df_prod['Code'].tolist()

##Preparing Filters
name_code = ['All']

for i in range(len(name_list)):
    name_code_un = str(name_list[i]) + ': ' + str(code_list[i])
    name_code.append(name_code_un)

to_filter = st.selectbox('Select a Product:',name_code)
selected = to_filter.split(': ')

if selected[0] == 'All':
    df_in_nodate = df_in
    df_out_nodate =df_out
    df_in_hour_filter = df_in_hour
    df_in_date_filter = df_in_date
    df_out_hour_filter = df_out_hour
    df_out_date_filter = df_out_date
    
    stock_in = df_in_nodate.shape[0]
    stock_out = df_out_nodate.shape[0]
    meta = df_prod['Target'].sum()
else:
    df_in_nodate = df_in.loc[df_in['nome_produto'] == selected[0]]
    df_out_nodate = df_out.loc[df_out['nome_produto'] == selected[0]]
    df_in_hour_filter = df_in_hour.loc[df_in_hour['nome_produto'] == selected[0]]
    df_in_date_filter = df_in_date.loc[df_in_date['nome_produto'] == selected[0]]
    df_out_hour_filter = df_out_hour.loc[df_out_hour['nome_produto'] == selected[0]]
    df_out_date_filter = df_out_date.loc[df_out_date['nome_produto'] == selected[0]]
    
    stock_in = df_in_nodate.shape[0]
    stock_out = df_out_nodate.shape[0]
    meta = df_in_hour_filter['meta'].mean()

quantidade_in_h = df_in_hour_filter.shape[0]
quantidade_in_d = df_in_date_filter.shape[0]
quantidade_out_h = df_out_hour_filter.shape[0]
quantidade_out_d = df_out_date_filter.shape[0]

df_in_date_filter.data_entrada=pd.to_datetime(df_in_date_filter.data_entrada)
df_group_in = df_in_date_filter.groupby([pd.Grouper(key='data_entrada',freq='H'),df_in_date_filter.nome_produto]).size().reset_index(name='count')

df_out_date_filter.data_saida=pd.to_datetime(df_out_date_filter.data_saida)
df_group_out = df_out_date_filter.groupby([pd.Grouper(key='data_saida',freq='H'),df_out_date_filter.nome_produto]).size().reset_index(name='count')

df_in_nodate.data_entrada=pd.to_datetime(df_in_nodate.data_entrada)
df_group_in_d = df_in_nodate.groupby([pd.Grouper(key='data_entrada',freq='D'),df_in_nodate.nome_produto]).size().reset_index(name='count')

df_out_nodate.data_saida=pd.to_datetime(df_out_nodate.data_saida)
df_group_out_d = df_out_nodate.groupby([pd.Grouper(key='data_saida',freq='D'),df_out_nodate.nome_produto]).size().reset_index(name='count')


kpi1, kpi2, kpi3, stock = st.columns(4)

kpi1.metric(
    label='Produced Last Hour',
    value=quantidade_in_h,
    delta = None
)

kpi2.metric(
    label='Target Hourly Production',
    value=meta,
    delta = None
)

perc_h_i = (quantidade_in_h*100)/meta
perc_h_i = round(perc_h_i,1)

kpi3.metric(
    label='%%',
    value=str(perc_h_i) + ' %',
    delta = None
)

stock.metric(
    label='In Stock',
    value = stock_in-stock_out,
    delta = None
)

kpi4, kpi5, kpi6, stats = st.columns(4)

kpi4.metric(
    label='Produced Last Day',
    value=quantidade_in_d,
    delta = None
)

kpi5.metric(
    label='Target Daily Production',
    value=meta*24,
    delta = None
)

perc_d_i = (quantidade_in_d*100)/(meta*24)
perc_d_i = round(perc_d_i,1)

kpi6.metric(
    label='%%',
    value=str(perc_d_i) + ' %',
    delta = None
)

if stock_in-stock_out < 5:
    stat = 'LOW'
elif stock_in-stock_out > 10:
    stat = 'HIGH'
else:
    stat = 'GOOD'

stats.metric(
    label='Stock Status',
    value=stat ,
    delta=None
)

kpi7, kpi8, kpi9, free1 = st.columns(4)

kpi7.metric(
    label='Sent Last Hour',
    value=quantidade_out_h,
    delta = None
)

kpi8.metric(
    label='Target Hourly Sent',
    value=meta,
    delta = None
)

perc_h_o = (quantidade_out_h*100)/(meta)
perc_h_o = round(perc_h_o,1)

kpi9.metric(
    label='%%',
    value=str(perc_h_o) + ' %',
    delta = None
)

free1.metric(
    label=' ',
    value=' ',
    delta = None
)

kpi10, kpi11, kpi12, free2 = st.columns(4)

kpi10.metric(
    label='Sent Last Day',
    value=quantidade_out_d,
    delta = None
)

kpi11.metric(
    label='Target Daily Sent',
    value=meta*24,
    delta = None
)

perc_d_o = (quantidade_out_d*100)/(meta*24)
perc_d_o = round(perc_d_o,1)

kpi12.metric(
    label='%%',
    value=str(perc_d_o) + ' %',
    delta = None
)

free2.metric(
    label=' ',
    value=' ',
    delta = None
)

graph1, graph2 = st.columns(2)

with graph1:
    fig_in = px.bar(df_group_in, x='data_entrada', y='count',title="Produced by Hour")
    fig_in.update_layout(title_font_size=30)
    fig_in.add_hline(y=meta, line_width=3, line_dash="dash", line_color="red")
    st.plotly_chart(fig_in, use_container_width=True)
    
with graph2:
    fig_out = px.bar(df_group_out, x='data_saida', y='count',title="Sent by Hour")
    fig_out.update_layout(title_font_size=30)
    fig_out.add_hline(y=meta, line_width=3, line_dash="dash", line_color="red")
    st.plotly_chart(fig_out, use_container_width=True)
    
graph3, graph4 = st.columns(2)

with graph3:
    fig_in_d = px.bar(df_group_in_d, x='data_entrada', y='count',title="Produced by Day")
    fig_in_d.update_layout(title_font_size=30)
    fig_in_d.add_hline(y=meta*24, line_width=3, line_dash="dash", line_color="red")
    st.plotly_chart(fig_in_d, use_container_width=True)
    
with graph4:
    fig_out_d = px.bar(df_group_out_d, x='data_saida', y='count',title="Sent by Day")
    fig_out_d.update_layout(title_font_size=30)
    fig_out_d.add_hline(y=meta*24, line_width=3, line_dash="dash", line_color="red")
    st.plotly_chart(fig_out_d, use_container_width=True)
    
sleep(10)
conn.dispose()
st.experimental_rerun() 