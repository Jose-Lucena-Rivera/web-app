import psycopg2
from flask import current_app
import os
from dotenv import load_dotenv

class BuoyDAO():
    def __init__(self):
        load_dotenv()
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    def close_connection(self):
        self.conn.close()

    def get_buoy_by_eui(self, eui):
        cursor = self.conn.cursor()

        query = "select bName from buoy where bEUI = %s;"
        cursor.execute(query, (eui,))
        bName = cursor.fetchone()[0] if cursor.rowcount > 0 else None
        print ("buoy name: ",bName)
        cursor.close()
        # self.conn.close()
        return bName
    
    def get_buoy_by_name(self, name):
        cursor = self.conn.cursor()

        query = "select bEUI from buoy where bName = %s;"
        cursor.execute(query, (name,))
        bEUI = cursor.fetchone()[0] if cursor.rowcount > 0 else None
        print ("buoy eui: ",bEUI)
        cursor.close()
        # self.conn.close()
        return bEUI
    
    def create_buoy(self, name, eui):
        cursor = self.conn.cursor()
        created = None
        try:
            query = "INSERT INTO buoy (bName, bEUI) VALUES (%s, %s) RETURNING bName, bEUI;"
            cursor.execute(query, (name, eui))
            created = cursor.fetchone()
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.conn.close()
        return created
    
    def get_all_buoys(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM buoy;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        self.conn.close()
        return result
    
    def delete_buoy(self, eui, name):
        cursor = self.conn.cursor()
        deleted = None
        try:
            query = "DELETE FROM buoy WHERE bEUI = %s AND bName = %s RETURNING bName, bEUI;"
            cursor.execute(query, (eui, name))
            deleted = cursor.fetchone()
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.conn.close()
        return deleted