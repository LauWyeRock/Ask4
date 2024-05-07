import streamlit as st
import pandas as pd


def convert_journals(file):
    df = pd.read_excel(file, header=4, skipfooter=1)
    df_cleaned = df.drop(df.columns[0], axis=1)
    df_cleaned = df_cleaned.dropna(axis=1, how='all')
    # df_cleaned = df_cleaned.dropna(how='all')
    df_cleaned = df_cleaned[df_cleaned['Adj'].notna()]



    output_df = pd.DataFrame({
                'Journal Reference': 'FYE2023 Conversion: Journal', #TransactionType, No. 
                'Date': df_cleaned['Date'],
                'Contact': df_cleaned['Name'],
                'Account': df_cleaned['Account'],
                'Description': df_cleaned['Memo/Description'],
                'Tax Included in Amount': None,
                'Debit Amount': df_cleaned['Debit'],
                'Credit Amount': df_cleaned['Credit']
            })
    

    return output_df


def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

st.title('Convert Journals')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    processed_data = convert_journals(uploaded_file)
    st.write("Processed Data", processed_data)
    csv = convert_df_to_csv(processed_data)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='journal_imports.csv',
        mime='text/csv',
    )