import streamlit as st
from lib.firebase_client import get_db

st.set_page_config(page_title="Gallery · CropGuard", page_icon="🖼️", layout="wide")

st.title("🖼️ Contributed Samples Gallery")
st.write("Every leaf sample contributed by farmers, with its crop and disease label.")


@st.cache_data(ttl=60)
def load_samples():
    db = get_db()
    docs = db.collection("samples").order_by(
        "createdAt", direction="DESCENDING"
    ).stream() if False else db.collection("samples").stream()
    samples = []
    for doc in docs:
        data = doc.to_dict()
        samples.append(data)
    return samples


samples = load_samples()

if not samples:
    st.info("No samples contributed yet. Be the first — go to 'Contribute a sample'.")
else:
    crop_options = ["All crops"] + sorted({s.get("cropName", "Unknown") for s in samples})
    crop_filter = st.selectbox("Filter by crop", crop_options)

    filtered = samples if crop_filter == "All crops" else [
        s for s in samples if s.get("cropName") == crop_filter
    ]

    st.caption(f"Showing {len(filtered)} of {len(samples)} samples")

    cols = st.columns(3)
    for i, sample in enumerate(filtered):
        with cols[i % 3]:
            image_url = sample.get("imageUrl")
            if image_url:
                st.image(image_url, use_container_width=True)
            st.markdown(f"**{sample.get('cropName', 'Unknown')}**")
            st.caption(sample.get("diseaseLabel", "No label"))
            st.divider()
