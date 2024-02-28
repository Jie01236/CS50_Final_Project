# PROJECT TITLE: Flight Footprints: Logging Every Journey

### 1 introduction :

This website was born out of my passion for travel and my fondness for documenting the cities I've visited. I found it cumbersome to constantly browse through calendars to recall my past journeys; there was no platform that offered a visual representation of the places I've been to. Therefore, I decided to design a website that could fulfill this need. Part of the design and functionality of this website came from the problemSet for week 9.

The core functionality of this platform is to provide a user-friendly way for travellers to track and display the cities we have visited. My favorite part is that it integrates a map that marks each city, making it an efficient tool for documenting past travels. Furthermore, when using various airline apps, I often encounter features that display the total miles I have flown. I find this to be very interesting. Therefore, I have also opted to calculate the distance between two places and sum all these distances to determine the total kilometers a user has flown or traversed


### 2. Description of different files and their purposes:

#### - app.py:
This is the main file that runs the Flask web application. It handles routing, user sessions, and the interaction with the database.

#### - helper.py :
This Python file provides several backend functionalities for a Flask-based web application. The first two functions(apology and login_required) were adapted and expanded from the content learned in Lesson 9, the get_coordinates function is the main feature of this file. It fetches the geographical coordinates of a city name by calling the Nominatim API provided by OpenStreetMap, returning the latitude and longitude. This functionality is useful for applications that require map positioning and geographic information.

#### - style.css:
A style sheet that defines the visual aesthetics of the website to ensure a good user experience

#### - database.db :
This database contains two tables. One is for recording basic user information, such as username, ID, password, and the total distance flown. The other table is for logging the travel information of the users, including points of departure and destination, travel dates, and the distance between the two locations.

#### - temoplates :
 templates in Flask are HTML files designed to be rendered by the Flask application, with the capability to include dynamic data and reuse common layouts across different pages
##### - apology.html:
this files will show Errors
##### - layout.html :
this file let individual pages inherit this layout and, helping to prevent repetition.
##### - login.html :
this file shows the form to let users log in.
##### - regis_form.html :
this file shows the form to let users register.
##### - history.html :
This page displays a table that includes the departure and destination locations, the date of travel, the distance between these two locations, and the total distance traveled.
##### - index.html :
This is the homepage of this website, showing the total journey and total distance.
##### - record.html :
This page is like the "buy.html" in finance, it amis to keep a record for user's every journey by typing in the departure, destination and date.
##### - remove.html :
This page is like the "sell.html" in finance, it amis to keep a remove the journey which the user wants to delet.
##### - distance.html :
This page is like the "quote.html" in finance, it amis to look up the distance between two citys, that might help users to decide where the next journey to go.
##### - distance2.html :
This page is like the "quoted.html" in finance, shows the result of the distance between two cities.
##### - map.html :
This page utilizes the Leaflet JS library to display a map with markers for the cities a user has traveled to. Upon loading, it fetches coordinate data from the server and displays these locations with markers on the map.


### 3. problems :
The limitation of this website lies in the fact that actual flights may involve layovers or be operated by different airlines, which can result in variations in the actual flight distance. Therefore, we can only record the straight-line distance. Additionally, since we rely on a free API for distance calculations, there might be a limit to the number of queries we can make.
