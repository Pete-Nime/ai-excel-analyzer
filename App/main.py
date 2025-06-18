import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from openai import OpenAI
import os

# Set up Streamlit page
st.set_page_config(page_title="AI Excel Analyzer", layout="wide")
st.title("📊 Excel Analyzer with GPT-4o")

# Set OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Sample dataset download (optional link)
st.markdown("📥 [Download Sample Dataset](https://ai-excel-analyzer.streamlit.app/sample_sales_data.csv)")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["csv", "xlsx"])

# GPT-4o Analysis Function
def generate_ai_insight(df):
    prompt = f"""
You are a data analyst AI. Analyze this dataset and return:
1. A short plain-English description.
2. Patterns or trends (if any).
3. Business suggestions.

First 5 rows:
{df.head(5).to_string()}

Data Types:
{dict(df.dtypes)}

Summary Stats:
{df.describe(include='all').to_string()}
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful data analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content

# Main app logic
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)

        st.subheader("1️⃣ First 5 Rows of Your Data")
        st.dataframe(df.head())

        st.subheader("2️⃣ Descriptive Summary")
        st.write(df.describe(include="all"))

        st.subheader("3️⃣ Visual Insights")
        numeric_cols = df.select_dtypes(include='number').columns.tolist()

        if numeric_cols:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📉 Histogram**")
                selected_col = st.selectbox("Choose a column", numeric_cols)
                plt.figure(figsize=(10, 4))
                sns.histplot(df[selected_col], kde=True)
                plt.title(f"Distribution of {selected_col}")
                st.pyplot(plt.gcf())

            with col2:
                st.markdown("**📦 Box Plot**")
                selected_col2 = st.selectbox("Choose a column", numeric_cols, key="box")
                plt.figure(figsize=(6, 4))
                sns.boxplot(y=df[selected_col2], color="orange")
                plt.title(f"Box Plot of {selected_col2}")
                st.pyplot(plt.gcf())
        else:
            st.warning("No numeric columns found.")

        st.subheader("4️⃣ AI-Generated Insights (Powered by GPT-4o)")
        with st.spinner("💡 Analyzing with AI... Please wait."):
            ai_result = generate_ai_insight(df)
            st.markdown(f"```markdown\n{ai_result}\n```")

        st.success("✅ Analysis Complete!")

    except Exception as e:
        st.error(f"❌ Error processing your file:\n\n{e}")
