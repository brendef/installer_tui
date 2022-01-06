from os import name
import sqlite3

class Database:
    # Establish a connection to the database if it exists else create it
    connection = sqlite3.connect('config.db') 
    cursor = connection.cursor()

    # First check that the database doesn't already exist
    # cursor.execute('DROP TABLE IF EXISTS firewall_config;')

    # Create the table containing all the firwall configurations
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS firewall_config(
            host CHAR(50),
            package CHAR(50),
            port INT,
            enabled BOOLEAN
            );
            ''')
                        
    connection.commit()

    # Function to insert data into the database 
    # Takes in the table name first and then the row
                                                                                    # NOTE: better this function to take multiple tuples of rows 
    def insert_firewall_config(self, host, package, port, enabled):
        self.cursor.execute('''
          INSERT INTO firewall_config (host, package, port, enabled)
                VALUES
                ('{}','{}',{},{})
          '''.format(host, package, port, enabled))
     
        self.connection.commit()
    
    def all_firewall_config(self):
        self.cursor.execute("SELECT * FROM firewall_config")
        records = self.cursor.fetchall()
        return records

    def get_ports(self):
        self.cursor.execute("SELECT port FROM firewall_config")
        records = self.cursor.fetchall()
        return records

    def is_enabled(self, port):
        self.cursor.execute("SELECT enabled FROM firewall_config WHERE port = {}".format(port))
        record = self.cursor.fetchone()
        return record[0]

    def enable_all_ports(self):
        self.cursor.execute("UPDATE firewall_config SET enabled = 1 WHERE enabled = 0")
        self.connection.commit()

    def disable_all_ports(self):
        self.cursor.execute("UPDATE firewall_config SET enabled = 0 WHERE enabled = 1")
        self.connection.commit()

    def is_database_empty(self):
        self.cursor.execute("SELECT * FROM firewall_config")
        records = self.cursor.fetchall()
        if (len(records) == 0):
            return True
        else:
            return False
    
    def add_new_port(self, host, package, port, status):
        self.cursor.execute("INSERT INTO firewall_config (host, package, port, enabled) VALUES ('{}','{}',{},{})".format(host, package, port, status))
        self.connection.commit()

    def enable_port(self, name):
        print(name)
        self.cursor.execute("UPDATE firewall_config SET enabled = 1 WHERE port={}".format(name))
        self.connection.commit()
    
    def disable_port(self, name):
        self.cursor.execute("UPDATE firewall_config SET enabled = 0 WHERE port={}".format(name))
        self.connection.commit()

    def remove_port(self, port):
        self.cursor.execute("DELETE FROM firewall_config WHERE port={}".format(port))
        self.connection.commit()


    # Check that the table doesn't already exist
    def drop_ports_to_remove(self):
        self.cursor.execute('DROP TABLE IF EXISTS ports_to_remove;')
        self.connection.commit()

    # Create the table containing all the firwall configurations
    def create_ports_to_remove(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ports_to_remove(
            port INT
            );
            ''')
        
        self.connection.commit()
    
    def add_port_to_remove(self, port):
        self.cursor.execute("INSERT INTO ports_to_remove (port) VALUES ({})".format(port))
        self.connection.commit()

    def get_ports_to_remove(self):
        self.cursor.execute("SELECT * FROM ports_to_remove")
        records = self.cursor.fetchall()
        return list(records)

    # Check that the table doesn't already exist
    def drop_ports_to_enable(self):
        self.cursor.execute('DROP TABLE IF EXISTS ports_to_enable;')
        self.connection.commit()

    # Create the table containing all the firwall configurations
    def create_ports_to_enable(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ports_to_enable(
            port INT
            );
            ''')
        
        self.connection.commit()

    def add_port_to_enable(self, port):
        self.cursor.execute("INSERT INTO ports_to_enable (port) VALUES ({})".format(port))
        self.connection.commit()
    
    def get_ports_to_enable(self):
        self.cursor.execute("SELECT * FROM ports_to_enable")
        records = self.cursor.fetchall()
        return list(records)

    # Check that the table doesn't already exist
    def drop_ports_to_disable(self):
        self.cursor.execute('DROP TABLE IF EXISTS ports_to_disable;')
        self.connection.commit()

    # Create the table containing all the firwall configurations
    def create_ports_to_disable(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ports_to_disable(
            port INT
            );
            ''')
        
        self.connection.commit()

    def add_port_to_disable(self, port):
        self.cursor.execute("INSERT INTO ports_to_disable (port) VALUES ({})".format(port))
        self.connection.commit()
    
    def get_ports_to_disable(self):
        self.cursor.execute("SELECT * FROM ports_to_disable")
        records = self.cursor.fetchall()
        return list(records)
        
                        
    
        
