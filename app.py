import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import serpapi
import requests

medicine_company=[]
med_price=[]

def compare(med_name):
    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "engine": "google_shopping",
        "q": med_name,
        "api_key": "pYqYRA8smRUSGotm4AqdLk5g",
        "gl":"in"
    }

    response = requests.get(url, params=params)
    data = response.json()
    shopping_results = data["shopping_results"]
    return shopping_results

c1, c2 = st.columns(2)
c1.image("logo.png", width=200)
c2.header("E-Pharmacy price comparison system")

st.sidebar.title("Enter name of medicine")
med_name = st.sidebar.text_input("Enter Name Here: ")
number = st.sidebar.text_input("Enter number of options here: ")

if st.sidebar.button("Search"):
    if med_name:
        shopping_results = compare(med_name)
        
        if shopping_results:
            if number and number.isdigit():
                shopping_results = shopping_results[:int(number)]
            
            lowest_price = float('inf')
            lowest_price_index = 0
            
            for i in range(len(shopping_results)):
                price_str = shopping_results[i].get('price', '$0')
                current_price = float(price_str.replace('$', '').replace(',', '').replace('₹', '').split()[0])
                medicine_company.append(shopping_results[i].get('seller'))
                med_price.append(float(price_str.replace('$', '').replace(',', '').replace('₹', '').split()[0]))
                
                if current_price < lowest_price:
                    lowest_price = current_price
                    lowest_price_index = i
            
            # Display best option
            st.success("🏆 Best Option Found!")
            best = shopping_results[lowest_price_index]
            st.write(f"**Title:** {best.get('title')}")
            st.write(f"**Price:** {best.get('price')}")
            st.write(f"**Seller:** {best.get('seller')}")
            
            st.markdown(f"**Buy Link:** [View Product]({best.get('product_link')})")
            
            # Show all results
            st.subheader("All Results:")
            for i, product in enumerate(shopping_results, 1):
                st.write(f"{i}. {product.get('title')} - {product.get('price')} ({product.get('seller')})")
                st.markdown(f" **Link:** [View Product]({product.get('product_link')})")
        else:
            st.warning("No results found")
    else:
        st.warning("Please enter a medicine name")
    
    #Chart Comparison
    df=pd.DataFrame(med_price, medicine_company)
    st.title("Chart Comparison")
    st.bar_chart(df)
    
    
    #Pie Chart
    st.title("Pie Chart")
    fig, ax = plt.subplots(figsize=(5,5))
    ax.pie(med_price, labels=medicine_company, shadow=True, autopct='%1.1f%%')
    ax.axis("equal")
    st.pyplot(fig)