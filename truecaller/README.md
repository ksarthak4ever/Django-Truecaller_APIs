## Objective

This aim of this project was to make REST Api's which are to be consumed by a mobile app like Truecaller. The APIs cover the authentication, complex search and spam functionality of an app like Truecalller.

## Setup the project

1. I have used Pipenv as the virtualenv, so i recommend using that and installing all the dependencies using `pipenv install` and then logging into the environment shell using `pipenv shell`

2. Migrate the database using `python manage.py migrate`. Here i am using the default django database i.e SQLite but for production i would recommend using PostgreSQL as the database.

3. I have created a small management command to setup the database with sample data stored in the `sample_data.json` file in the current working directory. You can update the sample data i.e change the user details to whatever suits you best for testing or can use the same sample data. To populate the database enter the migration command 

```
python manage.py populate_sample_data
```

4. Once the database have been setup, one can start the server using `python manage.py runserver` and begin testing the APIs, there are two APIs in the accounts app which are `UserRegister` and `UserLogin` APIs respectively for registering and logging in a user. There are also three APIs in the contacts app which are `SetSpamContact`, `ContactSearch` and `UserDetailProfileView` respectively for setting a number as spam, searching a person based on name or number or search query etc. and fetch the details of a search result along with the spam likelihood.

5. I would recommend using Postman or any similar tool for testing the APIs and as i'm using JWT as the authentication for security purposes, one must note to add the token into the header of the request as all the contacts APIs require authentication.

6. I have documented sample request/responses of all the APIs in the API_DOCS markdown file. 