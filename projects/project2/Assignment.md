# Michelin Restaurants

## Tasks
## Part 1: Data Analysis only
- The purpose of this section is to analyze data, no need to create any visualization.

1. Create a class called `Restaurant` which contains the properties
    - `name` of type `String`
    - `year` of type `String`
    - `city` of type `String`
    - `region` of type `String`
    - `cuisine` of type `String`
    - `price` of type `String`
    - `starts` of type `Int`
    - `location` of type `Coordinate`

        `Coordinate` is another class you need to create the contains the latitude and longitude where a restaurant is located.

2. Create a function called `restaurants_for_cuisine` that accepts any cuisine name and returns a list with elements of type `Restaurant` with all the restaurants that belong to that cuisine.

3. Create a function called `restaurants_for_star` that accepts any integer and returns a list of with elements of type `Restaurant` with all the restaurants that have that number of stars.

4. Create a function called `restaurants_for_city` that accepts any city name and returns a list of with elements of type `Restaurant` with all the restaurants that are part of that city.

5. Create a function called `gothenburg_michelins` that return a list with elementss of type `Restaurant` with all the Michelin restaurants located in Gothenburg.

## Part 2: Data Visualization
- The purpose of this section is to practice analyzing data and visualizing it.

1. What are the ten regions with most Michelin restaurants?
    - Show your results in a histogram.

2. How many Michelin restaurants are located in each Nordic country; e.g., Sweden, Norway, Island, Denmark, Finland?
    - Show your results in a histogram.

3. How many 1, 2, and 3 stars Michelin restaurants are in Sweden?
    - Show your results in a histogram.

4. Count the number of Swedish Michelin restaurant per cuisine. 
    - Show your results in a histogram

5. How many Michelin restaurants are there per cuisine?
    - Show your result in a histogram

6. Show in a map all Michelin restaurants.
    - The circle shall be colored based on the price. Use a color scale.
    - Hovering over a restaurant shall show the following information:
        - Restaurant name
        - Latitude
        - Longitude
        - Price. Represented as a number between 1 to 5.
        - Number of stars. Represented as a number between 1 to 3.

7. Consider the following price categories:
    - Plus: $ to $$
    - Premium: $$$ to $$$$
    - Premium Plus: $$$$$ and up

    7.1. How many Michelin restaurant belong to each category?
    - Show the results in a line chart. The line chart shall have 1 line per type of star. 

## Notes
1. Think on how you can create functions or classes to create a code that is reusable, modular, maintainable, and generic to work with any csv file of the same information.

## Presentation
Each student is required to make a 10 to 15 minute presentation showcasing the solution and explaining the reasons behind the design decisions regarding the code. That is, why you decided to structure the code the way you did.

The data in the CSV file is not fully cleaned. You will see inconsistancies. There is no right or wrong way of handling them. Part of the assignment is for you to handle them and during the presentation explain how you handled it and why you chose that method.

Be prepared for other students and the instructor to ask questions regarding your code.