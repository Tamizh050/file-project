import streamlit as st
import pandas as pd
import re

# ---------- 1. Load default or uploaded Excel ----------
@st.cache_data
def load_excel_file(file):
    try:
        df = pd.read_excel(file, dtype=str)
        df.columns = df.columns.str.strip()  # Clean headers
        return df
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        return pd.DataFrame()

# ---------- 2. Setup ----------
st.set_page_config(page_title="HSN Code Checker", layout="centered")
st.title("🔍 HSN Code Checker")
st.markdown("Check if a given **HSN code** exists in the master list.")

# ---------- 3. Load Default File ----------
DEFAULT_FILE = "HSN_SAC.xlsx"  # Replace with your actual path

try:
    default_df = load_excel_file(DEFAULT_FILE)
except:
    default_df = pd.DataFrame()

# ---------- 4. Optional Upload ----------
uploaded_file = st.file_uploader("📤 Upload a custom Excel file (optional)", type=["xlsx"])

if uploaded_file:
    df = load_excel_file(uploaded_file)
    source = "Uploaded File"
else:
    df = default_df
    source = "Default File"

if df.empty:
    st.error("❌ No valid file loaded. Please upload a valid HSN master Excel file.")
else:
    st.success(f"✅ Using data from: **{source}**")
    hsn_column = st.selectbox("🔽 Select column with HSN codes:", options=df.columns.tolist())

    user_input = st.text_input("🔍 Enter an HSN code to check:")

    if user_input:
        cleaned = user_input.strip().zfill(8)
        df[hsn_column] = df[hsn_column].astype(str).str.zfill(8)

        if re.fullmatch(r"\d{4}|\d{6}|\d{8}", user_input.strip()):
            if cleaned in df[hsn_column].values:
                result = df[df[hsn_column] == cleaned].iloc[0].to_dict()
                st.success(f"✅ HSN Code `{cleaned}` found in {source}!")
                st.json(result)
            else:
                st.error(f"❌ HSN Code `{cleaned}` not found.")
        else:
            st.warning("⚠️ Invalid format. HSN Code must be 4, 6, or 8 digits.")
