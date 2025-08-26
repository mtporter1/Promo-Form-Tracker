
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

FILE_PATH = "Americas Promo Tracker.Streamlit.xlsx"
SHEET_NAME = "Request Tracker"

# Load the data from Excel
@st.cache_data
def load_data():
    df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
    df.columns = df.iloc[0]  # Set first row as header
    df = df[1:].reset_index(drop=True)
    return df

data = load_data()

st.title("📋 Promo Request Form")
st.subheader("📑 Existing Requests")
st.dataframe(data, use_container_width=True)

# Allow user to select a row to edit or create new
selected_index = st.selectbox("Select a row to edit (or choose New Entry):",
                              options=["New Entry"] + list(data.index.astype(str)),
                              format_func=lambda x: f"Row {x}" if x != "New Entry" else "New Entry")

if selected_index != "New Entry":
    selected_index = int(selected_index)
    selected_row = data.loc[selected_index]
else:
    selected_row = {col: "" for col in data.columns}

st.subheader("✏️ Fill or Edit Request Form")

with st.form("promo_form"):
    request_type = st.selectbox("Request Type", ["Club Program", "EOL Invoice Pricing", "Other"],
                                 index=0 if not selected_row.get("Request Type") else ["Club Program", "EOL Invoice Pricing", "Other"].index(selected_row.get("Request Type", "Club Program")))
    date_added = st.date_input("Date Added", value=datetime.today())
    country = st.text_input("Country", selected_row.get("Country", ""))
    category = st.text_input("Category", selected_row.get("Category", ""))
    product = st.text_input("Product", selected_row.get("Product", ""))
    financial_request = st.text_area("Financial Request", selected_row.get("Financial Request", ""))
    parameters = st.text_area("Parameters", selected_row.get("Parameters", ""))
    requested_by = st.text_input("Requested By", selected_row.get("Requested By", ""))
    links = st.text_input("Links", selected_row.get("Links:", ""))
    notified_finance = st.checkbox("Notified Finance", value=(str(selected_row.get("Notified Finance", "")) == "True"))
    financial_decision = st.text_area("Financial Decision", selected_row.get("Financial Decision", ""))
    financial_feedback = st.text_area("Financial Feedback", selected_row.get("Financial Feedback", ""))

    submitted = st.form_submit_button("Submit")

    if submitted:
        st.info("Submission captured. Note: File write-back is disabled on Streamlit Cloud.")
        new_data = {
            "Request Type": request_type,
            "Date Added": date_added,
            "Country": country,
            "Category": category,
            "Product": product,
            "Financial Request": financial_request,
            "Parameters": parameters,
            "Requested By": requested_by,
            "Links:": links,
            "Notified Finance": notified_finance,
            "Financial Decision": financial_decision,
            "Financial Feedback": financial_feedback,
        }

        st.write("### Here is the submitted data:")
        st.json(new_data)
