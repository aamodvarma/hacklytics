import requests
import streamlit as st
import json
import os

def getResponse(query):

    url = "https://api-ares.traversaal.ai/live/predict"


    payload = { "query": [query] }
    headers = {
      "x-api-key": st.secrets["TRAVERSAAL"],
      "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        # Get the JSON content from the response
        json_content = response.json()

        # Specify the file path where you want to save the JSON content
        return json_content
    else:
        print(response.status_code)
        return response

