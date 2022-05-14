import os
import os.path
import io
import subprocess
import time
import re
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import altair as alt
from streamlit.scriptrunner.script_run_context import get_script_run_ctx
from streamlit.server.server import Server



API_URL = "https://api-inference.huggingface.co/models/Nakul24/RoBERTa-Goemotions-6"
headers = {"Authorization": "Bearer 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"}

ak_url = "https://7888th4wcl.execute-api.us-east-1.amazonaws.com/v1/predict"


def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def fetch(session, url):
        try:
            result = session.get(url)
            return result.json()
        except Exception:
            return {}

def main():  
    st.set_page_config(layout="wide",page_title="Mental Health")

    # Get headers
    session_id = get_script_run_ctx().session_id
    server = Server.get_current()
    session_info = server._get_session_info(session_id)
    if session_info.ws is None:
        # At first page load, this is None (at least until #4099 is fixed)
        st.markdown("Unable to get session websocket. Please refresh the page.")
        st.stop()
    headers = session_info.ws.request
    st.write(headers)

    
    st.title("Mental Health")
    st.text("AI to Predict mental status of a person")
    st.markdown(
        """[more info here](https://github.com/annasajkh/PianoGPT)"""
    )
    components.html("""
    <script src="https://apps.elfsight.com/p/platform.js" defer></script>
    <div class="elfsight-app-4c045bce-f323-4061-899e-f47ed67adf87"></div>
    """,height=650)

    
    
    session = requests.Session()
    with st.form("my_form"):
        st.header("Questions")
        st.subheader("Q1) How have you been feeling lately?")
        input_q1 = st.text_area("Type out all your feelings here")
        st.markdown("***")
        st.subheader("Q2) Why do you think you feel like this?")
        input_q2 = st.text_area("Please describe what caused your feelings")
        st.markdown("***")
        st.subheader("Q3) Since when are you feeling like this?")
        input_q3 = st.text_area("Please inform us about the timeframe of your current feeling")
        submitted = st.form_submit_button("Submit")
        
        #input_text = re.sub("\s+", " ", st.text_input("Enter text"))
        #index = st.number_input("ID", min_value=0, max_value=100, key="index")

    if submitted:
        st.write("Result")
        answers = input_q1 + " " + input_q2 + " " + input_q3
        out = query({"inputs": answers,})
        
        #st.text(pd.DataFrame.from_records(out[0]))

        #st.bar_chart(pd.DataFrame.from_records(out[0]))
        url = 'https://7fhrcwqoqh.execute-api.us-east-1.amazonaws.com/FirstStage/panacea'
        
        myobj = {
"messages": answers
}

        json_object = json.dumps(myobj, indent = 4)
        st.text(out)
        #x = requests.post(url, data = json_object)
        #out = x.text
        #st.text(x.text)
        #st.text(x.status_code)
        c = alt.Chart(pd.DataFrame.from_records(out[0])).mark_bar().encode(
            y='label',
            x='score').properties(width=200,height=350)
        
        st.altair_chart(c,use_container_width=True)
        
        # ADD Video in columns , add suggestions/resources based on current mood
        col1, col2 = st.columns(2)

        with col1:
            st.header("Your Current mood is")
            max_key = maxPricedItem = max(out[0], key=lambda x:x['score'])
            st.subheader(max_key['label'])
            #if max_key['label'] == 'anxiety':
                
            #st.image("https://static.streamlit.io/examples/cat.jpg")

        with col2:
            st.header("A dog")
            st.image("https://static.streamlit.io/examples/dog.jpg")
        
        
        
        
        #data = fetch(session, f"https://7fhrcwqoqh.execute-api.us-east-1.amazonaws.com/FirstStage/panacea")
        #if data:
        #    st.text(data)
        #else:
        #    st.error("Error")

        History = st.form_submit_button("View History") # Chart code in comment below
        

        '''
            alt.Chart(source).mark_bar().encode(
            x=alt.X('sum(yield)', stack="normalize"),
            y='variety',
            color='label'
            )


        '''

    '''
    picture = st.camera_input("Take a picture")
    if picture:
     st.image(picture)'''
    components.html("""
    <script src="https://apps.elfsight.com/p/platform.js" defer></script>
    <div class="elfsight-app-b996a8bc-edc2-4dc8-9b70-e462d9601b13"></div>
    """)
if __name__ == '__main__':
    main()

    #form = st.form(key="submit-form")

    #temperature = form.number_input("Temperature (the higher the value the less repetitive it will be)", min_value=0.3, max_value=1.0, value=1.0, step=0.01)
    #top_k = form.number_input("Top k (the number of highest probability to be consider)", min_value=3, max_value=50257, value=40, step=1)
    #generate = form.form_submit_button("Generate")






