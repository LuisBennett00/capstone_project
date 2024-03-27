import psycopg2
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pandas import DataFrame
import plotly.express as px
import plotly.graph_objects as go
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_data():
    try:
        ######## DATABASE CONNECTION AND DATA RETREIVAL ########
        conn = psycopg2.connect(
            dbname = "pagila",
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = "data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com",
            port = "5432"
        )

        cursor = conn.cursor()

        query = "SELECT * FROM student.mars_weather ORDER BY \"Date\" DESC"
        sol_query = "SELECT DISTINCT \"Sol Number\" FROM student.mars_weather"
        cursor.execute(query)

        rows = cursor.fetchall()
        print(rows)

        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        sol_numbers = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()
        return sol_numbers, df, rows
    
    except (Exception, psycopg2.Error) as err:
        print("Something went wrong - ", err)
        return None, None, None

def get_rover_photos():
    api_key = 'WNyrRQCzP5RIf5Dlhv6UgTKAr24pcA91aRGLuZ9U'
    nasa_url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key={api_key}'

    ######## GET LATEST CURIOSITY PHOTO FROM NASA API ########
    try:
        response = requests.get(nasa_url)
        curiosity_photo_data = response.json()

        if response.status_code == 200:
            latest_photo = curiosity_photo_data['latest_photos'][0]
            jpeg_url = latest_photo['img_src']
            photo_date = latest_photo.get('sol')
            camera_data = latest_photo.get('camera')
            camera_name = camera_data.get('full_name')
            return jpeg_url, photo_date, camera_name
        else:
            return f"Could not get latest photo. Status code: {response.status_code}"
    except Exception as err:
        return f"Error: {str(err)}"

def main():
    st.title("Mars Weather Data")
    st.divider()
    sol_numbers, df, rows = get_db_data()
    jpeg_url, photo_date, camera_name = get_rover_photos()

    with st.sidebar:
        selected_tab = st.radio("Available Martian Data", ["Latest Weather Updates", "Temperature", "Sunset and Sunrise", "Pressure"])
    if selected_tab == "Latest Weather Updates":
        st.header("Most recent weather updates:")
        ######## LAST SEVERAL DAYS OF WEATHER ########
        if rows:
            tab_titles = [f"{row[0]}" for row in rows]
            tabs = st.tabs(tab_titles)
            for i, row in enumerate(rows):
                with tabs[i]:
                    st.write(f"Date: {row[0]}")
                    st.write(f"Sol Number: {row[1]}")
                    st.write("Temperature Max:", row[2])
                    st.write("Temperature Min:", row[3])
                    st.write("Pressure:", row[4])
                    st.write("Sunrise:", row[5])
                    st.write("Sunset:", row[6])
        else:
            st.warning("No data available.")

        #st.write(df)
        st.divider()
        ######## DISPLAY CURIOSITY LATEST PHOTO ########
        st.write(f"Here is the latest photo from mars taken on Sol: {photo_date} using the {camera_name}!")
        st.image(jpeg_url, caption='Latest Photo from Curisoity!')

    elif selected_tab == "Temperature":
        st.header("Martian Max and Min Temperature Records")
        st.write("This page displays a time series of all the recorded minimum and maximum temperatures collected from the Curiosity Rover, the temperature is recored in fahrenheit and measured across Martian Sols(Martian equivelent of days)!
        ######## MAX AND MIN TEMPERATURE TIMESERIES ########
        df['Sol Number'] = pd.to_numeric(df['Sol Number'])
        df['Temperature Min'] = df['Temperature Min'].str.replace('°F', '').astype(float)
        #df['Temperature Max'] = df['Temperature Max'].str.replace('°F', '').astype(float)
        df = df.sort_values(by='Sol Number')
        plt.figure(figsize=(10, 6))
        plt.plot(df['Sol Number'], df['Temperature Min'], color='orange', linewidth = 5)
        #plt.plot(df['Sol Number'], df['Temperature Max'], color='orange', linewidth = 5)
        plt.xlabel('Sol Number')
        plt.ylabel('Temperature (F)')
        plt.title('Min Temperature per Sol')
        plt.grid(True)
        st.pyplot(plt)

        #st.divider()

        df['Sol Number'] = pd.to_numeric(df['Sol Number'])
        #df['Temperature Min'] = df['Temperature Min'].str.replace('°F', '').astype(float)
        df['Temperature Max'] = df['Temperature Max'].str.replace('°F', '').astype(float)
        df = df.sort_values(by='Sol Number')
        plt.figure(figsize=(10, 6))
        #plt.plot(df['Sol Number'], df['Temperature Min'], color='orange', linewidth = 5)
        plt.plot(df['Sol Number'], df['Temperature Max'], color='orange', linewidth = 5)
        plt.xlabel('Sol Number')
        plt.ylabel('Temperature (F)')
        plt.title('Max Temperature per Sol')
        plt.grid(True)
        st.pyplot(plt)

    elif selected_tab == "Sunset and Sunrise":
        st.header("Here is a visualisation of the sunset and sunrise times on Mars")
         ######## SUNET TIMESERIES ########

        df['Sunrise'] = pd.to_datetime(df['Sunrise'], format='%H:%M:%S')
        df['Sunset'] = pd.to_datetime(df['Sunset'], format='%H:%M:%S')

        sunrise_data = pd.to_datetime(df['Sunrise'], format='%H:%M:%S')
        sunset_data = pd.to_datetime(df['Sunset'], format='%H:%M:%S')
        time_difference = sunset_data - sunrise_data
        time_in_min = time_difference.dt.total_seconds() / 60
        time_difference_list = time_in_min.tolist()

    
        plt.figure(figsize=(10, 6))
        plt.plot(df['Sol Number'], df['Sunset'], marker='o', color='skyblue', linestyle='-', label='Sunset')
        plt.xlabel('Sol Number')
        plt.ylabel('Time of Sunset')
        plt.title('Sunset Time Series')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        #st.divider()

        ######## SUNRISE TIMESERIES ########
        plt.figure(figsize=(10, 6))
        plt.plot(df['Sol Number'], df['Sunrise'], marker='o', color='orange', linestyle='-', label='Sunrise')
        plt.xlabel('Sol Number')
        plt.ylabel('Time of Sunrise')
        plt.title('Sunrise Time Series')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

    elif selected_tab == "Pressure":
        st.header("Here is a visualisation of the pressure on Mars")
        ######## PRESSURE TIME SERIES ########
        df = df.sort_values(by='Sol Number')

        plt.figure(figsize=(10, 6))
        plt.plot(df['Sol Number'], df['Pressure'], color='orange', linewidth = 5)
        plt.xlabel('Sol Number')
        plt.ylabel('Pressure(Pa)')
        plt.title('Pressure Time Series')
        plt.grid(True)
        st.pyplot(plt)

if __name__ == "__main__":
    main()
