# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: {st.__version__}")
st.write(
  """Choose the Fruit you want in your custome smoothie!
  """
)

# Write directly to the app
# import streamlit as st
# title = st.text_input('Movie title','Life of Brain')
# st.write('The current movie title is',title)



## Insert a option box

option = st.selectbox(
    'what is your Favourite fruit?',
    ('Banana','Strawberries','Peaches')
)

st.write('your favourite is:', option)

from snowflake.snowpark.functions import col
cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list =st.multiselect(
    "choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

ingredients_string=""

if ingredients_list:
    

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '

# st.write(ingredients_string)




name_on_order = st.text_input('Name on Smoothie Order')

my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                    VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')"""

st.write(my_insert_stmt)
# st.stop



time_to_insert =st.button('Submit order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")    

import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
st.text(smoothiefroot_response.json())
sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
