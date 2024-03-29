import pandas as pd

def calculate_sales_overview(df, selected_year):
    try:
        current_year = int(selected_year[0])
        previous_year = current_year - 1

        df_current_year = df[(df['Year'] == current_year)]

        sales_current_year = df_current_year['Sales'].sum()
        sales_previous_year = df[(df['Year'] == previous_year)]['Sales'].sum()
        average_sales_per_unit = df_current_year['Sales'].sum() / df_current_year['Quantity'].sum()

        annual_sales = df.groupby('Year')['Sales'].sum().reset_index()
        annual_sales['YoY Growth'] = (annual_sales['Sales'].pct_change()) * 100
        yoy_growth_current_year = annual_sales[annual_sales['Year'] == current_year]['YoY Growth']
        print(f"Year on Year growth: {yoy_growth_current_year}%")
        
        preprocessed_data = {
            'sales_current_year': sales_current_year,
            'sales_previous_year': sales_previous_year,
            'average_sales_per_unit': average_sales_per_unit,
            'yoy_growth_current_year': yoy_growth_current_year,
        }

        return preprocessed_data
    except Exception as e:
        print(f"Error calculating sales overview: {e}")


def calculate_profit_overview(df, selected_year):
    try:
        current_year = int(selected_year[0])
        previous_year = selected_year[0] - 1

        profit_current_year = df[df['Year'] == current_year]['Profit'].sum()
        profit_previous_year = df[df['Year'] == previous_year]['Profit'].sum()

        average_profit_per_unit = df[(df['Year'] == current_year)]['Profit'].sum() / df[(df['Year'] == current_year)]['Quantity'].sum()
        annual_profit = df.groupby('Year')['Profit'].sum().reset_index()
        annual_profit['YoY Growth'] = (annual_profit['Profit'].pct_change()) * 100
        yoy_growth_current_year = annual_profit[annual_profit['Year'] == current_year]['YoY Growth']

        preprocessed_data = {
            'profit_current_year': profit_current_year,
            'profit_previous_year': profit_previous_year,
            'average_profit_per_unit': average_profit_per_unit,
            'yoy_growth_current_year': yoy_growth_current_year,
        }
        
        return preprocessed_data
    except Exception as e:
        print(f"Error calculating profit overview: {e}")


def calculate_monthly_sales_profit_data(df, selected_years, column):

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    current_year = int(selected_years[0])
    previous_year = current_year - 1
        
    monthly_data = df.groupby(['Year', 'Month'])[column].sum().unstack('Year')
    
    # Fill missing months with zeros
    for month in month_order:
        if month not in monthly_data.index:
            monthly_data.loc[month] = 0
            
    monthly_data = monthly_data.reindex(month_order)
    
    if previous_year not in monthly_data.columns:
        monthly_data[previous_year] = 0

    monthly_data = monthly_data[[previous_year, current_year]].fillna(0)
    monthly_data = monthly_data.reindex(columns=sorted(monthly_data.columns))

    prev = monthly_data[previous_year].sum()
    current_year = monthly_data[current_year].sum()

    print(f"Total {column} in Prev: {prev}")
    print(f"Total {column} in Current: {current_year}")

    return monthly_data



def calculate_top_product_with_sales(df, selected_years):

    df_year_filtered = df[df['Order Date'].dt.year == int(selected_years[0])]
    top_products = df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()

    total_sales_all_products = df_year_filtered['Sales'].sum()

    top_products['Sales Percent'] = (top_products['Sales'] / total_sales_all_products) * 100

    print("Top products")
    print(top_products)
    return top_products



def calculate_monthly_profit(df, selected_years):
    current_year = int(selected_years[0])
    previous_year = current_year - 1

    monthly_profit = df.groupby(['Year', 'Month'])['Profit'].sum().unstack('Year')
    
    if previous_year not in monthly_profit.columns:
        monthly_profit[previous_year] = 0

    monthly_profit = monthly_profit[[previous_year, current_year]]
    monthly_profit = monthly_profit.reindex(columns=sorted(monthly_profit.columns))

    return monthly_profit



def calculate_top_products_by_profit(df, selected_years):

    df = df[df['Order Date'].dt.year == int(selected_years[0])]
    top_products = df.groupby('Product Name')['Profit'].sum().nlargest(5).reset_index()
    total_profit = df['Profit'].sum()

    top_products['Profit Percent'] = (top_products['Profit'] / total_profit) * 100
    return top_products