import torch
import os
# Load the Falcon 7B model
from openai import OpenAI
import streamlit as st

def decode(hotel_description, query):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    prompt = f"""
    this is the hotel descriptoin:

    \"{hotel_description}\"

     and these are my requirements

    \"{query}\"

    now tell me why the hotel might be a good fit for me given the requirements, make it consise.
    """

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    str = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            str += (chunk.choices[0].delta.content)
    return str
    



