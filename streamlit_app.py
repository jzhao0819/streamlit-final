import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on March 17th")

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

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on March 17th")

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

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")

import streamlit as st
import pandas as pd

# Load data
@st.cache_data  # Cache data to improve performance
def load_data():
    df = pd.read_csv("Superstore_Sales_utf8.csv")  # Ensure the file contains 'Category', 'Sub_Category', 'Sales', 'Profit' columns
    return df

df = load_data()

# Title
st.title("Sales Data Analysis App")

# (1) Add a dropdown to select Category
category = st.selectbox("Select Category", df["Category"].unique())

# (2) Add a multi-select to choose Sub_Category
sub_categories = st.multiselect(
    "Select Sub_Category",
    df[df["Category"] == category]["Sub_Category"].unique()
)

# Filter data
filtered_data = df[(df["Category"] == category) & (df["Sub_Category"].isin(sub_categories))]

# (3) Show a line chart of sales for the selected items
if not filtered_data.empty:
    st.header("Sales Trend")
    # Convert date and aggregate by month
    filtered_data["Order_Date"] = pd.to_datetime(filtered_data["Order_Date"])
    filtered_data.set_index("Order_Date", inplace=True)
    monthly_sales = filtered_data.groupby([pd.Grouper(freq="M"), "Sub_Category"])["Sales"].sum().unstack().fillna(0)

    # Plot line chart of monthly sales trend
    st.line_chart(monthly_sales)

# (4) Show three metrics
if not filtered_data.empty:
    total_sales = filtered_data["Sales"].sum()
    total_profit = filtered_data["Profit"].sum()
    overall_profit_margin = (total_profit / total_sales) * 100

    # Calculate the overall average profit margin (all products across all categories)
    overall_avg_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", f"${total_sales:,.2f}")
    with col2:
        st.metric("Total Profit", f"${total_profit:,.2f}")
    with col3:
        st.metric(
            "Overall Profit Margin (%)",
            f"{overall_profit_margin:.2f}%",
            delta=f"{overall_profit_margin - overall_avg_profit_margin:.2f}%",  # (5) Use delta to show the difference
        )
else:
    st.write("Please select Sub_Category to view metrics.")
