## BeerRate

This application is intended to fulfill two functions: a service for users to rate beers and an e-commerce.
I didn't want to divide this application into two, so both the beer rating part and the store part are included in one 'webpage' application.

# Packages

For this project I used few additional packages

# Beer Rating Classes

The "Beer" class is the main model in the application. Any logged-in user can create it by a form. It has author, date, beer-specific variables and a boolean "isapproved".
When user creates a new beer in database it must be approved by superuser ("isapproved" False -> True), before it will be shown in "beer_list" page.

The second class is the "Review". Each user can add it to the existing Beer in the database (it consist of an user rating and a comment). Each review is assigned to specific beer by foreign key. Review can be banned by superuser (boolean "banned" False -> True).
One user can add only one review of specific beer (it is described in the next section). 

# Beer Rating Functions

There are two important Class Based Views. reviews_avg which finds reviews for specific beer, calculates average of users rating and rounds the result up to one decimal place. The second one is reviews_counter which counts number of review for specific beer. 

For some of function based views I used decorators to restrict access: @login_required - access only for logged-in users, @user_passes_test(lambda u: u.is_superuser) - access only for superuser. 
In html some sections are hidden from not logged-in users {% if user.is_authenticated %}, some sections are shown only for superuser {% if user.is_superuser %}.

From home.html useres can access Beer Ranking, superuser also can access list of beers pending for approval.
Approved Beers are displayed in Data Table in beer_list.html. It enables to search and filter beers existing in the database. More details and reviews can be displayed in beer_detail.html where users can also add their reviews.




