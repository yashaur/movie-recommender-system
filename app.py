import streamlit as st
from random import sample
import pickle
import json

with open('keywords.pkl', 'rb') as f:
    keywords = json.loads(pickle.load(f))

top_keywords = [kw for kw in keywords if keywords[kw] > 100]

def generate_keywords():
    st.session_state['random_keywords'] = sample(top_keywords, 18)

st.title('MOVIE KEYWORD RECOMMENDER')

st.write('Pick a few keywords:')

st.space('medium')

if 'random_keywords' not in st.session_state:
    st.session_state['random_keywords'] = generate_keywords()
random_keywords = st.session_state['random_keywords']

st.button('generate again', on_click=generate_keywords)

kw1, kw2, kw3, kw4, kw5, kw6 = st.columns(6)

kw1.button(label = random_keywords[0])
kw2.button(label = random_keywords[1])
kw3.button(label = random_keywords[2])
kw4.button(label = random_keywords[3])
kw5.button(label = random_keywords[4])
kw6.button(label = random_keywords[5])

kw7, kw8, kw9, kw10, kw11, kw12 = st.columns(6)

kw7.button(label = random_keywords[6])
kw8.button(label = random_keywords[7])
kw9.button(label = random_keywords[8])
kw10.button(label = random_keywords[9])
kw11.button(label = random_keywords[10])
kw12.button(label = random_keywords[11])

kw13, kw14, kw15, kw16, kw17, kw18 = st.columns(6)

kw13.button(label = random_keywords[12])
kw14.button(label = random_keywords[13])
kw15.button(label = random_keywords[14])
kw16.button(label = random_keywords[15])
kw17.button(label = random_keywords[16])
kw18.button(label = random_keywords[17])

st.button('Recommend me some movies')