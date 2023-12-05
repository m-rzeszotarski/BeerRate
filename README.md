# BeerRate

This application is designed to serve two functions: a service for users to rate beers and an e-commerce platform featuring beers brewed by myself.
I didn't want to divide the application into two separate entities, so both the beer rating and store functionalities are integrated into a single 'webpage' application.

## Packages

For this project, I utilized a few additional packages listed below:

[Package 1]
[Package 2]

## Beer Rating Classes

The primary model in the application is the **Beer** class. Any logged-in user can create a beer using a form. It includes author information, date, beer-specific variables, and a boolean **isapproved**. When a user creates a new beer in the database, it must be approved by a superuser (**isapproved** False -> True) before appearing on the **beer_list** page.

The second class is **Review**. Each user can add a review to an existing beer in the database, consisting of a user rating and a comment. Each review is linked to a specific beer through a **ForeignKey**. A superuser can ban a review (boolean **banned** False -> True). Each user can add only one review for a specific beer (details in the next section).

## Beer Rating Functions

Two important Class-Based Views are implemented: **reviews_avg**, which finds reviews for a specific beer, calculates the average user rating, and rounds the result to one decimal place, and **reviews_counter**, which counts the number of reviews for a specific beer. 

Some Function-Based Views use decorators to restrict access: **@login_required** allows access only for logged-in users, and **@user_passes_test(lambda u: u.is_superuser)** grants access only to superusers. In HTML, certain sections are hidden from non-logged-in users **{% if user.is_authenticated %}**, while others are visible only to superusers **{% if user.is_superuser %}**.

From **home.html**, users can access Beer Ranking, and superusers can view the list of beers pending approval. Approved beers are displayed in a Data Table in **beer_list.html**, allowing users to search and filter beers in the database. More details and reviews can be viewed in **beer_detail.html**, where users can also add their reviews. Only one review can be added by one user for one beer. In the **beer_detail** view, before saving a new review form, the function checks if the user has already created a review (using **objects.filter** and **.count())**. If the count is > 0, the old review is deleted, and only the new one is saved.

## E-commerce Classes

The **MyBeer** class represents items available in the shop. I opted not to inherit them with the "Beer" model to keep these classes separate due to different parameters and functions. For cart purposes, the **CartItem** class was created, where each CartItem is assigned to a specific MyBeer from the shop and a user by a **ForeignKey**. To complete a final order, the **Order** class was introduced, containing purchaser's data, products, price, and status.

## E-commerce Functions

From home.html, users can access the shop, and superusers can view a page displaying all created orders. In the shop **mybeer_list.html**, logged-in users can add beers to the cart. Superusers can also add new MyBeers using a form. In the cart **cart.html**, users can change the quantity of chosen items or remove them. The total price is calculated by multiplying the quantity of items in the cart by their price. If a user wants to make an order, they are redirected to a form where they must fill in their personal data. Cart items are found by filtering by the user. The price is calculated using the same principle as in the cart, with shipping charges added. After saving the order form, items from the cart are deleted. Several functions were created to manage the order status, which superusers can utilize from the **order_list.html** page. 

## Plans for improvement

- Add the possibility to fill in purchaser's data in the user tab; this data will be used by default in the order form.
- Include multiple shipping options.
- Integrate PayPal for payment.
- Implement a function to ban reviews (boolean is present but lacks a function for changing it).
​- Enhance access restriction and security measures.




