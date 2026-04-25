# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col

#Create a database connection to Snowflake.
conn = st.connection("snowflake")

session = conn.session()
session.sql("USE DATABASE smoothies").collect()
session.sql("USE SCHEMA public").collect()

# Write directly to the app.
st.title(f" :cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)



# Create a Snowpark session from the connection.
# This provides a few helpers on top of a standard Python connection.
# If you want to use a plain Snowflake connection instead, you can create
# one with conn.cursor().
name_on_order = ''
name_on_order = st.text_input("Name on Smoothie : ")
st.write("The name on your Smoothie will be:",name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list=[]
ingredients_list= st.multiselect("Choose up to 5 Ingredients : ",my_dataframe, max_selections = 5)

ingredients_string=''
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    for fruit_chosen in ingredients_list: 
        ingredients_string += fruit_chosen + " "

    st.write(ingredients_string)


my_insert_stmt = """ insert into smoothies.public.orders(name_on_order,ingredients)
values ('"""+ name_on_order +"""','""" + ingredients_string + """')"""

time_to_insert=st.button("Submit Order")    

#st.write(my_insert_stmt)

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
        
