# Reddit E-Juice Flavor Lookup Bot

> Post links to flavors mentioned in posts.

Fetches and links to flavor information from [E-Liquid Recipes](http://e-liquid-recipes.com/) and [All the Flavors](http://alltheflavors.com/).

## Setup
In order to access the Reddit API, client_id, client_secret and a refresh token is needed.
This has to happen in multiple steps:

* Enable dev account for your bot user, this will give you client_id and client_secret
* Set redirect URI to http://localhost:65010/authorize_callback
* Use the [reddit-oauth-helper](https://github.com/not-an-aardvark/reddit-oauth-helper) to obtain your **permanent** refresh token, select the following scopes: *identity*, *read* and *submit*
* Configure *praw.ini* with **client_id**, **client_secret** and **refresh_token** from above.

Your *praw.ini* should look something like so:
```
[flavor_bot]
client_id: cxxxGxxxiiiiuQ
client_secret: 5HJoC5-QXwuZBPT1Kh0a4o3Pb9c
refresh_token: 18729753-lyp_xe5oOdAHzVvzKWpH7sF2sNg
```

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
