#--------------------
# Clothing Catalog streamlit app
# Author: OG
# Description: Code adapted from the ESS-DLKW Snowflake workshop
# url: https://omargomez2-clothing-catalog-streamlit-app-bhyzo8.streamlit.app/
#-----------

import streamlit
import snowflake.connector
import psycopg2
import pandas

# connect to snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()

# connect to postgresql
def init_connection():
    return psycopg2.connect(**streamlit.secrets["postgres"])
conn = init_connection()
my_cur = conn.cursor()

streamlit.title("Clothing Catalog")

# run a snowflake query and put it all in a var called my_catalog
my_cur.execute("select \"COLOR_OR_STYLE\" from catalog_for_website;")
my_catalog = my_cur.fetchall()

# put the data into a dataframe
df = pandas.DataFrame(my_catalog)

# temp write the dataframe to the page so I Can see what I am working with
# streamlit.write(df)
# put the color_or_style column into a list
color_list = df[0].values.tolist()

# print(color_list)
# Let's put a pick list here so they can pick the color
option = streamlit.selectbox('Pick a sweatsuit color or style:', list(color_list))

# We'll build the image caption now, since we can
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

# use the option selected to go back and get all the info from the database
my_cur.execute("select \"DIRECT_URL\", \"PRICE\", \"SIZE_LIST\", \"UPSELL_PRODUCT_DESC\" from catalog_for_website where \"COLOR_OR_STYLE\" = '" + option + "';")
df2 = my_cur.fetchone()
streamlit.image(df2[0], width=400, caption= product_caption)
streamlit.write('Price: ', df2[1])
streamlit.write('Sizes Available: ',df2[2])
streamlit.write(df2[3])

conn.close()
