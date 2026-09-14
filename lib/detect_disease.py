def get_location_based_sprays(disease_name, latitude=None):
    """
    Provides global & regional treatment, fungicide, bactericide, and pesticide recommendations 
    for broad global plant pathogens (Fungal, Bacterial, Viral, and Pest Vectors).
    """
    disease_lower = disease_name.lower()
    
    # Check if location is South Asia / Subcontinent region
    is_south_asia = latitude is None or (5.0 <= latitude <= 37.0)

    # 1. FUNGAL LEAF SPOTS & BLIGHTS (Bipolaris, Physoderma, Alternaria, Cercospora, Phytophthora, Septoria)
    if any(k in disease_lower for k in [
        "bipolaris", "physoderma", "alternaria", "cercospora", "phytophthora", 
        "helminthosporium", "septoria", "blight", "spot", "scab", "anthracnose"
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

    # 2. POWDERY & DOWNY MILDEWS / RUSTS (Puccinia, Erysiphe, Plasmopara, Uromyces)
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

    # 3. WILTS, ROOT ROTS & CROWN ROTS (Fusarium, Rhizoctonia, Pythium, Sclerotium, Verticillium)
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

    # 4. BACTERIAL DISEASES (Xanthomonas, Pseudomonas, Erwinia, Ralstonia)
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

    # 5. VIRUSES & INSECT VECTORS (Mosaic, Curl, Aphid, Whitefly, Thrips, Mite)
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

    # 6. UNIVERSAL FALLBACK (Guarantees no diagnosis ever returns empty)
    return [
        "Broad-Spectrum Mancozeb 75% WP — 2g/L water",
        "Chlorothalonil 75% WP — 2g/L water",
        "Neem Oil Extract Solution (Organic) — 5ml/L water with mild soap"
    ]
