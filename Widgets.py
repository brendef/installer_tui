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
        a.FirewallStatusForm.display(a.FirewallStatusForm)

class PortChecbox(npyscreen.FormControlCheckbox):
    def whenToggled(self):
        enabled = database.is_enabled(self.name)
        if enabled:
            f.disable_port(self.name)
            database.disable_port(self.name)
        else:
            f.enable_port(self.name)
            database.enable_port(self.name)

class PortRemove(npyscreen.FormControlCheckbox):
    def whenToggled(self):
        if self.value:
            database.add_port_to_remove(self.name)

        
        


        
        


