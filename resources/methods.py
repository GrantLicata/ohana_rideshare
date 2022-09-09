
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users 
        (first_name, last_name, email, password, birthday, gender, language ,created_at, updated_at) 
        VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, %(birthday)s, %(gender)s, %(language)s, NOW() , NOW() )
        ;"""
        result = connectToMySQL(cls.db).query_db( query, data )
        return result

    @classmethod
    def update(cls, data):
        query = """UPDATE users 
        SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() 
        WHERE id = %(id)s
        ;"""
        print(query)
        result = connectToMySQL(cls.db).query_db( query, data )
        print("||-- Items updated in database --|| <> Results:", result)
        return result

    @classmethod
    def delete(cls, data):
        query = """DELETE 
        FROM users 
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db( query, data )
        print("||-- Items deleted from database --|| <> Results:", result)
        return result

    @classmethod
    def get_all(cls):
        query = """SELECT * 
        FROM users
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        data = []
        for item in results:
            data.append( cls(item) )
        return data
        
    @classmethod
    def get_by_email(cls,data):
        query = """SELECT * 
        FROM users 
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query,data)
        print("||-- Selected by email from database --|| <> Results:", result)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = """SELECT * 
        FROM recipes 
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query,data)
        print("||-- Selected by id from database --|| <> Results:", result)
        if len(result) < 1:
            return False
        return cls(result[0])

    # ||| Joined Tables 1:n ||| -> Users have many tweets, we want to gather all recipes and their associated user information. For each of the recipes, we are segregating the user information, generating a user object, and assigning that user to the recipe they made.
    @classmethod
    def get_all_many_with_user(cls):
        query = """SELECT * 
        FROM many 
        JOIN users 
        ON many.user_id = users.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        all_many = []
        for row in results:
            one_many_user_info = {
                'id': row["id"],
                'name': row["name"],
                'email': row["email"], 
                'password': row["password"],
                'created_at': row["created_at"],
                'updated_at': row["updated_at"]
            }
            user = user.User(one_many_user_info)
            one_many_instance = cls(row)
            one_many_instance.creator = user
        return all_many


    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name is required.")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name is required.")
            is_valid = False
        # Check database to see if email already exists.
        users = User.get_all()
        for user in users:
            if user.email == data['email']:
                flash("Email already exists.")
                is_valid = False
        if len(data['email']) < 1:
            flash("Email is required.")
            is_valid = False
        if len(data['birthday']) < 1:
            flash("Birthday is required.")
            is_valid = False
        if len(data['gender']) < 1:
            flash("Gender is required.")
            is_valid = False
        if len(data['language']) < 1:
            flash("Language is required.")
            is_valid = False
        if passwords['password'] != passwords['confirm_password']:
            flash("Passwords must be the same.")
            is_valid = False
        if len(passwords['password']) < 8:
            flash("Passwords must be longer than 8 characters.")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_password(passwords):
        is_valid = True
        return is_valid