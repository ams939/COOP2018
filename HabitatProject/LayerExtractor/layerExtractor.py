import rasterio
import psycopg2.extras
import DBInfo as dbi


def inputLayerValues(layer_filenames, columnnames, tablename):
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
        if not dbi.columnExists(col):
            print(f"Table {tablename} does not have column {col}")
        
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
        
    #Query coordinate and uuid info from table    
    cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cursor.execute(f"SELECT uuid, latitude, longitude FROM {tablename}")
    records = cursor.fetchall()
    
    for layer_filename in layer_filenames:
        #Attempt opening layer file
        try:
            layer = rasterio.open(layer_filename)
        except Exception as e:
            print(f"An error occurred with layer {layer_filename}. \n{e}")
            return
        
        #Extract uuid, lat & lon values from query
        for record in records:
            uuid = record["uuid"]
            longitude, latitude = record["longitude"], record["latitude"]
            
            '''
            TODO:
                Deal with no data values somehow
                Deal with indices out of range (catch exception?)
                Append data to database
            '''
            band = layer.read(1)
            x, y = layer.index(longitude, latitude)
            pixelValue = band[x, y]
        
        
            
        
        
        
        
        
    

def main():
    pass

if __name__ == "__main__":
    main()