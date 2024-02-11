from openai import OpenAI
import decoder_output
import hotel_chatbot
import traversaal
import streamlit as st
from qdrant_client import QdrantClient
from neural_searcher import NeuralSearcher


def home_page():
    # st.title("TraverGo")

    st.markdown("<h1 style='text-align: center; color: white;'>TraverGo</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>Find any type of Hotel you want !</h2>", unsafe_allow_html=True)
    st.session_state["value"] = None

    def search_hotels():
        query = st.text_input("Enter your hotel preferences:", placeholder ="clean and cheap hotel with good food and gym")

        if "load_state" not in st.session_state:
            st.session_state.load_state = False;

        # Perform semantic search when user submits query
        if query or st.session_state.load_state:
            st.session_state.load_state=True;
            neural_searcher = NeuralSearcher(collection_name="hotel_descriptions")
            results = sorted(neural_searcher.search(query), key=lambda d: d['sentiment_rate_average'])
            st.subheader("Hotels")
            for hotel in results:
                explore_hotel(hotel, query)  # Call a separate function for each hotel

    def explore_hotel(hotel, query):
        if "decoder" not in st.session_state:
            st.session_state['decoder'] = [0];

        button = st.checkbox(hotel['hotel_name'])


        if not button:
            if st.session_state.decoder == [0]:
                x = (decoder_output.decode(hotel['hotel_description'][:1000], query))
                st.session_state['value_1'] = x
                st.session_state.decoder = [st.session_state.decoder[0] + 1]
                st.write(x)

            elif (st.session_state.decoder == [1]):
                x = (decoder_output.decode(hotel['hotel_description'][:1000], query))
                st.session_state['value_2'] = x

                st.session_state.decoder = [st.session_state.decoder[0] + 1];
                st.write(x);

            elif st.session_state.decoder == [2]:
                x = (decoder_output.decode(hotel['hotel_description'][:1000], query))
                st.session_state['value_3'] = x;
                st.session_state.decoder = [st.session_state.decoder[0] + 1];
                st.write(x);


            if (st.session_state.decoder[0] >= 3):
                i = st.session_state.decoder[0] % 3
                l = ['value_1', 'value_2', 'value_3']
                st.session_state[l[i - 1]];
                st.session_state.decoder = [st.session_state.decoder[0] + 1];

        if button:
            st.session_state["value"] = hotel


        # if (st.session_state.decoder[0] < 3):
        #     st.write(decoder_output.decode(hotel['hotel_description'][:1000], query))
        #     st.session_state.decoder = [st.session_state[0] + 1];
        #

        question = st.text_input(f"Enter a question about {hotel['hotel_name']}:");
            
        if question:
            st.write(ares_api(question + "for" + hotel['hotel_name'] + "located in" + hotel['country']))
        # if "load_state" not in st.session_state:
            # st.session_state.load_state = False;
        # Perform semantic search when user submits query
        # if question:






    search_hotels()
    chat_page()


def ares_api(query):
    response_json = traversaal.getResponse(query);
    # if response_json is not json:
    #     return "Could not find information"
    return (response_json['data']['response_text'])
def chat_page():
    hotel = st.session_state["value"]
    st.session_state.value = None
    if (hotel == None):
        return;

    st.write(hotel['hotel_name']);
    st.title("Conversation")

    # Set OpenAI API key from Streamlit secrets
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # st.session_state.pop("messages")
    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    prompt = f"{hotel['hotel_description'][:2000]}\n\n you are a hotel advisor now, you should give the best response based on the above text. i will now ask you some questions get ready"
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
        x = ares_api(prompt)
        # Add user message to chat history
        st.session_state.messages[0]['content'] += "\n" + x;
        st.session_state.messages.append({"role": "assistant", "content": prompt})
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


    # hotel_chatbot.start_page();

home_page()
#
#
# page = st.sidebar.selectbox("Select a page", ["Home", "Chatbot"])
#
#
# if page == "Home":
#     home_page()
# elif page == "Chatbot":
#     chat_page(None)
#
