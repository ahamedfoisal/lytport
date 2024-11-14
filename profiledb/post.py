from .profiledb import BaseProfileTable
from sqlalchemy.exc import SQLAlchemyError

class Post(BaseProfileTable):
    def __init__(self, drop=False):
        super().__init__()
        self.table_name = 'posts_client'
        
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
                    `post_id` INT PRIMARY KEY AUTO_INCREMENT,
                    `user_id` INT,
                    `media_type` VARCHAR(50),
                    `media_url` VARCHAR(255),
                    `caption` TEXT,
                    `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
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

    def write(self, user_id, media_type, media_url, caption):
        query = f"""
        INSERT INTO `{self.table_name}` (`user_id`, `media_type`, `media_url`, `caption`, `timestamp`)
        VALUES (:user_id, :media_type, :media_url, :caption, CURRENT_TIMESTAMP);
        """
        params = {
            'user_id': user_id,
            'media_type': media_type,
            'media_url': media_url,
            'caption': caption
        }
        self.execute_query(query, params)
        print("Post added successfully.")

    def read(self):
        query = f"SELECT * FROM `{self.table_name}`;"
        results = self.fetch_query(query)
        print("Posts retrieved successfully.")
        return results

    def update(self, post_id, caption=None):
        query = f"""
        UPDATE `{self.table_name}` SET 
            `caption` = COALESCE(:caption, `caption`)
        WHERE `post_id` = :post_id;
        """
        params = {'post_id': post_id, 'caption': caption}
        self.execute_query(query, params)
        print("Post updated successfully.")

    def delete(self, post_id):
        query = f"DELETE FROM `{self.table_name}` WHERE `post_id` = :post_id;"
        params = {'post_id': post_id}
        self.execute_query(query, params)
        print("Post deleted successfully.")

    def drop_table(self):
        self.execute_query(f"DROP TABLE IF EXISTS `{self.table_name}`;")
        print(f"Table `{self.table_name}` dropped successfully.")
