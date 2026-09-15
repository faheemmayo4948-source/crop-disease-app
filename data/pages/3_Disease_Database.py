import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Disease Database · CropGuard", page_icon="📖", layout="centered")

st.title("📖 Crop Disease Knowledge Base")
st.write("Search reference disease records, pathogen details, symptoms, and treatment guidelines.")

# Safe path resolution for Streamlit Cloud
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(current_dir, "..", "data", "disease_database.csv"))

if not os.path.exists(csv_path):
    st.error(f"⚠️ Disease database file not found at path: `{csv_path}`")
    st.info("Please make sure `data/disease_database.csv` is uploaded to your GitHub repository.")
else:
    try:
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
            crop = row.get('Crop', 'Crop')
            disease = row.get('Disease', 'Disease Name')
            with st.expander(f"🌱 {crop} — {disease}"):
                st.write(f"**Scientific Name / Pathogen:** _{row.get('ScientificName', 'N/A')}_")
                st.write(f"**Symptoms:** {row.get('Symptoms', 'N/A')}")
                st.write(f"**Treatment / Spray Protocol:** {row.get('Treatment', 'N/A')}")
                if "Region" in row and pd.notna(row.get('Region')):
                    st.write(f"**Prevalent Region:** {row.get('Region')}")
    except Exception as e:
        st.error(f"Error reading CSV database: {e}")
