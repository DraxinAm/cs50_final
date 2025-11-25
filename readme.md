# RIZZCIPES
### Video Demo:
### Description:
#### The reason behind the project:
For my final project I decided to strengthen the muscles I grew from the Week 9 Finance exercise, therefore, I wanted to create a webpage that uses multiple languages. Instead of stocks I chose something that is closer to my heart, which is cooking and baking, thus I created a recipe logging site that lets you surf the community recipes.

The site works on a few basic premises:
- you can create your own recipes by filling out a form that stores your data in various SQL tables
- you can search for recipes that you or others using the site has created
- and you can favourite recipes into your own cookbook to make finding them easier.

I wanted the page to have a homey and comforting feel, so I chose the colours and fonts accordingly.

To start of, I built the basics of a webpage structure, for this I leaned heavily on the Finance problem and borrowed various functions and ideas, commenting it, when I did so. To learn a bit more I decided to use sqlite3 without the cs50 library, therefore I made a separate database.py file, where I stored the functions that communicated with the database for this project (recipes.db).

After i was finished with that I made the site be dependent upon creating a user, since many subpages require a user_id to specify the results. I made a register, a login and a logout page for this. I stored the user data in the users table, also used hashing from the werkzeug library.

Continuing on, I decided to turn towards creating the recipes. The form I put together was made with the other subpages in mind, so I separated the tags, ingredients and steps into different tables from the main one that stored the recipe infos:
- id
- user_id
- title
- description
- servings
- cook_time
- and finally created_at

I wished to store the time the recipe was created at, to make the home page show the latest recipes the user has made. Talking about the homepage, I wish to introduce the subpages in a bit more detail.

1. *Homepage* : As I have mentioned before, I made the webpage, so when the user has logged in, the first thing they see is their own recipes that they have created previously! These recipes appear in the form of Bootstrap cards, so when the user clicks on the button at the bottom of the card ("Go to details") they get to a recipe.html that asks for the specific recipe data from the database and fills out the form to present to the user.

2. *Create* : For the create a used tables, for a separate header, the quick infos I stored in the recipes table. Bellow that I implement a select tool, to search and choose from tags that represent different diets and so the user can assign them at least one, but max three tags. After that probably the biggest table of the site is the ingredient one, where the user can add at max 15 ingredients, parsing the unit of measure, the amount and the name of the ingredient. This is because in the future, if I want to develop my site further, I wanted to handle these datas separately.

3. *Search* : As the user, you can search based on the title of the recipe OR on the diet tags. For the title search, I used the LIKE operator in the sql query as opposed to fuzzy search to be effective. Either way you get to see the list part of the search, with the options appearing as cards, just like on the homepage. Once you click on the card you chose, you get to the full recipe page just like from the Homepage.

4. *Cookbook* : Finally, to find previous liked recipes faster, the user can favourite recipes on the full recipe page, which will be stored in a separate table as well. Once the user clicks one the Cookbook hyperlink on the navbar, they get to see a card collection, not unlike after a search or the Homepage.

My project uses Flask and instead of requirements.txt, uses uv to keep track of such details. Once the user wants to achieve something that the logic permits, or if they decide to remove the front-end blocks, they get to see the problem page, where the page will describe what went wrong.

On the files that I created and used:
In the database folder I stored all the files that has to do with the database (database itself as db, the database python class with the functions for interacting with the db, the init_databse, which initialises the database and the schema in an SQL file). In the static I stored the styles.css for formatting the webpage, in the templates I stored all the html files I made and use for the site. Outside I have the app.py with the routes and the README. One file that I have not mentioned before is the login.py. This houses my login function (which is quite similar to the finance problem from CS50x) and the problem function, which describes what went wrong to the user.

As opposed to the previous exercises, we could use AI to work on our final project. In this webpage, I mainly utilised it during the styling and formatting, to save my energies for the back-end part of the project, which interests me the most. I also used it occasionally to debug files, when I had no other idea and specifically told it, not to give me the solution, just the reason. Furthermore, I used external sites, but linked them accordingly.

All in all, I am excited about my final project and enthusiastic to work on it some more, once my knowledge and skills have grown!

(PS. One thing I would like to add in the future is a JavaScript empowered button that resides on the create.hmtl page, which if clicked, adds an additional row to the ingredients and steps part of the page, to make it more agile!)