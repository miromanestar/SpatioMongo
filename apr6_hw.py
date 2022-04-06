from pymongo import MongoClient 
from datetime import datetime

USERNAME = 'admin'
PASSWORD = 'password'
SERVER = 'localhost'
PORT = '27017'

CONNECTION_STRING = f'mongodb://{ USERNAME }:{ PASSWORD }@{ SERVER }:{ PORT }'

WALNUT_BRIDGE_COORDS = {
    'type': 'Point',
    'coordinates': [-85.307296, 35.058225]
}

def print_output(data):
    for doc in data:
        formatted_time = doc['arrest_date']
        time_string = formatted_time.strftime('%m/%d/%Y %H:%M')
        print(f'{time_string}')
        print(f'{doc["charges"]}')
        print(f'{doc["address_number"]} {doc["street_name"]}')
        print('')

def query1(collection):
    query = {
        'location': {
            '$nearSphere': {
                '$geometry': WALNUT_BRIDGE_COORDS,
                '$maxDistance': 3 * 1609.34
            }
        }
    }
    result = collection.find(query).limit(5)

    print('Query of closest 5 arrests to the walnut bridge\n')
    print_output(result)

def query2(collection):
    from_date = datetime.strptime('2022-04-04T00:00:00-0500', '%Y-%m-%dT%H:%M:%S%z')
    to_date = datetime.strptime('2022-04-4T23:59:59-0500', '%Y-%m-%dT%H:%M:%S%z')

    query = {
        'arrest_date': {
            '$gte': from_date, 
            '$lte': to_date
        }
    }
    result = collection.find(query)

    print('Query of vandalism on April 4th, 2022\n')
    print_output(result)

def query3(collection):
    from_date = datetime.strptime('2022-01-01T00:00:00-0500', '%Y-%m-%dT%H:%M:%S%z')
    to_date = datetime.strptime('2022-01-5T23:59:59-0500', '%Y-%m-%dT%H:%M:%S%z')

    query = {
        'location': {
            '$nearSphere': {
                '$geometry': WALNUT_BRIDGE_COORDS,
                '$maxDistance': 5 * 1609.34
            }
        },
        'arrest_date': {'$gte': from_date, '$lte': to_date}
    }
    result = collection.find(query)

    print('Query of all arrests within 5 miles of walnut street in the first 5 days January 2022')
    print_output(result)

if __name__ == '__main__':

    client = MongoClient(CONNECTION_STRING)
    db = client['UserDB']
    collection = db['Arrests']

    query1(collection)
    print('-----------------------------------------------------\n')
    query2(collection)
    print('-----------------------------------------------------\n')
    query3(collection)