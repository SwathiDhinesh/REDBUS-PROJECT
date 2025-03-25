
_                          **      Data-Scraping-with-Selenium-Dynamic-Filtering-using-Streamlit**__
_**Introduction*
  The Red Bus Project is a web scraping and visualization tool built with Selenium to extract bus information from the RedBus website. It stores the data in a MySQL database and provides an interactive visualization interface using Streamlit. The goal is to deliver insights into bus schedules, prices, ratings, and seat availability.
  
**
Technologies Used:**
Selenium: To automate web scraping from RedBus.
MySQL: As the database for storing the scraped data.
Streamlit: For creating a web-based interface for visualizing the data.
Python: For all backend operations, including scraping, data processing, and visualization.

**
FEATURES OF APPLICATION**
Retrive the Bus Information:
  Selenium is a powerful tool for automating web browsers, which is especially useful for web scraping tasks. If you want to retrieve bus details from RedBus, 
 you can use Selenium to automate the process of searching for buses and extracting the relevant information. This involves interacting with web elements 
 like input fields and buttons, waiting for the page to load, and extracting the desired details from the search results.
 
**Store data in database:**
The collected bus details data was transformed into pandas dataframes. Before that, a new database and tables were created using the MySQL connector. With the help of MySQL, the data was inserted into the respective tables. The database could be accessed and managed in the MySQL environment.
**
web app - streamlit:**
With the help of Streamlit, you can create an interactive application similar to RedBus by designing a user-friendly interface that allows users to search for bus routes, view available buses, and get details like departure times and price.



