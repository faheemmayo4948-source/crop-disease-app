# Location-based Spray Recommendations (Guaranteed Render)
st.markdown("#### 🎯 Recommended Chemical & Market Sprays" if lang == "English" else "#### 🎯 تجویز کردہ کیمیائی اسپرے")

sprays = pred.get("local_sprays", [])
if sprays:
    for spray in sprays:
        st.write(f"👉 **{spray}**")
else:
    st.write("👉 **Mancozeb 75% WP — 2g/L water**")
    st.write("👉 **Copper Oxychloride 50% WP — 2.5g/L water**")
