from sqlalchemy import create_engine
import streamlit as st
import pandas as pd
from PIL import Image


st.set_page_config(
    page_title="Main",
    page_icon=" ",
)

image = Image.open('fho_png2.png')


with st.sidebar:
    st.image(image)


st.title("Main Page")

st.image(image,use_column_width='always')
