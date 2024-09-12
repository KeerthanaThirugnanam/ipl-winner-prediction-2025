import streamlit as st
import pickle
import pandas as pd

teams = ['Royal Challengers Bangalore', 'Kolkata Knight Riders',
       'Delhi Capitals', 'Sunrisers Hyderabad', 'Mumbai Indians',
       'Kings XI Punjab', 'Gujarat Titans', 'Rajasthan Royals',
       'Chennai Super Kings', 'Lucknow Supergiants']

cities = ['Hyderabad', 'Rajkot', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata',
       'Delhi', 'Chandigarh', 'Kanpur', 'Jaipur', 'Chennai', 'Cape Town',
       'Port Elizabeth', 'Durban', 'Centurion', 'East London',
       'Johannesburg', 'Kimberley', 'Bloemfontein', 'Ahmedabad',
       'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Pune',
       'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah', 'Mohali',
       'Bengaluru']

pipe = pickle.load(open('pipe.pkl','rb'))
st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team',sorted(teams))

city = st.selectbox('Select host city',sorted(cities))

Target = st.number_input('Target')

col3,col4,col5 = st.columns(3)

with col3:
    Score = st.number_input('Score')
with col4:
    balls_left = st.number_input('Ball Left')
with col5:
    wickets_down = st.number_input('Wickets Down')

if st.button('Predict Probability'):
    runs_left = Target - Score
    if(batting_team==bowling_team):
        st.header("Please select two different teams!!!")
    elif(Target==0):
        st.header("Target must be >=1")
    elif(balls_left>120):
        st.header("Balls Left must be less than or equal to 120")
    elif(balls_left==0):
        st.header("Match has finished you can't predict now!!")
    else:
        crr = Score / (balls_left/6)
        rrr = (runs_left * 6) / balls_left
        wickets_remaining = 10 - wickets_down
        input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team],
                                 'city': [city], 'runs_left': [runs_left], 'balls_left': [balls_left],
                                 'wickets_remaining': [wickets_remaining],
                                 'total_runs_x': [Target], 'crr': [crr], 'rrr': [rrr]})
        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        st.header(batting_team + "- " + str(round(win * 100)) + "%")
        st.header(bowling_team + "- " + str(round(loss * 100)) + "%")