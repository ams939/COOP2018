import dataCleaner as dc

def cleanData(tablename, new_tablename):
    #Define columns to be selected from raw data
    columns = ["uuid", "genus", "specificepithet", "locality", "country",
               "stateprovince", "county", "datecollected"]
    
    #Use script function to select columns and add them to a new table
    dc.selectColumns(columns, tablename, new_tablename)
    
    #Extract lat, lon info from raw data and append to table created above
    dc.geopointProcessor(tablename, new_tablename)
    
    inp = input("Output CSV file of records without lon, lat info? (y/n) ")
    
    if inp == "y":
        filename = tablename + "_nullcoord.csv"
        dc.outputGeolocateCSV(new_tablename, filename)
        print("CSV file called " + filename + " has been created into script dir.")
    
    inp = input("Input a file containing georeferenced records? (y/n) ")
        if inp == y:
            inp = input("Enter the file's name: ")
            dc.inputGeolocateCSV(new_tablename, inp)
    
    dc.deleteNullPoints(tablename)
    dc.deleteDuplicates(tablename)
        
    
    
    
    

