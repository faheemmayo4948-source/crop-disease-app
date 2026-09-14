import base64
import requests
import streamlit as st
from io import BytesIO

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

PLANT_ID_URL = "https://plant.id/api/v3/health_assessment"

def get_location_based_sprays(disease_name, latitude=None):
    """
    Provides global & regional treatment, fungicide, bactericide, and pesticide recommendations 
    for broad global plant pathogens (Fungal, Bacterial, Viral, and Pest Vectors).
    """
    disease_lower = disease_name.lower()
    is_south_asia = latitude is None or (5.0 <= latitude <= 37.0)

    # 1. FUNGAL LEAF SPOTS & BLIGHTS (Bipolaris, Physoderma, Alternaria, Cercospora, Phytophthora, Septoria)
    if any(k in disease_lower for k in [
        "bipolaris", "physoderma", "alternaria", "cercospora", "phytophthora", 
        "helminthosporium", "septoria", "blight", "spot", "scab", "anthracnose", "leaf"
    ]):
        if is_south_asia:
            return [
                "Mancozeb 75% WP (e.g., Dithane M-45) — 2g/L water",
                "Propiconazole 25% EC (e.g., Tilt) — 1ml/L water",
                "Copper Oxychloride 50% WP — 2.5g/L water",
                "Cymoxanil + Mancozeb (e.g., Curzate) — 2g/L water (for Downy/Late Blight)"
            ]
        return [
            "Broad-spectrum Copper Fungicide (e.g., Kocide)",
            "Mancozeb 75% WP Foliar Spray",
            "Chlorothalonil 500 SC — 2ml/L water"
        ]

    # 2. POWDERY & DOWNY MILDEWS / RUSTS
    elif any(k in disease_lower for k in [
        "rust", "mildew", "puccinia", "erysiphe", "oidium", "peronospora", "plasmopara"
    ]):
        if is_south_asia:
            return [
                "Tebuconazole 250 EC (e.g., Folicur) — 1ml/L water",
                "Hexaconazole 5% EC — 2ml/L water",
                "Sulfur 80% WDG (e.g., Kumulus) — 3g/L water",
                "Azoxystrobin 23% SC — 1ml/L water"
            ]
        return [
            "Propiconazole Systemic Fungicide",
            "Sulfur Dusting / Wettable Sulfur Spray",
            "Myclobutanil / Azoxystrobin Foliar Spray"
        ]

    # 3. WILTS & ROTS
    elif any(k in disease_lower for k in [
        "rot", "wilt", "fusarium", "rhizoctonia", "pythium", "sclerotium", "verticillium"
    ]):
        if is_south_asia:
            return [
                "Carbendazim 50% WP (e.g., Bavistin) — Soil drenching @ 1.5g/L water",
                "Metalaxyl 8% + Mancozeb 64% WP (e.g., Ridomil Gold) — 2g/L water",
                "Trichoderma viride (Bio-fungicide) — Soil application 5g/L water"
            ]
        return [
            "Fosetyl-Aluminum Soil Drench (e.g., Aliette)",
            "Metalaxyl Systemic Fungicide",
            "Biological Trichoderma Harzianum Treatment"
        ]

    # 4. BACTERIAL DISEASES
    elif any(k in disease_lower for k in [
        "bacterial", "xanthomonas", "pseudomonas", "erwinia", "ralstonia", "canker"
    ]):
        if is_south_asia:
            return [
                "Streptomycin Sulphate + Tetracycline (e.g., Streptocycline) — 0.5g / 10L water",
                "Copper Hydroxide 77% WP — 2g/L water",
                "Kasugamycin 3% SL — 2ml/L water"
            ]
        return [
            "Copper Hydroxide Bactericide Spray",
            "Agricultural Streptomycin / Terramycin Formulation",
            "Bacillus subtilis Bio-bactericide"
        ]

    # 5. VIRUSES & INSECT VECTORS
    elif any(k in disease_lower for k in [
        "virus", "mosaic", "curl", "aphid", "whitefly", "thrips", "mite", "vector"
    ]):
        if is_south_asia:
            return [
                "Imidacloprid 17.8% SL (e.g., Confidor) — 0.5ml/L water (Target Whitefly/Aphids)",
                "Acetamiprid 20% SP — 0.5g/L water",
                "Thiamethoxam 25% WG — 0.3g/L water"
            ]
        return [
            "Systemic Neonicotinoid Insecticide (for pest vector control)",
            "Insecticidal Soap / Horticultural Neem Oil",
            "Spirotetramat (for piercing-sucking insects)"
        ]

    # 6. UNIVERSAL FALLBACK
    return [
        "Broad-Spectrum Mancozeb 75% WP — 2g/L water",
        "Chlorothalonil 75% WP — 2g/L water",
        "Neem Oil Extract Solution (Organic) — 5ml/L water with mild soap"
    ]

def detect_disease(image_bytes: bytes, content_type: str = "image/jpeg", latitude: float = None, longitude: float = None):
    """
    Calls Plant.id API v3 for diagnostics, treatments, and prevention protocols.
    """
    api_key = st.secrets.get("PLANT_ID_API_KEY", "")
    if not api_key:
        st.warning("⚠️ PLANT_ID_API_KEY Missing in Streamlit Secrets")
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
                disease_name = item.get("name", "Unknown Issue")
                probability = item.get("probability", 0.0)
                details = item.get("details", {}) or {}
                treatment_data = details.get("treatment", {}) or {}

                bio = treatment_data.get("biological", [])
                chem = treatment_data.get("chemical", [])
                prev = details.get("preventative_measures", [])

                local_sprays = get_location_based_sprays(disease_name, latitude)

                results.append({
                    "label": disease_name,
                    "score": probability,
                    "description": details.get("description", "No detailed description available."),
                    "biological": bio if isinstance(bio, list) else [bio],
                    "chemical": chem if isinstance(chem, list) else [chem],
                    "prevention": prev if isinstance(prev, list) else [prev],
                    "local_sprays": local_sprays
                })
            return results
    except Exception as e:
        st.error(f"API Error: {e}")
    
    return []

def generate_pdf_report(pred_data, lat=None, lon=None):
    """
    Generates an official PDF diagnostic report with author credentials.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#0F766E'), spaceAfter=4)
    sub_style = ParagraphStyle('SubStyle', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#475569'), spaceAfter=10)
    author_style = ParagraphStyle('AuthorStyle', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#0D9488'), spaceAfter=12)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#1E293B'), spaceBefore=8, spaceAfter=4)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=9, leading=13, textColor=colors.HexColor('#334155'))

    story = []

    # Header & Author Branding
    story.append(Paragraph("🌱 CropGuard — Official Agricultural Diagnostic Report", title_style))
    story.append(Paragraph("<b>Lead Researcher:</b> Muhammad Faheem (Graduate in Biological Sciences)", author_style))
    
    loc_text = f"GPS Coordinates: {lat:.4f}, {lon:.4f}" if lat else "GPS Location: Not Specified"
    story.append(Paragraph(f"<b>Platform:</b> CropGuard AI | {loc_text}", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))

    label = pred_data.get("label", "Unknown Issue")
    score = pred_data.get("score", 0.0) * 100
    description = pred_data.get("description", "N/A")

    story.append(Paragraph(f"Primary Diagnosis: {label} ({score:.1f}% Match)", heading_style))
    story.append(Paragraph(f"<b>Description:</b> {description}", body_style))
    story.append(Spacer(1, 8))

    bio = pred_data.get("biological", [])
    chem = pred_data.get("chemical", [])
    local_sprays = pred_data.get("local_sprays", [])
    prevention = pred_data.get("prevention", [])

    if bio:
        story.append(Paragraph("🌱 Biological / Organic Treatments:", heading_style))
        for b in bio:
            if b: story.append(Paragraph(f"• {b}", body_style))
        story.append(Spacer(1, 4))

    if chem:
        story.append(Paragraph("🧪 Recommended Chemical Control:", heading_style))
        for c in chem:
            if c: story.append(Paragraph(f"• {c}", body_style))
        story.append(Spacer(1, 4))

    if local_sprays:
        story.append(Paragraph("🎯 Localized Market Sprays:", heading_style))
        for spray in local_sprays:
            if spray: story.append(Paragraph(f"• {spray}", body_style))
        story.append(Spacer(1, 4))

    if prevention:
        story.append(Paragraph("🛡️ Preventive Guidelines:", heading_style))
        for p in prevention:
            if p: story.append(Paragraph(f"• {p}", body_style))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=6))
    story.append(Paragraph("<i>Verified & Prepared by Muhammad Faheem | Biological Sciences & AgriTech Diagnostics</i>", author_style))
    story.append(Paragraph("<i>Disclaimer: This document is an automated AI report intended to support agricultural advisory.</i>", sub_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
