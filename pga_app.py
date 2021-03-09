import streamlit as st
import pandas as pd
import altair as alt

#Create header
st.write(
    """
    # V1.2 of PGA App
    ## Andy Uttley 
    ### The following stats were scraped from the PGA website:
    """
)


#Bring in the data
data = pd.read_excel('/Users/andrewuttley/Desktop/PGAapp/PGA_Database.xlsx')
data

#Create and name sidebar
st.sidebar.header('Choose your weightings')

thisyear = st.sidebar.slider('2021 weighting', 0.0, 1.0, 1.0, 0.2)
lastyear = st.sidebar.slider('2020 weighting', 0.0, 1.0, 0.8, 0.2)
st.sidebar.write("""Now choose your metric weightings:""")

def user_input_features():
    sgott = st.sidebar.slider('SG Off the Tee', 0.0, 2.0, 1.0, 0.5)
    sgputt = st.sidebar.slider('SG Putting', 0.0, 2.0, 1.0, 0.5)
    sgt2g = st.sidebar.slider('SG Tee to Green', 0.0, 2.0, 1.0, 0.5)

    user_data = {'SG OTT': sgott,
                 'SG T2G': sgt2g,
                 'SG Putt': sgputt}
    features = pd.DataFrame(user_data, index=[0])
    return features

df_user = user_input_features()

#Display the user's chosen weightings
st.write(
    """
    ## your chosen weightings:
    """
)
df_user

#Output rankings based on users selections
st.write(
    """
    ## testing creating results dataframe
    """
)


def results_output():
    sg_ott = (data['SG_OTT_2020']*lastyear + data['SG_OTT_2021']*thisyear)/2 * df_user['SG OTT'][0]
    sg_t2g = (data['SG_TeeToGreen_2020'] + data['SG_TeeToGreen_2021']) * df_user['SG T2G'][0]
    sg_putt = (data['SG_Putting2020'] + data['SG_Putting2021']) * df_user['SG Putt'][0]
    results = {'Name': data['PLAYER NAME']
               , 'Total': sg_ott + sg_t2g + sg_putt
               , 'SG OTT Weighted': sg_ott
               ,'SG T2G Weighted': sg_t2g
               , 'SG Putt Weighted': sg_putt
               }
    resultpd = pd.DataFrame(results)
    resultpd.sort_values(by=['Total'], ascending=False, inplace=True)
    return resultpd

df_results  = results_output()
df_results

#try making a graph
chart = alt.Chart(df_results).mark_bar().encode(
    alt.X("Total", bin=False),
    y='Name',
)
st.altair_chart(chart)
alt.Chart()

