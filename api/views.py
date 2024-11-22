from pymongo import MongoClient
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserSerializer
from datetime import datetime, date

# Initialize MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client.user_management_db  # Database
users_collection = db.users  # Collection

class UserListCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            # Check for duplicate email or phone number
            existing_user = users_collection.find_one({"email": data['email']})
            if existing_user:
                return Response({"message": "User with this email already exists", "status": 400})

            existing_phone = users_collection.find_one({"phone_number": data['phone_number']})
            if existing_phone:
                return Response({"message": "User with this phone number already exists", "status": 400})
            
            # Convert `dob` from datetime.date to datetime.datetime if it's a date object
            if 'dob' in data and isinstance(data['dob'], date):
                data['dob'] = datetime.combine(data['dob'], datetime.min.time())
            
            data['user_id'] = str(uuid.uuid4())

            # Insert into MongoDB
            users_collection.insert_one(data)
            return Response({"message": "User created successfully", "user_id": data['user_id'], "status": 201})
        return Response({"message": serializer.errors, "status": 400})


class UserDetail(APIView):
    def get(self, request, user_id):
        user = users_collection.find_one({"user_id": user_id}, {"_id": 0})  # Exclude MongoDB's _id
        if not user:
            return Response({"message": "User not found", "status":404})
        return Response({"message": "User found", "data": user, "status":200})

    def put(self, request, user_id):
        serializer = UserSerializer(data=request.data, partial=True)  # Support partial updates
        if serializer.is_valid():
            user = users_collection.find_one({"user_id": user_id})
            if not user:
                return Response({"message": "User not found", "status":404})
            data = serializer.validated_data

            # Convert `dob` from datetime.date to datetime.datetime if it's a date object
            if 'dob' in data and isinstance(data['dob'], date):
                data['dob'] = datetime.combine(data['dob'], datetime.min.time())
            users_collection.update_one({"user_id": user_id}, {"$set": data})
            return Response({"message": "User updated successfully", "data": data, "status":200})
        return Response({"message": serializer.errors, "status": 400})


    def delete(self, request, user_id=None):
        if not user_id or user_id == "":
            return Response({"message": "User ID is required for deletion", "status": 400})
        result = users_collection.delete_one({"user_id": user_id})
        if result.deleted_count == 0:
            return Response({"message": "User not found", "status":404})
        return Response({"message": f"User with ID {user_id} deleted successfully", "status":200})

