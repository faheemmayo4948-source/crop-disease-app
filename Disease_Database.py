import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Disease Database · CropGuard", page_icon="📖", layout="centered")

st.title("📖 Crop Disease Knowledge Base")
st.write("Search reference disease records, pathogen details, symptoms, and treatment guidelines.")

csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "disease_database.csv")

if not os.path.exists(csv_path):
    st.error("⚠️ `data/disease_database.csv` file not found in directory.")
else:
    df = pd.read_csv(csv_path)

    search_query = st.text_input("🔍 Search by Crop, Disease, or Pathogen Name:")

    if search_query:
        filtered_df = df[
            df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        ]
    else:
        filtered_df = df

    st.write(f"Showing **{len(filtered_df)}** entries:")

    for _, row in filtered_df.iterrows():
        with st.expander(f"🌱 {row.get('Crop', 'Crop')} — {row.get('Disease', 'Disease Name')}"):
            st.write(f"**Scientific Name / Pathogen:** _{row.get('ScientificName', 'N/A')}_")
            st.write(f"**Symptoms:** {row.get('Symptoms', 'N/A')}")
            st.write(f"**Treatment / Spray Protocol:** {row.get('Treatment', 'N/A')}")
            if "Region" in row:
                st.write(f"**Prevalent Region:** {row.get('Region', 'N/A')}")
