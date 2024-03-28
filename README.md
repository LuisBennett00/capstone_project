As part of my capstone project, I developed this application to streamline the process of collecting and visualizing weather data from the NASA Curiosity rover’s website. Firstly I have created an application that uses selenium to scrape the NASA curisoity website and convert that data into a CSV file. This CSV file is then uploaded to a database where all weather data is collected and stored ready to be pulled. The main application pulls this data from the database and uses streamlit along with matplotlib to visualise this data. This proccess is 100% automated as the scraper and data uploader script are hosted on an AWS EC2 instance and are set to check for data everyday. The database is hosted on an AWS RDS insrance and the final application is hosted using Streamlit Cloud.