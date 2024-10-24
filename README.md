
# Instagram Analysis Data Model

This project is designed to analyze users' Instagram profiles and activities based on their IDs, compare them with successful creators, and provide actionable insights and real-time suggestions. The data model is structured to efficiently store and retrieve information related to user profiles, posts, engagements, and comments.

## Data Model Description

The data model consists of the following main entities:

1. **User**: Represents each Instagram user. Contains fields like `user_id`, `username`, `follower_count`, `following_count`, `bio`, and more.
2. **Post**: Stores information about each post made by the users. Includes `post_id`, `user_id`, `caption`, `likes`, `comments_count`, and `posted_at`.
3. **Follower**: Tracks data of their followers. Includes `user_id` and `follower_id`.
4. **Engagement**: Stores metrics such as likes, shares, and comments on posts. Includes `engagement_id`, `post_id`, `user_id`, and `engagement_type`.
5. **Comment**: Stores comments on each post, with fields such as `comment_id`, `post_id`, `user_id`, and `content`.

The relationships between these entities ensure that we can quickly retrieve information such as a user's posts, the engagements on each post, and the comments made by other users.

## Reasoning Behind Using SQL for This Project

We chose **SQL (Structured Query Language)** for this project due to the structured nature of the data and the need for complex queries and relationships. The data consists of multiple related entities, such as users, posts, and engagements, which benefit from SQL's ability to manage relational data efficiently. SQL databases like PostgreSQL or MySQL offer powerful querying capabilities, transaction management, and data integrity, making it a suitable choice for this project.

### Advantages of SQL for this Project:
1. **Relational Data**: SQL is ideal for handling relational data where tables are connected through foreign keys.
2. **Data Integrity**: Ensures data consistency through constraints and relationships.
3. **Complex Queries**: Supports complex joins, subqueries, and aggregations for generating insights.
4. **Scalability**: SQL databases like PostgreSQL are scalable and can handle large datasets with proper indexing and optimization.

## Database Setup Instructions

### 1. Database Configuration
1. Clone this repository or download the source code.
  ```
  git clone https://github.com/ahamedfoisal/lytport
  ```
2. Install the required packages:
  ```
  pip install -r requirements.txt
  ```
   
3. Create a `.env` file in the root directory of the project and add the following details:
  ```
  DB_SERVER=<your_db_server>
  DB_NAME=<your_db_name>
  DB_USER=<your_db_username>
  DB_PASSWORD=<your_db_password>
  ```

Replace the placeholders `<your_db_server>`, `<your_db_name>`, `<your_db_username>`, and `<your_db_password>` with your actual database connection details.

### 2. Setting Up the Database
If using PostgreSQL or MySQL, create a new database with the name specified in your `.env` file. Then, connect to the database and run the following command to create necessary tables:

```bash
python database.py
```

This script will establish a connection to your database and create tables such as `User`, `Post`, `Follower`, `Engagement`, and `Comment` based on the Entity-Relationship (ER) diagram.

### 3. Running the Application
Once the database is set up, run the application:

```bash
python app.py
```
## Entity-Relationship (ER) Diagram 

[ER Diagram](https://github.com/ahamedfoisal/lytport/blob/main/Detailed%20ER%20Diagram.png)

The ER Diagram illustrates the structure of the database schema used in this project. It highlights the entities and relationships, making it easier to understand the connections between different tables. 

### Diagram Overview
1. **User Entity**: Contains information about each Instagram user, including user ID, username, and profile details. This table is central and connected to other entities like `Post`, `Follower`, and `Engagement`.
2. **Post Entity**: Stores information about posts made by users. Each post is linked to a user through the `user_id` foreign key.
3. **Follower Entity**: Tracks the follower-following relationships between users. This table uses self-referencing foreign keys to establish user relationships.
4. **Engagement Entity**: Represents different types of engagements, such as likes and shares, associated with each post. The `engagement_type` field identifies the nature of each engagement.
5. **Comment Entity**: Stores comments on each post. The `comment_id` is unique for each comment, and the `post_id` establishes the relationship with the `Post` entity.

This structure allows for efficient querying and analysis of user activity and engagements, forming the basis of the recommendation system for content suggestions and analytics.

# API Documentation

Why is the API useful for the project?

The API is useful for the project because it allows us to interact with the database and perform CRUD operations on the data. We can use the API to create new users, get user by ID, get all users, update user by ID, delete user by ID. In other iterations, we will add more endpoints to the API to perform CRUD operations on the other entities. and thus we can give the client the ability to acccess the data and perform operations on the data easier and faster. 

### How to run the API

after installing the requirements, run the following command to start the server:
```
uvicorn backend:app --reload
```
now the server is running on http://localhost:8000/ 


## Endpoints

### 1. Create a new user

**POST** `/users/`

**Request Body**:
```
{
    "username": "new_user",
    "bio": "This is a test bio",
    "followers_count": 100,
    "following_count": 200,
    "location": "New York",
    "is_influential": true
}
```

**Response**:
```
{
    "user_id": 1,
    "username": "new_user",
    "bio": "This is a test bio",
    "followers_count": 100,
    "following_count": 200,
    "location": "New York",
    "is_influential": true
}
```

### 2. Get user by ID

**GET** `/users/{user_id}`

**Response**:
```
{
    "user_id": 1,
    "username": "new_user",
    "bio": "This is a test bio",
    "followers_count": 100,
    "following_count": 200,
    "location": "New York",
    "is_influential": true
}
```

### 3. Get all users

**GET** `/users/?limit=10`

**Response**:
```
[
    {
        "user_id": 1,
        "username": "new_user",
        "bio": "This is a test bio",
        "followers_count": 100,
        "following_count": 200,
        "location": "New York",
        "is_influential": true
    },
    {
        "user_id": 2,
        "username": "new_user2",
        "bio": "This is a test bio2",
        "followers_count": 200,
        "following_count": 300,
        "location": "New York2",
        "is_influential": true
    }
    ...
]
```

### 4. Update user by ID

**PUT** `/users/{user_id}`

**Request Body**:
```
{
    "username": "updated_user",
    "bio": "This is an updated bio",
    
}
```

**Response**:
```
{
    "user_id": 1,
    "username": "updated_user",
    "bio": "This is an updated bio"
}
```

### 5. Delete user by ID

**DELETE** `/users/{user_id}`

**Response**:
```
{
    "message": "User deleted successfully"
}
```

postman workspace link : https://lytport.postman.co/workspace/lytport-Workspace~74aea609-4b7f-4d51-8e01-93e421a00dd9/request/13199683-174130b7-1bbf-4529-91fa-c330e960304b?action=share&creator=39096649&ctx=documentation

Here is a video that shows the API in action on Postman: 
[video](https://drive.google.com/file/d/1Wn1aov0bsPVxiruXh8Rl8aW2foWoFbvh/view?usp=sharing)



