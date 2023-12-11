# BeerRate

This application is designed to serve two functions: a service for users to rate beers and an e-commerce platform featuring beers brewed by myself.
I didn't want to divide the application into two separate entities, so both the beer rating and store functionalities are integrated into a single 'webpage' application.

## Packages

For this project, I utilized a few additional packages listed below:
- Django - the main framework that enabled the creation of a web application.
- django_crispy_forms - the package allowing for more pleasant customization of forms.
- crispy-bootstrap4 - Bootstrap4 template pack for django-crispy-forms.
- django-paypal - package for PayPal integration in my e-commerce
- Charts.js - in fact it is not a package, but JavaScript library which I used for charts generation

## Main Classes

The primary model in the application is the **BeerMain** model. This abstrat class was created because beers in e-commerce contains some different variables than that in the rating app. **Beer** (model for rating) and **MyBeer** (model for e-commerce) are inheriting form BeerMain class. 
The second one is **Review**. This model was created to allow users to rate and review beers. Review can apply to **Beer** and **MyBeer** so I decided to use **GenericForeignKey** which allows to assign beer reviews depending on its model (**ContentType**) and number in the database (**PrimaryKey**). A superuser can ban a review (boolean **banned** False -> True). Each user can add only one review for a specific beer (details in the Review Functions section).

## Main Views

Class-Based Views are implemented in **BeerMain**: 
- **reviews_avg(self, value)**, which finds users reviews for a specific beer (by **ContentType** and **pk**), calculates the average of **value** (it can be a users score, hop, malt, roast etc.), and rounds the result to one decimal place. Later this function is used to present average of users rating of beer's parameters on a chart in **beer_detail.html** and **mybeer_detail.html**
- **reviews_counter(self)**, which counts the number of reviews for a specific beer.

Function-Based Views:
detail
handle review

## Beer Rating Classes

For Beer Rating model the **Beer** class was created inheriting from **BeerMain** abstract class. Any logged-in user can create a "beer" using a form. It includes author information, date, beer-specific variables, and a boolean **isapproved**. When a user creates a new beer in the database, it must be approved by a superuser (**isapproved**: False -> True) before appearing on the **beer_list** page.

## Beer Rating Views

Some Function-Based Views use decorators to restrict access: **@login_required** allows access only for logged-in users, and **@user_passes_test(lambda u: u.is_superuser)** grants access only to superusers. In HTML, certain sections are hidden from non-logged-in users **{% if user.is_authenticated %}**, while others are visible only to superusers **{% if user.is_superuser %}**.

From **home.html**, users can access Beer Ranking, and superusers can view the list of beers pending approval. Approved beers are displayed in a Data Table in **beer_list.html**, allowing users to search and filter beers in the database. More details and reviews can be viewed in **beer_detail.html**, where users can also add their reviews. Also on this page a chart is displayed, created in Charts.js, which displays average user ratings on beer parameters.

## E-commerce Classes

The **MyBeer** class represents items available in the shop (it is also inheriting from **BeerMain** abstract class). For cart purposes, the **CartItem** class was created, where each CartItem is assigned to a specific MyBeer from the shop and a user by a **ForeignKey**. To complete a final order, the **Order** class was introduced, containing purchaser's data, products, price, and status.

## E-commerce Functions

From **home.html**, users can access the shop **mybeer_list.html**, and superusers can view a page displaying all created orders **order_list** (and change their status using dedicated function). In the shop **mybeer_list.html**, logged-in users can add beers to the cart. Superusers can also add new MyBeers using a form. In the cart **cart.html**, users can change the quantity of chosen items or remove them. The total price is calculated by multiplying the quantity of items in the cart by their price. If a user wants to make an order, they are redirected to a form where they must fill in their personal data. Products in cart are found by filtering CartItems by the user. The order price is calculated using the same principle as in the cart, but also shipping charges are added. After saving the order form, items from the cart are deleted and user is rediracted to the PayPal page. 

## Plans for improvement

- Add the possibility to fill in purchaser's data in the user tab; this data will be used by default in the order form.
- Include multiple shipping options.
- Implement a function to ban reviews (boolean is present but lacks a function for changing it).
- Remove autoscale from charts and make y in range 0 - 10
​- Enhance access restriction and security measures.
- Modify page: mybeer_list, mybeer_detail




