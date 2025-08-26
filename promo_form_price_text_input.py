
import streamlit as st
import pandas as pd
from datetime import datetime

FILE_PATH = "Americas Promo Tracker.Streamlit.xlsx"
SHEET_NAME = "Request Tracker"

# Load and clean the Excel sheet robustly
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
    eu3_details = st.text_area("For EU3 Please Enter Resellers Participating and Margin Support Per Unit by Reseller.", selected_row.get("Parameters", ""))
    requested_by = st.text_input("Requested By", selected_row.get("Requested By", ""))

    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success("Submission captured (Note: file saving is disabled on Streamlit Cloud).")
        new_data = {
            "Promotion Driver": promo_driver,
            "Start Date": start_date,
            "End Date": end_date,
            "Country": country,
            "Business Unit": business_unit,
            "Product": product,
            "Promo Price": promo_price,
            "EU3 Details": eu3_details,
            "Requested By": requested_by
        }
        st.write("### Submitted Data")
        st.json(new_data)
