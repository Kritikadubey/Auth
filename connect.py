import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
from config import cred 

def check_and_create_database():
    flag = True
    try:
        connection = mysql.connector.connect(
            host = cred["dbhost"],
            user = cred["dbuser"],
            password = cred["dbpassword"]
        )
        cursor = connection.cursor()

        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()

        if (cred["dbname"],) not in databases:
            cursor.execute(f"CREATE DATABASE {cred['dbname']}")
            print("\nSuccsesfully  Created the Database\n")
        else:
            print(f"\nDatabase {cred['dbname']} already exist\n")
        
        connection.database = cred["dbname"]
        print(f"\nconnected to database {cred['dbname']}\n")

    except Error as err:
        print(f"Error:{err}")
        flag = False
    finally:
        cursor.close()
        connection.close()
        return flag
    
def check_and_create_table():
    flag = True
    try:
        connection = mysql.connector.connect(
            host = cred["dbhost"],
            user = cred["dbuser"],
            password = cred["dbpassword"],
            database = cred["dbname"]
        )
        cursor = connection.cursor()
        query = f"SHOW TABLES;"
        cursor.execute(query)
        tables = cursor.fetchall()

        if (cred["dbTableName"],) not in tables:
            print(f"\nTable {cred['dbTableName']} does not exist, Creating table...\n")
            schema = cred["dbTableSchema"]
            query = f"CREATE TABLE {cred['dbTableName']} ({schema});" 
            cursor.execute(query)
            print(f"\nTable {cred['dbTableName']} is successfully created\n")
        
        else:
            print(f"Table {cred['dbTableName']} exist\n")
            
    except Error as err:
        print(f"Error: {err}")
        flag = False
    finally:
        cursor.close()
        connection.close()
        return flag
    
def add_profile(name, gmail, password, face_id, education, proffesion, dob):
    flag = True
    try:
        connection = mysql.connector.connect(
            host = cred["dbhost"],
            user = cred["dbuser"],
            password = cred["dbpassword"],
            database = cred["dbname"]
        )
        cursor = connection.cursor()
        query = f"""
        INSERT INTO {cred["dbTableName"]}(name, gmail, password, faceid, education, proffesion, dob)
        VALUES(%s, %s, %s, %s, %s, %s, %s);
        """
        values = (name, gmail, password, face_id, education, proffesion, dob)
        cursor.execute(query, values)
        connection.commit()
        print(f"\n Profile Created ")
    except Error as err:
        print(f"Error: {err}")
        flag = False
    finally:
        cursor.close()
        connection.close()
        return flag
    
def get_password(email):
    password = None
    try:
        connection = mysql.connector.connect(
            host = cred["dbhost"],
            user = cred["dbuser"],
            password = cred["dbpassword"],
            database = cred["dbname"]
        )
        cursor = connection.cursor()
        
        query = f"SELECT password FROM {cred['dbTableName']} WHERE gmail = %s;"
        cursor.execute(query, (email,))
        
        password = cursor.fetchone()
    except Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()
        return password

    
def get_faceid(email):
    faceid = None
    try:
        connection = mysql.connector.connect(
            host = cred["dbhost"],
            user = cred["dbuser"],
            password = cred["dbpassword"],
            database = cred["dbname"]
        )
        cursor = connection.cursor()
        query = f"""
        select faceid from {cred["dbTableName"]} where gmail = %s;
        """
        cursor.execute(query, (email,))
        faceid = cursor.fetchone()
    except Error as err:
        print(f"Error : {err}")
    finally:
        cursor.close()
        connection.close()
        return faceid

def get_profile(email):
    profile = None
    try:
        connection = mysql.connector.connect(
            host = cred["dbhost"],
            user = cred["dbuser"],
            password = cred["dbpassword"],
            database = cred["dbname"]
        )
        cursor = connection.cursor()
        query = f"""
        select accno, name, dob, education, PROFFESION from {cred["dbTableName"]} where gmail = %s;
        """
        cursor.execute(query, (email,))
        profile = cursor.fetchone()
    except Error as err:
        print(f"Error : {err}")
    finally:
        cursor.close()
        connection.close()
        return profile

async def store_otp(email, otp):
    flag = True
    try:
        connection = mysql.connector.connect(
            host = cred["dbhost"],
            user = cred["dbuser"],
            password = cred["dbpassword"],
            database = cred["dbname"]
        )
        cursor = connection.cursor()
        expire_time = datetime.now() + timedelta(minutes=5)
        query = "INSERT INTO otp_table (email, otp_code, expires_at) VALUES (%s, %s, %s)"
        cursor.execute(query, (email, otp, expire_time))
        connection.commit()
    except Exception as error:
        print(f"Error: ", error)
        flag = False
    finally:
        cursor.close()
        connection.close()
        return flag

def validate_otp(email, input_otp):
    message = ""
    status = None
    try:
        connection = mysql.connector.connect(
            host = cred["dbhost"],
            user = cred["dbuser"],
            password = cred["dbpassword"],
            database = cred["dbname"]
        )
        cursor = connection.cursor()
        query = "SELECT otp_code, expires_at FROM otp_table WHERE email = %s ORDER BY created_at DESC LIMIT 1"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result:
            stored_otp, expires_at = result
            if datetime.now() > expires_at:
                message = "OTP has expire !"
                status = False
            elif stored_otp == input_otp:
                print("OTP is valid!")
                message = "OTP is valid!"
                status = True
            else:
                message = "Invalid OTP"
                status = False
        else:
            message = "No OTP found for this email"
            status = False 
    except Exception as e:
        print("Error: ", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return {"status" : status, "description" : message}

if __name__ == "__main__":
    check_and_create_database()
    check_and_create_table()
