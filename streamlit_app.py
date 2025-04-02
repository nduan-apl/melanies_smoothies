# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched
from snowflake.snowpark.context import get_active_session

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
name_on_order = st.text_input("Name on smoothie")
st.write("The name on your smoothie will be:", name_on_order)

session = get_active_session()
og_dataset = session.table("smoothies.public.orders")


my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)

    query = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES('{ingredients_string}', '{name_on_order}')
    """
    
    # st.write(query)
    # st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(query).collect()
        st.success('Your Smoothie is ordered', icon="✅")
