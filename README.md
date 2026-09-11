# CropGuard — Streamlit Version

Ye same project ka Streamlit (Python) version hai jo **streamlit.app** (Streamlit Community Cloud) per free live deploy ho sakta hai.

Pages:
- `app.py` — Homepage
- `pages/1_Detect_Disease.py` — Leaf image upload -> pretrained Hugging Face model se disease detect
- `pages/2_Contribute_Data.py` — Labeled image submit -> Firebase Storage + Firestore mein save
- `pages/3_Disease_Database.py` — Search/browse-able global disease database (`data/disease_database.csv`), photo detection se alag

## Disease Database ko hazaron tak barhana

`data/disease_database.csv` abhi ~70 real diseases k sath start hoti hai (columns: `Crop,Disease,ScientificName,Symptoms,Treatment,Region`). Isay barhane k 2 tareeqay hain:

1. **Manually rows add karen** — same format mein CSV mein naye rows likhte jaen.
2. **Public sources se import karen** — jaisay:
   - CABI Plantwise Knowledge Bank (plantwise.org)
   - EPPO Global Database (gd.eppo.int)
   - USDA Plant Disease databases
   
   In sites se disease name, symptoms, treatment nikal k CSV mein daal saktay hain (copy karne se pehlay har site ki terms of use zaroor check kar len).

Yaad rahe: **photo se detection** (`1_Detect_Disease.py`) hamesha model k trained classes tak mehdood rahega (abhi ~38 diseases) — koi bhi existing AI model duniya bhar ki hazaron diseases photo se pehchan nahi sakta, kyunke itni saari diseases ki labeled images exist hi nahi karti. Database page is limitation ko cover karta hai — jab AI match na kare, user khud search kar k apni disease dhoond sakta hai.

## 1. Local setup

```bash
python -m venv venv
source venv/bin/activate   # Windows per: venv\Scripts\activate
pip install -r requirements.txt
```

`.streamlit/secrets.toml.example` ko copy kar k `.streamlit/secrets.toml` banayen aur real values daalen:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Phir run karen:

```bash
streamlit run app.py
```

## 2. Firebase setup (Contribute Data feature k liye)

1. https://console.firebase.google.com per project banayen, **Storage** aur **Firestore** enable karen.
2. Project Settings > Service Accounts > "Generate new private key" — isse ek JSON file milegi.
3. Us JSON file ki values `.streamlit/secrets.toml` k `[firebase_service_account]` section mein paste karen.
4. `firebase_storage_bucket` mein apna bucket name daalen (Firebase console > Storage per milega, jaisay `your-project-id.appspot.com`).

## 3. Hugging Face token (Detect Disease feature k liye)

1. https://huggingface.co per free account banayen.
2. Settings > Access Tokens se "Read" token banayen.
3. Ye token `.streamlit/secrets.toml` mein `hf_api_token` mein daalen.

## 4. GitHub per push karna

```bash
git init
git add .
git commit -m "Initial commit - CropGuard Streamlit app"
git branch -M main
git remote add origin https://github.com/<aapka-username>/<repo-name>.git
git push -u origin main
```

**Zaroori:** `secrets.toml` (asli file, `.example` nahi) kabhi GitHub per push na karen — `.gitignore` mein already add hai, so ye khud-b-khud exclude ho jayegi.

## 5. streamlit.app per live deploy karna

1. https://share.streamlit.io per GitHub account se login karen.
2. "Create app" per click karen, apni GitHub repo aur `app.py` select karen.
3. "Advanced settings" mein **Secrets** section open karen aur apni `secrets.toml` ka pura content wahan paste kar den (ye Streamlit Cloud ka apna secure secrets manager hai).
4. "Deploy" per click karen — chand minute mein `https://<app-name>.streamlit.app` per live ho jayega.

Har baar `main` branch per naya commit push karne per, Streamlit Cloud automatically redeploy kar deta hai.

## Next steps

- Research student login/data-access page add karna
- Companies k liye data export/admin panel banana
- Apna khud ka trained model laga kar pretrained model replace karna
