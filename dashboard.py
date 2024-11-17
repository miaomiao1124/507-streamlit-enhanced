import streamlit as st
import pandas as pd
import plotly.express as px

# Header and Subheader
st.header("2024 AHI 507 Streamlit Dashboard")
st.subheader("Exploring school learning modalities data from NCES for 2021")

st.text("""
This dashboard focuses on the recently released school learning modalities data 
from the National Center for Education Statistics (NCES) for the academic year 2020-2021.
""")

# Load data
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000")
df['week_recoded'] = pd.to_datetime(df['week'])
df['zip_code'] = df['zip_code'].astype(str)

# Summary metrics
st.write("### Dataset Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Columns", df.shape[1])
col2.metric("Rows", len(df))
col3.metric("Unique Districts/Schools", df['district_name'].nunique())

# Display raw data
st.write("### Raw Data")
st.dataframe(df)

# Pivot table for weekly learning modality trends
table = pd.pivot_table(df, values='student_count', index=['week'], 
                       columns=['learning_modality'], aggfunc="sum").reset_index()

# Bar charts for each learning modality
st.write("### Weekly Trends for Each Learning Modality")
st.bar_chart(data=table.set_index("week")[["Hybrid"]])
st.bar_chart(data=table.set_index("week")[["In Person"]])
st.bar_chart(data=table.set_index("week")[["Remote"]])

# Line chart for trends across all modalities
st.write("### Trends Across All Learning Modalities")
st.line_chart(data=table.set_index("week")[["Hybrid", "In Person", "Remote"]])

# Histogram for student count distribution
st.write("### Distribution of Student Counts by Learning Modality")
fig_hist = px.histogram(df, x="student_count", color="learning_modality", nbins=10,
                        title="Distribution of Student Counts Across Modalities")
st.plotly_chart(fig_hist)

# Interactive filter by district
st.write("### Filter Data by District")
districts = df['district_name'].unique()
selected_district = st.selectbox("Select a District", districts)
filtered_data = df[df['district_name'] == selected_district]

st.write(f"Data for District: {selected_district}")
st.write(filtered_data[['week', 'learning_modality', 'student_count']])
