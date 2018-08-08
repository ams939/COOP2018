import DBInfo
import records
import json

'''
The purpose of this script is to provide a variety of tools for cleaning up and
processing iDigBio data in a PostgreSQL database. This script utilizes other
custom scripts like DBInfo to work with a local database, the format of the
data in the local database is assumed to be as produced by the DataWorkflow
scripts. 
'''

def selectColumns(column_names, tablename, new_tablename):
    '''
    Function that takes a list of column names that exist in another database
    table (within the same database) and creates a new table with the columns
    defined in the list. Also takes name of table with columns being selected
    and name of new table to be created as arguments.
    '''
    #Check that source table exists
    if not DBInfo.tableExists(tablename):
        print("Table " + tablename + " does not exist.")
        return
    
    #Check that destination table does not already exist
    if DBInfo.tableExists(new_tablename):
        print("Table " + new_tablename + " already exists.")
        return
    
    #Base string for command to DB
    command = "CREATE TABLE " + new_tablename + " AS SELECT "
    
    #Create string of column names separated by commas for command
    command += ", ".join(column_names) + " FROM " + tablename
    
    #Send command to database (prints error if fails)
    DBInfo.executeCommand(command)
    
def outputGeolocateCSV(tablename, filename):
    '''
    Takes a table in the local database and outputs it as a CSV file into
    script directory. Takes name of table to be copied and output filename
    as arguments. Only outputs uuid, locality, country, stateprovince and
    county which will be used in geolocation process
    '''
    if not DBInfo.tableExists(tablename):
        print("Table " + tablename + " does not exist.")
        return
    
    #Query resulting in all rows & columns
    query = "SELECT locality, country, stateprovince, county, uuid FROM " + tablename
    
    #Command to be passed to DB
    command = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
    
    #Establish connection to DB
    connection = DBInfo.connectDB()
    cursor = connection.cursor()
    
    with open(filename, "w") as file:
        cursor.copy_expert(command, file)
    
    cursor.close()
    connection.close()
    
def geopointProcessor(tablename, new_tablename):
    '''
    Retrieves geopoint information from raw data table, appends it into cleaned
    data table as lon and lat fields. Does simple lat & lon validation. Takes
    the raw data table name and cleaned data table names as arguments.
    '''
    
    #Check that given tables exist
    if not DBInfo.tableExists(tablename):
        print("Table " + tablename + " does not exist")
        return
    if not DBInfo.tableExists(new_tablename):
        print("Table " + new_tablename + " does not exist")
        return
    
    #Connect to local DB
    connection = DBInfo.connectDB()
    cursor = connection.cursor()
    
    #Try adding lon. and lat. columns to new table
    try:
        cursor.execute("ALTER TABLE " + new_tablename + " ADD COLUMN longitude DECIMAL")
        cursor.execute("ALTER TABLE " + new_tablename + " ADD COLUMN latitude DECIMAL")
    except connection.ProgrammingError as e:
        print("An error occured: ")
        print(e)
        connection.close()
        return
    
    #Commit column additions to database
    connection.commit()
    
    #Retrieve geopoint and uuid info from raw data table
    db = records.Database("postgresql://postgres:idigbio123@localhost/testdb")
    rows = db.query("SELECT uuid, geopoint FROM " + tablename)
    
    #Extract lat & lon info from each record that has it
    for row in rows:
        if row["geopoint"] != None:
            #Extract lon & lat from geopoint
            geopoint = json.loads(row["geopoint"])
            lon, lat = geopoint["lon"], geopoint["lat"]
            
            #Validate lon & lat values
            if -90 > lat > 90:
                continue
            if -180 > lon > 180:
                continue
            if lat == 0 and lon == 0:
                continue
                
            #uuid preserved as it will be used to identify the record
            uuid = row["uuid"]
            
            #Build insert command for new table, lookup done using uuid
            cmd = "UPDATE {0} SET longitude = {1}, latitude = {2} WHERE uuid = '{3}'".format(new_tablename, lon, lat, uuid)
            try:
                cursor.execute(cmd)
            except connection.ProgrammingError as e:
                connection.rollback()
                print("An error has occurred:")
                print(e)
                print("Ommitting record " + uuid)
        
        #Commit added lat & lon info into database
        connection.commit()
    
    #Terminate connection to DB
    cursor.close()
    connection.close()
            
    
    
    
    
def main():
    '''
    Main function, for testing purposes only
    '''
    columns = ["uuid", "scientificname", "locality"]
    tablename = "pumaconcolor"
    new_tablename = "pumatest"
    filename = "csvtest.csv"
    
    #outputGeolocateCSV(tablename, filename)
    
    selectColumns(columns, tablename, new_tablename)
    
    geopointProcessor(tablename, new_tablename)
    
    
    
    

if __name__ == "__main__":
    main()
    
    
    
