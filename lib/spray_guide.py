import pandas as pd


def categorize_disease(disease_name: str) -> str:
    """Roughly categorize a disease by keywords in its name."""
    name = disease_name.lower()

    if "virus" in name or "viral" in name or "mosaic" in name or "curl" in name:
        return "Viral"
    if "bacter" in name:
        return "Bacterial"
    if any(keyword in name for keyword in [
        "blight", "mildew", "rust", "rot", "wilt", "anthracnose",
        "scab", "smut", "mold", "mould", "leaf spot", "canker"
    ]):
        return "Fungal"
    if any(keyword in name for keyword in ["mite", "aphid", "borer", "weevil"]):
        return "Pest/Insect"

    return "General"


def get_spray_recommendation(disease_name: str) -> dict:
    df = pd.read_csv("data/spray_guide.csv")
    category = categorize_disease(disease_name)
    row = df[df["Category"] == category]

    if row.empty:
        row = df[df["Category"] == "General"]

    row = row.iloc[0]
    return {
        "category": category,
        "treatment_class": row["TreatmentClass"],
        "guidance": row["GeneralGuidance"],
        "timing": row["Timing"],
        "precautions": row["Precautions"],
    }
