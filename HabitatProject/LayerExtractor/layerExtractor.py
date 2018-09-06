from pathlib import Path
import gc
import rasterio
import psycopg2.extras
import DBInfo as dbi


def inputLayerValues(layer_filenames, columnnames, tablename):
    '''
    Function that samples layer data files with coordinates from local database,
    creates new columns for each layer and populates them with sampled data.
    Takes a list with layer file paths within it as first argument, list of
    column names for each layer file to be created in local database as second
    argument and the table's name as third argument
    
    '''
    #Check that table exists in local DB
    if not dbi.tableExists(tablename):
        print(f"Table {tablename} does not exist")
        return
    
    #Check that columns given don't exist already
    for col in columnnames:
        if dbi.columnExists(tablename, col):
            print(f"Column {col} already exists in {tablename}.")
            return
    
    #Check that table has lon, lat & uuid columns   
    for col in ['longitude', 'latitude', 'uuid']:
        if not dbi.columnExists(tablename, col):
            print(f"Table {tablename} does not have column {col}")
            return
    
    #Check there are as many column names as there are file names
    if len(layer_filenames) != len(columnnames):
        print("Mismatching # of layer filenames and column names to be created")
        return
    
    #Check that given file names exist
    for file in layer_filenames:
        path = Path(file)
        if not path.is_file():
            print(f"File {file} does not exist.")
            return
            
   
    #Connect to local DB
    connection = dbi.connectDB()
    cursor = connection.cursor()
    
    #Initialize columns in the local DB table, columns are of decimal type
    for col in columnnames:
        try:
            cursor.execute(f"ALTER TABLE {tablename} ADD COLUMN {col} DECIMAL")
        except connection.ProgrammingError as e:
            print(f"An error occurred: \n{e}")
            connection.close()
            return
        
        #Save changes to local DB
        connection.commit()
        
    #Get coordinate and uuid info from table    
    cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cursor.execute(f"SELECT uuid, latitude, longitude FROM {tablename}")
    records = cursor.fetchall()
    
    for i in range(0, len(layer_filenames)):
        #Attempt opening layer file
        try:
            layer = rasterio.open(layer_filenames[i])
        except rasterio.errors.RasterioIOError as e:
            print(f"An error occurred with reading layer {layer_filenames[i]}. \n{e}")
            connection.close()
            return
        
        #Column to be populated with layer data
        col_name = columnnames[i]
        
        #Read layer into program as array of pixel values
        data = layer.read(1)
        
        #Get layer's nodata value
        nodata_value = layer.nodatavals[0]
        
        #Extract uuid, lat & lon values from query
        for record in records:
            uuid = record["uuid"]
            
            #Convert from decimal.Decimal to float
            longitude, latitude = float(record["longitude"]), float(record["latitude"])
            
            #Convert CRS coordinates to array indices
            x, y = layer.index(longitude, latitude)

            #Access pixel value at coordinates within the array
            try:
                pixel_value = data[x, y]
            except IndexError as e:
                continue
            
            #If pixel value is nodata value, proceed to next record
            if pixel_value == nodata_value:
                continue
            
            #Build data insertion command
            cmd = (f"UPDATE {tablename} SET {col_name} = {pixel_value} WHERE "
                   f"uuid = '{uuid}'")
            
            #Send command to local DB
            try:
                cursor.execute(cmd)
            except connection.ProgrammingError as e:
                connection.rollback()
                print(f"An error occurred with inserting value {pixel_value} "
                      f"into column {col_name} for record {uuid}. Proceeding to "
                      "next record")
                print(e)
                continue
            
            #Save changes to DB
            connection.commit()
        
        #Free memory taken by layer data array & layer object
        del data
        layer.close()
        gc.collect()
            
    
    #Terminate connection to DB
    cursor.close()
    connection.close()
            
def deleteNullValues(columnnames, tablename):
    '''
    Deletes records that have a null value in a column listed in the 'columnnames'
    list given as an argument to the function. Second argument is table name 
    where records will be deleted from.
    '''
    #Check that table exists
    if not dbi.tableExists(tablename):
        print(f"Table {tablename} does not exist.")
        return
    
    #Check that columns given exist
    for col in columnnames:
        if not dbi.columnExists(tablename, col):
            print(f"Column {col} does not exist in {tablename}.")
            return
    
    #Connect to local DB
    connection = dbi.connectDB()
    cursor = connection.cursor()
    
    #Begin forming DB query command
    for i in range(len(columnnames)):
        columnnames[i] = columnnames[i] + " IS NULL"
        
    cmd = f"DELETE FROM {tablename} WHERE " + " OR ".join(columnnames)
    
    #Send command to local DB
    try:
        cursor.execute(cmd)
        rows_affected = cursor.rowcount
    except connection.ProgrammingError as e:
        print(f"An error occurred: \n{e}")
        connection.close()
        return
    
    #Save changes to local DB
    connection.commit()
    
    print(f"{rows_affected} rows have been deleted.")
    
    #Terminate connection to DB
    cursor.close()
    connection.close()
    

def main():
    layer_filenames = ['landcover_test.tif', 'precipitation_test.tif',
                       'elevation_test.tif', 'temperature_test.tif']
    columnnames = ['landcover','precipitation','elevation','temperature']
    tablename = 'test'
    
    inputLayerValues(layer_filenames, columnnames, tablename)

if __name__ == "__main__":
    main()