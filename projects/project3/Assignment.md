# Tasks

## Background
For this assignment we will practice using APIs, downloading data from the internet, and visualizing such a data.

The API we will use in this assignment is about countries: `https://restcountries.com/#api-endpoints-v3`

Few things to keep in mind when working on this assignment:
- Remember the importance of reading the API's documentation.
- We will use version 3.1 of the API.

## Part 1: Data Analysis only
The purpose of this section is to analyze data, no need to create visualization. 

1. Create a class called `Currency` which has the following properties:
    - `name` of type `String`
    - `code` of type `String`

2. Create an `enum` class called `Region` which has the following properties:
    - `Africa`
    - `Americas`
    - `Asia`
    - `Europe`
    - `Oceania`

3. Create an `enum` class called `Direction` which contains the following values:
    - `Left`
    - `Right`

4. Create a class called `Language` which contains the following properties:
    - `name`
    - `code`

5. Create a class called `Country` which contains the following properties:
    - `official_name` of type `String`
    - `common_name` of type `String`
    - `capital` of type `String`
    - `region` of type `Region`
    - `area` of type `Float`
    - `population` of type `Float`
    - `languages` of type `List<Language>`
    - `currencies` of type `List<Currency>`
    - `driving_direction` of type `Direction`
    - `land_locked` of type `Boolean`
    - `un_member` of type `Boolean`

    Notes:
    - `Currency` is the type you downloaded in Step #1.
    - `Direction`, `Language`, and `Region` are the classes you created in steps 2, 3, and 4.

6. To the class `Country` add a function called `countries` which has no arguments and performs and API request to obtain the list of all countries. The function shall return a `List<Country>`.

7. To the class `Country` add a function called `countries_per_region` which has one argument of type `Region`. The function shall perform an API request and return a `List<Country>` with all the countries in the provided region.

8. To the class `Country` add a function named `country_for_name` which has one argument called `name` of type `String`. The fuction shall perform an API request to return a `Country` object with all the information of the provided country name.

9. To the class `Country` add a function called `countries_for_language` which has one argument called `language_name` of type `String`. The function shall perform an API request and returns all the countries that speak the provided language.

## Part 2: Data Visualization
The purpose of this section is to use the code and fuctions perviously created to create the following visualizations.

1. Create a histogram showing the number of countries per region.

2. Create a histogram showing the 15 countries with the largest population.

3. Create a histogram showing the number of countries that drive in the right and left direction.

4. Create a histogram showing the number of countries that belong to the UN.

5. Create a histogram showing the number of countries that have English, Spanish, Italian, French, German, and Swedish as their primary language.

6. Create a histogram showing the top 20 most used currencies.