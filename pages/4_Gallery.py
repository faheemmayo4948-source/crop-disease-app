import streamlit as st
import pandas as pd
from lib.firebase_client import get_db

st.set_page_config(page_title="Gallery · CropGuard", page_icon="🔒", layout="wide")

# --- Password gate ---
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.title("🔒 Admin Access Required")
    password = st.text_input("Enter admin password", type="password")
    if st.button("Unlock"):
        if password == st.secrets.get("admin_password"):
            st.session_state.admin_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

# --- Everything below is only visible after correct password ---
st.title("🖼️ Contributed Samples (Private)")
st.caption("This data is private — visible only to admins, never to public visitors.")


@st.cache_data(ttl=60)
def load_samples():
    db = get_db()
    docs = db.collection("samples").stream()
    return [doc.to_dict() for doc in docs]


samples = load_samples()

if not samples:
    st.info("No samples contributed yet.")
else:
    df = pd.DataFrame(samples)
    st.caption(f"Total samples: {len(df)}")

    crop_options = ["All crops"] + sorted(df["cropName"].dropna().unique().tolist())
    crop_filter = st.selectbox("Filter by crop", crop_options)
    filtered_df = df if crop_filter == "All crops" else df[df["cropName"] == crop_filter]

    # CSV export for companies
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download as CSV (for company sharing)",
        data=csv,
        file_name="cropguard_samples.csv",
        mime="text/csv",
    )

    st.divider()

    cols = st.columns(3)
    for i, row in filtered_df.reset_index(drop=True).iterrows():
        with cols[i % 3]:
            if pd.notna(row.get("imageUrl")):
                st.image(row["imageUrl"], use_container_width=True)
            st.markdown(f"**{row.get('cropName', 'Unknown')}**")
            st.caption(row.get("diseaseLabel", "No label"))
            st.divider()

if st.button("🔒 Lock again"):
    st.session_state.admin_authenticated = False
    st.rerun()
