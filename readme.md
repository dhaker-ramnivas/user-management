Run this project and use postman for api test make sure you enter correct detail in setting for email to sent link on email

##How To Run project:
## SIMPLE USER MANAGEMENT

### Setup Local environment

#### Python 
Install python 3

```
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
```

##### Run command
 ```$ python manage.py makemigrations
    $ python manage.py migrate
    $  python manage.py  loaddata Assignment/fixtures/initial_data.json 


```



### Sample Output

######## POST API: 
/user/register/

	INPUT:
		{
	
			"username":"ramnivas32",
			"email":"ramnivas32@gmail.com",
			"password":123456
		}
	
	OUTPUT:
		{
    			"status": true,
  			  "user": {
  			    	  "message": "go to email and verify link",
  			     	 "email": "ramnivas32@gmail.com",
    			     	 "username": "ramnivas32"
  				  }
		}
	If user already register then
	
	OUTPUT:
		{
   			 "status": false,
   			 "Error": "Email Id already Exist"
		}
	

######## GET API:
http://127.0.0.1:8000/user/login/?Content-Type=application/json&email=ramnivas@gmail.com&password=123456

OUTPUT:
	{
    "message": "Successfully logged in",
    "status": true,
    "user": {
        "email": "ramnivas@gmail.com",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1Njk3OTM2NzMsImVtYWlsIjoicmFtbml2YXNAZ21haWwuY29tIiwidXNlcm5hbWUiOiJyYW1uaXZhcyIsInVzZXJfaWQiOjJ9.e_4DNqZmASdmO9Sdf5IUk5h6ToIo5JH2-N4rnW3xcT8",
        "username": "ramnivas"
    }
}

OR 

OUTPUT:
	{
    "status": false,
    "data": {},
    "Error": "User not found"
}

OR
{
    "Error": "Password is Incorrect ",
    "status": false,
    "data": {
        "Content-Type": "application/json",
        "password": "1234565",
        "email": "ramnivas@gmail.com"
    }
}


##### Account ACTIVATE

get from email this type of link

###############http://127.0.0.1:8000/user/activate/?token=Bearer%20eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImthYmVAYmk2ZzRmMnR1YmUuY29tIiwidXNlcl9pZCI6NywidXNlcm5hbWUiOiJyYW02Z252ZjRpYXMxIiwiZXhwIjoxNTY5ODM4MzczfQ.n7gk3JmwOeNIAJ4ptMNLoymqHkolfDUNvL_2oSbTvGE


###########
#################### responce:



{
    "message": "Account Activated,please login with email",
    "status": true
}



OR


If already activated then

{
    "message": "please login with email",
    "status": false
}



########### Write Data

http://127.0.0.1:8000/user/content-post/?token=Bearer%20eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImthYmVAYmk2ZzRmMnR1YmUuY29tIiwidXNlcl9pZCI6NywidXNlcm5hbWUiOiJyYW02Z252ZjRpYXMxIiwiZXhwIjoxNTY5ODM4MzczfQ.n7gk3JmwOeNIAJ4ptMNLoymqHkolfDUNvL_2oSbTvGE

#################### Responce
{
    "message": "Successfully written data ",
    "status": true
}




######### Retrive API

http://127.0.0.1:8000/user/content-get/?token=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo4LCJ1c2VybmFtZSI6ImFudWoiLCJleHAiOjE1Njk4MzkxMzAsImVtYWlsIjoiYW51akBnbWFpbC5jb20ifQ.aLT8OdoyxrQ6fHC89DikovGiSiMyue2r_C_jegae-0Y

Responce:
{
    "status": true,
    "data": [
        {
            "text": "hiiiisdfdsfdfiiiiiii",
            "author": "anuj"
        },
        {
            "text": "hiiiiiiiiiii",
            "author": "vishal"
        },
        {
            "text": "hiiiisdfdsfdfiiiiiii",
            "author": "vishal"
        }
    ]
}


bydefault in accending order by user

to descending add in token 
&is_acccending=0

http://127.0.0.1:8000/user/content-get/?token=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo4LCJ1c2VybmFtZSI6ImFudWoiLCJleHAiOjE1Njk4MzkxMzAsImVtYWlsIjoiYW51akBnbWFpbC5jb20ifQ.aLT8OdoyxrQ6fHC89DikovGiSiMyue2r_C_jegae-0Y&is_accending=0

responce

 {
    "status": true,
    "data": [
        {
            "text": "hiiiiiiiiiii",
            "author": "vishal"
        },
        {
            "text": "hiiiisdfdsfdfiiiiiii",
            "author": "vishal"
        },
        {
            "text": "hiiiisdfdsfdfiiiiiii",
            "author": "anuj"
        }
    ]
}
