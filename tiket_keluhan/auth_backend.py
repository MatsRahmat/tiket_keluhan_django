from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from tiket_keluhan.models import CustomUserModel

class DualLogin(BaseBackend):
    
    def authenticate(self, request, login_id, user_id=None,password=None):
        print("Masuk ke sinii cuy, custom backend")
        if login_id:
            if user_id:
                # Login Nasabah
                try:
                    user = CustomUserModel.objects.get(user_id=user_id, login_id=login_id)
                    return user
                except CustomUserModel.DoesNotExist as ex:
                    print("Nasabah not found")
                except Exception as e:
                    print(e)    
                return None
            elif password:
                # Login reguler untuk operator, staff dan direktur
                try:
                    user = CustomUserModel.objects.get(login_id=login_id)
                    if user and check_password(password, user.password):
                        return user
                except CustomUserModel.DoesNotExist as ex:
                    print("User not found")
                except Exception as e:
                    print(e)
                return None
            
        return None
    
    def get_user(self, user_id):
        try:
            return CustomUserModel.objects.get(pk=user_id)
        except CustomUserModel.DoesNotExist:
            print("User Not found")
            return None