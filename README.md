# microblog
It it a microblog developed using flask. I have depoyed it on Heroku, and you can go to https://flask-microblog-napchat.herokuapp.com/ and have a try :)

to-do list:
-----------
- use setuptools to configurate app.
- Using Blueprint features to reconstruct.
- Add OAuth authentication.
- Add user/password anthentication system.
- add one more many-to-many self-referential relationship to implement the block feature hidding the posts of users from users he have blocked.
- add feature of grouping your followed users.
- every posts have its own page. And you can edit them.
- edit posts.

extensions:
-----------------------
1. Flask-WhooshAlchemy: It integrates a Whoosh database with Flask_SQLAlchemy models, we use the extension to implement our text searching.
2. Flask-WTF: Forms
3. Flask-Login: Login system
4. Flask-OpenID: OpenID server
5. sqlalchemy-migrate: database migration 
6. Flask-Babel: l18n and L10n, to translate application into different language
7. coverage: a test coverage tool can observe a running applicaiton and take note of which lines of code execute and which do not.
8. guess-language: for client-server translating function
9. Flask-Mail: mail server.
10. Flask-SQLAlchemy: our database management.
11. flipflop:
12. flask_profiler: for profiling.
