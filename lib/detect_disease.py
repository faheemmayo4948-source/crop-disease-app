import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Disease Database - CropGuard", page_icon="📚")
st.title("📚 Plant Disease Database")

csv_path = "data/disease_database.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    
    search = st.text_input("🔍 Search by Crop or Disease Name", "")
    if search:
        df_filtered = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().values, axis=1)]
    else:
        df_filtered = df
        
    st.dataframe(df_filtered, use_container_width=True)
else:
    st.warning("`data/disease_database.csv` file nahi mili. Path verify karein.")
