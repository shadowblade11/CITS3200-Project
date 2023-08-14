import os
import platform
import sqlite3
from sqlite3 import Error



# deleteRecord and checkTables just for debugging purposes
def deleteRecord():
    try:
        connect = sqlite3.connect('app.db')
        cursor = connect.cursor()
        print("Connected to SQLite")

        # Deleting single record now
        sql_delete_query = """DELETE from uploads"""
        cursor.execute(sql_delete_query)
        connect.commit()
        print("Record deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if connect:
            connect.close()
            print("the sqlite connection is closed")

def checkTables():
  try:
    connect = sqlite3.connect('app.db')
    print("[INFO] : Successful connection!")

    # Getting all tables from sqlite_master
    sql_query = """SELECT name FROM sqlite_master
    WHERE type='table';"""
    cursor = connect.cursor()
    cursor.execute(sql_query)
    print("\nList of tables")
    print(cursor.fetchall())
    
    # Display files in DB
    print('\nFiles in uploads table:')
    data=cursor.execute('''SELECT file_name FROM uploads''')
    for column in data:
        print(column)
    
  except sqlite3.Error as error:
    print("[INFO]: Failed to execute the above query", error)    
  finally:
    if connect:
        connect.close()

def insertDB(filePath, fileBlob):
  try:
    connect = sqlite3.connect('app.db')
    print("[INFO] : Successful connection!")
    cur = connect.cursor()
    sqlInsertFileQuery = '''INSERT INTO uploads(file_name, file_blob)
      VALUES(?, ?)'''
    cur = connect.cursor()
    cur.execute(sqlInsertFileQuery, (filePath, fileBlob,))
    connect.commit()
    print("[INFO] : The blob for ", filePath, " is in the database.")
    lastEntry = cur.lastrowid
    return lastEntry
  except Error as e:
    print(e)
  finally:
    if connect:
      connect.close()
    else:
      error = "An error has occurred"

def convertBinary(filePath):
  with open(filePath, 'rb') as file:
    binary = file.read()
  return binary

def readBlobData(entryID):
  try:
    connect = sqlite3.connect('app.db')
    cur = connect.cursor()
    print("[INFO] : Connected to SQLite to readBlobData")
    sqlFetchBlobQuery = """ SELECT * from uploads where id = ?"""
    cur.execute(sqlFetchBlobQuery, (entryID,))
    record = cur.fetchall()
    for row in record:
      convertedFileName = row[1]
      photoBinCode = row[2]
      if platform.system() == "Windows":
        lastSlashIndex = convertedFileName.rfind("\\") + 1
      else:
        lastSlashIndex = convertedFileName.rfind("/") + 1
      finalFileName = convertedFileName[lastSlashIndex:]
      writeToFile(photoBinCode, finalFileName)
      print("[DATA] : Image successfully stored on disk. Check the working directory. \n")
    cur.close()
  except sqlite3.Error as error:
    print("[INFO] : Failed to read blob data from sqlite table", error)
  finally:
    if connect:
      connect.close()

def writeToFile(binData, fileName):
  with open(fileName, 'wb') as file:
    file.write(binData)
  print("[DATA] : The following file has been written to the working directory: ", fileName)

#right now this is just called from the soundTest.py to store the recordings in the upload and will retrieve the latest entry in the db
def storeRecording(fileName):
  filePath = fileName
  file_blob = convertBinary(filePath)
  lastEntry = insertDB(filePath, file_blob)
  readBlobData(lastEntry)

#if need to store italian audio but can set up when webpage is settled
def storeAudio(fileName):  
  filePath = fileName
  file_blob = convertBinary(filePath)
  lastEntry = insertDB(filePath, file_blob)
  readBlobData(lastEntry)

def main():
  #filePath = ""
  #file_blob = convertBinary(filePath)
  #lastEntry = insertDB(filePath, file_blob)
  #readBlobData(lastEntry)
  checkTables()
  deleteRecord()

if __name__ == "__main__":
    main()



