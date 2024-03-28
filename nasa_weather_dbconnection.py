import psycopg2
import csv
import os

def db_connection(new_data):
    try:
        ######## DATABASE CONNECTION AND DATA UPLOAD ########
        conn = psycopg2.connect(
            dbname = "pagila",
            user = os.environ.get('DB_USER'),
            password = os.environ.get('DB_PASSWORD'),
            host = "data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com",
            port = "5432"
        )

        cursor = conn.cursor()

        ######## OPEN CSV AND RECORD DATA ########
        with open(new_data, 'r') as file:
            csv_reader = csv.DictReader(file)
            for i in csv_reader:
                date = i['Date']
                sol_number = int(i['Sol Number'])
                temperature_max = i['Temperature Max']
                temperature_min = i['Temperature Min']
                pressure = int(i['Pressure'])
                sunrise = i['Sunrise']
                sunset = i['Sunset']

                ######## CHECK FOR EXISTING DATA BASED ON UNIQUE DATA ########
                query = "SELECT COUNT(*) FROM student.mars_weather WHERE \"Date\" = %s AND \"Sol Number\" = %s"
                cursor.execute(query, (date, sol_number))
                exisiting_data_count = cursor.fetchone()[0]
                
                ######## INSERT NEW DATA TO DATABASE ########
                if exisiting_data_count == 0:
                    insert_query = """INSERT INTO student.mars_weather ("Date", "Sol Number", "Temperature Max", "Temperature Min", "Pressure", "Sunrise", "Sunset") VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(insert_query, (date, sol_number, temperature_max, temperature_min, pressure, sunrise, sunset))
                    conn.commit()
                    print("New data was successfully added!")
                else:
                    print("No new data to insert")

        cursor.close()
        conn.close()

    except (Exception, psycopg2.Error) as err:
        print("Connection error = ", err)


new_data = 'mars.csv'
db_connection(new_data)