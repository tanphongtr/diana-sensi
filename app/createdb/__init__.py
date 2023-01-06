import os
from app.models import User
# from django.contrib.auth.models import User

try:
    superuser = User.objects.create_superuser(
        username= os.getenv('APP_ROOT_USER', 'root'),
        email= os.getenv('APP_ROOT_EMAIL', ''),
        password=os.getenv('APP_ROOT_PASSWORD', 'root@123')
    )
    print(f"Super User with username `{os.getenv('APP_ROOT_USER', 'root')}` and password `{os.getenv('APP_ROOT_PASSWORD', 'root@123')}`")
    superuser.save()
except:
    print(f"Super User with username `{os.getenv('APP_ROOT_USER', 'root')}` is already present")


class CreateDb:
    def run():
        print(12312)