import streamlit as st
from openai import OpenAI


def start_page():
    hotel = st.session_state["value"]
    print(hotel['hotel_name']);
    return ;
    # if received_data:
    #     st.write(f"Data received from page 1: {received_data}")

    if (hotel == None) :
        st.write("Please select a hotel");
        return ;

        st.title("ChatGPT-like clone")

    # Set OpenAI API key from Streamlit secrets
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # st.session_state.pop("messages")
    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    prompt = f"Hotel Description - {hotel['hotel_description']}\n\n You are a hotel advisor, now I will ask you some questoins based on the above descriptoin. Give me objective answers to these questions. Now introduce yourself by naming the hotel and giving a 1 sentence hotel introduction"
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "user", "content": prompt}]

    # Display chat messages from history on app rerun
    # keys_subset = list(st.session_state.messages.keys())[1:]
    # subset_dict = {key: original_dict[key] for key in keys_subset}



    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)



    #Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})



    #
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []
    # # Display chat messages from history on app rerun
    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])
    # if prompt := st.chat_input("What is up?"):
    # # Display user message in chat message container
    #     with st.chat_message("user"):
    #         st.markdown(prompt)
    #     # Add user message to chat history
    #     st.session_state.messages.append({"role": "user", "content": prompt})
    #
    #
    #
    #
    #
