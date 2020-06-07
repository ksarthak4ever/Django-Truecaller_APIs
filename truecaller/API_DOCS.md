# Accounts API docs

## 1. Register endpoint.

### URL:

```
http://localhost:8000/account/register/
```

### Parameters:

- Method: POST
- headers:

```
{
    Content-type: application/json
}
```

### Sample payload:

```
{
	"name":"Sarthak Kumar",
	"phone_number": "7754938370",
	"password": "testing123",
	"email": "kumarsarthak800@gmail.com"
}
```

### Sample response:

- Status code: 201

Data:

```
{
    "id": 1,
    "u_id": "380c7321-59e2-4262-85f7-337127ece1d8",
    "name": "Sarthak Kumar",
    "phone_number": "7754938370",
    "email": "kumarsarthak800@gmail.com",
    "spam_count": 0,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTk2Njg3OTk5fQ.wi6YRigds4DdtArZt5MtB0GWu1rSdg9sW-LBzvOKf2Q"
}
```

## 2. Login endpoint.

### URL:

```
http://localhost:8000/account/login/
```

### Parameters:

- Method: POST
- headers:

```
{
    Content-type: application/json
}
```

### Sample payload:

```
{
	"phone_number": "7754938370",
	"password": "testing123"
}
```

### Sample response:

```
{
    "id_": 1,
    "u_id": "380c7321-59e2-4262-85f7-337127ece1d8",
    "name": "Sarthak Kumar",
    "phone_number": "7754938370",
    "email": "kumarsarthak800@gmail.com",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTk2Njg4MTMxfQ.zzArFwDSZAeHa0PQ_fNYqYEMe3MMDAMmVVZDjaqagPQ"
}
```

`Note` :~ As phone number is a unique field for a user so i am using that for registering and logging in a user. I have also implemented JWT Authentication for security purposes so the above recieved token should be set in the request headers for all the other APIs as no other API can be accessed without authentication.


# Contacts API docs.

## 3. Set Spam Endpoint

### URL:

```
http://localhost:8000/contact/spam/
```

### Parameters:

- Method: POST
- headers:

```
{
    Content-type: application/json
}
{
	Authorization: Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTk2Njg4MTMxfQ.zzArFwDSZAeHa0PQ_fNYqYEMe3MMDAMmVVZDjaqagPQ
}
```

### Sample payload:

```
{
	"phone_number": "7754938371"
}
```

### Sample response:

status code: 200

Data:

```
{
    "id": 1,
    "name": "",
    "phone_number": "7754938371",
    "spam_count": 3
}
```

`Note` :~ This API is used to report a number as spam by a user. The reported number can belong to anyone for example another registered user, a contact or just a random number. A user should not be allowed to report themself as spam. We are using an integer counter like Truecaller to keep track of how many times a number has been reported. In case a random number is reported, we are saving the number in our database as a contact object with no name and a spam counter of 1.


## 4. Searching a person endpoint

### URL:

```
http://localhost:8000/contact/search/
```

### Parameters:

- Method: GET
- headers:

```
{
    Content-type: application/json
}
{
	Authorization: Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTk2Njg4MTMxfQ.zzArFwDSZAeHa0PQ_fNYqYEMe3MMDAMmVVZDjaqagPQ
}
```

### Sample payload:

```
Query Params :~ name or phone_number
for example :~
http://localhost:8000/contact/search/?phone_number=7754938370
or 
http://localhost:8000/contact/search/?name=Kumar
```

### Sample response:

status code: 200

Data:

```
{
    "id": 1,
    "name": "Sarthak Kumar",
    "phone_number": "7754938370",
    "spam_count": 0
}
```

`Note` :~ This API is used to search a person in the global database of the app. All the search related functionalities are covered by this app. I created small helper functions to reduce the size of the actual api and make it a bit modularised.


## 5. Fetching Details.

### URL:

```
http://localhost:8000/contact/detail/6/
```

### Parameters:

- Method: GET
- headers:

```
{
    Content-type: application/json
}
{
	Authorization: Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTk2Njg4MTMxfQ.zzArFwDSZAeHa0PQ_fNYqYEMe3MMDAMmVVZDjaqagPQ
}
```

### Sample Response:

status code: 200

Data:

```
{
    "id": 6,
    "name": "Shelby Ballard",
    "phone_number": "+1(824)467-3579",
    "spam_count": 0
}
```

`Note` :~ This API is used to fetch the details of a specific user or contact i.e name, email, phone number and even the spam count.


