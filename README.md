Hello, I am Anthony Tsiantis. This Web Application was created as my final project for the CS50 course offered by Harvard University. I made this website in August, 2020.

For my final project, my goal was to create a program that greatly impacted my community and possibly even the world.
With the current global Coronavirus Pandemic, I decided to use my newly found knowledge in web development to create a website that displays custom coronavirus data to those in need. This webpage was developed using HTML, CSS, Javascript, AJAX, Python, Flask, SQL and Jinja. I have created this website for two different types of users, Patients and Healthcare workers.

Firstly, patients can create an account and login.
Once logged in, they will be redirected to their homepage where their COVID-19 test results will be displayed, as well as additional global and local coronavirus data.
Using Javascript geolocation, the website obtains the user's location and with the help of Google Maps geocoding API, the website returns the country and state that the user is physically located in.
With this knowledge, we can get local data about the coronavirus and display it to the users.
Also, I implemented google's maps API which displays a mini-map on the website with a marker on the user's location.
The idea of the map idea is to display the fastest route from the user to the hospital.

The Settings' Route will show the user their current email and allow the user to change their email.
The Forgot Password tab allows the user to change their password once logged in.
Finally, the Logout Tab allows the user to logout of their account.

Healthcare workers have access to the same features, in addition to a few other functions.
The first exclusive feature Healthcare workers have access to is a complete list of patients and their COVID statuses.
Once lab results are in, Healthcare providers can update the COVID-19 lab results of their patients by using the update tab.
If multiple users have the same name, the update tab will redirect them to a new HTML page where the healthcare workers can select the user based on email or user identification.

I created an API KEY variable in the javascript.js file to upload your own google maps API key!
