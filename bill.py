import streamlit as st
import pandas as pd
import numpy as np


def convert_bills(file):
    df = pd.read_excel(file, header=4, skipfooter=1)
    df_cleaned = df.drop(df.columns[0], axis=1)
    df_cleaned = df_cleaned.dropna(axis=1, how='all')
    # df_cleaned = df_cleaned.dropna(how='all')
    df_cleaned = df_cleaned[df_cleaned['Date'].notna()]
    df_cleaned['Currency'] = df_cleaned['Account'].str[-3:]
    df_cleaned['Bill Reference'] = df_cleaned['No.'].fillna("Bill").astype(str) + " (" + df_cleaned['Currency'] + ")"



    output_df = pd.DataFrame({
                "Bill Reference": df_cleaned['Bill Reference'],
                "Supplier" : df_cleaned['Supplier'], 
                "Date": df_cleaned['Date'],
                "Item / Description" : df_cleaned['Memo/Description'],
                "Bill Account" : df_cleaned['Account'],
                "Tax Included in Amount" : None,
                'Total Amount (SGD)': df_cleaned['Amount'],
                "Internal Notes": None,
                "Amount Paid": np.where(df_cleaned['Transaction Type'] == 'Bill',abs(df_cleaned['Open Balance'] - df_cleaned['Amount']), None),
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

st.title('Convert Bills')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    processed_data = convert_bills(uploaded_file)
    st.write("Processed Data", processed_data)
    csv = convert_df_to_csv(processed_data)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='bil_imports.csv',
        mime='text/csv',
    )