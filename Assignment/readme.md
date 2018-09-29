Sample Output

POST API: 
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
	

GET API:
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


