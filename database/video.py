from database.database import BaseTable
from sqlalchemy.exc import SQLAlchemyError

class Video(BaseTable):
    def __init__(self, drop=False):
        super().__init__()
        self.table_name = 'videos'
        
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
                    `thumbnail` VARCHAR(255),
                    `url` VARCHAR(255),
                    `caption` TEXT,
                    `time_posted` TIMESTAMP,
                    `location` VARCHAR(255),
                    `duration` INT,
                    FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
                );
                """
                self.execute_query(query)
        except SQLAlchemyError as e:
            pass

    def write(self, post_id, user_id, title, thumbnail, url, caption, time_posted, location, duration):
        query = f"""
        INSERT INTO `{self.table_name}` (`post_id`, `user_id`, `title`, `thumbnail`, `url`, `caption`, `time_posted`, `location`, `duration`)
        VALUES (:post_id, :user_id, :title, :thumbnail, :url, :caption, :time_posted, :location, :duration);
        """
        params = {
            'post_id': post_id,
            'user_id': user_id,
            'title': title,
            'thumbnail': thumbnail,
            'url': url,
            'caption': caption,
            'time_posted': time_posted,
            'location': location,
            'duration': duration
        }
        self.execute_query(query, params)

    def read(self):
        query = f"SELECT * FROM `{self.table_name}`;"
        return self.fetch_query(query)

    def update(self, post_id, title=None, thumbnail=None, url=None, caption=None, time_posted=None, location=None, duration=None):
        query = f"""
        UPDATE `{self.table_name}` SET 
            `title` = COALESCE(:title, `title`),
            `thumbnail` = COALESCE(:thumbnail, `thumbnail`),
            `url` = COALESCE(:url, `url`),
            `caption` = COALESCE(:caption, `caption`),
            `time_posted` = COALESCE(:time_posted, `time_posted`),
            `location` = COALESCE(:location, `location`),
            `duration` = COALESCE(:duration, `duration`)
        WHERE `post_id` = :post_id;
        """
        params = {
            'post_id': post_id,
            'title': title,
            'thumbnail': thumbnail,
            'url': url,
            'caption': caption,
            'time_posted': time_posted,
            'location': location,
            'duration': duration
        }
        self.execute_query(query, params)

    def delete(self, post_id):
        query = f"DELETE FROM `{self.table_name}` WHERE `post_id` = :post_id;"
        params = {'post_id': post_id}
        self.execute_query(query, params)

    def drop_table(self):
        self.execute_query(f"DROP TABLE IF EXISTS `{self.table_name}`;")
