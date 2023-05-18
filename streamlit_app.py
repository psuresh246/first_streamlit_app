import streamlit;
import pandas;
import requests;
import snowflake.connector;

streamlit.title('Diner app');
streamlit.header('Breakfast Menu');
streamlit.text('Omega 3 & Blueberry Oatmeal');
streamlit.text('Kale, Spinach & Rocket Smoothie');
streamlit.text('Hard-Boiled Free-Range Egg');
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇');
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt");
my_fruit_list = my_fruit_list.set_index('Fruit');
# Let's put a pick list here so they can pick the fruit they want to include 
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Apple']);
fruit_toshow = my_fruit_list.loc[fruit_selected];

# Display the table on the page
streamlit.dataframe(my_fruit_list);

# display selected fruit
streamlit.dataframe(fruit_toshow);

fruityvice_response=requests.get('https://fruityvice.com/api/fruit/watermelon');
# using pandas to normalise the json data from prev. requests.get api response.
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# build a datatable using dataframe.
streamlit.dataframe(fruityvice_normalized);

#snowflake connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * From PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.text("Fruit Load List Contains:")
streamlit.dataframe(my_data_rows);

# allow user to add a new fruit to list.
add_my_fruit = streamlit.text_input("What fruit would you like to add?");
streamlit.write("thanks for adding '"+add_my_fruit+"'");
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('"+add_my_fruit+"')");
