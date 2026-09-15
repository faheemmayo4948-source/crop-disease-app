import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Disease Database - CropGuard",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Plant Disease Reference Database")
st.write("Pakistani fasalon ki aam bimariyon, unki alamat (symptoms), aur ilaj (treatments) ki mukammal maloomat.")

csv_path = "data/disease_database.csv"

if not os.path.exists(csv_path):
    st.error(f"❌ Database file missing! Barae meherbani check karein ke `{csv_path}` file repository mein maujood hai.")
    st.stop()

# Read CSV Data
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    st.error(f"❌ File read karne mein masla aya: {str(e)}")
    st.stop()

# Search and Filter Section
col1, col2 = st.columns([2, 1])

with col1:
    search_query = st.text_input("🔍 Search by Crop, Disease, Symptoms, or Treatment", placeholder="e.g. Wheat, Blight, Rust, Mancozeb")

with col2:
    all_crops = ["All Crops"] + sorted(list(df["Crop"].dropna().unique()))
    selected_crop = st.selectbox("🌾 Filter by Crop", all_crops)

# Data Filtering Logic
filtered_df = df.copy()

if selected_crop != "All Crops":
    filtered_df = filtered_df[filtered_df["Crop"] == selected_crop]

if search_query.strip():
    query = search_query.strip().lower()
    filtered_df = filtered_df[
        filtered_df.apply(lambda row: query in str(row.values).lower(), axis=1)
    ]

st.markdown("---")

# Disease Count Display
st.subheader(f"Total Results: {len(filtered_df)}")

if filtered_df.empty:
    st.info("Koi matching disease nahi mili. Search criteria change karke dobara koshish karein.")
else:
    # Detailed Cards View
    for idx, row in filtered_df.iterrows():
        with st.expander(f"🌾 **{row['Crop']}** — {row['Disease']} (*{row.get('ScientificName', 'N/A')}*)"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Symptoms (Alamat):**\n{row.get('Symptoms', 'N/A')}")
                st.markdown(f"**Affected Region:** {row.get('Region', 'N/A')}")
            with col_b:
                st.markdown(f"**Recommended Treatment (Ilaj):**\n{row.get('Treatment', 'N/A')}")

    st.markdown("---")
    st.subheader("📊 Complete Reference Table")
    st.dataframe(filtered_df, use_container_width=True)
