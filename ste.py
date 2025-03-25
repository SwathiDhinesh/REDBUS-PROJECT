# importing libraries
import pandas as pd
import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import time

lists_A=[]
df_A=pd.read_csv("ap2.csv")
for i,r in df_A.iterrows():
    lists_A.append(r["Route_name"])


lists_As=[]
df_As=pd.read_csv("as2.csv")
for i,r in df_As.iterrows():
    lists_As.append(r["Route_name"])


lists_C=[]
df_C=pd.read_csv("ch2.csv")
for i,r in df_C.iterrows():
    lists_C.append(r["Route_name"])


lists_H=[]
df_H=pd.read_csv("HR2.csv")
for i,r in df_H.iterrows():
    lists_H.append(r["Route_name"])


lists_jk=[]
df_jk=pd.read_csv("j&K2.csv")
for i,r in df_jk.iterrows():
    lists_jk.append(r["Route_name"])


lists_Ka=[]
df_Ka=pd.read_csv("kada2.csv")
for i,r in df_Ka.iterrows():
    lists_Ka.append(r["Route_name"])


lists_Kr=[]
df_Kr=pd.read_csv(r"D:\vscode1\redbus_selenium\kr2.csv")
for i,r in df_Kr.iterrows():
    lists_Kr.append(r["Route_name"])


lists_T=[]
df_T=pd.read_csv("Ts2.csv")
for i,r in df_T.iterrows():
    lists_T.append(r["Route_name"])


lists_U=[]
df_U=pd.read_csv("up2.csv")
for i,r in df_U.iterrows():
    lists_U.append(r["Route_name"])


lists_W=[]
df_W=pd.read_csv("wb2.csv")
for i,r in df_W.iterrows():
    lists_W.append(r["Route_name"])

#setting up streamlit page
st.set_page_config(layout="wide")


st.markdown("<h1 style='text-align: center; color:#0d2cee ; padding: 20px;'>RED BUS PROJECT --- WEB SCRAPING</h1>", unsafe_allow_html=True)

st.image(r"C:\Users\ADMIN\Desktop\REDBUS PROJECT\red-bus-india-google-maps-1200x900.png",width=750)


st.balloons()


# Apply custom styling to sidebar text using HTML and CSS
st.sidebar.markdown(
    """
    <style>
    .sidebar-title {
        font-size: 30px;  # Increase this value for larger text
        font-weight: bold;
        color: #ee4a0d;  # You can change the color if needed
    }
    .sidebar-radio label {
        font-size: 20px;  # Increase this value for the radio button options
        font-weight: bold;
        color: #333333;  # Customize the color of the radio options
    }
    </style>
    <div class="sidebar-title">🚎 REDBUS BOOKING </div>
    """, unsafe_allow_html=True
)



# Create a radio button menu in the sidebar
web = st.sidebar.radio(
    "🚎 OnlineBus", 
    options=["Home", "🚩 States and 🛣️ Routes"], 
    index=0  # Default selected option
)   
#Display content based on the menu option selected
if web == "Home":

    st.title(":violet[Welcome to REDBUS-ONLINE🚎]")  
    st.video("https://youtu.be/eyAAUGhvZu8?si=Rwba2SEVu_KyW4bm")
    st.write("This is the Homepage of the Redbus Project Overview.")
    st.markdown("The 'Redbus Data Scraping and Filtering with Streamlit Application' aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry.")
    st.markdown("Skills Used:Selenium, Python, Pandas, MySQL,mysql-connector-python, Streamlit.")
    st.subheader(":green[Developed-by:] SWATHI.P")


if web == "🚩States and 🛣️Routes":
    # Title and description for the "States and Routes 🛣️" section
     st.title("## States and Routes 🛣️")
     st.write("Here you will find information on bus routes and states.")
    # Select box for choosing a state
State= st.selectbox("Select a state from the list",
    ["Kerala", "Andhra Pradesh", "Telangana", "Goa", 
      "Himachal", "Assam", "Uttar Pradesh", "West Bengal","Chandigarh","Jammu and Kashmir"])


# Create two columns for bus type and fare range selection
col1, col2 = st.columns(2)

with col1:
    # Radio button for bus type selection
    select_type = st.radio("Choose bus type", ("Sleeper", "Semi-Sleeper", "Others"))

with col2:
    # Radio button for fare range selection
    select_fare = st.radio(" Choose bus fare range", ("150-1000", "1000-2000", "2000 and above"))

st.markdown("<h3 style='font-size: 24px; font-weight: bold;'>Select the time</h3>", unsafe_allow_html=True)

# Time picker for selecting the time
TIME = st.time_input("⌚🕒")

# Display the information based on selections
st.write("### Selected Information:")
st.write(f"State: {State}")
st.write(f"Bus Type: {select_type}")
st.write(f"Fare Range: {select_fare}")
st.write(f"Selected Time: {TIME}")

# Function to fetch bus data based on user inputs (bus_type, fare_range, route_name)
def type_and_fare(bus_type, fare_range, route_name, time):
    # Connect to MySQL database
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="redbus")
    mycursor = conn.cursor()

    # Define fare range based on selection
    if fare_range == "100-1000":
        fare_min, fare_max = 100, 1000
    elif fare_range == "1000-2000":
        fare_min, fare_max = 1000, 2000
    else:
        fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

    # Define bus type condition
    if bus_type == "sleeper":
        bus_type_condition = "Bus_type LIKE '%Sleeper%'"
    elif bus_type == "semi-sleeper":
        bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper%'"
    else:
        bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

    # Parameterized SQL query to prevent SQL injection
    query = '''
        SELECT * FROM bus_details 
        WHERE Price BETWEEN %s AND %s
        AND Route_name = %s
        AND {bus_type_condition} 
        AND Start_time >= %s
        ORDER BY Price, Start_time DESC
    '''.format(bus_type_condition=bus_type_condition)

    mycursor.execute(query, (fare_min, fare_max, route_name, time))
    out = mycursor.fetchall()

    # Close the connection
    conn.close()

    # If no results found, return an empty DataFrame
    if not out:
        return pd.DataFrame()

    # Dynamically retrieve column names from query results
    columns_names = [desc[0] for desc in mycursor.description]

    # Create DataFrame
    df = pd.DataFrame(out, columns=columns_names)
    return df



# Kerala bus fare filtering section
if State == "Kerala":
    K = st.selectbox("Select Route", lists_Kr)  # Select route from the list

    # Getting bus type, fare range, and time input from the user
    select_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-Sleeper", "Others"))
    select_fare = st.radio("Select Fare Range", ("100-1000", "1000-2000", "2000 and above"))
    TIME = st.time_input("Select Start Time")

    # Fetching bus data based on the selected filters
    df_result = type_and_fare(select_type, select_fare, K, TIME)

    # Displaying the result in a dataframe
    if not df_result.empty:
        st.dataframe(df_result)
    else:
        st.warning("No buses found for the selected filters.")

# Andhra bus fare filtering section
if State == "Andhra Pradesh":
    K = st.selectbox("Select Route", lists_A)  # Select route from the list

    # Getting bus type, fare range, and time input from the user
    select_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-Sleeper", "Others"))
    select_fare = st.radio("Select Fare Range", ("100-1000", "1000-2000", "2000 and above"))
    TIME = st.time_input("Select Start Time")

    # Fetching bus data based on the selected filters
    df_result = type_and_fare(select_type, select_fare, K, TIME)

    # Displaying the result in a dataframe
    if not df_result.empty:
        st.dataframe(df_result)
    else:
        st.warning("No buses found for the selected filters.")


# Assam bus fare filtering section
if State == "Assam":
    K = st.selectbox("Select Route", lists_As)  # Select route from the list

    # Getting bus type, fare range, and time input from the user
    select_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-Sleeper", "Others"))
    select_fare = st.radio("Select Fare Range", ("100-1000", "1000-2000", "2000 and above"))
    TIME = st.time_input("Select Start Time")

    # Fetching bus data based on the selected filters
    df_result = type_and_fare(select_type, select_fare, K, TIME)

    # Displaying the result in a dataframe
    if not df_result.empty:
        st.dataframe(df_result)
    else:
        st.warning("No buses found for the selected filters.")


# chandigarh bus fare filtering section
if State == "chandigarh":
    K = st.selectbox("Select Route", lists_C)  # Select route from the list

    # Getting bus type, fare range, and time input from the user
    select_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-Sleeper", "Others"))
    select_fare = st.radio("Select Fare Range", ("100-1000", "1000-2000", "2000 and above"))
    TIME = st.time_input("Select Start Time")

    # Fetching bus data based on the selected filters
    df_result = type_and_fare(select_type, select_fare, K, TIME)

    # Displaying the result in a dataframe
    if not df_result.empty:
        st.dataframe(df_result)
    else:
        st.warning("No buses found for the selected filters.")        

# Himachal bus fare filtering section
if State == "Himachal":
    K = st.selectbox("Select Route", lists_H)  # Select route from the list

    # Getting bus type, fare range, and time input from the user
    select_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-Sleeper", "Others"))
    select_fare = st.radio("Select Fare Range", ("100-1000", "1000-2000", "2000 and above"))
    TIME = st.time_input("Select Start Time")

    # Fetching bus data based on the selected filters
    df_result = type_and_fare(select_type, select_fare, K, TIME)

    # Displaying the result in a dataframe
    if not df_result.empty:
        st.dataframe(df_result)
    else:
        st.warning("No buses found for the selected filters.")        

# Jammu & Kashmir bus fare filtering section
if State == "Jammu & Kashmir":
    K = st.selectbox("Select Route", lists_jk)  # Select route from the list

    # Getting bus type, fare range, and time input from the user
    select_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-Sleeper", "Others"))
    select_fare = st.radio("Select Fare Range", ("100-1000", "1000-2000", "2000 and above"))
    TIME = st.time_input("Select Start Time")

    # Fetching bus data based on the selected filters
    df_result = type_and_fare(select_type, select_fare, K, TIME)

    # Displaying the result in a dataframe
    if not df_result.empty:
        st.dataframe(df_result)
    else:
        st.warning("No buses found for the selected filters.")       

# GOA bus fare filtering section
if State=="Goa":
    K = st.selectbox("Select Route", lists_Ka)  # Select route from the list

    # Getting bus type, fare range, and time input from the user
    select_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-Sleeper", "Others"))
    select_fare = st.radio("Select Fare Range", ("100-1000", "1000-2000", "2000 and above"))
    TIME = st.time_input("Select Start Time")

    # Fetching bus data based on the selected filters
    df_result = type_and_fare(select_type, select_fare, K, TIME)

    # Displaying the result in a dataframe
    if not df_result.empty:
        st.dataframe(df_result)
    else:
        st.warning("No buses found for the selected filters.")       

# Telangana bus fare filtering section
if State == "Telangana":
    K = st.selectbox("Select Route", lists_T)  # Select route from the list

    # Getting bus type, fare range, and time input from the user
    select_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-Sleeper", "Others"))
    select_fare = st.radio("Select Fare Range", ("100-1000", "1000-2000", "2000 and above"))
    TIME = st.time_input("Select Start Time")

    # Fetching bus data based on the selected filters
    df_result = type_and_fare(select_type, select_fare, K, TIME)

    # Displaying the result in a dataframe
    if not df_result.empty:
        st.dataframe(df_result)
    else:
        st.warning("No buses found for the selected filters.")       

# West Bengalbus fare filtering section
if State == "West Bengal":
    K = st.selectbox("Select Route", lists_W)  # Select route from the list

    # Getting bus type, fare range, and time input from the user
    select_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-Sleeper", "Others"))
    select_fare = st.radio("Select Fare Range", ("100-1000", "1000-2000", "2000 and above"))
    TIME = st.time_input("Select Start Time")

    # Fetching bus data based on the selected filters
    df_result = type_and_fare(select_type, select_fare, K, TIME)

    # Displaying the result in a dataframe
    if not df_result.empty:
        st.dataframe(df_result)
    else:
        st.warning("No buses found for the selected filters.")       

# Uttar Pradesh bus fare filtering section
if State == "Uttar Pradesh":
    K = st.selectbox("Select Route", lists_U)  # Select route from the list

    # Getting bus type, fare range, and time input from the user
    select_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-Sleeper", "Others"))
    select_fare = st.radio("Select Fare Range", ("100-1000", "1000-2000", "2000 and above"))
    TIME = st.time_input("Select Start Time")

    # Fetching bus data based on the selected filters
    df_result = type_and_fare(select_type, select_fare, K, TIME)

    # Displaying the result in a dataframe
    if not df_result.empty:
        st.dataframe(df_result)
    else:
        st.warning("No buses found for the selected filters.")       

    