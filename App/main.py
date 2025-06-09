import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Excel Analyzer", layout="wide")

st.title("📊 AI Excel Analyzer")
st.write("Upload your Excel or CSV file to get insights.")

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    
    st.subheader("📄 Preview")
    st.dataframe(df.head())

    st.subheader("🧠 Summary (Coming Soon)")
    st.info("This would use GPT to summarize the dataset.")
    
    st.subheader("📈 Auto Charts")
    st.bar_chart(df.select_dtypes(include='number'))
