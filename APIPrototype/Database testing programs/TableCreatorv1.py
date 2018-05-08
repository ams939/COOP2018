import idigbio
import psycopg2
import TableSchemaCreator

def createTable(result):
    #Connect to database, db name is testdb
    connection = psycopg2.connect(database="testdb", user="postgres",
                              password="idigbio123", host="127.0.0.1", port="5432")
    #Initialize cursor
    cursor = connection.cursor()
    
    TableSchemaCreator.createSchema(result)
    
    for record in result["items"]:
        insert_base = "INSERT INTO test "
        insert_keys = "("
        insert_values = "("

        keys_values = list(record["indexTerms"].items())
        
        for i in range(0, len(keys_values)):
            key = keys_values[i][0]
            raw_value = str(keys_values[i][1])
            value = raw_value.replace("'", '"')
            
            if i == (len(keys_values) - 1):
                insert_keys += "\"" + key + "\")"
                insert_values += "'" + value + "')"
            else:
                insert_keys += "\"" + key + "\", "
                insert_values += "'" + value + "', "
                
        insert_command = insert_base + insert_keys + " VALUES " + insert_values
        cursor.execute(insert_command)
    
    connection.commit()
    cursor.close()
    connection.close()
        


def main():
    #Initialize idigbio API
    api = idigbio.json()
    
    #Define query dictionary
    rq = {"scientificname":"panthera pardus", "country":"india"}
    
    #Assign query results
    result = api.search_records(rq, limit=30)
    
    createTable(result)
    
    
if __name__ == "__main__":
    main()