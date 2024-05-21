# BeerRate

This application is designed to serve two functions: an e-commerce platform featuring beers brewed by myself and a service for users to rate beers.
I didn't want to divide the application into two separate entities, so both the store and the beer rating functionalities are integrated into a single 'webpage' application.
The webpage might look a bit old and raw, but I chose not to use any ready-made Bootstrap templates or similar options.

## Packages

Several additional packages were utilized for this project:

- Django: The primary framework enabling the creation of the web application.
- django_crispy_forms: A package facilitating pleasant customization of forms.
- crispy-bootstrap4: Bootstrap4 template pack for django-crispy-forms.
- django-paypal: A package for PayPal integration in the e-commerce section.
- Charts.js: not a package, but worth highlighting JavaScript library used for charts generation

## Main Classes

The primary model in the application is the **BeerMain** model. This abstrat class was created as beers in the e-commerce section have different variables compared to the rating app. **Beer** (model for rating) and **MyBeer** (model for my beers in e-commerce) are inheriting form BeerMain class. 
The second crucial class is **Review**, created to enable users to rate and review beers. Reviews can be applied to both **Beer** and **MyBeer** models, and a **GenericForeignKey** is used to assign reviews based on the model (**ContentType**) and database position (**PrimaryKey**). Superusers have the ability to ban a review by toggling the **banned** boolean (False to True). Each user is restricted to adding only one review per beer (the function checks whether the review was created by a given user for a given object).

## Main Views

Class-Based Views implemented in **BeerMain**: 
- **reviews_avg(self, value)**: This view finds users reviews for a given beer (by **ContentType** and **pk**), calculates the average of **value** (which can represent a user's score, hop, malt, roast, etc.), and rounds the result to one decimal place. This average is then used to present the users' average rating of beer parameters on a chart in **beer_detail.html** and **mybeer_detail.html**.
- **reviews_counter(self)**: This function counts the number of reviews for a specific beer.

Function-Based Views:
- **def detail(request, model, template_name, pk)**: This view supports two models (**Beer** and **MyBeer**) and is called by two different views: **def beer_detail** or **def mybeer_detail** (depending where it is used). It returns a two lists that are utilized for chart creation, reviews of selected beer and a form for review creation.
- **def object_remove(request, model, template_name, pk)**: This view is used to handle removing instances of: Beer, MyBeer, CartItem and Order (this two classes will be explained later). It gets an object depending on its model and pk, and deletes it. If the object is a Beer or MyBeer, it also removes all associated reviews.
- **def handle_review_ban(request, review, is_banned)** - this view is used to handle banning a comments and it is called by **def review_ban(request, pk)** or **def review_unban(request, pk)** (depending on the superuser's intent).

## Beer Rating Classes

For Beer Rating model the **Beer** class was created inheriting from **BeerMain** abstract class. Any logged-in user can create a "beer" using a form. It includes author information, date, beer-specific variables, and a boolean **isapproved**. When a user creates a new beer in the database, it must be approved by a superuser by toggling the **isapproved** boolean (False to True) before appearing on the **beer_list** page.

## Beer Rating Views

Some Function-Based Views use decorators to restrict access: **@login_required**  permits access exclusively for logged-in users, and **@user_passes_test(lambda u: u.is_superuser)** grants access only to superusers. In HTML, certain sections are hidden from non-logged-in users **{% if user.is_authenticated %}**, while others are visible only to superusers **{% if user.is_superuser %}**.

From **home.html**, users can access Beer Ranking, and superusers can view the list of beers pending approval. Approved beers are displayed in a Data Table in **beer_list.html**, allowing users to search and filter beers in the database. More details and reviews can be viewed in **beer_detail.html**, where users can also add their reviews. Additionally, a chart generated by Charts.js is displayed on this page, illustrating the average user ratings for various beer parameters.

## E-commerce Classes

The **MyBeer** class represents items available in the shop (it is also inheriting from **BeerMain** abstract class). For cart purposes, the **CartItem** class was created, where each CartItem is assigned to a specific MyBeer from the shop and a user by a **ForeignKey**. To complete a final order, the **Order** class was introduced, containing purchaser's data, products, price, and status.

## E-commerce Views

From **home.html**, users can access the shop **mybeer_list.html**, and superusers can view a page displaying all created orders **order_list** (and change their status using dedicated function). In the shop **mybeer_list.html**, logged-in users can add beers to the cart. Superusers can also add new MyBeers using a form. In the cart **cart.html**, users can change the quantity of chosen items or remove them. The total price is calculated by multiplying the quantity of items in the cart by their price.  If a user wishes to place an order, they are redirected to a form where they provide their personal data. The products in the cart are identified by filtering CartItems associated with the user. TThe order price follows the same principle as in the cart, with shipping charges added. After saving the order form, items from the cart are deleted and user is rediracted to the PayPal page. 




