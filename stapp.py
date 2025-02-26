import streamlit as st
from pathlib import Path

from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent

from sqlalchemy import create_engine
import sqlite3
import pyodbc
from langchain_groq import ChatGroq

# database option
Localdb="use_localdb"
mysql="use_mysql"
sqlserver="use_sqlserver"

radio_opt = [
    "Use SQLite 3 Database - Student.db",
    "Connect to MySQL Database",
    "Connect to SQL Server Database"
]

selected_opt = st.sidebar.radio(label="Choose the DB you want to chat with", options=radio_opt)

if radio_opt.index(selected_opt) == 1:
    db_uri = mysql
    mysql_host = st.sidebar.text_input("Provide MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database")
elif radio_opt.index(selected_opt) == 2:
    db_uri = sqlserver
    sqlserver_host = st.sidebar.text_input("SQL Server Host")
    sqlserver_database = st.sidebar.text_input("SQL Server Database")
    sqlserver_user = st.sidebar.text_input("SQL Server User")
    sqlserver_password = st.sidebar.text_input("SQL Server Password", type="password")
else:
    db_uri = Localdb

api_key = st.sidebar.text_input(label="GRoq API Key", type="password")

if not db_uri:
    st.info("Please enter the database information.")

if not api_key:
    st.info("Please add the Groq API Key.")

    ##Llm model
llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None,
                 sqlserver_host=None, sqlserver_database=None, sqlserver_user=None, sqlserver_password=None):
    if db_uri == Localdb:
        dbfilepath = Path("student.db").absolute()
        print(dbfilepath)
        creator = lambda: sqlite3.connect(str(dbfilepath))

        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    
    elif db_uri == mysql:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))

    elif db_uri == sqlserver:
        if not (sqlserver_host and sqlserver_database and sqlserver_user and sqlserver_password):
            st.error("Please provide all SQL Server connection details.")
            st.stop()
        
        connection_string = f"mssql+pyodbc://{sqlserver_user}:{sqlserver_password}@{sqlserver_host}/{sqlserver_database}?driver=ODBC+Driver+17+for+SQL+Server"
        return SQLDatabase(create_engine(connection_string))
    
    ## configured database bassed on selection

if db_uri == mysql:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
elif db_uri == sqlserver:
    db = configure_db(db_uri, sqlserver_host=sqlserver_host, sqlserver_database=sqlserver_database, 
                      sqlserver_user=sqlserver_user, sqlserver_password=sqlserver_password)
else:
    db = configure_db(db_uri)


# Toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools=toolkit.get_tools()


# Agent
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Chat History
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query, callbacks=[streamlit_callback])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
