# A sample script to create a temporary copy of a Paradox database, connect to it, and query it.
# Requires PyPyODBC: https://pypi.python.org/pypi/pypyodbc

# Written by Anthony Eden - http://mediarealm.com.au/


import os
import shutil
import pypyodbc
#"Z:\\barak\\DATA-NEW\\"
# Set this to the full fold path of your database:
DBFolder = "C:\\Users\\Eldad\\Documents\\barak\\DATA-NEW"


def DBSetupTempCopy(DBFolder):
    # Work out the path to our temporary folder
    tempFolderName = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DBTEMP")

    # Delete the temporary directory (if exists)
    shutil.rmtree(tempFolderName, True)

    # Copy this database to the temporary directory
    shutil.copytree(
        DBFolder,
        tempFolderName
    )

    # Remove existing lock files from the database
    try:
        shutil.move(os.path.join(tempFolderName, "net", "PDOXUSRS.NET"),
                    os.path.join(tempFolderName, "net", "REMOVED-PDOXUSRS.NET"))
    except:
        pass

    try:
        shutil.move(os.path.join(tempFolderName, "PDOXUSRS.LCK"), os.path.join(tempFolderName, "REMOVED-PDOXUSRS.LCK"))
    except:
        pass

    try:
        shutil.move(os.path.join(tempFolderName, "PARADOX.LCK"), os.path.join(tempFolderName, "REMOVED-PARADOX.LCK"))
    except:
        pass

    return tempFolderName


def DBConnect(folder):
    # Setup Paradox SQL DB Connection and return a cursor

    SQLConnectionString = r"Driver={{Microsoft Paradox Driver (*.db )\}};DriverID=538;Fil=Paradox 7.X;DefaultDir={0};Dbq={0};CollatingSequence=ASCII;".format(
        folder)

    dbConn = pypyodbc.connect(SQLConnectionString, autocommit=True)
    return dbConn.cursor()


def DBQuery(cur, query, params=[]):
    # Run a DB Query and return the results as a list of dicts

    cur.execute(query, params)
    headers = [item[0] for item in cur.description]
    returndata = []

    for x in cur:
        thisrow = {}
        for i, y in enumerate(x):
            thisrow[headers[i]] = y

        returndata.append(thisrow)

    return returndata


if __name__ == "__main__":
    # Copy the database to a temporary folder
    tempFolderName = DBSetupTempCopy(DBFolder)

    # Connect to the database
    cur = DBConnect(tempFolderName)

    # Perform a sample DB Query and print it
    print(DBQuery(cur, "SELECT * FROM climain""", []))


    cur.close()