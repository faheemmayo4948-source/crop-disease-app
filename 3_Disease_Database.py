import streamlit as st
import pandas as pd

st.set_page_config(page_title="Disease Database · CropGuard", page_icon="🌍")

st.title("🌍 Global Disease Database")
st.write(
    "Search or browse crop diseases from around the world — symptoms, "
    "scientific name, and treatment. This is a reference list, separate "
    "from the photo-based detector, and can keep growing over time."
)


@st.cache_data
def load_database():
    return pd.read_csv("data/disease_database.csv")


df = load_database()

col1, col2 = st.columns([2, 1])
with col1:
    query = st.text_input("Search by disease, crop, or symptom", placeholder="e.g. blight, rice, wilting")
with col2:
    crop_filter = st.selectbox("Filter by crop", ["All crops"] + sorted(df["Crop"].unique().tolist()))

filtered = df.copy()

if crop_filter != "All crops":
    filtered = filtered[filtered["Crop"] == crop_filter]

if query:
    q = query.lower()
    mask = filtered.apply(lambda row: q in " ".join(row.astype(str)).lower(), axis=1)
    filtered = filtered[mask]

st.caption(f"Showing {len(filtered)} of {len(df)} entries")

for _, row in filtered.iterrows():
    with st.expander(f"{row['Disease']} — {row['Crop']}"):
        st.markdown(f"**Scientific name:** _{row['ScientificName']}_")
        st.markdown(f"**Symptoms:** {row['Symptoms']}")
        st.markdown(f"**Treatment:** {row['Treatment']}")
        st.markdown(f"**Region:** {row['Region']}")

st.divider()
st.caption(
    "Want to add more entries? Open data/disease_database.csv and add new "
    "rows in the same format — the page picks them up automatically."
)
