import streamlit as st
import pandas as pd


def convert_invoices(file):
    df = pd.read_excel(file, header=4, skipfooter=1)
    df_cleaned = df.drop(df.columns[0], axis=1)
    df_cleaned = df_cleaned.dropna(axis=1, how='all')
    # df_cleaned = df_cleaned.dropna(how='all')
    df_cleaned = df_cleaned[df_cleaned['Date'].notna()]


    output_df = pd.DataFrame({
                "Invoice Reference": df_cleaned['Number'],
                "Customer" : df_cleaned['Customer'], 
                "Date": df_cleaned['Date'],
                "Item / Description" : df_cleaned['Memo/Description'],
                "Invoice Account" : None,
                "Tax Included in Amount" : None,
                'Total Amount (SGD)': df_cleaned['Amount'],
                "Internal Notes": None,
                "Amount Paid": abs(df_cleaned['Balance']- df_cleaned['Amount']),
                "Payment Method": None,
                "Payment Account": None,
                "Payment Ref #": None,
                "Transaction Fee Included (SGD)": None,
                "Tax Included in Transaction Fees (SGD)" : None,
                "Transaction Fee Expense Account": None,
                "Amount Withholding": None,
                "Withholding Ref #" : None
            })

    return output_df

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

st.title('Convert Invoices')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    processed_data = convert_invoices(uploaded_file)
    st.write("Processed Data", processed_data)
    csv = convert_df_to_csv(processed_data)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='invoice_imports.csv',
        mime='text/csv',
    )