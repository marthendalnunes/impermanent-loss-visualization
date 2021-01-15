import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
from math import sqrt
plt.rcParams["figure.figsize"]=10,5


def impermanent_loss(price_ratio):
   return 2 * (sqrt(price_ratio) / (1 + price_ratio)) - 1


class Asset:
    def __init__(self, name, price_change):
        self.name = name
        self.price_change = price_change
        self.impermanent_loss = impermanent_loss(1 + self.price_change)


# Make chart
price_ratio_list = np.linspace(0, 5, 1000)
impermanent_loss_list = [100 * impermanent_loss(price_ratio) for price_ratio in price_ratio_list]
price_ratio_list = 100 * price_ratio_list


st.title('Impermanent Loss Visualization')

asset_name = st.text_input("Asset", value="ETH")
asset_price_change=st.number_input("Price Change %", value=0.0, min_value=-100.0, max_value=400.0)

if asset_name:
    price_ratio = 1 + asset_price_change/100
    asset = Asset(asset_name, asset_price_change/100)

    st.header("Impermament loss: {:.2f}%".format(abs(100*asset.impermanent_loss)))
    st.write("Asset price ratio: {:.2f}".format(price_ratio))
    st.write("Asset:", asset_name, "Price change: {:.2f}%".format(asset_price_change))

    fig, ax = plt.subplots()
    ax.scatter(100*(asset.price_change+1), 100*asset.impermanent_loss, s=50, color='r')
    ax.plot(price_ratio_list, impermanent_loss_list, zorder=0)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_xlabel("Current price as percentage of initial price")
    ax.set_ylabel("Change in total liquidity value")
    st.pyplot(fig)


