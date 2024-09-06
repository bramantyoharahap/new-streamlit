import streamlit as st
from streamlit_gsheets import GSheetsConnection

spreadsheet_master = "https://docs.google.com/spreadsheets/d/1WYwhKtns9Jd0QZ4QmlJOd_YO9baQG5sBLGeBcf-hJMY"
spreadsheet_response = "https://docs.google.com/spreadsheets/d/1PbqBhlvhcIFN7i-19vVZqEkYX45s07mcgn3QVyUQdjQ"

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df_question = conn.read(spreadsheet=spreadsheet_master, worksheet="Question")
df_response_header = conn.read(spreadsheet=spreadsheet_response, worksheet="Response - Header")

# Print results.
# for row in df_question.itertuples():
#     st.write(f"{int(row.Id)} - {row.Question}")

for row in df_response_header.itertuples():
    st.write(f"{int(row.Id)} - {row.Date} - {row.Person} - {row.Question}")


# st.title("🎈 My new app")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )
