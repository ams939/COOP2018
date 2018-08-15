import DBInfo
import psycopg2.extras
import json
import csv

'''
The purpose of this script is to provide a variety of tools for cleaning up and
processing iDigBio data in a PostgreSQL database. This script utilizes other
custom scripts like DBInfo to work with the local database, the format of the
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
        print(f"Table {tablename} does not exist.")
        return
    
    #Check that destination table does not already exist
    if DBInfo.tableExists(new_tablename):
        print(f"Table {new_tablename} already exists.")
        return
    
    #Check that given columns exist in DB
    for column in column_names:
        if not DBInfo.columnExists(tablename, column):
            print(f"Column {column} does not exist in table {tablename}")
            return
    
    #Base string for command to DB
    command = "CREATE TABLE " + new_tablename + " AS SELECT "
    
    #Create string of column names separated by commas for command
    command += ", ".join(column_names) + " FROM " + tablename
    
    #Send command to database and commit change
    connection = DBInfo.connectDB()
    cursor = connection.cursor()
    try:
        cursor.execute(command)
    except connection.ProgrammingError as e:
        print("There was an error with the local database:")
        print(e)
        return
    
    connection.commit()
    
    print(f"Table {new_tablename} has been created.")
    
    
def outputGeolocateCSV(tablename, filename):
    '''
    Takes a table in the local database created by the select columns script
    and outputs it as a CSV file into script directory. Takes name of table to 
    be copied and output filename as arguments. Only outputs uuid, locality, 
    country, stateprovince and county which will be used in geolocation process.
    Omits records with no locality string from CSV as they cannot be georeferenced.
    '''
    if not DBInfo.tableExists(tablename):
        print(f"Table {tablename} does not exist.")
        return
    
    #Query resulting in rows & columns with NULL lon, lat and non-NULL locality string
    query = ("SELECT locality, country, stateprovince, county, latitude,"
             f" longitude, uuid FROM {tablename} WHERE locality IS NOT NULL"
             " AND (latitude IS NULL OR longitude IS NULL)")
    
    #Command to be passed to DB
    command = f"COPY ({query}) TO STDOUT WITH CSV HEADER"
    
    #Establish connection to DB
    connection = DBInfo.connectDB()
    cursor = connection.cursor()
    
    with open(filename, "w") as file:
        cursor.copy_expert(command, file)
        
    print(f"A file called {filename} containing the table {tablename}"
          " has been saved to the script's directory.")
    
    cursor.close()
    connection.close()
    

def inputGeolocateCSV(tablename, filename):
    '''
    Function that reads csv file with geolocated specimen data and stores
    results (lon & lat) in local db table. Expects csv file to be in format 
    defined in the Geolocate CSV formatting specifications.
    '''
    #Connect to database
    connection = DBInfo.connectDB()
    cursor = connection.cursor()
    
    #Check that table given exists
    if not DBInfo.tableExists(tablename):
        print(f"Table {tablename} does not exist.")
        return
    
    #Check that file given is readable
    try:
        csvfile = open(filename, "r")
        reader = csv.DictReader(csvfile)
    except IOError as e:
        print(f"File {filename} could not be read.")
        return 
  
    for row in reader:
        lat, lon = row["latitude"], row["longitude"]
        uuid = row["uuid"]
        flag = '["geolocate_georeference"]'
                
        #Skip rows with no lat or lon value
        if lat == "" or lon == "":
            continue
        
        #Build database insert command
        cmd = (f"UPDATE {tablename} SET latitude = {lat}, longitude = {lon}, "
               f"flags = '{flag}' WHERE uuid = '{uuid}'")
        
        try:
            cursor.execute(cmd)
        except connection.ProgrammingError as e:
            connection.rollback()
            print("There was an error with inputting data into the DB:")
            print(e)
            continue
            
        #Save changes to local database
        connection.commit()
    
    #Close connection to database and close file
    cursor.close()
    connection.close()
    csvfile.close()

  
def geopointProcessor(tablename, new_tablename):
    '''
    Retrieves geopoint information from raw data table, appends it into cleaned
    data table as lon and lat fields. Does simple lat & lon validation. Takes
    the raw data table name and cleaned data table names as arguments.
    '''
    
    #Check that given tables exist
    if not DBInfo.tableExists(tablename):
        print(f"Table {tablename} does not exist")
        return
    if not DBInfo.tableExists(new_tablename):
        print(f"Table {new_tablename} does not exist")
        return
    
    #Connect to local DB
    connection = DBInfo.connectDB()
    cursor = connection.cursor()
    
    #Try adding lon. and lat. columns to new table
    try:
        cursor.execute(f"ALTER TABLE {new_tablename} ADD COLUMN longitude DECIMAL")
        cursor.execute(f"ALTER TABLE {new_tablename} ADD COLUMN latitude DECIMAL")
        cursor.execute(f"ALTER TABLE {new_tablename} ADD COLUMN flags TEXT")
    except connection.ProgrammingError as e:
        print("An error occured: ")
        print(e)
        connection.close()
        return
    
    #Commit column additions to database
    connection.commit()
    
    #Retrieve geopoint and uuid info from raw data table
    cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cursor.execute(f"SELECT uuid, geopoint FROM {tablename}")
    rows = cursor.fetchall()
    
    #Extract lat & lon info from each record that has it
    for row in rows:
        if row["geopoint"] != None:
            #Extract lon & lat from geopoint
            geopoint = json.loads(row["geopoint"])
            lon, lat = geopoint["lon"], geopoint["lat"]
            flag = '["idigbio_georeference"]'
            
            #Validate lon & lat values, if invalid proceed to next record
            if -90 > lat > 90:
                continue
            if -180 > lon > 180:
                continue
            if lat == 0 and lon == 0:
                continue
                
            #uuid preserved as it will be used to identify the record
            uuid = row["uuid"]
            
            #Build insert command for new table, lookup done using uuid
            cmd = (f"UPDATE {new_tablename} SET longitude = {lon}, "
                   f"latitude = {lat}, flags = '{flag}' WHERE uuid = '{uuid}'")
            
            try:
                cursor.execute(cmd)
            except connection.ProgrammingError as e:
                connection.rollback()
                print("An error has occurred:")
                print(e)
                print(f"Ommitting record {uuid}")
                continue
        
        #Commit added lat & lon info into database
        connection.commit()
    
    print(f"Geopoint information from table {tablename} "
          f"has been successfully appended to table {new_tablename}")
    
    #Terminate connection to DB
    cursor.close()
    connection.close()
    
def selectTimeRange(tablename, start = None, end = None):
    '''
    Function for removing records from local database table that are outside
    a time range specified by the user. If end date not given, defaults to current
    date. Also removes records with null or unrealistic date. 
    Dates given in YYYY-MM-DD format.
    '''
    #Validate database table
    if not DBInfo.tableExists(tablename):
        print(f"Table {tablename} does not exist.")
        return
    if not DBInfo.columnExists(tablename, "datecollected"):
        print(f"Table {tablename} does not have column 'datecollected'")
        return
    
    #Connect to DB
    connection = DBInfo.connectDB()
    cursor = connection.cursor()
    
    #Command for removing records with null date or date in future
    cmd = (f"DELETE FROM {tablename} WHERE datecollected IS NULL OR "
           "datecollected >= CURRENT_DATE")
    
    #Send command to local database and save changes
    cursor.execute(cmd)
    connection.commit()
    
    #Determine appropriate command based on dates given
    if start == None and end == None:
        connection.close()
        return
    elif start == None and end != None:
        cmd = f"DELETE FROM {tablename} WHERE datecollected > '{end}'"
    elif start != None and end == None:
        cmd = f"DELETE FROM {tablename} WHERE datecollected < '{start}'"
    elif start != None and end != None:
        cmd = (f"DELETE FROM {tablename} WHERE datecollected < '{start}' OR "
               f"datecollected > '{end}'")
    else:
        return
    
    #Send command to local database
    try:
        cursor.execute(cmd)
    except connection.ProgrammingError as e:
        print("An error occured: ")
        print(e)
        connection.close()
        return
    
    #Save changes to local database
    connection.commit()
    
    print("Records outside specified time range have been successfully deleted")
    
    #Terminate connection to DB
    cursor.close()
    connection.close()
    
def deleteNullPoints(tablename):
    '''
    Function that deletes records in local database that have no lon, lat
    information.
    '''
    if not DBInfo.tableExists(tablename):
        print(f"Table {tablename} does not exist.")
        return
    if not DBInfo.columnExists(tablename, "longitude") or not DBInfo.columnExists(tablename, "latitude"):
        print("Table does not contain longitude or latitude column.")
        return
    
    connection = DBInfo.connectDB()
    cursor = connection.cursor()
    
    cmd = f"DELETE FROM {tablename} WHERE longitude IS NULL OR latitude IS NULL"
    
    try:
        cursor.execute(cmd)
        rows_affected = cursor.rowcount
    except connection.ProgrammingError as e:
        print("An error has occurred:")
        print(e)
        return
    
    #Save changes to the local database
    connection.commit()
    
    print(f"{rows_affected} null coordinate records have been succesfully removed.")
    
    #Terminate connection to DB
    cursor.close()
    connection.close()
    
def deleteDuplicates(tablename):
    '''
    Function that removes records with duplicate lon, lat values
    '''
    #Check that table & needed columns exist
    if not DBInfo.tableExists(tablename):
        print(f"Table {tablename} does not exist.")
        return
    if not DBInfo.columnExists(tablename, "longitude") or not DBInfo.columnExists(tablename, "latitude"):
        print("Table does not contain longitude or latitude column.")
        return
    
    #Establish connection to database
    connection = DBInfo.connectDB()
    cursor = connection.cursor()
    
    #Construct duplicate removal command
    cmd = (f"DELETE FROM {tablename} WHERE uuid NOT IN ( SELECT uuid FROM "
           f"( SELECT DISTINCT ON (longitude, latitude) * FROM {tablename} ) "
           "AS derivedtable);")
    
    #Attempt to execute command in local database
    try:
        cursor.execute(cmd)
        rows_affected = cursor.rowcount
    except connection.ProgrammingError as e:
        print("There was an error:")
        print(e)
        connection.close()
        return
    
    #Save changes & terminate connection
    connection.commit()
    cursor.close()
    connection.close()
    
    print(f"{rows_affected} duplicates successfully removed.")
    
 
def main():
    '''
    Main function, for testing purposes only
    '''
    columns = ["uuid", "scientificname", "locality"]
    tablename = "leoparduspardalis"
    new_tablename = "leoparduspardalis_cleaned"
    filename = "csvtest.csv"
    
    #outputGeolocateCSV(tablename, filename)
    
    selectColumns(columns, tablename, new_tablename)
    
    #geopointProcessor(tablename, new_tablename)
     

if __name__ == "__main__":
    main()