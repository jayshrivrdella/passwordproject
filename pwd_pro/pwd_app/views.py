from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import PwdSerializer, LoginCustomSerializer
from .models import Users

import argon2
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from argon2 import PasswordHasher
import time
import random, string


# def generate_hash_for_password(password,salt_length=20, time_cost=2, memory_cost=65536 * 2,parallelism=2):
#     randu = "".join(random.choices(string.digits, k = 3))
#     hashed_password = argon2.hash_password(password.encode('utf-8'), salt = randu, time_cost = 2, memory_cost=65536, parallelism=2)
#     #ph = PasswordHasher(password = password, salt_lengthtime_cost=time_cost, memory_cost=memory_cost, parallelism=parallelism)
#     return randu, hashed_password


# Example usage
# if __name__ == "__main__":
#     password = "example_password"
#     start_time = time.time()
#     salt, hash_value = generate_hash_for_password(password)
#     end_time = time.time()
#
#     print(f"Salt: {salt.hex()}")
#     print(f"Hashed Password: {hash_value}")
#     print(f"Time taken: {round(end_time - start_time, 3) * 1000} milliseconds")

class SignUp(CreateAPIView):
    serializer_class = PwdSerializer

    def post(self, request, *args, **kwargs):
        try:
            # username = Users.objects.get(username = request.data['username'])
            randu = "".join(random.choices(string.digits, k=16)).encode('utf-8')
            #randu = 3
            pas = request.data['hashvalue'].encode('utf-8')
            hashed_password = argon2.hash_password(password=pas, salt=randu, time_cost=2, memory_cost=65536,
                                                   parallelism=2)
            serializer = PwdSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.validated_data['salt'] = randu,
                serializer.validated_data['hashvalue'] = hashed_password
                serializer.save()
                data_response = {
                    'response_code': status.HTTP_200_OK,
                    'message': "Product Created successfully",
                    'status_flag': True,
                    'status': "success",
                    'method': request.method,
                    'error_details': None,
                    'data': {'user': serializer.data}}
                return Response(data_response)
            else:
                data_response = {
                    'response_code': status.HTTP_400_BAD_REQUEST,
                    'message': "email not registered",
                    'status_flag': False,
                    'status': "Failed",
                    'error_details': None,
                    'data': []}
                return Response(data_response)
        except Exception as error:
            return Response({
                'response_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'INTERNAL_SERVER_ERROR',
                'status_flag': False,
                'status': "Failed",
                'error_details': str(error),
                'data': []})


# class Login(CreateAPIView):
#     serializer_class = LoginCustomSerializer
#
#     def post(self, request, *args, **kwargs):
#         try:
#             obj = Users.objects.get(username = request.data['username'])
#             hashval = obj.hashvalue
#             hv = request.data['hashvalue']
#             hasher = argon2.PasswordHasher()
#             hasher.verify(hashval,hv)
#             serializer = PwdSerializer(instance=obj)
#             # print("Password is correct. User authenticated.")
#             return Response({"data":serializer.data})
#         except Exception as ve:
#             # print("An error occurred during password verification:", ve)
#             return Response({"data":ve})

from argon2.exceptions import InvalidHashError

class Login(CreateAPIView):
    serializer_class = LoginCustomSerializer

    def post(self, request, *args, **kwargs):
        try:
            obj = Users.objects.get(username=request.data['username'])
            hashval = obj.hashvalue
            hv = request.data['hashvalue'].encode('utf-8')
            # password = argon2.hash_password(password=hv, salt=randu, time_cost=2, memory_cost=65536,
            #                      parallelism=2)
            hasher = argon2.PasswordHasher()
            hasher.verify(hv,hashval)
            serializer = PwdSerializer(instance=obj)
            return Response({"data": serializer.data})
        except InvalidHashError as ih_error:
            error_message = "Invalid password hash or password does not match."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Users.DoesNotExist:
            error_message = "User not found."
            return Response({"error": error_message}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ve:
            error_message = "An error occurred during password verification."
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
