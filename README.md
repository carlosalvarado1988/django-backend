# Django Backend

Django official documentation:
https://www.django-rest-framework.org/

course video: https://www.youtube.com/watch?v=c708Nf0cHrs
course time: 2:04min

## Setup the local env

create a virtual environment

> python3.11 -m venv venv
> source venv/bin/activate

add file requirements.txt with the following info:

> django>=4.00,<4.1.0
> djangorestframework
> pyyaml
> requests
> django-cors-headers

then run the following commands to install the dependencies

> pip install -r requirements.txt
> pip install --upgrade pip

create two folders: backend and client.
navigate to backend folder and run the following command to install the framework

> django admin startproject cfehome .

## Run the local env

run the server

> source venv/bin/activate
> cd backend/
> python3 manage.py runserver 8000

run a client file:

> python3 client/details.py

## Session Authentication && Permissions

## Views as an REST API

We import libs from the framework
from rest_framework import generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

these generic views, function based view or the mixins allow to create class methods that automate a lot of the work for a REST API, it handes status codes, updates to database, args handling, permissions and more.

### Permissions

Generics views can use permission classes.
from rest_framework import permissions
https://docs.djangoproject.com/en/4.2/topics/auth/default/

## Authentication

we need to create a super user
navigate to the backend folder.

> python3 backend/manage.py createsuperuser

for this project, it is left as: carlosalvarado
for testing purposes, password is 1234
navigate to admin panel:

> localhost:8000/admin/

creating another user named: staff, with password sept2023

Custom Models can be added to the admin view, go to admin.py inside the model folder Product:
add this line:

> from .models import Product
> admin.site.register(Product)

then special permissins need to be given to each user to do things with the modules
http://localhost:8000/admin/
![admin pannel - add permission](image.png)

when Login, i have a session that is read by the API viewer.
http://localhost:8000/api/products/
it can create registers at the bottom

in the admin, you can also create a group for special permission, eg:
![Alt text](image-1.png)

Then it can be added to a specific user:
![Alt text](image-2.png)

so there are two level of permission, at the user itself, or at a group.

### Custom permissions

We create the file. permissions.py inside the models folder, in this case products.
we create the class: IsStaffEditorPermission
inside it we def a method: has_permission

> def has_permission(self, request, view):
> user = request.user
> print('into IsStaffEditorPermission')
> print(user.get_all_permissions())
> if user.is_staff:
> if user.has_perm("products.view_product"):
> return True
> return False
> return False

note: on the built in admin tool, permissions can be tested, you can access different tables or data, and test different actions as only see, edit, create or delete.

### Token authentication

we need to add a built-in module from rest_framework, the authtoken.
into the cfehome directory, look for settings, look for the array of INSTALLED_APPS, and add:

> INSTALLED_APPS = [
>
> > ..,
> > 'rest_framework.authtoken',
> > ...
> > ]

then make sure to run migrations.

> python3 backend/manage.py migrate

now i got a tokens table.
![Alt text](image-3.png)

then adding, a rest api to get the tokem, inside api urls.py

> from rest_framework.authtoken.views import obtain_auth_token
> .. and the urlspatters:
> path('auth/', obtain_auth_token)

Lastly, in the products views, we need to add the atuthentication method for auth.

> authentication_classes = [
>
> > authentication.SessionAuthentication,
> > authentication.TokenAuthentication
> > ]

then, the client needs to change the wait is making its calls to the api.
eg. client/list.py
first get the token and then add it as a hearder.

> endopoint = "http://localhost:8000/api/products/"

    token = get_auth_token_response.json()['token']
    headers = {
        "Authorization": f"Token {token}"
    }

Note. Django authentication works with 'Token' authorization, if we want to use Bearer, we need to modify a bit (override) the exitsint.
so e add a authorization.py file in the API directory.

in authorization.py

> from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
> class TokenAuthentication(BaseTokenAuth)
> keyword = 'Bearer'

then we add our custom method to override the authentication method in views.py of products module.

## A default pattern to reuse auth models.

so far we have built specefic use cases for our product model. how about reusing some in different new modules?
we refer to their documentation: https://www.django-rest-framework.org/#installation:~:text=DEFAULT_PERMISSION_CLASSES

> 'DEFAULT_PERMISSION_CLASSES': [
> > 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
> >'WE REFER TO THE PATH'
> >]
