import streamlit as st
From pathlib import path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from lanchain.callbacks import streamlitcallbackhandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
import pyodbc

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

LocalDB= "Use_Localdb"  
SQlServer= "use_sqlserver"

radio_opt=["Use SQLLite 3 Database- Student.db","Connect to you sql_server Database"]

selected_opt=st.sidebar.radio(label="Choose the DB which you want to chat",options=radio_opt)

if radio_opt.index(selected_opt)==1:
    db_uri = SQlServer
    sqlserver_host = st.sidebar.text_input("Provide SQL Server Host")
    sqlserver_user = st.sidebar.text_input("SQL Server User")
    sqlserver_password = st.sidebar.text_input("SQL Server Password", type="password")
    sqlserver_db = st.sidebar.text_input("SQL Server Database")
   
   ''' if sqlserver_host and sqlserver_user and sqlserver_password and sqlserver_db:
      db_uri=sqlserver.format(user=sqlserver_user,pASSword=sqlserver_password,host=sqlserver_host,database=sqlserver_db)
    else :
      db_uri=none'''
else:
    db_uri=LOcalDB

api_key=st.sidebar.text_input(label="GRoq API Key",type="password")

if not db_uri:
    st.info("Please enter the database information and uri")

if not api_key:
    st.info("Please add the groq api key")

### llm mODEL
llm=ChatGroq(gorq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri,sqlserver_host=None,sqlserver_user=None, sqlserver_password=None,sqlserver_db=None):
    if db_uri==LOcalDB:
        dbfilepath=(path(__file__).parent/"student.db").absolute()
        print(dbfilepath)
        creator=lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro",uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=creator))
    elif db_uri==SQlServer
        if not (sqlserver_host and sqlserver_user and sqlserver_password and sqlserver_db):
            st.error("Please provide correct details")
            st.stop()
        return SQLDatabase(create_engine(f"mssql+pyodbc://{user}:{password}@{host}/{database}?driver=ODBC+Driver+17+for+SQL+Server"))
    

    if db_uri==SQlServer
        db= configure_db(db_uri,sqlserver_host,sqlserver_user, sqlserver_password,sqlserver_db)
    else:
        db=configure_db(db_uri)
        
    
    
    