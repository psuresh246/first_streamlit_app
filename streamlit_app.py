import streamlit;
import pandas;
import requests;
import snowflake.connector;
from urllib.error import URLError;

streamlit.title('Diner app');
streamlit.header('Breakfast Menu');
streamlit.text('Omega 3 & Blueberry Oatmeal');
streamlit.text('Kale, Spinach & Rocket Smoothie');
streamlit.text('Hard-Boiled Free-Range Egg');
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇');
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt");
my_fruit_list = my_fruit_list.set_index('Fruit');
# Let's put a pick list here so they can pick the fruit they want to include 
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Apple']);
fruit_toshow = my_fruit_list.loc[fruit_selected];

# Display the table on the page
streamlit.dataframe(my_fruit_list);

# display selected fruit
streamlit.dataframe(fruit_toshow);

# function for retrieving fruitvice data from api.
def get_fruityvice_data(_fruit_choice):
  fruityvice_response=requests.get('https://fruityvice.com/api/fruit/'+fruit_choice);
  # using pandas to normalise the json data from prev. requests.get api response.
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json());
  return fruityvice_normalized;

streamlit.header("Fruityvice Fruit Advice");
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?');
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.");
  else:
    # use function get_fruityvice_data to get data
    fv_data = get_fruityvice_data(fruit_choice);
    # build a datatable using dataframe.
    streamlit.dataframe(fv_data);

except URLError as e:
   streamlit.error();

#streamlit.stop();
#snowflake connector

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
     my_cur.execute("select * From PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST");
     return my_cur.fetchall();

# add a button to load the fruit.
if streamlit.button("Get Fruit Load List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]);
  my_data_rows = get_fruit_load_list();
  streamlit.dataframe(my_data_rows);

# allow user to add a new fruit to list.
add_my_fruit = streamlit.text_input("What fruit would you like to add?");
streamlit.write("thanks for adding '"+add_my_fruit+"'");
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('"+add_my_fruit+"')");


