import os
import sqlite3
from sqlite3 import Error

def insertDB(filePath, fileBlob): 
  try:
    conn = sqlite3.connect('app.db')
    print("[INFO] : Successful connection!")
    cur = conn.cursor()
    sql_insert_file_query = '''INSERT INTO uploads(file_name, file_blob)
      VALUES(?, ?)'''
    cur = conn.cursor()
    cur.execute(sql_insert_file_query, (filePath, fileBlob, ))
    conn.commit()
    print("[INFO] : The blob for ", filePath, " is in the database.") 
    lastEntry = cur.lastrowid
    return lastEntry
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()
    else:
      error = "An error has occurred."

def convertBinary(filePath):
  with open(filePath, 'rb') as file:
    binary = file.read()
  return binary

def readData(entry_id):
  try:
    conn = sqlite3.connect('app.db')
    cur = conn.cursor()
    print("[INFO] : Connected to SQLite to read_blob_data")
    sql_fetch_blob_query = """SELECT * from uploads where id = ?"""
    cur.execute(sql_fetch_blob_query, (entry_id,))
    record = cur.fetchall()
    for row in record:
      converted_file_name = row[1]
      photo_binarycode  = row[2]
      # parse out the file name from converted_file_name
      # Windows developers should reverse "/" to "\" to match your file path names 
      last_slash_index = converted_file_name.rfind("/") + 1 
      final_file_name = converted_file_name[last_slash_index:] 
      writeToFile(photo_binarycode, final_file_name)
      print("[DATA] : Image successfully stored on disk. Check the project directory. \n")
    cur.close()
  except sqlite3.Error as error:
    print("[INFO] : Failed to read blob data from sqlite table", error)
  finally:
    if conn:
        conn.close()

def writeToFile(binary_data, file_name):
  with open(file_name, 'wb') as file:
    file.write(binary_data)
  print("[DATA] : The following file has been written to the project directory: ", file_name)

def main():
    filePath = "/Users/Shareen/recording.wav"
    fileBlob = convertBinary(filePath)
    lastEntry = insertDB(filePath, fileBlob)
    readData(lastEntry)

if __name__ == "__main__":
    main()
