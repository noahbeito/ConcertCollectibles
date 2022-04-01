#Streamlit file

import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

@st.cache(allow_output_mutation=True)
def load_contract():
    with open(Path('./collectible_abi.json')) as f:
        collectible_abi = json.load(f)
    
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address = contract_address,
        abi = collectible_abi
    )

    return contract

contract = load_contract()

st.title("Register New Concert Collectible")
accounts = w3.eth.accounts
address = st.selectbox("Select Collectible Owner", options=accounts)
collectible_uri = st.text_input("The URI to the collectible")

if st.button("Register Collectible"):
    tx_hash = contract.functions.registerCollectible(address, collectible_uri).transact({
        "from": address,
        #arbitrary gas estimate for test network. Oracle needed
        "gas": 1000000
    })
    receipt = w3.eth.waitForTransactionReciept(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

