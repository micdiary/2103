import csv
from pymongo import MongoClient
import pandas as pd


def read_csv_file(fileName):
    data = []

    df = pd.read_csv(f'2103\\Data\\2103_{fileName}_Data.csv')

    for _, row in df.iterrows():
        obj = {}
        for i in df.columns:
            # if column = scholarship
            if i == "scholarship" and str(row[i]).find("[") > -1:
                data_scholarships = []
                scholarships = row[i].split("},{")
                for j in scholarships:
                    temp = j.split(":")
                    # removing unnecessary characters
                    for index,k in enumerate(temp):
                        temp[index] = k.replace("[","").replace("{","").replace("]","")
                        if index == 0:
                            temp[index] = k.replace("[","").replace("{","").replace("]","").replace(",","")
                    # temp[0] = scholarship_name
                    # temp[1] = criteria
                    data_scholarships.append({temp[0]:temp[1]})
                obj[i] = data_scholarships
            else:
                obj[i] = row[i]
        data.append(obj)

    return data


def get_and_create_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017/"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    dblist = client.list_database_names()
    if "mydatabase" in dblist:
        print("The database exists.")
    else:
        mydb = client['2104_Assignment']
    
    return mydb

def append_data_into_db(data, dbName, collectionName):
    coll = get_and_create_collection(dbName,collectionName)
    coll.insert_many(data)

def get_and_create_collection(dbName,collName):
    coll = dbName[f"{collName}"]
    return coll

if __name__ == "__main__":
    # Get the database
    mydb = get_and_create_database()

    data = read_csv_file("NoSQL")
    append_data_into_db(data, mydb, "School")