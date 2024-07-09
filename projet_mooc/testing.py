'''from pymongo import MongoClient

# Connect to the MongoDB client
client = MongoClient('mongodb://mongoadmin:GRETA2024@4.233.138.30')

# Specify the database and collection
db = client['mooc']
collection = db['user']

# Define the courses and sessions  to filter and project
courses_sessions = [
    'MinesTelecom/04017/session01',
    'MinesTelecom/04017S02/session02',
    'MinesTelecom/04018/session01',
    'MinesTelecom/04018S02/session02',
    'MinesTelecom/04021/session01',
    'MinesTelecom/04021S02/session02',
    'course-v1:MinesTelecom+04017+session03',
    'course-v1:MinesTelecom+04021+session03',
    'course-v1:MinesTelecom+04018+session03',
    'course-v1:MinesTelecom+04017+session04'
]

# Construct the filter dictionary
filter_dict = {
    f'{course_session}.grade': {'$gte': '0.0'} for course_session in courses_sessions
}

# Construct the projection dictionary
projection_dict = {'username': 1}

# Add fields for each course session to the projection dictionary
for course_session in courses_sessions:
    projection_dict[f'{course_session}.grade'] = 1
    projection_dict[f'{course_session}.goals'] = 1
    projection_dict[f'{course_session}.level_of_education'] = 1


try:
    # Perform the query
    result = collection.find(filter=filter_dict, projection=projection_dict)

    # Check if any documents are returned
    found = False
    for doc in result:
        print(doc)
        found = True

    if not found:
        print("No matching documents found.")
except Exception as e:
    print("An error occurred:", e)'''

from pymongo import MongoClient
import pandas as pd

# Connect to the MongoDB client
client = MongoClient('mongodb://mongoadmin:GRETA2024@4.233.138.30')

# Specify the database and collection
db = client['mooc']
collection = db['user']

# Define the courses and sessions to filter and project
courses_sessions = [
    'MinesTelecom/04017/session01',
    'MinesTelecom/04017S02/session02',
    'MinesTelecom/04018/session01',
    'MinesTelecom/04018S02/session02',
    'MinesTelecom/04021/session01',
    'MinesTelecom/04021S02/session02',
    'course-v1:MinesTelecom+04017+session03',
    'course-v1:MinesTelecom+04021+session03',
    'course-v1:MinesTelecom+04018+session03',
    'course-v1:MinesTelecom+04017+session04'
]

# Construct the filter dictionary
filter_dict = {
    '$or': [{f'{course_session}.grade': {'$gt': '0.0'}} for course_session in courses_sessions]
}

# Construct the projection dictionary
projection_dict = {'_id': 0, 'username': 1}

# Add fields for each course session to the projection dictionary
for course_session in courses_sessions:
    projection_dict[f'{course_session}.grade'] = 1
    projection_dict[f'{course_session}.goals'] = 1
    projection_dict[f'{course_session}.level_of_education'] = 1

try:
    # Perform the query
    result = collection.find(filter=filter_dict, projection=projection_dict)

    # Convert the result to a list of dictionaries
    result_list = list(result)

    # df = pd.DataFrame(result_list)

    # # Print the DataFrame
    # print(df)



    # Create a list to hold the separated data
    separated_data = []

    # Iterate over each document
    for doc in result_list:
        username = doc.get('username')
        for course_session in courses_sessions:
            session_data = doc.get(course_session)
            if session_data:
                grade = session_data.get('grade')
                goals = session_data.get('goals')
                level_of_education = session_data.get('level_of_education')
                # Add the extracted data to the separated data list
                separated_data.append({
                    'username': username,
                    'course_session': course_session,
                    'grade': grade,
                    'goals': goals,
                    'level_of_education': level_of_education
                })

    # Convert the separated data to a DataFrame
    df_separated = pd.DataFrame(separated_data)

    # Print the DataFrame
    print(df_separated)

    if df_separated.empty:
        print("No matching documents found.")
except Exception as e:
    print("An error occurred:", e)
