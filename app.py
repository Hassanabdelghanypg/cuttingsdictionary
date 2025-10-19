import pandas as pd
import streamlit as st
import re


# Streamlit app configuration

st.set_page_config(page_title="Cuttings Description Dictionary", page_icon="🪨", layout="centered")
a,b,c = st.columns([1,3,1])

with b:
    st.markdown("### Cuttings Description Dictionary")
    st.markdown("Convert your cutting description from the short form to the normal form, or vice versa.")



# Building the logic def

@st.cache_data

def load_dictionary():

    df = pd.read_csv("cutting_description.csv")

    # Sort by word length (longest first)
    df = df.sort_values(by="word", key=lambda x: x.str.len(), ascending=False)

    # Two dictionaries
    fullToShort = dict(zip(df["word"].str.lower().str.strip(), df["short"].str.lower().str.strip()))
    shortToFull = dict(zip(df["short"].str.lower().str.strip(), df["word"].str.lower().str.strip()))

    return fullToShort, shortToFull


fullToShort, shorToFull = load_dictionary()


# Mode Toggle

st.markdown("---")

col1, col2, col3 = st.columns([1,2,1])

with col2:

    mode =st.toggle("Swap Mode (Short ↔ Full)", value= False)

st.write("")

# User Input

with st.form("cuttings_form"):

    user_input = st.text_area(
        "**Enter description here :**",  
        placeholder="e.g. sandstone: colorless, fine to very fine, rounded to subrounded...").lower().strip(
        )
    submitted = st.form_submit_button("Convert")

# Conversion Function

def  convert_text(text, dictionary):

    words = text.lower()
    result = words

    for key in sorted(dictionary.keys(), key=len, reverse=True):

        escapedKey = re.escape(key)

        if re.fullmatch(r"[a-z0-9\s]+", key):

            pattern = r"\b" + escapedKey + r"\b"
        
        else:

            pattern = escapedKey
        
        result = re.sub(pattern, dictionary[key], result)

    return result


# Convert based on mode chosed

if user_input:

    if mode:

        result = convert_text(user_input, shorToFull).capitalize()
    
    else:

        result = convert_text(user_input, fullToShort).capitalize()
    
    st.markdown("#### Converted Output")
    st.markdown(f"**{result}**")


st.markdown("---")
st.caption("Created by Hassan Abdelghany · All Rights Reserved to Rootex.digital")