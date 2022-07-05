import pickle
import pandas as pd
import streamlit as st
from babel.numbers import format_currency
from PIL import Image
data=pd.read_csv("final_data_guvi_app")
model = pickle.load(open('xg_model_pkl','rb'))
def main():
    # Create a page dropdown
    image = Image.open('house app.jpg')
    st.sidebar.image(image,width=100)
    st.sidebar.title("Guvi_Homes")
    col1, col2 = st.columns( [0.5, 0.5])
    with col1:
        st.title("Guvi_Homes")   
    with col2:
        st.image(image,  width=150)
    page = st.sidebar.selectbox("Select One", ['ABOUT',"PRICE PREDICTION"])
    if page == "ABOUT":
        st.title('Welcome to Guvi_Homes')
        st.subheader('Guvi Homes is a website where you can look at sales data for Chennai and project the price range of your dream house.')
        st.write('Creator Profile:')
        st.write('**Creator:** Kaviarasan K G')
        st.write('**Mail Id:** kaviarasangk5@gmail.com')
        st.write("**Linked In:** https://www.linkedin.com/in/kaviarasan-gunalan-53733b235")

    if page == "PRICE PREDICTION":
        st.title('PRICE PREDICTION')
        AREA = st.selectbox("Select an Area ",data.AREA.unique())
        if AREA == 'Chrompet':
            grouped=data[data['AREA']=='Chrompet']
            AREA = 2
        elif AREA == 'Karapakkam':
            grouped=data[data['AREA']=='Karapakkam']
            AREA  = 4
        elif AREA == 'KK Nagar':
            grouped=data[data['AREA']=='KK Nagar']
            AREA = 3
        elif AREA == 'Anna Nagar':
            grouped=data[data['AREA']=='Anna Nagar']
            AREA = 1
        elif AREA == 'Adyar':
            grouped=data[data['AREA']=='Adyar']
            AREA = 0
        elif AREA == 'T Nagar':
            grouped=data[data['AREA']=='T Nagar']
            AREA = 5
        elif AREA == 'Velachery':
            grouped=data[data['AREA']=='Velachery']
            AREA = 6

        INT_SQFT = st.slider("SQFT Required",int(data.INT_SQFT.min()),int(data.INT_SQFT.max()))

        DIST_MAINROAD = st.slider("DIST_MAINROAD",int(data.DIST_MAINROAD.min()),int(data.DIST_MAINROAD.max()))
        
        N_BEDROOM = st.slider("No of Bedrooms",int(data.N_BEDROOM.min()),int(data.N_BEDROOM.max()))

        N_BATHROOM = st.slider("No of Bathrooms",int(data.N_BATHROOM.min()),int(data.N_BATHROOM.max()))

        N_ROOM = st.slider("Total no of rooms",int(data.N_ROOM.min()),int(data.N_ROOM.max()))

        #Coverting SALE_COND categorical to numerical
        SALE_COND = st.selectbox("SALE_COND Preference",grouped.SALE_COND.unique())
        if SALE_COND == 'Partial':
            SALE_COND = 0
        elif SALE_COND == 'Family':
            SALE_COND = 1
        elif SALE_COND == 'AbNormal':
            SALE_COND = 2
        elif SALE_COND == 'Normal Sale':
            SALE_COND = 3
        else:
            SALE_COND = 4

        PARK_FACIL = st.radio("Parking Area",data.PARK_FACIL.unique())
        if PARK_FACIL == 'Yes':
            PARK_FACIL = 1
        else:
            PARK_FACIL = 0
        
        #Coverting UTILITY_AVAIL categorical to numerical
        UTILITY_AVAIL = st.selectbox("UTILITY_AVAILBLITY Preference",grouped.UTILITY_AVAIL.unique())
        if UTILITY_AVAIL == 'ELO':
            UTILITY_AVAIL = 0
        elif UTILITY_AVAIL == 'NoSeWa':
            UTILITY_AVAIL = 1
        elif UTILITY_AVAIL == 'NoSewr':
            UTILITY_AVAIL = 2
        else:
            UTILITY_AVAIL = 3

        STREET = st.selectbox("Access TO THE Building",data.STREET.unique())

        if STREET == 'Gravel':
            STREET = 0
        elif STREET == 'Paved':
            STREET = 2
        else:
            STREET = 1

        #Coverting MZZONe categorical to numerical
        MZZONE = st.selectbox("Chennai Zone Preference",grouped.MZZONE.unique())
        if MZZONE == 'A':
            MZZONE = 0
        elif MZZONE == 'RH':
            MZZONE = 3
        elif MZZONE == 'RL':
            MZZONE = 4
        elif MZZONE == 'I':
            MZZONE = 2
        elif MZZONE == 'C':
            MZZONE = 1
        else:
            MZZONE = 5
        

        AGE_OF_BUILDING = st.slider("AGE_OF_BUILDING",int(data.AGE_OF_BUILDING.min()),int(data.AGE_OF_BUILDING.max()))


        BUILDTYPE_Commercial = st.radio("BUILDTYPE_Commercial",data.BUILDTYPE_Commercial.unique())
        if BUILDTYPE_Commercial == 'Yes':
            BUILDTYPE_Commercial = 1
        else:
            BUILDTYPE_Commercial = 0
        
        BUILDTYPE_House = st.radio("BUILDTYPE_House",data.BUILDTYPE_House.unique())
        if BUILDTYPE_House == 'Yes':
            BUILDTYPE_House = 1
        else:
            BUILDTYPE_House = 0
        
        BUILDTYPE_Others = st.radio("BUILDTYPE_Others",data.BUILDTYPE_Others.unique())
        if BUILDTYPE_Others == 'Yes':
            BUILDTYPE_Others = 1
        else:
            BUILDTYPE_Others = 0

        input = pd.DataFrame([[AREA,INT_SQFT,DIST_MAINROAD,N_BEDROOM,N_BATHROOM,N_ROOM,SALE_COND,PARK_FACIL,UTILITY_AVAIL,STREET,MZZONE,AGE_OF_BUILDING,BUILDTYPE_Commercial,BUILDTYPE_House,BUILDTYPE_Others]],columns=['AREA','INT_SQFT','DIST_MAINROAD','N_BEDROOM','N_BATHROOM','N_ROOM','SALE_COND','PARK_FACIL','UTILITY_AVAIL','STREET','MZZONE','AGE_OF_BUILDING','BUILDTYPE_Commercial','BUILDTYPE_House','BUILDTYPE_Others'],index=['index'])
                            
                            
        #st.dataframe(input)

        valu = model.predict(input)
        low=int(valu-(valu*0.02))
        low = format_currency(low, 'INR', locale='en_IN')


        high=int(valu+(valu*0.02))
        high = format_currency(high, 'INR', locale='en_IN')

        #print('Estimated value is:',low , 'to', high)


        if st.button(" Get Price",help="Click to predict the price"):
            st.markdown("<h1 style='text-align: center; color: Green;'>Predicted House Price Range</h1>", unsafe_allow_html=True)
            st.write(" ",  low , 'to', high   ," ")
            st.snow()

if __name__=='__main__':
    main()