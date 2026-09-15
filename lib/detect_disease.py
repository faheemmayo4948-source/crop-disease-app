import base64
import requests
import streamlit as st
from io import BytesIO
from gtts import gTTS

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

PLANT_ID_URL = "https://plant.id/api/v3/health_assessment"

def get_location_based_sprays(disease_name, latitude=None):
    disease_lower = str(disease_name).lower()
    is_south_asia = latitude is None or (5.0 <= latitude <= 37.0)

    if any(k in disease_lower for k in [
        "bipolaris", "physoderma", "alternaria", "cercospora", "phytophthora", 
        "helminthosporium", "septoria", "blight", "spot", "scab", "anthracnose", "leaf"
    ]):
        if is_south_asia:
            return [
                "Mancozeb 75% WP (e.g., Dithane M-45) — 2g / Liter water",
                "Propiconazole 25% EC (e.g., Tilt) — 1ml / Liter water",
                "Copper Oxychloride 50% WP — 2.5g / Liter water"
            ]
        return [
            "Broad-spectrum Copper Fungicide — 2g / Liter water",
            "Mancozeb 75% WP Foliar Spray — 2g / Liter water"
        ]

    elif any(k in disease_lower for k in [
        "rust", "mildew", "puccinia", "erysiphe", "oidium", "peronospora", "plasmopara"
    ]):
        if is_south_asia:
            return [
                "Tebuconazole 250 EC (e.g., Folicur) — 1ml / Liter water",
                "Hexaconazole 5% EC — 2ml / Liter water",
                "Sulfur 80% WDG (e.g., Kumulus) — 3g / Liter water"
            ]
        return [
            "Propiconazole Systemic Fungicide — 1ml / Liter water",
            "Wettable Sulfur Spray — 3g / Liter water"
        ]

    elif any(k in disease_lower for k in [
        "rot", "wilt", "fusarium", "rhizoctonia", "pythium", "sclerotium", "verticillium"
    ]):
        return [
            "Carbendazim 50% WP (e.g., Bavistin) — Soil Drenching @ 1.5g / Liter water",
            "Metalaxyl 8% + Mancozeb 64% WP — 2g / Liter water"
        ]

    elif any(k in disease_lower for k in [
        "bacterial", "xanthomonas", "pseudomonas", "erwinia", "virus", "mosaic", "curl"
    ]):
        return [
            "Streptomycin Sulphate + Tetracycline — 0.5g / 10 Liter water",
            "Copper Hydroxide 77% WP — 2g / Liter water"
        ]

    return [
        "Mancozeb 75% WP (Broad Spectrum Fungicide) — 2g / Liter water",
        "Copper Oxychloride 50% WP — 2.5g / Liter water",
        "Neem Oil Extract Solution (Organic) — 5ml / Liter water"
    ]


def generate_audio_guide(text: str, lang: str = "en"):
    """
    gTTS se audio stream generate karta hai in-memory BytesIO buffer mein.
    """
    try:
        tts_lang = "ur" if lang == "ur" else "en"
        tts = gTTS(text=text, lang=tts_lang)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        st.error(f"Audio generation error: {e}")
        return None


def detect_disease(image_bytes: bytes, content_type: str = "image/jpeg", latitude: float = None, longitude: float = None):
    api_key = st.secrets.get("PLANT_ID_API_KEY", "")
    if not api_key:
        st.error("⚠️ PLANT_ID_API_KEY Secrets mein nahi mili.")
        return []

    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
    headers = {
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "images": [f"data:{content_type};base64,{encoded_image}"],
        "latitude": latitude or 31.5204,
        "longitude": longitude or 74.3587,
        "similar_images": True
    }
    params = {
        "details": "cause,description,treatment,preventative_measures"
    }

    try:
        response = requests.post(PLANT_ID_URL, json=payload, headers=headers, params=params, timeout=25)
        if response.status_code in [200, 201]:
            data = response.json()
            suggestions = data.get("result", {}).get("disease", {}).get("suggestions", [])
            
            results = []
            for item in suggestions[:3]:
                disease_name = item.get("name", "Crop Issue Detected")
                probability = item.get("probability", 0.0)
                details = item.get("details", {}) or {}

                bio = ["Neem Oil Spray (5ml/L) to prevent fungal spore spread."]
                prev = [
                    "Maintain field sanitation and clean infected leaves.",
                    "Ensure adequate air ventilation between plant rows."
                ]

                local_sprays = get_location_based_sprays(disease_name, latitude)

                results.append({
                    "label": disease_name,
                    "score": probability,
                    "description": details.get("description", "Pathogen activity observed on leaf foliage."),
                    "biological": bio,
                    "prevention": prev,
                    "local_sprays": local_sprays
                })
            return results
    except Exception as e:
        st.error(f"API Error: {e}")
    
    return []


def generate_pdf_report(pred_data, lat=None, lon=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#0F766E'), spaceAfter=4)
    sub_style = ParagraphStyle('SubStyle', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#475569'), spaceAfter=10)
    author_style = ParagraphStyle('AuthorStyle', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#0D9488'), spaceAfter=12)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#1E293B'), spaceBefore=8, spaceAfter=4)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=9, leading=13, textColor=colors.HexColor('#334155'))

    story = []
    story.append(Paragraph("🌱 CropGuard — Agricultural Diagnostic Report", title_style))
    story.append(Paragraph("<b>Lead Researcher:</b> Muhammad Faheem (Biological Sciences)", author_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))

    label = pred_data.get("label", "Crop Issue")
    score = pred_data.get("score", 0.0) * 100

    story.append(Paragraph(f"Primary Diagnosis: {label} ({score:.1f}% Match)", heading_style))
    story.append(Paragraph(f"<b>Description:</b> {pred_data.get('description', 'N/A')}", body_style))
    story.append(Spacer(1, 8))

    sprays = pred_data.get("local_sprays", [])
    if sprays:
        story.append(Paragraph("🎯 Recommended Chemical Sprays:", heading_style))
        for spray in sprays:
            story.append(Paragraph(f"• {spray}", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
