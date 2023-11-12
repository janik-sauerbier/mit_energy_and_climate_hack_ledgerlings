import os
import streamlit as st
import streamlit.components.v1 as components
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
import pandas as pd
import numpy as np
from openai import OpenAI
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Function to create sparklines
def plot_sparkline(data):
    plt.figure(figsize=(2, 0.5))  # Adjust the size as needed
    plt.plot(data, color='green')
    ax = plt.gca()  # Get the current axis
    ax.get_xaxis().set_visible(False)  # Hide the x-axis
    ax.get_yaxis().set_visible(False)  # Hide the y-axis
    for spine in plt.gca().spines.values():  # Remove borders
        spine.set_visible(False)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight', pad_inches=0)  # Save plot to a buffer
    plt.close()
    return buf




# Load your CSV file
df = pd.read_csv('datasets/Company Database - rev.s+emissions.csv')


search_query = st.text_input("Enter your search term")

def search_data(query, data):
    if query:  # only search if there is a query
        # Simple case-insensitive search across the DataFrame
        return data[data.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    return data  # return all data if no query

#Display Result
if search_query:
    # Filter DataFrame based on search query
    filtered_data = df[df['Symbol'].str.contains(search_query, case=False)]

    # Display each row in a separate box with a sparkline
    for index, row in filtered_data.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])  # Adjust column widths as needed

            with col1:
                st.subheader(row['Symbol'])
                st.text(f" Revenues 2022: {row[' Revenues 2022']}")  # Replace 'Column2'
                st.text(f"Emissions 2022: {row['Emissions 2022']}")  # Replace 'Column3'# Display other data if necessary

            with col2:
                # Assuming 'YearlyData' is a column with comma-separated numbers
                for _ in range(3):  # Adjust the range for more or less padding
                    st.empty()
                data_series = [float(x) for x in row['Emissions 2022'].split(',')]
                st.image(plot_sparkline(data_series), use_column_width=True)
                st.markdown('<p style="font-weight:bold; font-size: 14px;">Carbon Emissions over time</p>', unsafe_allow_html=True)                       
                st.empty()
                st.text(f"Esg Performance: {row['Esg Performance']}")  # Replace 'Column2'

            st.markdown("---")  # Adds a horizontal line for separation




# Custom CSS to inject contained within a Markdown
st.markdown("""
<style>
.box {
    height: 200px;
    background-color: #F3F3F3;
    border: 2px solid #FFFFFF;
    border-radius: 10px;  # Adjust for rounded corners
    padding: 50px;
    margin: 10px;
}
</style>
""", unsafe_allow_html=True)

# Layout with 2 columns
col1, col2 = st.columns(2)

# First column with two boxes
with col1:
    # First box
    st.image("datasets/emissions.png", caption="Top 10 Companies by Emissions")
    # Second box
    st.image("datasets/revenue.png", caption="Top 10 Companies by Revenue")

# Second column with two boxes
with col2:
    # Third box
    st.image("datasets/esg_score.png", caption="Top 10 Companies by ESG Score")
    # Fourth box
    st.image("datasets/fdx.png", caption="Cumulative emissions of top polluter")
    