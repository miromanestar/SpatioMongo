import argparse, json
from pymongo import MongoClient, InsertOne, GEOSPHERE
from pymongo.errors import BulkWriteError
from datetime import datetime

parser = argparse.ArgumentParser(description='Bulk import GeoJSON file into MongoDB')
parser.add_argument('-f', required=True, help='input file')
parser.add_argument('-s', default='localhost', help='target server name (default is localhost)')
parser.add_argument('-port', default='27017', help='server port (default is 27017)')
parser.add_argument('-d', help='target database name', default='UserDB')
parser.add_argument('-c', help='target collection to insert to', default='Arrests')
parser.add_argument('-u', help='username (optional)', default='admin')
parser.add_argument('-p', help='password (optional)', default='password')
args = parser.parse_args()

USERNAME = args.u
PASSWORD = args.p

INPUT_FILE = args.f

DB_NAME = args.d
COLLECTION_NAME = args.c

SERVER = args.s
PORT = args.port

CONNECTION_STRING = f'mongodb://{ SERVER }:{ PORT }'

def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client[DB_NAME]

def load_data():
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
    return data['features']
        
def upload_data(collection, data):

    collection.create_index([("location", GEOSPHERE)])

    bulk = []
    for feature in data:
        item = feature['properties']
        item['arrest_date'] = datetime.strptime(f"{ item['arrest_date'] }-0500", '%Y-%m-%dT%H:%M:%S.000%z')
        item['location'] = feature['geometry']
        bulk.append(InsertOne(item))

    try:
        result = collection.bulk_write(bulk, ordered=False)
        print(f'{result.inserted_count} documents inserted')
    except BulkWriteError as error:
        print('Errors encountered inserting data')
        print(f'Succesfully inserted {result.inserted_count} documents')
        print(f'{error.details}')

if __name__ == "__main__":

    data = load_data()

    database = get_database()
    collection = database[COLLECTION_NAME]

    upload_data(collection, data)