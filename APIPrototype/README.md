## APIPrototype scripts

Below is a brief description of the scripts that make up the API Prototype. For examples of usage and further documentation, 
please see the "Data Workflow" notebook in the repository's "Jupyter Notebooks" folder.

**DEPENDENCIES** To function, these scripts require the user to install the psycopg2, records, bottle and idigbio Python modules.
All four modules can be installed via pip.
In addition, the user must have a PostgreSQL database set up and set the connection details to the database in the "DBInfo.py" and "DBQuery.py" scripts.
In "DBInfo.py", the user must set the database details in the "connectDB()" function. In "DBQuery.py", the user must set the database details in the "psqlQuery()" and "psqlGetRecord()" functions.
Make sure that the "APIServer.py" script is running before making query requests to the database with the "API.py" functions

### Scripts

**API.py** - Main user interface to the API, contains functions for all of the API's functionalities. These mainly include:


createTable(rq, tablename, limit) - Creates a table with data retrieved from iDigBio. "rq" is a dictionary containing query terms (For format see the notebook examples), "tablename" is the name of the table to be created and limit is an optional argument for limiting the no. of results returned.

searchRecords(rq, tablename, limit) - Queries a table defined in argument "tablename" in the user's PostgreSQL database using the "rq" dictionary, returns results as dictionary. For return format, see notebook examples.

viewRecord(uuid, tablename) - Queries table defined in argument "tablename" in user's PostgreSQL database using, returns record with uuid defined in argument "uuid".



**APIServer.py** - A script that launches a Bottle server which the API uses to handle requests from the user.

**DBInfo.py** - Script with functions that deal with managing a PostgreSQL database and providing information about it to the caller.

**DBQuery.py** - Script with functions that query a PostgreSQL database that contains data loaded into it using "API.py"'s "createTable()" function. Used by the "APIServer.py" script.

**iDigBioQuery.py** - Script with function that performs user's query to iDigBio's servers, using their Python API. This script is used by "TableCreator.py" to load data into the user's PostgreSQL database.

**main.py** - Placeholder script for user's script that interacts with the API. Not a functioning part of the API itself, simply an example of interacting with it.

**qsGenerator.py** - Creates a URL querystring that is sent to the API server, used by the "API.py" function to translate the user's rq dictionary into a query string.

**TableCreator.py** - Creates a table in the user's PostgreSQL database with data from iDigBio based on the rq dictionary  that the user defines in "API.py"'s "createTable()" function

**TableSchemaCreator.py** - Used by "TableCreator.py" to create the database table into which the iDigBio data is loaded. Most significantly determines the correct types for each database field.


For further  details on each scripts implementation, see the example notebook or read the comments within the scripts.


