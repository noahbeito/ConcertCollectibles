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
    with open(Path('./contracts/compiled/ticket_abi.json')) as f:
        ticket_abi = json.load(f)
    
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address = contract_address,
        abi = ticket_abi
    )

    return contract

contract = load_contract()
#####################################################################
# Register new collectible
#####################################################################
st.title("Register New Ticket")
accounts = w3.eth.accounts
address = st.selectbox("Select Ticket Owner", options=accounts)
ticket_uri = st.text_input("The URI to the ticket")

if st.button("Register Ticket"):
    tx_hash = contract.functions.registerTicket(address, ticket_uri).transact({
        "from": address,
        #arbitrary gas estimate for test network. Oracle needed
        "gas": 1000000
    })
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))


#####################################################################
# Display a collectible token
#####################################################################
st.markdown("## Display a Concert Ticket")

selected_address = st.selectbox("Select Account", options=accounts)

tokens = contract.functions.balanceOf(selected_address).call()

st.write(f"This address owns {tokens} tickets")

token_id = st.selectbox("Tickets", list(range(tokens)))

if st.button("Display"):

    #Use contract's ownerOf function to get token owner
    owner = contract.functions.ownerOf(token_id).call()

    st.write(f"The token is registered to {owner}")

    # Use contract's tokenURI funtion to get token URI
    token_uri = contract.functions.tokenURI(token_id).call()

    st.write(f"The tokenURI is {token_uri}")
    st.image(token_uri)
