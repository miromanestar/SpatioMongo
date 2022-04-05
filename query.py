from pymongo import MongoClient 
from bson.son import SON
from datetime import datetime

USERNAME = 'admin'
PASSWORD = 'password'
SERVER = 'localhost'
PORT = '27017'

CONNECTION_STRING = f'mongodb://{ USERNAME }:{ PASSWORD }@{ SERVER }:{ PORT }'

if __name__ == '__main__':

    client = MongoClient(CONNECTION_STRING)
    db = client['UserDB']
    collection = db['Arrests']

    query = {'location': SON([('$nearSphere', [-85.307296, 35.058225]), ('$maxDistance', 3)])}
    result = collection.find(query).limit(5)

    print('Query of closest 5 arrests to the walnut bridge')
    for doc in result:
        formatted_time = datetime.strptime(doc['arrest_date'], '%Y-%m-%dT%H:%M:%S.000')
        time_string = formatted_time.strftime('%m/%d/%Y %H:%M')
        print(f'{time_string}')
        print(f'{doc["charges"]}')
        print(f'{doc["address_number"]} {doc["street_name"]}')
        print('')