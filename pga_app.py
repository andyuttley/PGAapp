import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from PIL import Image

#Create header
st.write(
    """
    # PGA Data Modeller     
    """)

st.write(
    """
    Using data scraped from www.pgatour.com 
    Use the left side of the screen to apply  weightings to the different metrics. This will 
    give you a ranked 'predicted outcome' based on your selections.
    """)

#Bring in the data
data = pd.read_excel('/Users/andrewuttley/Desktop/PGAapp/PGA_Database.xlsx')

#Create and name sidebar
st.sidebar.header('Choose your weightings')

st.sidebar.write("""#### Choose your SG bias""")
def user_input_features():
    sgott = st.sidebar.slider('SG Off the Tee', 0, 100, 90, 5)
    sga2g = st.sidebar.slider('SG Approach to Green', 0, 100, 80, 5)
    sgatg = st.sidebar.slider('SG Around the Green', 0, 100, 50, 5)
    sgputt = st.sidebar.slider('SG Putting', 0, 100, 70, 5)

    user_data = {'SG OTT': sgott,
                 'SG A2G': sga2g,
                 'SG ATG': sgatg,
                 'SG Putt': sgputt}
    features = pd.DataFrame(user_data, index=[0])
    return features

df_user = user_input_features()

if st.sidebar.checkbox("Choose your own recency bias"):
    def user_input_biased():
        thisyear = st.sidebar.slider('2021 weighting', 0, 100, 100, 5)
        lastyear = st.sidebar.slider('2020 weighting', 0, 100, 100, 5)
        biased_data = {'this year': thisyear/100,
                       'last year': lastyear/100}
        biased = pd.DataFrame(biased_data, index=[0])
        return biased


    df_user_biased = user_input_biased()

else:
    def user_input_biased():
        thisyear = 100
        lastyear = 100
        biased_data = {'this year': thisyear / 100,
                       'last year': lastyear / 100}
        biased = pd.DataFrame(biased_data, index=[0])
        return biased
    df_user_biased = user_input_biased()


#Display the user's chosen weightings
st.write(
    """
    ## your chosen weighting %  :
    """
)
df_user

#Output rankings based on users selections
st.write(
    """
    ## YOUR PREDICTION
    """
)

#image
image = Image.open('/Users/andrewuttley/Desktop/PGAapp/Tiger.jpg')
st.image(image)


def results_output():
    sg_ott = (data['SG_OTT_2020']*df_user_biased['last year'][0] + data['SG_OTT_2021']*df_user_biased['this year'][0]) * df_user['SG OTT'][0]/100
    sg_a2g = (data['SG_A2G_2020']*df_user_biased['last year'][0]  + data['SG_A2G_2021']*df_user_biased['this year'][0]) * df_user['SG A2G'][0] / 100
    sg_atg = (data['SG_ATG_2020']*df_user_biased['last year'][0]  + data['SG_ATG_2021']*df_user_biased['this year'][0]) * df_user['SG ATG'][0] / 100
    sg_putt = (data['SG_Putting2020']*df_user_biased['last year'][0]  + data['SG_Putting2021']*df_user_biased['this year'][0]) * df_user['SG Putt'][0]/100
    results = {'Name': data['PLAYER NAME']
               , 'Total SG per round': sg_ott + sg_a2g + sg_atg + sg_putt
               , 'SG OTT Weighted': sg_ott
               , 'SG A2G Weighted': sg_a2g
               , 'SG ATG Weighted': sg_atg
               , 'SG Putt Weighted': sg_putt
               }
    resultpd = pd.DataFrame(results)
    resultpd.sort_values(by=['Total SG per round'], ascending=False, inplace=True)
    return resultpd

df_results  = results_output()


# use softmax to create the % probability
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return (e_x / e_x.sum(axis=0))*100

df_results['Win prediction %'] = softmax(df_results['Total SG per round'])
df_results2 = df_results[['Name', 'Win prediction %', 'Total SG per round']]
df_results2

