#----Importing Dependencies----

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go

#----Reading the cleaned and preprocessed data----

df = pd.read_parquet('cleaned_traffic.parquet')

#---Columns of Dataframe------

#['City', 'Vehicle Type', 'Weather', 'Economic Condition', 'Day Of Week',
#       'Hour Of Day', 'Speed', 'Is Peak Hour', 'Random Event Occurred',
#       'Energy Consumption', 'Traffic Density']

#----Page Configuration----

st.set_page_config('🚦FutureFlow Traffic Dashboard', layout = 'wide')
st.markdown('<style>div.block-container{padding-top:0.5rem;}</style>', unsafe_allow_html=True)

#----Sidebar / Filters----

with st.sidebar:
  with st.container(border = True):
    st.markdown('### Filters')
    
    #----Vehicles----
    
    vehicle = st.multiselect(label = 'Select the Vehicle Type', options = list(df['Vehicle Type'].unique()))
    
    if not vehicle:
      df1 = df.copy()
    else:
      df1 = df[df['Vehicle Type'].isin(vehicle)]
      
    filtercar = df1['Vehicle Type'].count()
    #----City----
    
    city = st.multiselect(label='Select the city', options = list(df['City'].unique()))
    
    if not city:
      df2 = df1.copy()
    else:
      df2 = df1[df1['City'].isin(city)]
      
    #----Weather----
    
    weather = st.multiselect(label='Select the Weather condition', options = list(df['Weather'].unique()))
    
    if not weather:
      df3 = df2.copy()
    else:
      df3 = df2[df2['Weather'].isin(weather)]
      
    #----Peak Hours----
    
    st.write('Peak Hours')
    
    col1, col2 = st.columns([0.5,0.5])
    
    with col1:
      yespeak = st.checkbox(label='Yes')
      
    with col2:
      nopeak = st.checkbox(label='No')
    
    if yespeak:
      if nopeak:
        df4 = df3.copy()
      else:
        df4 = df3[df3['Is Peak Hour']]
    else:
      if nopeak:
        df4 = df3[~df3['Is Peak Hour']]
      else:
        df4 = df3.copy()
        
    #----Economic Conditions----
    
    condition = st.multiselect(label='Select the Economic Condition', options= list(df4['Economic Condition'].unique()))
    
    if not condition:
      df5 = df4.copy()
    else:
      df5 = df4[df4['Economic Condition'].isin(condition)]
      
    #----Random Event Occurred----
    
    st.write('Random Event Occurred')
    
    col3, col4 = st.columns([0.5,0.5])
    
    with col3:
      randomyes = st.checkbox('Occur')
    with col4:
      randomno = st.checkbox('Not Occur')
      
    if randomyes:
      if randomno:
        df6 = df5.copy()
      else:
        df6 = df5[df5['Random Event Occurred']]
    else:
      if randomno:
        df6 = df5[~df5['Random Event Occurred']]
      else:
        df6 = df5.copy()
        
    #----Day Of Week----
    
    day = st.multiselect(label='Select the Day', options=list(df['Day Of Week'].unique()))
    
    if not day:
      filterdf = df6.copy()
    else:
      filterdf = df6[df6['Day Of Week'].isin(day)]
      
c1, c2, cl3,cl4 = st.columns([0.55,0.15,0.15,0.15])

with c1:
  st.title('🚦FutureFlow Traffic Dashboard')
  
with c2:
  st.metric(label='Total Vehicles', value=filtercar, delta='🚘Total Vehicles', delta_color='off')

with cl3:
  filterrandom = filterdf[filterdf['Random Event Occurred']==True]['Random Event Occurred'].count()
  st.metric(label='Random Event', value=filterrandom, delta='🚘Random Events', delta_color='off')
  
with cl4:
  filterhour = df4[df4['Is Peak Hour']==True]['Is Peak Hour'].count()
  st.metric(label='Peak Hours', value=filterhour, delta='🚘Peak Hours', delta_color='off')
    
###----Tabs----###
      
t1,t2 = st.tabs(['Summary View','Dataset']) #tabs Configuration

with t1:
  st.markdown('### Summary View') #markdown 
  
  c3,c4 = st.columns([0.7,0.3])
  
  with c3: #column 3
    st.markdown('##### City vs. Traffic Density by Time Period') #title of plot

    densitydf = filterdf.groupby(['City','Time Period'])['Traffic Density'].mean().unstack() #filtered data
    
    traces = []
    
    for col in densitydf.columns:
      trace = go.Bar(x = densitydf.index, y = densitydf[col], name=col)
      traces.append(trace)
      
    layout = dict(xaxis_tickangle = 0, xaxis_title = 'City', yaxis_title = 'Average Traffic Density',xaxis = dict(tickfont = dict(size = 15)))
    
    fig1 = go.Figure(layout=layout,data = traces)
    st.plotly_chart(fig1, use_container_width=True)
    
  with c4: #column 4
    piedf = filterdf['Vehicle Type'].value_counts().reset_index()
    st.markdown('##### Distrubution of Total Vehicles')
    fig2 = px.pie(piedf, values=piedf['count'], labels=piedf['Vehicle Type'], names='Vehicle Type')
    fig2.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20)
    fig2.update_layout(showlegend=True)
    st.plotly_chart(fig2, use_container_width=True)

    
  c5,c6,c7 = st.columns([0.4,0.3,0.3])
  
  with c5: #column 5
    se_df = filterdf.groupby(['Day Of Week'])[['Traffic Density', 'Energy Consumption']].mean().reset_index()
    st.markdown('##### Coorelation between Traffic Density and Electricity Consumption')
    fig3 = px.scatter(se_df, x = 'Traffic Density', y = 'Energy Consumption', size='Energy Consumption',hover_name='Day Of Week',color='Day Of Week',size_max=60)
    st.plotly_chart(fig3, use_container_width=True)
    
  with c6: #column 6
    st.markdown('##### Coorelation between Speed and Electricity Consumption')
    speed_relation = filterdf.groupby(['Day Of Week'])[['Speed', 'Energy Consumption']].mean().reset_index()
    fig4 = px.scatter(speed_relation, x = 'Speed', y = 'Energy Consumption', size='Speed',hover_name='Day Of Week',color='Day Of Week',size_max=60)
    st.plotly_chart(fig4, use_container_width=True)
  
  with c7: #column 7
    st.markdown('##### Distribution of Traffic by Time Period')
    carbardf = filterdf.groupby('Time Period')['Vehicle Type'].count().reset_index()
    fig5 = px.bar(carbardf, x='Time Period', y='Vehicle Type')
    fig5.update_layout(bargap=0.2)
    st.plotly_chart(fig5, use_container_width=True)
  
with t2: #tab 2
  c8,c9 = st.columns([0.5,0.5])
  
  with c8:
    st.markdown('##### Distribution of Vechiles in City')
    c10, c11,_ = st.columns([0.25,0.25,0.50])
    with c10:
      minbox = st.checkbox(label='Min', value = False)
    with c11:
      maxbox = st.checkbox(label='Max', value = True)
      
    citydf = df.groupby(['City','Vehicle Type']).size().unstack()
    
    if minbox:
      if maxbox:
        st.dataframe(citydf.style.highlight_max(axis=0, color='lightgreen'), hide_index=False, use_container_width=True)
      else:
        st.dataframe(citydf.style.highlight_min(axis=0, color='salmon'), hide_index=False, use_container_width=True)
    else:
      st.dataframe(citydf.style.highlight_max(axis=0, color='lightgreen'), hide_index=False, use_container_width=True)
      
  with c9:
    randomevent = df[df['Random Event Occurred'] == True].groupby(['City','Time Period']).size().unstack()
    
    st.markdown('##### When Random Event Occured like Accident / Road collapse etc.')
    
    c12, c13,_ = st.columns([0.3,0.3,0.4])
    
    with c12:
      yes_event = st.checkbox(label='Occured', value = False)
    with c13:
      no_event = st.checkbox(label='Not Occured',value = True)
    
    if yes_event:
      if no_event:
        st.dataframe(randomevent, hide_index=False,use_container_width=True)
      else:
        st.dataframe(randomevent.style.highlight_max(axis = 0, color = 'salmon'), hide_index=False,use_container_width=True)
    else:
      st.dataframe(randomevent, hide_index=False,use_container_width=True)
      
  st.markdown('### Dataset')
  st.dataframe(filterdf,use_container_width=True)