from .profiledb import BaseProfileTable
from sqlalchemy.exc import SQLAlchemyError

class User(BaseProfileTable):
    def __init__(self, drop=False):
        super().__init__()
        self.table_name = 'user_client'
        self.execute_query("SET FOREIGN_KEY_CHECKS = 0;")
        
        if drop:
            self.drop_table()
        else:
            self.create_table()

    def create_table(self):
        try:
            result = self.fetch_query(f"SHOW TABLES LIKE '{self.table_name}';")
            if not result:
                query = f"""
                CREATE TABLE `{self.table_name}` (
                    `user_id` INT PRIMARY KEY AUTO_INCREMENT,
                    `username` VARCHAR(255),
                    `bio` TEXT,
                    `followers_count` INT,
                    `following_count` INT,
                    `location` VARCHAR(255),
                    `is_influential` BOOLEAN
                );
                """
                self.execute_query(query)
                print(f"Table `{self.table_name}` created successfully.")
            else:
                print(f"Table `{self.table_name}` already exists.")
        except SQLAlchemyError as e:
            print(f"Error creating table `{self.table_name}`: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error creating table `{self.table_name}`: {e}")
            raise

    def write(self, user_id, username, bio, followers_count, following_count, location, is_influential):
        query = f"""
        INSERT INTO `{self.table_name}` (`user_id`, `username`, `bio`, `followers_count`, `following_count`, `location`, `is_influential`)
        VALUES (:user_id, :username, :bio, :followers_count, :following_count, :location, :is_influential);
        """
        params = {
            'user_id': user_id,
            'username': username,
            'bio': bio,
            'followers_count': followers_count,
            'following_count': following_count,
            'location': location,
            'is_influential': is_influential
        }
        self.execute_query(query, params)
        print("User added successfully.")

    def read(self):
        query = f"SELECT * FROM `{self.table_name}`;"
        results = self.fetch_query(query)
        print("Users retrieved successfully.")
        return results

    def read_all(self, limit):
        query = f"SELECT user_id, username, bio, followers_count, following_count, location, is_influential FROM `{self.table_name}` LIMIT {limit};"
        results = self.fetch_query(query)
        print("Limited users retrieved successfully.")
        return results
    
    def read_by_id(self, user_id: str):
        query = f"SELECT * FROM `{self.table_name}` WHERE `user_id` = :user_id;"
        params = {'user_id': user_id}
        result = self.fetch_query(query, params)
        
        if result:
            user_tuple = result[0]
            user_dict = {
                'user_id': user_tuple[0],
                'username': user_tuple[1],
                'bio': user_tuple[2],
                'followers_count': user_tuple[3],
                'following_count': user_tuple[4],
                'location': user_tuple[5],
                'is_influential': bool(user_tuple[6])
            }
            return user_dict
        return None

    def read_by_username(self, username: str):
        query = f"SELECT * FROM `{self.table_name}` WHERE `username` = :username;"
        params = {'username': username}
        result = self.fetch_query(query, params)
        print("User retrieved by username successfully.")
        return result

    def update(self, user_id, username=None, bio=None):
        query = f"""
        UPDATE `{self.table_name}` SET 
            `username` = COALESCE(:username, `username`), 
            `bio` = COALESCE(:bio, `bio`)
        WHERE `user_id` = :user_id;
        """
        params = {'user_id': user_id, 'username': username, 'bio': bio}
        self.execute_query(query, params)
        print("User updated successfully.")

    def delete(self, user_id):
        query = f"DELETE FROM `{self.table_name}` WHERE `user_id` = :user_id;"
        params = {'user_id': user_id}
        self.execute_query(query, params)
        print("User deleted successfully.")

    def drop_table(self):
        self.execute_query(f"DROP TABLE IF EXISTS `{self.table_name}`;")
        print(f"Table `{self.table_name}` dropped successfully.")

    def check_username_exists(self, username: str):
        query = f"SELECT * FROM `{self.table_name}` WHERE `username` = :username;"
        params = {'username': username}
        result = self.fetch_query(query, params)
        exists = bool(result)
        print(f"Username exists: {exists}")
        return exists
