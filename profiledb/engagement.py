from .profiledb import BaseProfileTable
from sqlalchemy.exc import SQLAlchemyError

class Engagement(BaseProfileTable):
    def __init__(self, drop=False):
        super().__init__()
        self.table_name = 'engagements_client'
        
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
                    `engagement_id` INT PRIMARY KEY AUTO_INCREMENT,
                    `post_id` INT,
                    `likes_count` INT,
                    `comments_count` INT,
                    `shares_count` INT,
                    `video_completion_rate` FLOAT,
                    FOREIGN KEY (`post_id`) REFERENCES `posts`(`post_id`)
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

    def write(self, post_id, likes_count, comments_count, shares_count, video_completion_rate):
        query = f"""
        INSERT INTO `{self.table_name}` (`post_id`, `likes_count`, `comments_count`, `shares_count`, `video_completion_rate`)
        VALUES (:post_id, :likes_count, :comments_count, :shares_count, :video_completion_rate);
        """
        params = {
            'post_id': post_id,
            'likes_count': likes_count,
            'comments_count': comments_count,
            'shares_count': shares_count,
            'video_completion_rate': video_completion_rate
        }
        self.execute_query(query, params)
        print("Engagement record added successfully.")

    def read(self):
        query = f"SELECT * FROM `{self.table_name}`;"
        results = self.fetch_query(query)
        print("Engagement records retrieved successfully.")
        return results

    def update(self, engagement_id, likes_count=None, comments_count=None, shares_count=None, video_completion_rate=None):
        query = f"""
        UPDATE `{self.table_name}` SET 
            `likes_count` = COALESCE(:likes_count, `likes_count`), 
            `comments_count` = COALESCE(:comments_count, `comments_count`),
            `shares_count` = COALESCE(:shares_count, `shares_count`),
            `video_completion_rate` = COALESCE(:video_completion_rate, `video_completion_rate`)
        WHERE `engagement_id` = :engagement_id;
        """
        params = {
            'engagement_id': engagement_id,
            'likes_count': likes_count,
            'comments_count': comments_count,
            'shares_count': shares_count,
            'video_completion_rate': video_completion_rate
        }
        self.execute_query(query, params)
        print("Engagement record updated successfully.")

    def delete(self, engagement_id):
        query = f"DELETE FROM `{self.table_name}` WHERE `engagement_id` = :engagement_id;"
        params = {'engagement_id': engagement_id}
        self.execute_query(query, params)
        print("Engagement record deleted successfully.")

    def drop_table(self):
        self.execute_query(f"DROP TABLE IF EXISTS `{self.table_name}`;")
        print(f"Table `{self.table_name}` dropped successfully.")
