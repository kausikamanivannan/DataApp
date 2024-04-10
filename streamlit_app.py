import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
import math

st.title("Data App Assignment")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

selected_category = st.selectbox("Select a Category", df['Category'].unique())

filtered_df = df[df['Category'] == selected_category]

selected_subcategories = st.multiselect("Select Subcategories", filtered_df['Sub_Category'].unique())

filtered_df = filtered_df[filtered_df['Sub_Category'].isin(selected_subcategories)]

if not filtered_df.empty:
    sales_by_date = filtered_df.groupby('Order_Date')['Sales'].sum()
    st.line_chart(sales_by_date)

    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    overall_profit_margin = (total_profit / total_sales) * 100

    st.write("### Metrics")
    st.metric(label="Total Sales", value=total_sales)
    st.metric(label="Total Profit", value=total_profit)
    st.metric(label="Overall Profit Margin (%)", value=overall_profit_margin)

    overall_avg_profit_margin = (df['Profit'].sum() / df['Sales'].sum()) * 100

    profit_margin_difference = overall_profit_margin - overall_avg_profit_margin
    st.metric(label="Profit Margin Difference", value=profit_margin_difference, delta=True)
else:
    st.write("No data available for the selected category and subcategories.")
