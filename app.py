import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Growth", layout="wide")

# Custom CSS for dark mode
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("🔄 Data Transformer")
st.write("## Convert your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader("**Upload your files (CSV or Excel)**", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Read file based on format
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue
        
        st.subheader(f"📄 Preview of {file.name}")
        st.dataframe(df.head())
        
        # Data Cleaning Options
        with st.expander(f"🛠 Data Cleaning Options for {file.name}"):
            if st.checkbox(f"Remove duplicates in {file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates removed!")
            
            if st.checkbox(f"Fill missing values in {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✅ Missing values filled!")
            
            # Column selection
            selected_columns = st.multiselect(f"Select columns to keep for {file.name}", df.columns, default=df.columns)
            df = df[selected_columns]
        
        # Data Visualization
        with st.expander(f"📊 Data Visualization for {file.name}"):
            if not df.select_dtypes(include='number').empty:
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
            else:
                st.warning("⚠ No numerical data available for visualization.")
        
        # File Conversion
        with st.expander(f"🔄 Conversion Options for {file.name}"):
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                else:
                    df.to_excel(buffer, index=False, engine='xlsxwriter')
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
                buffer.seek(0)
                st.download_button(
                    label=f"Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
        
    st.success("🎉 All files processed successfully!")