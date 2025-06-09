import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="AI Excel Analyzer", layout="wide")

st.title("📊 Excel Analyzer")

uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["csv", "xlsx"])

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
                st.markdown("**Histogram**")
                selected_col = st.selectbox("Select column for histogram", numeric_cols)
                plt.figure(figsize=(10, 4))
                sns.histplot(df[selected_col], kde=True)
                plt.title(f"Distribution of {selected_col}")
                st.pyplot(plt.gcf())

            with col2:
                st.markdown("**Box Plot**")
                selected_col2 = st.selectbox("Select column for box plot", numeric_cols, key="box")
                plt.figure(figsize=(6, 4))
                sns.boxplot(y=df[selected_col2], color="orange")
                plt.title(f"Box Plot of {selected_col2}")
                st.pyplot(plt.gcf())
        else:
            st.warning("No numeric columns available for charting.")

        st.subheader("4️⃣ Summary Insight")
        st.success(f"This dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")
        st.info(f"Column types: {dict(df.dtypes)}")
        if 'date' in df.columns or any('date' in col.lower() for col in df.columns):
            st.markdown("🕒 This dataset appears to contain time-series data.")

    except Exception as e:
        st.error(f"Something went wrong while processing your file: {e}")
