from qdrant_client import QdrantClient
import streamlit as st

from qdrant_client.models import Filter
from sentence_transformers import SentenceTransformer

#
class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        # Initialize encoder model
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        # initialize Qdrant client
         # self.qdrant_client = QdrantClient("http://localhost:6333")
        self.qdrant_client = QdrantClient(
            url="https://ed55d75f-bb54-4c09-8907-8d112e6278a1.us-east4-0.gcp.cloud.qdrant.io",
            api_key=st.secrets["QDRANT_API_KEY"],
        )

    def search(self, text: str):
        # Convert text query into vector
        vector = self.model.encode(text).tolist()

        #
        # city_of_interest = "Berlin"
        # # Define a filter for cities
        # city_filter = Filter(**{
        #     "must": [{
        #         "key": "country", # Store city information in a field of the same name 
        #         "match": { # This condition checks if payload field has the requested value
        #             "value": "London" 
        #         }
        #     }]
        # })
        #
        # Use `vector` for search for closest vectors in the collection
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=None,  # If you don't want any filters for now
            limit=5,  # 5 the most closest results is enough
        )
        # `search_result` contains found vector ids with similarity scores along with the stored payload
        # In this function you are interested in payload only
        payloads = [hit.payload for hit in search_result]
        return payloads


print("HELO");
neural_searcher = NeuralSearcher(collection_name="hotel_descriptions")
print(neural_searcher.search(text = "i want a cheap hotel in istanbul with free wifi and gym"))
#
