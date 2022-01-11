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

    def is_firewall_config_empty(self):
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
        
    # Packages
    # ---------------------

    cursor.execute('DROP TABLE IF EXISTS pip_list;')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS pip_list(
            host CHAR(50),
            package CHAR(50),
            library CHAR(100),
            installed BOOLEAN
            );
            ''')
                        
    connection.commit()

    def is_pip_list_empty(self):
        self.cursor.execute("SELECT * FROM pip_list")
        records = self.cursor.fetchall()
        if (len(records) == 0):
            return True
        else:
            return False

    def insert_pip_list(self, host, package, library, installed):
        self.cursor.execute('''
          INSERT INTO pip_list (host, package, library, installed)
                VALUES
                ('{}','{}','{}',{})
          '''.format(host, package, library, installed))
     
        self.connection.commit()
    
    def get_libraries(self):
        self.cursor.execute("SELECT library FROM pip_list")
        records = self.cursor.fetchall()
        return records
    
    def add_new_library(self, host, package, library, status):
        self.cursor.execute("INSERT INTO pip_list (host, package, library, installed) VALUES ('{}','{}','{}',{})".format(host, package, library, status))
        self.connection.commit()

    def get_total_libraries(self):
        self.cursor.execute("SELECT COUNT(*) FROM pip_list")
        count = self.cursor.fetchall()
        return count[0]
                        
    def install_all_libraries(self):
        self.cursor.execute("UPDATE pip_list SET installed = 1 WHERE installed=0")
        self.connection.commit()
        
# Apt get
    cursor.execute('DROP TABLE IF EXISTS apt_list;')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS apt_list(
            host CHAR(50),
            package CHAR(50),
            apt_package CHAR(100),
            installed BOOLEAN
            );
            ''')
                        
    connection.commit()

    def is_apt_list_empty(self):
        self.cursor.execute("SELECT * FROM apt_list")
        records = self.cursor.fetchall()
        if (len(records) == 0):
            return True
        else:
            return False

    def get_apt_packages(self):
        self.cursor.execute("SELECT apt_package FROM apt_list")
        records = self.cursor.fetchall()
        return records
    
    def add_new_apt_package(self, host, package, apt_package, status):
        self.cursor.execute("INSERT INTO apt_list (host, package, apt_package, installed) VALUES ('{}','{}','{}',{})".format(host, package, apt_package, status))
        self.connection.commit()
    
    def get_total_apt_packages(self):
        self.cursor.execute("SELECT COUNT(*) FROM apt_list")
        count = self.cursor.fetchall()
        return count[0]

    def get_apt_packages(self):
        self.cursor.execute("SELECT apt_package FROM apt_list")
        records = self.cursor.fetchall()
        return records

    def install_all_apt_packages(self):
        self.cursor.execute("UPDATE apt_list SET installed = 1 WHERE installed=0")
        self.connection.commit()

    def insert_apt_list(self, host, package, apt_package, installed):
        self.cursor.execute('''
          INSERT INTO apt_list (host, package, apt_package, installed)
                VALUES
                ('{}','{}','{}',{})
          '''.format(host, package, apt_package, installed))
     
        self.connection.commit()

    # Server Details SSH
    cursor.execute('DROP TABLE IF EXISTS server_details;')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS server_details(
            host CHAR(50),
            user CHAR(50),
            pem_address CHAR(100)
            );
            ''')
                        
    connection.commit()

    def add_server_details(self, host, user, pem_address):
        self.cursor.execute("INSERT INTO server_details (host, user, pem_address) VALUES ('{}','{}','{}')".format(host, user, pem_address))
        self.connection.commit()
    