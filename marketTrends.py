import pandas as pd

# Load the dataset
all_data = pd.read_csv('ALL_mix_data/2023_sales_data.csv')

# Convert 'Date' column to datetime format
all_data['Date'] = pd.to_datetime(all_data['Date'], format='%d/%m/%Y')

# Extract month and year for analysis
all_data['Month'] = all_data['Date'].dt.month
all_data['Year'] = all_data['Date'].dt.year

# Group data by month and category for trends
monthly_sales = all_data.groupby(['Year', 'Month', 'Category']).agg({
    'Total': 'sum',
    'Quantity': 'sum'
}).reset_index()

# Identify top-performing and underperforming months
total_sales_month = all_data.groupby(['Year', 'Month'])['Total'].sum().reset_index()
top_months = total_sales_month.sort_values(by='Total', ascending=False).head(4)
underperforming_months = total_sales_month.sort_values(by='Total').head(4)

# Analyze category performance
category_performance = all_data.groupby('Category')['Total'].sum().sort_values(ascending=False).reset_index()

# Analyze payment method preference
payment_analysis = all_data.groupby('Payment_Method')['Total'].sum().sort_values(ascending=False).reset_index()

# Gender-based purchasing trends
gender_trends = all_data.groupby('Gender').agg({
    'Total': 'sum',
    'Quantity': 'sum'
}).reset_index()

# Market Recommendations
recommendations = []

# Identify top-performing categories
top_categories = category_performance.head(2)['Category'].tolist()
recommendations.append(f"Focus marketing efforts on top categories: {', '.join(top_categories)}.")

# Seasonal trends
if top_months['Month'].isin([12, 1, 4]).any():
    recommendations.append("Plan promotions around festive seasons and summer holidays.")

# Underperforming month action
recommendations.append("Consider discount campaigns or introducing new products during underperforming months.")

# Payment trends
popular_payment = payment_analysis.iloc[0]['Payment_Method']
recommendations.append(f"Encourage the use of '{popular_payment}' by offering exclusive discounts or rewards.")

# Gender-based trends
if gender_trends.loc[0, 'Total'] > gender_trends.loc[1, 'Total']:
    recommendations.append("Target promotional campaigns more towards Male customers.")
else:
    recommendations.append("Target promotional campaigns more towards Female customers.")

# Print results
print("Market Trend Analysis and Recommendations")
print("\nTop Performing Months:")
print(top_months)
print("\nUnderperforming Months:")
print(underperforming_months)
print("\nCategory Performance:")
print(category_performance)
print("\nPayment Method Analysis:")
print(payment_analysis)
print("\nGender-Based Trends:")
print(gender_trends)
print("\nRecommendations:")
for rec in recommendations:
    print(f"- {rec}")
