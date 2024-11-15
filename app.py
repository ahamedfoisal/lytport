from database.comments import Comment
from database.follower import Follower
from database.engagement import Engagement 
from database.post import Post
from database.user import User
from database.database import Database
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import pandas as pd

user_db = User()
post_db = Post()
comment_db = Comment()
engagement_db = Engagement()
follower_db = Follower()

def drop_tables_in_order():
    try:
        with Database.get_engine().connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            Engagement(drop=True)
            Comment(drop=True)
            Follower(drop=True)
            Post(drop=True)
            User(drop=True)
            print("All tables dropped successfully.")
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    except SQLAlchemyError as e:
        print(f"Error dropping tables: {e}")
        raise

def load_users_from_csv(file_path):
    data_df = pd.read_csv(file_path)
    user_db = User()

    for _, row in data_df.iterrows():
        user_db.write(
            user_id=int(row['id']) + 8,
            name=row['name'],
            username=row['username'], 
            category=row['category'],
            # business_category=row['business_category'],
            bio=row['bio'], 
            followers=row['followers'], 
            follows=row['follows'], 
            is_verified=bool(row['is_verified']),
            video_count=row['video_count'],
            image_count=row['image_count']
            # location="N/A"
        )
    print(f"Loaded {len(data_df)} records into the User table.")

def load_images_from_csv(file_path):
    """Load image posts from CSV into the Post table."""
    data_df = pd.read_csv(file_path)
    post_db = Post()

    for _, row in data_df.iterrows():
        post_db.write(
            user_id=int(row['user_id']) + 8, 
            post_id=int(row['image_id']),
            media_type="image", 
            media_url=row['src'], 
            caption=row['accessibility_caption']
        )
    print(f"Loaded {len(data_df)} image records into the Post table.")

def load_videos_from_csv(file_path):
    """Load video posts from CSV into the Post table."""
    data_df = pd.read_csv(file_path)
    post_db = Post()

    for _, row in data_df.iterrows():
        post_db.write(
            user_id=int(row['user_id']) + 8, 
            post_id=int(row['video_id']),
            media_type="video", 
            media_url=row['url'], 
            caption=row['captions']
        )
    print(f"Loaded {len(data_df)} video records into the Post table.")

def load_comments_from_csv(file_path):
    data_df = pd.read_csv(file_path)
    comment_db = Comment()

    for _, row in data_df.iterrows():
        comment_db.write(
            post_id=row['post_id'], 
            user_id=int(row['user_id']) + 8, 
            message=row['message'], 
            like_count=row['like_count']
        )
    print(f"Loaded {len(data_df)} records into the Comment table.")

def load_engagements_from_csv(file_path):
    data_df = pd.read_csv(file_path)
    engagement_db = Engagement()

    for _, row in data_df.iterrows():
        engagement_db.write(
            post_id=row['image_id', 'video_id'], 
            likes_count=row['likes'], 
            comments_count=row['comments_count'], 
            # shares_count=row['shares_count'], 
            # video_completion_rate=row['video_completion_rate']
        )
    print(f"Loaded {len(data_df)} records into the Engagement table.")

def main():
    # drop_tables_in_order()

    load_users_from_csv('real_data/users.csv')
    # load_images_from_csv('real_data/images.csv')
    # load_videos_from_csv('real_data/videos.csv')
    # # load_comments_from_csv('real_data/images.csv', 'real_data/videos.csv')
    # load_engagements_from_csv('real_data/images.csv', 'real_data/videos.csv')

    # Optionally, read and print data for validation
    user_db = User()
    print("Users:", user_db.read())

    post_db = Post()
    print("Posts:", post_db.read())

    comment_db = Comment()
    print("Comments:", comment_db.read())

    engagement_db = Engagement()
    print("Engagements:", engagement_db.read())

    Database.close_connection()

if __name__ == "__main__":
    main()
