import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from pandasql import sqldf

spreadsheet_master = "https://docs.google.com/spreadsheets/d/1WYwhKtns9Jd0QZ4QmlJOd_YO9baQG5sBLGeBcf-hJMY"
spreadsheet_response = "https://docs.google.com/spreadsheets/d/1PbqBhlvhcIFN7i-19vVZqEkYX45s07mcgn3QVyUQdjQ"

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df_question = conn.read(spreadsheet=spreadsheet_master, worksheet="Question")
df_option = conn.read(spreadsheet=spreadsheet_master, worksheet="Option")
df_response_header = conn.read(spreadsheet=spreadsheet_response, worksheet="Response - Header")
df_response_detail = conn.read(spreadsheet=spreadsheet_response, worksheet="Response - Detail")
df_sale = conn.read(spreadsheet=spreadsheet_master, worksheet="Test")

response_data = pd.merge(left= df_response_header, right=df_response_detail, left_on="Id", right_on="ResponseId")
response_data = pd.merge(left= response_data, right=df_option, left_on="Option", right_on="Id")
response_data['Grade'] = response_data['Grade'].astype(int)

for i in range(1,30):
    _df = sqldf(f"""            
        Select 
            Person,
            cast(Grade as varchar) as Rank,  
            Sequence,
            (select count(distinct person) from df_response_header) as Responder
        from response_data where Question = {i}
        """)
    st.bar_chart(_df, x="Sequence", y="Responder", color="Rank", stack="normalize")
    
    #("#c0e6f5","#b5e6a2","#daf2d0", "#ffff00", "#ff0000")
