import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
from math import sqrt
plt.rcParams["figure.figsize"]=10,5


def linespace(n_lines):
    for i in range(n_lines):
        st.text("")


def impermanent_loss(price_ratio):
   return 2 * (sqrt(price_ratio) / (1 + price_ratio)) - 1


def impermanent_loss_weight(asset_1_change, asset_1_weight,
                            asset_2_change, asset_2_weight):
   value_held = ((1 + asset_1_change/100) * (asset_1_weight/100)) + ((1 + asset_2_change/100) * (asset_2_weight/100))
   value_pool = ((1 + asset_1_change/100) ** (asset_1_weight/100)) * ((1 + asset_2_change/100) ** (asset_2_weight/100))
   if asset_1_change == asset_2_change:
       il=0
       
   else:
       il = value_pool/value_held - 1
   #return {"Value pool":value_pool, "Value held":value_held, "Impermanent Loss":il}
   return il

  
class Asset:
    def __init__(self, name, price_change):
        self.name = name
        self.price_change = price_change
        self.impermanent_loss = impermanent_loss(1 + self.price_change)





st.title('Impermanent Loss Visualization')

columns = st.beta_columns(4)


with columns[0]:
    st.header("Asset")
    asset_name = st.text_input("Asset", value="ETH")
    asset_name_2 = st.text_input("Asset", value="BAL")

with columns[1]:
    st.header('Price change')
    asset_price_change=st.number_input("Price Change %", value=0.0, 
                                        min_value=-100.0, max_value=400.0,key=0)                  
    asset_price_change_2=st.number_input("Price Change %", value=0.0, 
                                        min_value=-100.0, max_value=400.0,key=1)

with columns[2]:
    st.header('Pool weight')

    weight = st.number_input("Pool weight%", value=50.0, 
                             min_value=1.0, max_value=100.0,key=0)
    weight_2 = st.number_input("Pool weight%", value=50.0, 
                               min_value=1.0, max_value=100.0,key=1)

with columns[3]:
    linespace(7)
    remove = st.button("Remove {}".format(asset_name))
    linespace(2)
    remove_2 = st.button("Remove {}".format(asset_name_2))

il = impermanent_loss_weight(asset_price_change,weight,asset_price_change_2, weight_2)
# Make chart
price_ratio_list = np.linspace(0, 5, 1000)
price_ratio_list = 100 * price_ratio_list
price_change_list = np.linspace(-1, 4, 1000)



if (asset_name and asset_name_2):
    impermanent_loss_list = [100 * impermanent_loss_weight(price_change, weight, 0, weight_2) for price_change in price_change_list]
    price_ratio = (1+asset_price_change*weight/100)/(1+asset_price_change_2*weight_2/100)
    asset = Asset(asset_name, asset_price_change/100)

    st.header("Impermament loss: {:.2f}%".format(abs(100*il)))
    st.write("Asset price ratio: {:.2f}".format(price_ratio))
    st.write("Asset:", asset_name, "Price change: {:.2f}%".format(asset_price_change))

    fig, ax = plt.subplots()
    ax.scatter(100*(price_ratio), 100*il, s=50, color='r')
    ax.plot(price_ratio_list, impermanent_loss_list, zorder=0)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_xlabel("Current price as percentage of initial price")
    ax.set_ylabel("Change in total liquidity value")
    st.pyplot(fig)


