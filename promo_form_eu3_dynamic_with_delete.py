
import streamlit as st
import pandas as pd
from datetime import datetime

FILE_PATH = "Americas Promo Tracker.Streamlit.xlsx"
SHEET_NAME = "Request Tracker"

@st.cache_data
def load_data():
    df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME, header=None)
    for i in range(len(df)):
        if df.iloc[i].notna().sum() >= 3:
            df.columns = df.iloc[i]
            df = df[i + 1:]
            break
    df = df.dropna(axis=1, how='all')
    df.columns = df.columns.astype(str).str.strip()
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.reset_index(drop=True)
    return df

data = load_data()
selected_row = {col: "" for col in data.columns}

if "eu3_rows" not in st.session_state:
    st.session_state.eu3_rows = [{"reseller": "", "support": ""}]

st.subheader("📋 Promo Request Form")

with st.form("promo_form"):
    promo_driver = st.selectbox(
        "Promotion Driver",
        ["Reseller Event Opportunity", "Gap Closer", "Inventory Clean Up"]
    )
    start_date = st.date_input("Start Date", value=datetime.today())
    end_date = st.date_input("End Date", value=datetime.today())
    country = st.text_input("Country", selected_row.get("Country", ""))
    business_unit = st.selectbox("Business Unit", ["Wearables", "Out Loud Audio"])
    product = st.text_input("Product", selected_row.get("Product", ""))
    promo_price = st.text_input("Promo Price (Enter a numeric value)", selected_row.get("Promo Price", ""))
    requested_by = st.text_input("Requested By", selected_row.get("Requested By", ""))

    st.markdown("**For EU3 Please Enter Resellers Participating and Margin Support Per Unit by Reseller.**")

    updated_rows = []
    for i, row in enumerate(st.session_state.eu3_rows):
        c1, c2, c3 = st.columns([0.45, 0.45, 0.1])
        reseller = c1.text_input("Reseller", value=row["reseller"], key=f"reseller_{i}")
        support = c2.text_input("Margin Support", value=row["support"], key=f"support_{i}")
        if c3.button("❌", key=f"remove_{i}"):
            continue  # skip appending this row = delete
        updated_rows.append({"reseller": reseller, "support": support})
    st.session_state.eu3_rows = updated_rows

    if st.form_submit_button("+ Add EU3 Row"):
        st.session_state.eu3_rows.append({"reseller": "", "support": ""})

if st.button("Submit"):
    st.success("Submission captured (Note: file saving is disabled on Streamlit Cloud).")
    new_data = {
        "Promotion Driver": promo_driver,
        "Start Date": start_date,
        "End Date": end_date,
        "Country": country,
        "Business Unit": business_unit,
        "Product": product,
        "Promo Price": promo_price,
        "EU3 Reseller Data": st.session_state.eu3_rows,
        "Requested By": requested_by
    }
    st.write("### Submitted Data")
    st.json(new_data)
