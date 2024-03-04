import pandas as pd
import streamlit as st
import altair as alt

st.title('Brazilian E-Commerce Dashboard :shopping_bags:')

# Load dataset
full_df = pd.read_csv("data used.csv")
full_df['order_purchase_timestamp'] = pd.to_datetime(full_df['order_purchase_timestamp'])
full_df['order_delivered_customer_date'] = pd.to_datetime(full_df['order_delivered_customer_date'])
full_df['order_purchase_timestamp'] = pd.to_datetime(full_df['order_purchase_timestamp'])
full_df['order_estimated_delivery_date'] = pd.to_datetime(full_df['order_estimated_delivery_date'])

Order_Quantity = full_df['order_id'].nunique()
Product_Quantity = full_df['product_id'].nunique()
Number_of_Customer = full_df['customer_id'].nunique()
Number_of_Seller = full_df['seller_id'].nunique()

st.text('Order Quantity')
st.write(Order_Quantity)

st.text('Product Quantity')
st.write(Product_Quantity)

st.text('Number of Customer')
st.write(Number_of_Customer)

st.text('Number of Seller')
st.write(Number_of_Seller)


# Bagaimana tren pembelian pada aplikasi dari tahun 2016 - 2018?
st.subheader('Top 10 Sellers by Number of Orders')
monthly_purchase = full_df.resample('M', on='order_purchase_timestamp')['price'].sum()
st.line_chart(monthly_purchase)

with st.expander("See explanation"):
    st.write(
        """Berdasarkan grafik tersebut dapat dilihat bahwa tren pembelian pada aplikasi E-Commerce cenderung meningkat dari tahun 2016-2018, namun mengalami beberapa fluktuasi pada titik waktu tertentu. Terlihat juga adanya pola musiman di mana harga cenderung meningkat di awal tahun.
        """
    )

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

with st.expander("See explanation"):
    st.write(
        """Berdasarkan grafik tersebut dapat dilihat bahwa negara bagian dengan total pembelian tertinggi berdasarkan harga berasal dari negara bagian Sao Paulo (SP) dengan tingkat pembelian di atas 5.000.000,
        diikuti oleh Rio de Janeiro (RJ), dan Minas Gerais (MG) dengan tingkat pembelian lebih dari 1.500.000. 
        Di sisi lain, Roraima (RR), Amapa (AP), dan Acre (AC) adalah negara bagian dengan tingkat pembelian terendah dengan angka di bawah 20.000.
        """
    )

# Bagaimana performa penjual berdasarkan jumlah pesanan dan total penjualan?
seller_performance = full_df.groupby(['seller_id']).agg({'order_id': 'count', 'price': 'sum'})
seller_performance.sort_values(by='order_id', ascending=False, inplace=True)
top_sellers = seller_performance.head(10)

st.subheader('Top 10 Sellers by Number of Orders')


chart = alt.Chart(top_sellers.reset_index()).mark_bar().encode(
    x=alt.X('seller_id:N', sort=alt.EncodingSortField(field='order_id', order='descending')),
    y='order_id',
    color=alt.value('skyblue')
).properties(width=alt.Step(80))

st.altair_chart(chart, use_container_width=True)

with st.expander("See explanation"):
    st.write(
        """Berdasarkan grafik tersebut dapat dilihat bahwa 10 seller dengan order quantity tertinggi memiliki tingkat jumlah pesanan di atas 1000 dalam rentang waktu 2 tahun.
        """
    )



st.caption('Copyright © Ario`s Project 2024')



