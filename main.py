import streamlit as st
st.title("Welcome to my app")
st.header("I am a header")
st.subheader("I am a subheader")
st.write("I am a paragraph")
st.markdown("<h1>This is a markdown", unsafe_allow_html=True);
st.markdown("<marquee>This :orange[is marquee] it will be :green[be going] :blue[again and again]", unsafe_allow_html=True);

st.image("https://img10.hotstar.com/image/upload/f_auto/sources/r1/cms/prod/6981/1715848956981-h", caption="Mera nam bhi shinchan hai, main shararat se bhara")


gender = st.radio("Gender", options=['Male', 'Female', 'Loser'])
st.error(gender)

name = st.text_input("Enter your name")
st.success(name)
st.text_input("Enter your password", type='password')
st.button("Signin")

