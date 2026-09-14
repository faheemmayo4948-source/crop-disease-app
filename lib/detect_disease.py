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

def get_location_based_sprays(disease_name, latitude):
    """
    Suggests relevant localized chemical sprays based on geography.
    """
    disease_lower = disease_name.lower()
    is_south_asia = latitude and (5.0 <= latitude <= 37.0)
    
    if "blight" in disease_lower or "spot" in disease_lower:
        if is_south_asia:
            return [
                "Mancozeb 75% WP (e.g., Dithane M-45) — 2g per liter water",
                "Copper Oxychloride 50% WP — 2.5g per liter water",
                "Cymoxanil + Mancozeb (e.g., Curzate) — for advanced blight"
            ]
        return ["Broad-spectrum Copper Fungicide", "Mancozeb Foliar Spray"]
        
    elif "rust" in disease_lower or "mildew" in disease_lower:
        if is_south_asia:
            return [
                "Tebuconazole 250 EC (e.g., Folicur) — 1ml per liter water",
                "Hexaconazole 5% EC — 2ml per liter water",
                "Sulfur 80% WDG — 3g per liter water"
            ]
        return ["Propiconazole Systemic Fungicide", "Sulfur-based Dust/Spray"]
        
    elif "rot" in disease_lower or "wilt" in disease_lower:
        return [
            "Carbendazim 50% WP (e.g., Bavistin) — Soil drenching 1.5g/L",
            "Trichoderma viride (Bio-fungicide) — 5g per liter water"
        ]
    
    return [
        "Chlorothalonil 75% WP — 2g per liter water",
        "Neem Oil Solution (Organic) — 5ml per liter water with mild liquid soap"
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
