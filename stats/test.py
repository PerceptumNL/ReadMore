import psycopg2
import pandas as pd
import sqlite3
import sqlalchemy

print "--Connecting to database.."
engine = sqlalchemy.create_engine('postgresql://elise@localhost:5432/read_more')

print "--Running queries..."
query = "SELECT * FROM content_article;"
content_articles = pd.read_sql(query, engine)
print content_articles

