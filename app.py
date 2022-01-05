import npyscreen
import Functions as f
import Database as d
import Widgets as w

class WelcomeForm(npyscreen.ActionForm):
    def create( self ):
        self.add(npyscreen.TitleText, name="Welcome to the installer!")
        hostname = self.add( npyscreen.TitleText, name="Enter Hostname:")
        # self.nextrely +=1
        package  = self.add( npyscreen.TitleText, name="Enter Package:")
    
    def on_ok(self):
        self.parentApp.switchForm('UFW_STATUS')

class RemovePort(npyscreen.ActionForm):
    def create(self) :
        database.drop_ports_to_remove()
        database.create_ports_to_remove()
        self.add(npyscreen.TitleText, name="Select all the ports that you would like to remove")
        ports = database.get_ports()

        for port in ports:
            self.add(w.PortRemove, name="{}".format(port[0]))                
    
    def on_ok(self):
        for port in database.get_ports_to_remove():
            database.remove_port(port[0])

        database.drop_ports_to_remove()
        self.parentApp.switchForm('UFW_STATUS')

class ConfirmPortAdded (npyscreen.ActionForm):
    def create(self):
        self.add(npyscreen.TitleText, name="Port added and activated")
    
    def on_ok(self):
        self.parentApp.switchForm('UFW_STATUS')


class FirewallStatusForm(npyscreen.ActionForm, npyscreen.FormWithMenus):
    firewallStatus = f.get_ufw_status()

    def create(self):
        self.add(npyscreen.FixedText, value="All the selected ports are already active.")
        self.add(npyscreen.FixedText, value="Uncheck enabled ports to disable them.")
        self.nextrely += 1
        self.add(npyscreen.FixedText, value="UFW Current Status: {}".format(self.firewallStatus))
        self.nextrely += 1

        if self.firewallStatus == 'active':
            ports = database.get_ports()
            self.add(w.SelectAllPorts, name="Select All")

            for port in ports:
                self.add(w.PortChecbox, name="{}".format(port[0])).value = database.is_enabled(port[0])

            self.newPort = self.add(npyscreen.TitleText, name="Add Port: ")
            self.add(npyscreen.Button, name="Add port", value_changed_callback=self.add_port)
        else:
            self.add(npyscreen.Button, name="Enable Firewall", value_changed_callback=self.toggle_firewall)
        
        self.menu = self.new_menu(name="Main Menu")
        self.menu.addItem("Turn firewall on/off", self.toggle_firewall, "t")
        self.menu.addItem("Remove port", self.remove_port, "r")

    def add_port(self, widget):
        database.add_new_port("Package", "Host", self.newPort.value, 1)
        self.parentApp.switchForm('UFW_PORT_CONFIRM')

    def remove_port(self):
        self.parentApp.switchForm('UFW_REMOVE_PORT')

    def toggle_firewall(self, widget):
        if self.firewallStatus == 'active':
            f.System("sudo ufw disable")
        else:
            f.System("sudo ufw enable")

    def exit_form(self):
        self.parentApp.switchForm(None)

    def on_ok(self):
        self.parentApp.switchForm('UFW_CONFIG')

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', WelcomeForm)
        self.addForm('UFW_STATUS', FirewallStatusForm, name="UFW Ports Configuration")
        self.addForm('UFW_PORT_CONFIRM', ConfirmPortAdded, name="UFW Port Confirmed")
        self.addForm('UFW_REMOVE_PORT', RemovePort, name="UFW Config: Remove Port")

if __name__ == "__main__":
    # Dummy data
    host = "19216811" # Grab this from pervious screen
    package = "Fullhouse" # Grab this from the previous screen

    # Get open ports
    openPorts = f.get_open_ports()

    # Convert key to integer 
    # Later try to do this from the get_open_ports() function 
    openPorts = {int(key):value for key, value in openPorts.items()}

    # This is constant
    firewallDefaultPorts = { 22 : 0, 80 : 0, 443 : 0, 9000 : 0, 3306 : 0, 10000 : 0 }

    # combine the open ports with the default ports status 
    firewallDefaultPorts.update(openPorts)

    # Install the necessary packages 
    f.System("sudo apt-get install ufw -y")

    # Create the database
    database = d.Database()

    if database.is_database_empty():
        # Insert ports into database
        for port, status in firewallDefaultPorts.items():
            database.insert_firewall_config(host, package, port, status)

    app = App().run()