import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Convertor",layout="wide", page_icon="📂")
st.title("File Convertor & Cleaner")
st.write("Upload csv or excel files,clean data and convert formats.")

files = st.file_uploader("Upload CSV or Excel Files", type=['csv','xlsx'], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split('.')[-1]
        df = pd.read_csv(file) if ext == 'csv' else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())
               
        if st.checkbox(f"Remove Duplicates  -{file.name}"):
            df.drop_duplicates(inplace=True)
            st.success("Duplicates removed successfully.")
            st.dataframe(df.head())

            if st.checkbox(f"File missing values -{file.name}"):
                df.fillna(df.select_dtypes(include='number').mean(), inplace=True)
                st.success("Missing values filled with mean successfully.")
                st.dataframe(df.head())     
                
            selected_columns = st.multiselect(f"Select columns - {file.name}", df.columns, default = df.column)
            df = df[selected_columns]
            st.dataframe(df.head())

            if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include='number').empty:
                st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

            format_choice = st.radio(f"Convert {file.name} to:",['csv','Excel'], key=file.name)

            if st.button(f"Downlaod {file.name} to {format_choice}"):
                output = BytesIO()
                if format_choice == 'csv':
                    df.to_csv(output, index=False)
                    mine = 'text/csv'
                    new_name = file.name.replace('xlsx','csv')
                else:
                    df.to_excel(output, index=False, engine='openpyxl')
                    mine = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    new_name = file.name.replace('csv','xlsx')
                     
                output.seek(0)
                st.download_button(new_name,data=output,mimetype=mine)


                st.success(f"{file.name} converted successfully to {format_choice}.")
                
                
