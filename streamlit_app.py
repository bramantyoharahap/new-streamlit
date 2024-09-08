import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from pandasql import sqldf
import plotly.express as px

spreadsheet_master = "https://docs.google.com/spreadsheets/d/1WYwhKtns9Jd0QZ4QmlJOd_YO9baQG5sBLGeBcf-hJMY"
spreadsheet_response = "https://docs.google.com/spreadsheets/d/1PbqBhlvhcIFN7i-19vVZqEkYX45s07mcgn3QVyUQdjQ"

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df_question = conn.read(spreadsheet=spreadsheet_master, worksheet="Question")
df_domain = conn.read(spreadsheet=spreadsheet_master, worksheet="Domain")
df_option = conn.read(spreadsheet=spreadsheet_master, worksheet="Option")
df_option['Grade'] = df_option['Grade'].astype(int)
df_response_header = conn.read(spreadsheet=spreadsheet_response, worksheet="Response - Header")
df_response_detail = conn.read(spreadsheet=spreadsheet_response, worksheet="Response - Detail")
# df_response_header = conn.read(spreadsheet=spreadsheet_response, worksheet="RH")
# df_response_detail = conn.read(spreadsheet=spreadsheet_response, worksheet="RD")
df_sale = conn.read(spreadsheet=spreadsheet_master, worksheet="Test")

# response_data = pd.merge(left= df_response_header, right=df_response_detail, left_on="Id", right_on="ResponseId")
# response_data = pd.merge(left= response_data, right=df_option, left_on="Option", right_on="Id")
# response_data['Grade'] = response_data['Grade'].astype(int)

#("#c0e6f5","#b5e6a2","#daf2d0", "#ffff00", "#ff0000")


def fn1():
    for i in range(1,30):
        _df = sqldf(f"""            
            Select 
                Person,
                cast(Grade as varchar) as Rank,  
                Sequence,
                (select count(distinct person) from df_response_header) as Responder
            from response_data where Question = {i}
            """)
        st.bar_chart(_df, x="Sequence", y="Responder", color="Rank", stack=None)
        
def fn2():
    for i in range(1,30):
        _df = sqldf(f"""
            WITH T AS(            
                select 
                    a.Id,
                    a.Date,
                    a.Person,
                    a.Question,
                    b.Sequence,
                    b.Option,
                    cast(e.Grade as varchar(1)) as Rank
                from df_response_header as a 
                inner join df_response_detail as b on a.Id = b.ResponseId
                left join df_question as c on c.Id = a.Question
                inner join df_domain as d on d.Id = c.Domain 
                left join df_option as e on e.Id = b.Option
                where a.Question = {i}
            )
            SELECT 
                Sequence,
                case 
                    when Rank=1 then '#72d8ff'
                    when Rank=2 then '#b5e6a2'
                    when Rank=3 then '#daf2d0'
                    when Rank=4 then '#ffff47'
                    when Rank=5 then '#fd5454'
                end as Color,
                count(*) as ResponderCount
            FROM T
            GROUP BY Sequence, Color
            ORDER BY Sequence;
            """)
        df_temp = sqldf(f"""
            select 
                d.Name,
                a.Question as QId,
                c.Question as Question
            from df_response_header as a 
            inner join df_response_detail as b on a.Id = b.ResponseId
            left join df_question as c on c.Id = a.Question
            inner join df_domain as d on d.Id = c.Domain 
            left join df_option as e on e.Id = b.Option
            where a.Question = {i}
            group by d.Name
                       """)
        
        st.title(f"""
                 Domain - {df_temp.loc[0,'Name']}\n
                 Question: {int(df_temp.loc[0,'QId'])} - {df_temp.loc[0,'Question']}
                 """)
        
        fig = px.bar(
            _df, 
            x="Sequence", 
            y="ResponderCount", 
            color="Color",
            color_discrete_map="identity",
            text_auto=False)
        
        fig.update_yaxes(range=[0,10])
        st.plotly_chart(fig)
        # st.bar_chart(_df, x="Sequence", y="ResponderCount", color="Rank", stack=None)
        
def fn3():
    for i in range(1,7):
        _df = sqldf(f"""
            WITH T AS(            
                select 
                    a.Id,
                    a.Date,
                    a.Person,
                    a.Question,
                    b.Sequence,
                    b.Option,
                    cast(e.Grade as varchar(1)) as Rank,
                    (select count(distinct person) from df_response_header) as ResponderCount
                from df_response_header as a 
                inner join df_response_detail as b on a.Id = b.ResponseId
                left join df_question as c on c.Id = a.Question
                inner join df_domain as d on d.Id = c.Domain 
                left join df_option as e on e.Id = b.Option
                where d.Id = {i}
            )
            SELECT 
                Sequence,
                Rank,
                case 
                    when Rank=1 then '#72d8ff'
                    when Rank=2 then '#b5e6a2'
                    when Rank=3 then '#daf2d0'
                    when Rank=4 then '#ffff47'
                    when Rank=5 then '#fd5454'
                end as Color,
                count(*) as ResponderCount
            FROM T
            GROUP BY Sequence, 
                Rank,
                Color
            ORDER BY Sequence, Rank;
            """)
        
        df_temp = sqldf(f"""
            select 
                Name
            from df_domain
            where Id = {i}
                       """)
        
        st.title(f"""
                 Domain - {df_temp.loc[0,'Name']}
                 """)
        
        fig = px.bar(
            _df, 
            x="Sequence", 
            y="ResponderCount", 
            color="Color",
            color_discrete_map="identity",
            text_auto=False)
        
        fig.update_yaxes(range=[0,50])
        st.plotly_chart(fig)
        # st.bar_chart(_df, x="Sequence", y="ResponderCount", color="Rank", stack=None)
        
# fn1()
# fn2()
fn3()

def _fn2():
    for i in range(1,30):
        _df = sqldf(f"""
            WITH T AS(            
                select 
                    a.Id,
                    a.Date,
                    a.Person,
                    a.Question,
                    b.Sequence,
                    b.Option,
                    cast(e.Grade as varchar(1)) as Rank
                    ,
                    (select count(distinct person) from df_response_header) as ResponderCount
                from df_response_header as a 
                inner join df_response_detail as b on a.Id = b.ResponseId
                left join df_question as c on c.Id = a.Question
                inner join df_domain as d on d.Id = c.Domain 
                left join df_option as e on e.Id = b.Option
                where a.Question = {i}
            )
            SELECT 
                *,
                case 
                    when Rank=1 then '#72d8ff'
                    when Rank=2 then '#b5e6a2'
                    when Rank=3 then '#daf2d0'
                    when Rank=4 then '#ffff47'
                    when Rank=5 then '#fd5454'
                end as Color
            FROM T
            GROUP BY Color
            ORDER BY Sequence;
            """)
        df_temp = sqldf(f"""
            select 
                d.Name,
                a.Question as QId,
                c.Question as Question
            from df_response_header as a 
            inner join df_response_detail as b on a.Id = b.ResponseId
            left join df_question as c on c.Id = a.Question
            inner join df_domain as d on d.Id = c.Domain 
            left join df_option as e on e.Id = b.Option
            where a.Question = {i}
            group by d.Name
                       """)
        
        st.title(f"""
                 Domain - {df_temp.loc[0,'Name']}\n
                 Question: {int(df_temp.loc[0,'QId'])} - {df_temp.loc[0,'Question']}
                 """)
        
        fig = px.bar(
            _df, 
            x="Sequence", 
            y="ResponderCount", 
            color="Color",
            color_discrete_map="identity",
            text_auto=False)
        
        fig.update_yaxes(range=[0,100])
        st.plotly_chart(fig)
        # st.bar_chart(_df, x="Sequence", y="ResponderCount", color="Rank", stack=None)
    
    
