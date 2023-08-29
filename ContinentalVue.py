import pandas as pd
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px

st.markdown("<h1 style='text-align: center; color: black;'>Explore The Continents</h1>", unsafe_allow_html=True)

photo = Image.open('map2.png')
st.image(photo.resize([700,300]))


import mysql.connector as connection  
## this imports the mysql connector to enable the data manipulation on python

mydb = connection.connect(host='relational.fit.cvut.cz', database = 'world', user = 'guest', password = 'relational', use_pure = True)
## this connects to the "world" database from my sql 

#selecting databse with specified columns to use from SQL
conti = pd.read_sql_query('SELECT Continent, Name as Country, Region, Population, GNP, SurfaceArea, IndepYear as "Year of Independence", LifeExpectancy, LocalName, GovernmentForm , HeadofState as "Head of State" FROM Country', mydb)
conti.to_csv('MainCountryData.csv', index=False)


st.sidebar.title ('Select Continent')

Continents = st.sidebar.selectbox('Choose a Continent', conti['Continent'].unique())

filtered_df = conti[(conti['Continent'] == Continents)]
st.write(filtered_df)



# main page image
from PIL import Image
fun = Image.open('funfacts.jpg')
##st.image(fun.resize([300,200]))
st.title(f'Fun Facts About - :red[_{Continents}_]')

st.divider()




#GNP
# calculating GNP for filtered continents    
GNP = filtered_df['GNP'].sum()
totalgnp = conti['GNP'].sum()
avggnp = (GNP/totalgnp) * 100
gnp = Image.open('gnp3.jpg')
st.image(gnp.resize([280,250]))

if st.button('GNP'):
        st.write (f"{Continents} has a total GNP of {GNP:,} USD")
        st.write(f"This is {round(avggnp)}% of the world's GNP")

        #pie chart to show GNP distribution by percentage
        gnpcount = pd.read_sql_query('SELECT continent, sum(GNP) as GNP FROM Country GROUP BY continent', mydb)
        y = gnpcount['GNP']
        x= gnpcount['continent']
        fig = px.pie(values = y, names =x, title = 'GNP Distribution by Continents')
        fig.update_layout(height = 600, width = 580, title = {'font':{'size':23}})
       
        st.plotly_chart(fig)
        
        

st.divider()


#Population
 ## to calculate population by continent 
pop = filtered_df['Population'].sum() 
totalpop = conti['Population'].sum()
avgpop = (pop/totalpop) * 100
popphoto = Image.open('popu.jpg') 
st.image(popphoto.resize([270,230]))

if st.button('Population'):
              
        st.write (f"The total population in {Continents} is {pop:,}")
        st.write(f"This is {round(avgpop)}% of the world's population") 
        
        #plot pie chart to show population distribution by continent
        popconti = pd.read_sql_query('SELECT continent, sum(Population) as PopSum FROM Country GROUP BY continent', mydb)

        y1 = popconti['PopSum']
        x1= popconti['continent']
        fig1 = px.pie(values= y1, names = x1, title = 'World Population Distribution by Continents')
        fig1.update_layout(height = 600, width = 580, title = {'font':{'size':23}})
        
        st.plotly_chart(fig1)


st.divider()



# Country count
##Calculating number of countries in each continent
countrycount = filtered_df.shape[0]
cont = Image.open('countries.png') 
st.image(cont.resize([270,230]))
if st.button('Number of Countries'):
        st.write(f"There are {countrycount} countries in {Continents}")
    




st.divider()
   


#Surface Area
## Calculating the percentage surface area by continents
surfarea = filtered_df['SurfaceArea'].sum()
surf = Image.open('surf2.png') 
st.image(surf.resize([320,250]))
if st.button('Surface Area'):
        st.write (f"The total Surface Area for {Continents} is {surfarea:,} Square Kilometers")

        #calulate avg surface area for filtered continent and write output
        totalsurf = conti['SurfaceArea'].sum()
        avgsurf = (surfarea/totalsurf) * 100
        st.write(f"This is {round(avgsurf)}% of the entire Earth's surface")


        #pie plot to show distribution of surface area by percentage for all the continents
        surfaceplot = pd.read_sql_query('SELECT continent, sum(SurfaceArea) as SurfaceArea from Country GROUP BY continent', mydb)
        y2= surfaceplot['SurfaceArea']
        x2= surfaceplot['continent']
        fig2 =px.pie(values = y2, names= x2, title= 'World Surface Area By Continent')   
        fig2.update_layout(height = 600, width = 570, title = {'font':{'size':23}}) 
        
        st.plotly_chart(fig2)

        

st.divider()





## Analysing languages spoken in each continent
Lang = pd.read_sql_query('SELECT Continent, Language FROM Country as co JOIN CountryLanguage as cl ON co.Code = cl.CountryCode', mydb)
merg = Lang.merge(filtered_df)
Langmerg = merg['Language'].unique()
nooflang = Langmerg.shape[0]
langphoto = Image.open('lang2.jpg') 
st.image(langphoto.resize([250,200]))

if st.button('Languages Spoken'):
        st.write(f'{nooflang} languages are spoken in {Continents}')
        st.write(f'The Languages spoken in {Continents} are {Langmerg}')  
        
   
        
     



st.divider()






avglife = filtered_df['LifeExpectancy'].mean()
lifephoto = Image.open('life.jpg') 
st.image(lifephoto.resize([250,200]))
if st.button('Average Life Expectancy'):
        
        # chart to show life expectancy in all the continents
        lifExp = pd.read_sql_query('SELECT continent, ROUND(AVG(LifeExpectancy),0) as AvgLife From Country WHERE LifeExpectancy IS NOT NULL GROUP BY continent', mydb)
        y4 = lifExp['AvgLife']
        x4 = lifExp['continent']

        fig4 = px.bar(x=x4, y=y4, 
                      labels= {'x': 'Continents', 'y': 'Average Life Expectancy(years)'}, 
                      title = 'Average Life Expectancy by Continent',
                      color_discrete_sequence=['skyblue'], text=y4)
        fig4.update_layout(title = {'font':{'size':23}})
        
        fig4.update_layout(height = 500, width = 750)
        st.plotly_chart(fig4)

        st.write  (f'The average life expectancy in {Continents} is {round(avglife)} years') 
