from database.database import BaseTable
from sqlalchemy.exc import SQLAlchemyError

class Image(BaseTable):
    def __init__(self, drop=False):
        super().__init__()
        self.table_name = 'images'
        
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
                    `title` VARCHAR(255),
                    `url` VARCHAR(255),
                    `caption` TEXT,
                    `time_posted` TIMESTAMP,
                    `location` VARCHAR(255),
                    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
                );
                """
                self.execute_query(query)
        except SQLAlchemyError as e:
            pass

    def write(self, post_id, user_id, title, url, caption, time_posted, location):
        query = f"""
        INSERT INTO `{self.table_name}` (`post_id`, `user_id`, `title`, `url`, `caption`, `time_posted`, `location`)
        VALUES (:post_id, :user_id, :title, :url, :caption, :time_posted, :location);
        """
        params = {
            'post_id': post_id,
            'user_id': user_id,
            'title': title,
            'url': url,
            'caption': caption,
            'time_posted': time_posted,
            'location': location
        }
        self.execute_query(query, params)

    def read(self):
        query = f"SELECT * FROM `{self.table_name}`;"
        return self.fetch_query(query)

    def update(self, post_id, title=None, url=None, caption=None, time_posted=None, location=None):
        query = f"""
        UPDATE `{self.table_name}` SET 
            `title` = COALESCE(:title, `title`),
            `url` = COALESCE(:url, `url`),
            `caption` = COALESCE(:caption, `caption`),
            `time_posted` = COALESCE(:time_posted, `time_posted`),
            `location` = COALESCE(:location, `location`)
        WHERE `post_id` = :post_id;
        """
        params = {
            'post_id': post_id,
            'title': title,
            'url': url,
            'caption': caption,
            'time_posted': time_posted,
            'location': location
        }
        self.execute_query(query, params)

    def delete(self, post_id):
        query = f"DELETE FROM `{self.table_name}` WHERE `post_id` = :post_id;"
        params = {'post_id': post_id}
        self.execute_query(query, params)

    def drop_table(self):
        self.execute_query(f"DROP TABLE IF EXISTS `{self.table_name}`;")
