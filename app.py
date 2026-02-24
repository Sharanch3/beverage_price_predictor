import streamlit as st

st.set_page_config(
    page_title="Beverage Price Predictor",
    page_icon= "🍷",
    layout= "centered"
)
st.title("CodeX: Beverage Price Predictor")
st.write(" ")


with st.form(key= "Beverage Price Predictor", width= "stretch"):
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.number_input(label="Age", min_value= 18, max_value= 100, step= 1)
        st.selectbox(label="Income Level (in Lakhs)", options= ['<10L', '10L - 15L', '16L - 25L', '26L - 35L', '> 35L'])
        st.selectbox(label="Awarness of other Brand", options= ['0 to 1', '2 to 4', 'above 4'])
        st.selectbox(label="Packaging Preferences", options= ['Simple', 'Premium', 'Eco-Friendly'])


    with col2:
        st.selectbox(label="Gender", options= ['M', 'F'])
        st.selectbox(label="Consume Count (weekly)", options= ['0-2 times', '3-4 times', '5-7 times'])
        st.selectbox(label="Reason for choosing brand", options= ['Price', 'Quality', 'Availability', 'Brand Reputation'])
        st.selectbox(label= "Health Concerns", options= ["Low (Not very concerned)", 
         "Medium (Moderately health-conscious)", 
         "High (Very health-conscious)"])

    
    with col3:
        st.selectbox(label="Zone", options= ['Urban', 'Metro', 'Rural', 'Semi-Urban'])
        st.selectbox(label="Current Brand", options= ['Newcomer', 'Established'])
        st.selectbox(label="Flavor Preferences", options= ['Traditional', 'Exotic'])
        st.selectbox("Typical Use", options= ['Active (eg. Sports, gym)', 'Social (eg. Parties)', 'Casual (eg. At home)'])


    with col4:
        st.selectbox(label= "Occupation", options= ['Working Professional', 'Student', 'Entrepreneur', 'Retired'])
        st.selectbox(label= "Preferable Size", options= ["Small (250 ml)", "Medium (500 ml)", "Large (1 L)"])
        st.selectbox(label="Purchase Channel", options=["Online", "Retail Store"])




    st.write(" ")
    if st.form_submit_button("Predict Price Range", type= "primary"):
        st.success(body= "Price Range: 200-300 INR", width="stretch")
        