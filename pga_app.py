import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from PIL import Image


linkedinlink = '[Andy Uttley - LinkedIn](https://www.linkedin.com/in/andrewuttley/)'
mediumlink = '[Andy Uttley - Medium Blog](https://andy-uttley.medium.com/)'

#Create header
st.write("""# PGA Data Modeller""")
st.write("""## How it works""")
st.write("Model your predicted winner by using the left side of the screen to apply  weightings to the different metrics. This will give you a ranked 'predicted outcome' based on your selections. "
         "The current selections are those deemed most appropriate to the Masters based on recent outcomes.")
st.write("## For more information visit:")
st.write(mediumlink, " | ", linkedinlink)


#image
image = Image.open('Tiger.jpg')
st.image(image)

#Bring in the data
data = pd.read_excel('PGA_Database.xlsx')
st.write("## THE DATA BEING USED")
data

#Create and name sidebar
st.sidebar.header('Choose your weightings')

st.sidebar.write("""#### Choose your SG bias""")
def user_input_features():
    sgott = st.sidebar.slider('SG Off the Tee', 0, 100, 70, 5)
    sga2g = st.sidebar.slider('SG Approach to Green', 0, 100, 90, 5)
    sgatg = st.sidebar.slider('SG Around the Green', 0, 100, 50, 5)
    sgputt = st.sidebar.slider('SG Putting', 0, 100, 25, 5)
    sgmasters = st.sidebar.slider('SG Masters History', 0, 100, 80, 5)
    sgtotal = st.sidebar.slider('SG Total', 0, 100, 25, 5)
    sgpar5 = st.sidebar.slider('SG Par 5s', 0, 100, 75, 5)
    sgpar4 = st.sidebar.slider('SG Par 4s', 0, 100, 25, 5)
    sgpar3 = st.sidebar.slider('SG Par 3s', 0, 100, 20, 5)



    user_data = {'SG OTT': sgott,
                 'SG A2G': sga2g,
                 'SG ATG': sgatg,
                 'SG Putt': sgputt,
                 'SG Total': sgtotal,
                 'SG Par 5': sgpar5,
                 'SG Par 4': sgpar4,
                 'SG Par 3': sgpar3,
                 'SG Masters': sgmasters}
    features = pd.DataFrame(user_data, index=[0])
    return features

df_user = user_input_features()

if st.sidebar.checkbox("Choose a recency bias"):
    def user_input_biased():
        thisyear = st.sidebar.slider('2021 weighting', 0, 100, 100, 5)
        lastyear = st.sidebar.slider('2020 weighting', 0, 100, 80, 5)
        biased_data = {'this year': thisyear/100,
                       'last year': lastyear/100}
        biased = pd.DataFrame(biased_data, index=[0])
        return biased


    df_user_biased = user_input_biased()

else:
    def user_input_biased():
        thisyear = 100
        lastyear = 60
        biased_data = {'this year': thisyear / 100,
                       'last year': lastyear / 100}
        biased = pd.DataFrame(biased_data, index=[0])
        return biased
    df_user_biased = user_input_biased()


st.write("## YOUR CHOSEN WEIGHTINGS: ")
df_user



#Output rankings based on users selections
st.write(
    """
    ## YOUR PREDICTION OUTPUT
    """
)

def results_output():
    sg_ott = (data['SG_OTT_2020']*df_user_biased['last year'][0] + data['SG_OTT_2021']*df_user_biased['this year'][0]) * df_user['SG OTT'][0] / 100
    sg_a2g = (data['SG_A2G_2020']*df_user_biased['last year'][0]  + data['SG_A2G_2021']*df_user_biased['this year'][0]) * df_user['SG A2G'][0] / 100
    sg_atg = (data['SG_ATG_2020']*df_user_biased['last year'][0]  + data['SG_ATG_2021']*df_user_biased['this year'][0]) * df_user['SG ATG'][0] / 100
    sg_total = (data['SG_Total_2020']*df_user_biased['last year'][0]  + data['SG_Total_2021']*df_user_biased['this year'][0]) * df_user['SG Total'][0]/100
    sg_putt = (data['SG_Putting2020']*df_user_biased['last year'][0]  + data['SG_Putting2021']*df_user_biased['this year'][0]) * df_user['SG Putt'][0]/100
    #SG Par requires additional logic
    sgpar5 = (5 - data['Par5ScoringAvg_2020'] * df_user_biased['last year'][0] + 5 - data['Par5ScoringAvg_2021'] * df_user_biased['this year'][0]) * df_user['SG Par 5'][0] / 100
    sgpar4 = (4 - data['Par4ScoringAvg_2020'] * df_user_biased['last year'][0] + 4 - data['Par4ScoringAvg_2021'] * df_user_biased['this year'][0]) * df_user['SG Par 4'][0] / 100
    sgpar3 = (3 - data['Par3ScoringAvg_2020'] * df_user_biased['last year'][0] + 3 - data['Par3ScoringAvg_2021'] * df_user_biased['this year'][0]) * df_user['SG Par 3'][0] / 100
    #SG Masters diff calc
    sgmasters = (data['MastersSG']*((df_user_biased['last year'][0] + df_user_biased['this year'][0])/2) * df_user['SG Masters'][0]/100)

    results = {'Name': data['PLAYER NAME']
               , 'Total SG per round': (sg_ott + sg_a2g + sg_atg + sg_putt + sgpar5 + sgpar4 + sgpar3 + sgmasters + sg_total)
               , 'SG OTT Weighted': sg_ott
               , 'SG A2G Weighted': sg_a2g
               , 'SG ATG Weighted': sg_atg
               , 'SG Putt Weighted': sg_putt
               , 'SG Par 5 Weighted': sgpar5
                , 'SG Par 4 Weighted': sgpar4
                , 'SG Par 3 Weighted': sgpar3
                , 'SG Masters': sgmasters
                 , 'SG Total': sg_total
               }
    resultpd = pd.DataFrame(results)
    resultpd.sort_values(by=['Total SG per round'], ascending=False, inplace=True)
    return resultpd


df_results  = results_output()


# use softmax to create the % probability
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return (e_x / e_x.sum(axis=0))*100

df_results['prediction'] = softmax(df_results['Total SG per round'])
df_results2 = df_results[['Name', 'prediction', 'Total SG per round']]
df_results2.reset_index(inplace=True)

winner = df_results2['Name'][0]
predperc = df_results2['prediction'][0]
st.markdown(f"Your predicted winner is **{winner:}** who has a **{predperc:.2f}**% chance of winning")

#image of winner
try:
    winnerimage = Image.open(winner+'.jpg')
    st.image(winnerimage)
except:
    pass

# create bar chart
st.write("## RANKED RESULTS OF TOP 20")


chart = alt.Chart(df_results2[:20]).mark_bar().encode(
    x=alt.X("prediction"),
    y=alt.Y('Name', sort='-x'),
    opacity=alt.value(1),
color=alt.condition(
    alt.datum.Name == df_results2['Name'][0],  # If it's the top ranked prediction
        alt.value('#f63366'),     #  sets the bar to the streamlit pink.
        alt.value('grey')  ) # else this colour
).properties(
    width=380
)


text = chart.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text=alt.Text('prediction', format=',.2r')
)

st.altair_chart(chart+text)

st.write("## Full table of results")
df_results2