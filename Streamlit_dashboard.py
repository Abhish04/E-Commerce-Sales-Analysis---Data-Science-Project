import streamlit as st
import pandas as pd
import plotly.express as px
# import plotly.graph_objects as go
# import matplotlib.pyplot as plt

# functions 


# main codes
# executing main function
if __name__ == "__main__":
    # setting the page configuration
    st.set_page_config(page_title="E-Commerce Sales",page_icon="AVI",layout="wide")

    # custom bachground color
    st.markdown(
        """
        <style>
        body {
            background-color: #000000;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("E-Commerce Sales")

    st.sidebar.title("WELCOME")

    # upload file
    uploaded_file = st.sidebar.file_uploader("CHOOSE YOUR FILE:", type=["csv","xlsx"])


    if uploaded_file is not None:
        #read the file
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Invalid file type, Please upload CSV or Excel file.")
        except Exception as e:
            st.error(f"Error reading file: {e}")

        st.header("DATA PREPARATION")

        st.write("The first 5 rows and the shape of the DataFrame.")
        st.write(df.head(5))

        st.write("Shape and size of Dataframe:", df.shape)

        st.header("DATA EXPLORATION")


        explo1, explo2, explo3 = st.columns(spec=[1,1,1],gap="small")
        
        with explo1:
            # Examine data types
            st.write("Data Types:\n", df.dtypes)

        with explo2:
            # Check for missing values
            missing_values = df.isnull().sum()
            missing_percentage = (missing_values / len(df)) * 100
            st.write("\nMissing Values:\n", missing_values)
        
        with explo3:
            st.write("\nMissing Value Percentage:\n", missing_percentage)

        st.write("--")
        
        explo4, explo5 = st.columns(spec=[2,1],gap="small")
        # Descriptive statistics
        
        with explo4:
            st.write("\nDescriptive Statistics:\n", df.describe())
        
        with explo5:
            st.write("\nDescriptive Statistics for Quantity and UnitPrice:\n", df[['Quantity', 'UnitPrice']].describe())

        st.write("--")
        
        # Dimensions
        st.write("\nDataFrame Dimensions:", df.shape)

        # Unique values for categorical columns
        st.write("\nUnique Countries:\n", df['Country'].unique())

        st.header("DATA CLEANING")
        st.write("Cleaning the data by handling missing values, removing duplicates, and addressing outliers in 'Quantity' and 'UnitPrice'.")

        # Remove rows with missing 'Description'
        df.dropna(subset=['Description'], inplace=True)

        # Remove rows with missing 'CustomerID' (chosen strategy: remove rows)
        df.dropna(subset=['CustomerID'], inplace=True)

        # Remove duplicate rows
        df.drop_duplicates(inplace=True)


        cle1, cle2 = st.columns(spec=[1,1],gap="small")

        with cle1:
            # Investigate and handle outliers in 'Quantity'
            st.write(df['Quantity'].describe())
            # Remove negative quantity values.
            df = df[df['Quantity'] > 0]
            # Cap the 'Quantity' at the 99th percentile.
            quantity_99th = df['Quantity'].quantile(0.99)
            df['Quantity'] = df['Quantity'].clip(upper=quantity_99th)

        with cle2:
            # Investigate and handle outliers in 'UnitPrice'
            st.write(df['UnitPrice'].describe())
            # Remove values where 'UnitPrice' is less than 0.
            df = df[df['UnitPrice'] >= 0]
            # Cap the 'UnitPrice' at the 99th percentile
            unitprice_99th = df['UnitPrice'].quantile(0.99)
            df['UnitPrice'] = df['UnitPrice'].clip(upper=unitprice_99th)

        
        st.write("--")

        st.subheader("Data After Cleaning")
        st.write(df.head())

        st.header("DATA WRANGLING")
        st.write("Create new features as instructed: 'TotalSales', 'InvoiceMonth', 'InvoiceYear', and 'CustomerSegment'")
        
        # Calculate total sales value
        df['TotalSales'] = df['Quantity'] * df['UnitPrice']

        # Extract month and year from InvoiceDate
        df['InvoiceMonth'] = df['InvoiceDate'].dt.month
        df['InvoiceYear'] = df['InvoiceDate'].dt.year

        # Customer segmentation (example using quantiles)
        # You can adjust the quantiles or use other methods for segmentation.
        sales_quantiles = df['TotalSales'].quantile([0.33, 0.66])
        def customer_segment(sales):
            if sales <= sales_quantiles[0.33]:
                return 'Low'
            elif sales <= sales_quantiles[0.66]:
                return 'Medium'
            else:
                return 'High'
        df['CustomerSegment'] = df['TotalSales'].apply(customer_segment)

        st.write(df.head())

        st.header("DATA ANALYSIS")
        st.write("Calculating the total revenue, average order value, analyze sales trends, identify top-selling products and countries, and analyze customer purchase patterns.")

        # 1. Total revenue
        total_revenue = df['TotalSales'].sum().round(2)
        st.write(f"Total Revenue: {total_revenue}")

        # 2. Average Order Value (AOV)
        aov = df['TotalSales'].mean().round(2)
        st.write(f"Average Order Value: {aov}")

        st.write("--")
        
        col1, col2, col3 = st.columns(spec=[1,1,1],gap="small")

        with col1:
            # 3. Sales trends over time (monthly)
            monthly_sales = df.groupby('InvoiceMonth')['TotalSales'].sum()
            st.write("\nMonthly Sales:\n", monthly_sales)

        with col2:
            # 4. Top 5 best-selling products
            top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(5)
            st.write("\nTop 5 Best-Selling Products:\n", top_products)

        with col3:
            # 5. Top 5 countries by revenue
            top_countries = df.groupby('Country')['TotalSales'].sum().sort_values(ascending=False).head(5)
            st.write("\nTop 5 Countries by Revenue:\n", top_countries)

        
        st.write("--")
        col4, col5, col6 = st.columns(spec=[1,1,1],gap="small")

        with col4:
            # 6. Customer purchase patterns
            # Frequency of purchases
            customer_frequency = df.groupby('CustomerID')['InvoiceNo'].count()
            st.write("\nCustomer Purchase Frequency:\n", customer_frequency.head())

        with col5:
            # Monetary value of transactions
            customer_monetary_value = df.groupby('CustomerID')['TotalSales'].sum()
            st.write("\nCustomer Monetary Value:\n", customer_monetary_value.head())

        with col6:
            # Average number of items per order
            customer_avg_items = df.groupby('CustomerID')['Quantity'].mean()
            st.write("\nCustomer Average Items per Order:\n", customer_avg_items.head())

        
        st.write("--")
        # Analyze purchase patterns by customer segment
        segment_analysis = df.groupby('CustomerSegment')['TotalSales'].agg(['mean', 'sum', 'count'])
        st.write("\nCustomer Segment Analysis:\n", segment_analysis)

        st.header("DATA VISUALISATION")
        st.write("Visualizing the data to gain insights and understand the trends and patterns in the data")

        # 1. Sales Trends (Monthly)
        st.subheader("Monthly Sales Trend")
        monthly_sales = df.groupby('InvoiceMonth')['TotalSales'].sum().reset_index()
        fig_monthly_sales = px.line(monthly_sales, x='InvoiceMonth', y='TotalSales', title='Monthly Sales Trend', labels={'InvoiceMonth': 'Month', 'TotalSales': 'Total Sales'}, markers=True)
        fig_monthly_sales.update_traces(line=dict(width=2.5), marker=dict(size=8))
        fig_monthly_sales.update_layout(hovermode="x unified")
        st.plotly_chart(fig_monthly_sales)

        # 2. Top-Selling Products
        st.subheader("Top 10 Best-Selling Products")
        top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_top_products = px.bar(top_products, x='Quantity', y='Description', orientation='h', title='Top 10 Best-Selling Products', labels={'Quantity': 'Total Quantity Sold', 'Description': 'Product Description'}, color='Quantity')
        fig_top_products.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_top_products)

        # 3. Geographic Distribution of Sales
        st.subheader("Geographic Distribution of Sales")
        country_sales = df.groupby('Country')['TotalSales'].sum().reset_index()
        fig_country_sales = px.choropleth(country_sales, locations='Country', locationmode='country names', color='TotalSales', hover_name='Country', title='Geographic Distribution of Sales', color_continuous_scale='Viridis', labels={'TotalSales': 'Total Sales'})
        st.plotly_chart(fig_country_sales)

        # 4. Customer Segmentation
        st.subheader("Distribution of Customers Across Segments")
        customer_segment_counts = df['CustomerSegment'].value_counts().reset_index()
        fig_customer_segments = px.pie(customer_segment_counts, values='count', names='CustomerSegment', title='Distribution of Customers Across Segments', color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_customer_segments)

        # 5. Additional Visualization (Scatter plot)
        st.subheader("Quantity vs. Unit Price")
        fig_scatter = px.scatter(df, x='Quantity', y='UnitPrice', title='Quantity vs. Unit Price', labels={'Quantity': 'Quantity', 'UnitPrice': 'Unit Price'}, color='CustomerSegment', hover_data=['TotalSales', 'Description'])
        st.plotly_chart(fig_scatter)


        st.header("SUMMARY")

        st.subheader("Q&A")
        st.write("What are the key sales metrics? Total revenue is 7,641,742.08, and the average order value (AOV) is 19.46.")
        st.write("What are the top-selling products and countries? \"JUMBO BAG RED RETROSPOT\" is the top-selling product. The UK is the top revenue-generating country, followed by EIRE, Netherlands, Germany, and France.")
        st.write("What are the observed sales trends? Monthly sales data show fluctuations, with November exhibiting the highest sales (1,064,716.86), likely due to seasonality.")
        st.write("How are customers segmented, and what are their purchase patterns? Customers are segmented into \"Low\", \"Medium\", and \"High\" spending groups based on tercile quantiles of total sales. Further analysis of purchase frequency, monetary value, and average items per order is provided by customer ID.")

        st.subheader("2. Data Analysis Key Findings")
        st.write("Significant Missing Data: 24.93% of customer IDs were missing, requiring removal of those rows for subsequent analysis.")
        st.write("Outlier Handling: Outliers were present in both 'Quantity' and 'UnitPrice' columns. Negative quantities were removed, and outliers were capped at the 99th percentile for both features to avoid skewed results.")
        st.write("November Sales Peak: Monthly sales analysis reveals a peak in November (1,064,716.86), suggesting potential holiday seasonality impacting sales.")
        st.write("Product and Geographic Focus: \"JUMBO BAG RED RETROSPOT\" is the top-selling product. The UK significantly dominates revenue, with other European countries showing substantial contributions.")
        st.write("Customer Segmentation: Customers were segmented into three groups based on total sales, allowing for analysis of purchase patterns within each segment.")

        st.subheader("3. Insights or Next Steps")
        st.write("Investigate November Sales Peak: Analyze the drivers behind the November sales peak. Further investigate promotions or marketing activities conducted during this month.")
        st.write("Refine Customer Segmentation: Explore more sophisticated customer segmentation techniques (e.g., RFM analysis) to gain deeper insights into customer")

    else:
        st.header("PLEASE UPLOAD YOUR DATA THROUGH SIDEBAR FOR ANALYSIS")