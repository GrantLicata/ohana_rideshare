from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash 
import re
from pprint import pprint

# Validation schematics
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Ride:
    db = "ohana"  # <--- Enter database reference
    def __init__(self ,data):
        self.id = data['id']
        self.destination = data['destination']
        self.pick_up_location = data['pick_up_location']
        self.date = data['date']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.driver = None
        self.rider = None

    @classmethod
    def save_ride(cls, data):
        query = """INSERT INTO rides 
        (destination, pick_up_location, date, details, user2_id, created_at, updated_at) 
        VALUES ( %(destination)s , %(pick_up_location)s , %(date)s, %(details)s, %(user2_id)s, NOW() , NOW() )
        ;"""
        result = connectToMySQL(cls.db).query_db( query, data )
        return result

    @classmethod
    def update_ride(cls, data):
        query = """UPDATE rides 
        SET pick_up_location = %(pick_up_location)s, details = %(details)s, updated_at = NOW() 
        WHERE id = %(id)s
        ;"""
        print(query)
        result = connectToMySQL(cls.db).query_db( query, data )
        print("||-- Items updated in database --|| <> Results:", result)
        return result

    @classmethod
    def assign_driver(cls, data):
        query = """UPDATE rides 
        SET user_id = %(driver_id)s, updated_at = NOW() 
        WHERE id = %(ride_id)s
        ;"""
        print(query)
        result = connectToMySQL(cls.db).query_db( query, data )
        print("||-- Items updated in database --|| <> Results:", result)
        return result

    @classmethod
    def get_all_rides_driver_and_rider(cls):
        query = """SELECT * 
        FROM users
        JOIN rides
        ON rides.user_id = users.id
        JOIN users as riders
        ON rides.user2_id = riders.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        print("The query results are:",results)
        all_rides = []
        for each in results:
            # Create a ride instance
            one_instance = cls(each)
            # Create a driver instance
            rides_driver_data = {
                'id': each["user_id"],
                'first_name': each["first_name"],
                'last_name': each["last_name"],
                'email': each["email"], 
                'password': each["password"],
                'created_at': each["created_at"],
                'updated_at': each["updated_at"]
            }
            driver = user.User(rides_driver_data)
            one_instance.driver = driver
            # Create a rider instance
            rides_rider_data = {
                'id': each["riders.id"],
                'first_name': each["riders.first_name"],
                'last_name': each["riders.last_name"],
                'email': each["riders.email"], 
                'password': each["riders.password"],
                'created_at': each["riders.created_at"],
                'updated_at': each["riders.updated_at"]
            }
            rider = user.User(rides_rider_data)
            one_instance.rider = rider
            # Append all the outputs to the list
            all_rides.append(one_instance)
        return all_rides

    @classmethod
    def get_all_rides_and_rider(cls):
        query = """SELECT * 
        FROM rides
        JOIN users
        ON users.id = rides.user2_id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        print("These are the rides and rider results")
        pprint(results)
        all_rides = []
        for each in results:
            # Create a ride instance
            one_instance = cls(each)
            # Create a rider instance
            rides_rider_data = {
                'id': each["user2_id"],
                'first_name': each["first_name"],
                'last_name': each["last_name"],
                'email': each["email"], 
                'password': each["password"],
                'created_at': each["users.created_at"],
                'updated_at': each["users.updated_at"]
            }
            rider = user.User(rides_rider_data)
            one_instance.rider = rider
            # Append all the outputs to the list
            all_rides.append(one_instance)
        return all_rides

    @classmethod
    def delete(cls, data):
        query = """DELETE 
        FROM rides
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db( query, data )
        print("||-- Items deleted from database --|| <> Results:", result)
        return result

    @classmethod
    def get_all_ride(cls,data):
        query = """SELECT * 
        FROM rides
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])