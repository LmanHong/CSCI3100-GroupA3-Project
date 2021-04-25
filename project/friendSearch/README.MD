# FriendSearch
This folder contains files for friendSearch(sending request to user) and friendMatching(accepting request) module of the CUHK Tinder.

#### Models
1. `FriendList` **To maintain the relation between two users**, if A want to make a friend to B, two rows will be formed and stored to this models, i.e. A->B->acp and B->A->acp

2. `Request` **To store the request send by the user**, the user can view the requests sent by other user.

Please refer to 'models.py' for the search queries, the queries to make request, accept request.

#### views
1. `FriendSearchView` **The user can view the criteria for searching an ideal user, after input these criteria and click "Search", the users that not a friend of him or fulfill all criteria will be displayed**
2. `RequestView` **To view the requests sent by other users, and choose if the user accepts them**

Please refer to 'view.py' for the information of the view.
