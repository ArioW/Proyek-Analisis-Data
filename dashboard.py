import pandas as pd
import streamlit as st
import altair as alt

st.title('Brazilian E-Commerce Dashboard')

# Load dataset
full_df = pd.read_csv("full data.csv")
full_df['order_purchase_timestamp'] = pd.to_datetime(full_df['order_purchase_timestamp'])
full_df['order_delivered_customer_date'] = pd.to_datetime(full_df['order_delivered_customer_date'])
full_df['order_purchase_timestamp'] = pd.to_datetime(full_df['order_purchase_timestamp'])
full_df['order_estimated_delivery_date'] = pd.to_datetime(full_df['order_estimated_delivery_date'])

# Bagaimana tren pembelian pada aplikasi dari tahun 2016 - 2018?
st.subheader('Top 10 Sellers by Number of Orders')
monthly_purchase = full_df.resample('M', on='order_purchase_timestamp')['price'].sum()
st.line_chart(monthly_purchase)

# Negara mana dengan total pembelian tertinggi?
total_purchase_by_state = full_df.groupby('customer_state')['price'].sum()
sorted_states = total_purchase_by_state.sort_values(ascending=False).reset_index()
data = sorted_states.sort_values(by='price', ascending=False)
st.subheader('Total Purchase by State')
bar_chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('customer_state:N', title='Negara Pelanggan', sort=alt.EncodingSortField(field='price', op='sum', order='descending')),
    y=alt.Y('price:Q', title='Total Pembelian'),
    color=alt.condition(
        alt.datum.price == alt.expr.max('price'),
        alt.value('orange'),
        alt.value('blue')
    )
).properties(
    width=600,
    height=400
)
st.altair_chart(bar_chart, use_container_width=True)

# Bagaimana performa penjual berdasarkan jumlah pesanan dan total penjualan?

seller_performance = full_df.groupby(['seller_id']).agg({'order_id': 'count', 'price': 'sum'})
seller_performance.sort_values(by='order_id', ascending=False, inplace=True)
top_sellers = seller_performance.head(10)

# Streamlit app
st.subheader('Top 10 Sellers by Number of Orders')

# Altair bar plot with ordinal scale for X-axis
chart = alt.Chart(top_sellers.reset_index()).mark_bar().encode(
    x=alt.X('seller_id:N', sort=alt.EncodingSortField(field='order_id', order='descending')),
    y='order_id',
    color=alt.value('skyblue')
).properties(width=alt.Step(80))

st.altair_chart(chart, use_container_width=True)







