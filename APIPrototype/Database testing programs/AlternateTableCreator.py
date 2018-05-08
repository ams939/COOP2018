import idigbio
import psycopg2
import TableSchemaCreator

def createTable(result):
    #Connect to database, db name is testdb
    connection = psycopg2.connect(database="testdb", user="postgres",
                              password="idigbio123", host="127.0.0.1", port="5432")
    #Initialize cursor
    cursor = connection.cursor()
    
    '''
    TODO:
        Query database table test to get list of fields it contains
        Loop through records, use list of fields in DB to get only relevant
        values from results dictionary (only pick fields present in DB).
        Use the dict.get(key) function for this to avoid KeyError in case field 
        doesnt exist in record.
    '''
    
def main():
    pass

if __name__ == "__main__":
    main()