from os import remove
import npyscreen
import Database as d
import app as a
import Functions as f

# Create the database
database = d.Database()

class SelectAllPorts(npyscreen.Checkbox):
    def whenToggled(self):
        database.enable_all_ports()

class PortChecbox(npyscreen.FormControlCheckbox):
    def whenToggled(self):
        enabled = database.is_enabled(self.name)
        if enabled:
            database.add_port_to_disable(self.name)
            # database.disable_port(self.name)
        else:
            database.add_port_to_enable(self.name)
            # database.enable_port(self.name)

    
        
        


        
        


