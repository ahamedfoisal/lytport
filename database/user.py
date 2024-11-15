from database.database import BaseTable

class User(BaseTable):
    def __init__(self, drop=False):
        super().__init__()
        self.table_name = 'users'
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
                    `name` VARCHAR(255),
                    `username` VARCHAR(255),
                    `category` VARCHAR(255),
                    `bio` TEXT,
                    `followers` INT,
                    `follows` INT,
                    `is_verified` BOOLEAN,
                    `video_count` INT,
                    `image_count` INT
                );
                """
                self.execute_query(query)
        except Exception as e:
            pass

    def write(self, user_id, name, username, category, bio, followers, follows, is_verified, video_count, image_count):
        query = f"""
        INSERT INTO `{self.table_name}` (`user_id`, `name`, `username`, `category`, `bio`, `followers`, `follows`, `is_verified`, `video_count`, `image_count`)
        VALUES (:user_id, :name, :username, :category, :bio, :followers, :follows, :is_verified, :video_count, :image_count);
        """
        params = {
            'user_id': user_id,
            'name': name,
            'username': username,
            'category': category,
            'bio': bio,
            'followers': followers,
            'follows': follows,
            'is_verified': is_verified,
            'video_count': video_count,
            'image_count': image_count
        }
        self.execute_query(query, params)

    def read(self):
        query = f"SELECT * FROM `{self.table_name}`;"
        return self.fetch_query(query)
    
    def read_all(self, limit):
        query = f"SELECT user_id, name, username, category, bio, followers, follows, is_verified, video_count, image_count FROM `{self.table_name}` LIMIT {limit};"
        return self.fetch_query(query)
    
    def read_by_id(self, user_id: str):
        query = f"SELECT * FROM `{self.table_name}` WHERE `user_id` = {user_id};"
        result = self.fetch_query(query)
        if result:
            user_tuple = result[0]
            user_dict = {
                'user_id': user_tuple[0],
                'name': user_tuple[1],
                'username': user_tuple[2],
                'category': user_tuple[3],
                'bio': user_tuple[4],
                'followers': user_tuple[5],
                'follows': user_tuple[6],
                'is_verified': bool(user_tuple[7]),
                'video_count': user_tuple[8],
                'image_count': user_tuple[9]
            }
            return user_dict

        return None

    def read_by_username(self, username: str):
        query = f"SELECT * FROM `{self.table_name}` WHERE `username` = '{username}';"
        return self.fetch_query(query)
    
    # Expanded to allow updates to all columns except user_id
    def update(self, user_id, name=None, username=None, category=None, bio=None, followers=None, follows=None, is_verified=None, video_count=None, image_count=None):
        query = f"""
        UPDATE `{self.table_name}` SET 
            `name` = COALESCE(:name, `name`), 
            `username` = COALESCE(:username, `username`),
            `category` = COALESCE(:category, `category`),
            `bio` = COALESCE(:bio, `bio`),
            `followers` = COALESCE(:followers, `followers`),
            `follows` = COALESCE(:follows, `follows`),
            `is_verified` = COALESCE(:is_verified, `is_verified`),
            `video_count` = COALESCE(:video_count, `video_count`),
            `image_count` = COALESCE(:image_count, `image_count`)
        WHERE `user_id` = :user_id;
        """
        params = {
            'user_id': user_id,
            'name': name,
            'username': username,
            'category': category,
            'bio': bio,
            'followers': followers,
            'follows': follows,
            'is_verified': is_verified,
            'video_count': video_count,
            'image_count': image_count
        }
        self.execute_query(query, params)

    def delete(self, user_id):
        query = f"DELETE FROM `{self.table_name}` WHERE `user_id` = :user_id;"
        params = {'user_id': user_id}
        self.execute_query(query, params)

    def drop_table(self):
        self.execute_query(f"DROP TABLE IF EXISTS `{self.table_name}`;")

    def check_username_exists(self, username: str):
        query = f"SELECT * FROM `{self.table_name}` WHERE `username` = :username;"
        params = {'username': username}
        result = self.fetch_query(query, params)
        return bool(result)
