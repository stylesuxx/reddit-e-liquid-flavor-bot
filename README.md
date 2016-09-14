# Reddit E-Juice Flavor Lookup Bot

> Post links to flavors mentioned in posts.

Fetches and links to flavor information from [E-Liquid Recipes](http://e-liquid-recipes.com/) and [All the Flavors](http://alltheflavors.com/).

## Setup
In order to access the Reddit API, client_id, client_secret and a refresh token is needed.
This has to happen in multiple steps:

* Enable dev account for your bot user, this will give you client_id and client_secret
* Configure *praw.ini* with **client_id** and **client_secret** from above. Also set **redirect_uri** - this can be anything like *http://127.0.0.1:12345/redirect*
* Run the OAuth helper to generate a URL to grants permissions and generates the **refresh_token**
* Add the **refresh_token** to *praw.ini*

## Usage
To use, post a flavor name like so: [[ Flavor Name by Business Short Name ]] or [[ Flavor Name ]]

Some examples:
```
* [[Strawberry Ripe by TPA]]  
* [[ Strawberry (Ripe)]]  
* [[ Banana Ripe by TPA ]]  
* [[   Koolada 10% by TPA]]  
* [[Pinkman  ]]  
* [[   Lime Tahity Cold Pressed by FA   ]]  
* [[ Wiener Schnitzel ]]  
* [[ Cheesecake Graham Crust by TPA ]]  
* [[ Butter by FA ]]   
* [[ Cookie by FA ]]  
* [[ Banana Cream by LA ]]  
* [[ Bing Cherry ]]  
* [[ Red Touch (Strawberry) by FA ]]  
* [[ Cookie by FA ]]  
* [[ Whipped Cream by FA ]]  
* [[ Vienna Cream by FA ]]  
* [[ Vanilla Cupcake by CAP ]]  
* [[ Butter by FA ]]
```
