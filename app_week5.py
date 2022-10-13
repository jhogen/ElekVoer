#!/usr/bin/env python
# coding: utf-8

# In[93]:


#!pip install streamlit_folium
#!pip install requests #1x uitvoeren
#!pip install geopandas
#!pip install openpyxl
import pandas as pd
import requests
import plotly.express as px
import plotly as pl
#import geopandas as gp
import streamlit as st
from streamlit_folium import folium_static
import folium


# In[2]:


st.set_page_config(page_title="Dashboard Groep 23", page_icon="♫", layout = "wide", initial_sidebar_state="expanded")


# In[3]:


#Titel van elke pagina aanmaken.
st.title('Case 3 - Elektrische Voertuigen')


# In[4]:


#Het toevoegen van een sidebar.
st.sidebar.title('Navigatie')


# In[5]:


df = pd.read_csv('laadpaaldata.csv')
df.head()


# In[6]:


df["ChargeTime"].count()


# In[7]:


df_chargetime = df[~(df['ChargeTime'] < 0) & ~(df['ChargeTime'] > 24)]   


# In[8]:


df_chargetime["ChargeTime"].count()


# In[108]:


df_chargetime2 = df[~(df['ChargeTime'] < 0) & ~(df['ChargeTime'] > 12)]   


# In[ ]:





# In[10]:


r = requests.get('https://opendata.rdw.nl/resource/w4rt-e856.json')
x = r.json()
df1 = pd.DataFrame(x).dropna(axis='columns')
df1.head()


# In[11]:


df1.info()


# In[12]:


#Voor lijndiagram auto's per maand, voor auto's gebruik ik kenteken of anders index
df1['kenteken'].count()


# In[106]:


API_KEY = "f6e73cf6-c087-4dc2-90ed-0e5093326c04"
r = requests.get('https://api.openchargemap.io/v3/poi?key={API_KEY}')
x = r.json()
df2 = pd.DataFrame(x).dropna(axis='columns')
#df2.head()
#df2['AddressInfo'][0]['Country']['Title']


# In[14]:


df2.head()


# In[98]:


#Het inladen van de data. Deze is afkomstig van de RDW. Om de vergelijking goed uit te kunnen voeren wordt er data gebruikt van de 'R' serie kentekens.
#Vanwege de groote van het bestand (120.000+ rijen) is een excel bestand gebruikt in plaats van een csv.
#De tabel wordt omgezet in een Pandas Dataframe met de naam df3.

#df3 = pd.read_excel('Gegevens_Brandstof_R.xlsx')
#df3.head()#Histogram van de laadtijd 


# In[101]:


#De dataframe wordt hier weergeven in een boxplot. Hier is te zien wanneer, hoeveel en wat voor soort brandstoffen er worden geregisteerd voor nieuwe voertuigen.
#Dit wordt gedaan door de data aan te halen van de RDW.

#box1 = px.box(df3, y='Brandstof omschrijving', x='Datum eerste toelating', color="Brandstof omschrijving")

#box1.update_layout(
    #title_text='Registratie R serie',  
#)

#box1.update_xaxes(title_text='Datum eerste toelating')
#box1.update_yaxes(title_text='Brandstof')

#box1.show()


# In[102]:


#Deze plot geeft weer tussen welke periode voertuigen uit de R serie zijn geregistreed. Ook is de soort brandstofcategorie te zien.

#lijn1 = px.line(df3, x='Datum eerste toelating', y='Brandstof omschrijving', color="Brandstof omschrijving")

#lijn1.update_layout(
    #title_text='Registratie R serie',  
#)

#lijn1.update_xaxes(title_text='Datum eerste toelating')
#lijn1.update_yaxes(title_text='Brandstof')


#lijn1.show()


# In[96]:


fig = px.histogram(df_chargetime, x="ChargeTime")

fig.update_layout(
    title_text='Laadtijden per auto (t/m 24 uur lang)',
    xaxis_title_text='Laadtijd (in uren)',
    yaxis_title_text="Hoeveelheid auto's")
#fig.show()


# In[94]:





# In[ ]:





# In[91]:


#Histogram van de laadtijd
histogram1 = px.histogram(df_chargetime2, x="ChargeTime", color_discrete_sequence=["#293f95", "magenta"])

histogram1.update_layout(
    title_text='Laadtijden per auto (t/m 12 uur lang)',
    xaxis_title_text='Laadtijd (in uren)',
    yaxis_title_text="Hoeveelheid auto's")

histogram1.add_annotation(x=0.98, y=0.85,
            text=df_chargetime["ChargeTime"].median(),
            showarrow=False,
            yshift=10,
            xref="paper",
            yref="paper",
            bordercolor="#ffffff",
            borderwidth=0.5,
            bgcolor="#293f95",
            opacity=1,
            font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
            )

histogram1.add_annotation(x=0.98, y=0.60,
            text=df_chargetime["ChargeTime"].mean(),
            showarrow=False,
            yshift=10,
            xref="paper",
            yref="paper",
            bordercolor="#ffffff",
            borderwidth=0.5,
            bgcolor="#293f95",
            opacity=1,
            font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
            )

histogram1.add_annotation(x=0.98, y=0.92,
            text=" Mediaan = ",
            showarrow=False,
            yshift=10,
            xref="paper",
            yref="paper",
            bordercolor="#ffffff",
            borderwidth=0,
            bgcolor="#293f95",
            opacity=1,
            font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
            )

histogram1.add_annotation(x=0.98, y=0.70,
            text=" Gemiddelde = ",
            showarrow=False,
            yshift=10,
            xref="paper",
            yref="paper",
            bordercolor="#ffffff",
            borderwidth=0,
            bgcolor="#293f95",
            opacity=1,
            font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ),
            )


# In[17]:


df_chargetime["ChargeTime"].median()


# In[110]:


#  ik heb een functie gevonden op het internet voor het toevoegen van een categorische legenda:
# (bron: https://stackoverflow.com/questions/65042654/how-to-add-categorical-legend-to-python-folium-map)

def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """

    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map


# In[111]:


m = folium.Map(location=[42.416775, 5.703790], zoom_start=6).add_to(m)

for index,row in df2.iterrows():
    if row['AddressInfo']['Country']['Title'] == 'Spain':
        folium.Marker(location=[row['AddressInfo']['Latitude'], row['AddressInfo']['Longitude']],popup=row['AddressInfo']['AddressLine1'], icon=folium.Icon(color='red')).add_to(m)
    elif row['AddressInfo']['Country']['Title'] == 'Italy':
        folium.Marker(location=[row['AddressInfo']['Latitude'], row['AddressInfo']['Longitude']],popup=row['AddressInfo']['AddressLine1'], icon=folium.Icon(color='green')).add_to(m)

m = add_categorical_legend(m, 'Legenda',
labels = ["Spain","Italy"],
colors = ["Red","Green"])


# In[107]:


#De gehele opbouw van de streamlit app!:
pages = st.sidebar.radio('paginas',options=['Home', 'Datasets', 'Histogram', 'Lijndiagram', 'Kaart'], label_visibility='hidden')

if pages == 'Home':
    st.subheader("Case 3 - Elektrische voertuigen - GROEP 23")
    st.markdown("Data Science 2022 - HvA - Osman, Thomas, Floris & Jakob")
    
elif pages == 'Datasets':
    st.markdown("Hieronder de weergaves van de rauwe en de bewerkte datasets die wij hebben gebruikt.")
    
    st.subheader('#1 Laadpaaldata.csv')
    st.markdown("Hier een overzicht van wat het .csv bestand van de laadpaaldata laat zien. Ons viel meteen één ding op toen wij naar ChargeTime keken, er zitten namelijk veel negatieve waardes in deze kolom.")
    st.dataframe(data=df, use_container_width=False)
    
    st.markdown("De gefilterde en opgeschoonde dataset:")
    st.markdown("Bij 'ChargeTime' hebben wij nu alle data onder de 0 uur en boven de 12 uur weggehaald. Dit geeft een veel duidelijker beeld van de oplaadtijden per auto.")
    st.dataframe(data=df_chargetime, use_container_width=False)
    
    st.subheader('#2 API van RDW')
    st.markdown("Hieronder is een overzicht te zien van de API van de opendata van RDW die wij hebben aangehaald:")
    st.dataframe(data=df1, use_container_width=False)
    st.markdown("Bron: Opendata RDW")
    
    st.subheader("Samengevoegde dataset van de RDW-datasets")
    st.markdown("Het inladen van de data. Deze is afkomstig van de RDW. Om de vergelijking goed uit te kunnen voeren wordt er data gebruikt van de 'R' serie kentekens. Vanwege de grootte van het bestand (120.000+ rijen) is een Excel-bestand gebruikt in plaats van een CSV-bestand. De tabel wordt omgezet in een Pandas Dataframe met de naam df3.")
    st.markdown("De gekentekende voertuigen en de gekentekende voertuigen brandstof datasets van de RDW zijn gecombineerd. De API geeft maar 1000 voertuigen weer dus wij hebben een lijst van alle 14 miljoen voertuigen in Nederland gebruikt. Deze hebben wij daarna gefilterd, dit is wel een grote operatie geweest en dit lukte niet binnen jupiter notebook. Daarom hebben wij dit proces binnen Excel gedaan.")
    st.markdown("Hier staat de dataset maar die is te zwaar om in te laden in streamlit dus die is te vinden in de Jupiter Notebook.")
    #st.dataframe(data=df3, use_container_width=False)
    st.markdown("Bron: Opendata RDW")
    
    st.subheader('#3 API OpenChargeMap')
    st.markdown("Net als bij de API van het RDW hebben wij hier de API aangehaald van de OpenChargeMap:")
    st.dataframe(data=df2, use_container_width=False)
    st.markdown("Bron: OpenChargeMap")
    
elif pages == 'Histogram':
        st.subheader('Histogram van de laadtijd per auto')
        st.markdown("Bekijk hier een histogram van de oplaadtijd per auto, toegespitst op de eerder geselecteerde data (bij de pagina Datasets) die tussen de 0 en de 24 uur valt.")
        st.plotly_chart(histogram1)
elif pages == 'Lijndiagram':
        st.subheader('Lijndiagram van de registratieperiode van verschillende voertuigen per brandstofcategorie')
        st.markdown("Deze plot geeft weer tussen welke periode voertuigen uit de R serie zijn geregistreed. Ook is de soort brandstofcategorie te zien.")
        st.image("lijn1.png")
        #st.plotly_chart(lijn1)
        st.subheader("En een boxplot versie")
        st.markdown("De dataframe wordt hier weergeven in een boxplot. Hier is te zien wanneer, hoeveel en wat voor soort brandstoffen er worden geregisteerd voor nieuwe voertuigen. Dit wordt gedaan door de data aan te halen van de RDW.")
        st.image("box1.png")
        #st.plotly_chart(box1)
elif pages == 'Kaart':
        st.subheader('Kaart van laadpalen in Spanje & Italië')
        st.markdown("Zie hieronder een kaart die alle laadpalen in Spanje en Italië laat zien uit de OpenChargeMap API. Klik op de markers om meer informatie te krijgen over de locatie van de laadpaal en zoom vooral in om meer laadpalen te kunnen zien!")
        folium_static(m)


# In[27]:


#Turkije is uit de API gehaald? Alleen Spanje wordt nog opgehaald. Dus nu Spanje & Italië
#for index,row in df2.iterrows():
    #print(row['AddressInfo']['Country']['Title'])

