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
    def create(self):
        database.drop_ports_to_remove()
        database.create_ports_to_remove()
        self.add(npyscreen.TitleText, name="Select all the ports that you would like to remove")
        ports = database.get_ports()

        for port in ports:
            self.add(w.PortRemove, name="{}".format(port[0]))                
    
    def on_ok(self):
        for port in database.get_ports_to_remove():
            database.remove_port(port[0])
            f.disable_port(port[0])

        database.drop_ports_to_remove()
        self.parentApp.switchForm('UFW_STATUS')

class FirewallStatusForm(npyscreen.ActionForm, npyscreen.FormWithMenus):
    firewallStatus = f.get_ufw_status()

    def create(self):
        self.add(npyscreen.FixedText, value="All the selected ports are already active.")
        self.add(npyscreen.FixedText, value="Uncheck enabled ports to disable them.")
        self.nextrely += 1
        self.add(npyscreen.FixedText, value="UFW Current Status: {}".format(self.firewallStatus))
        self.nextrely += 1

        self.newPort = self.add(npyscreen.TitleText, name="add:")
        self.add(npyscreen.Button, name="Add Port", value_changed_callback = self.add_port)

        self.nextrely += 1

        self.ports = []
        self.enabledPorts = []

        if self.firewallStatus == 'active':
            for position, port in enumerate(database.get_ports()):
                if database.is_enabled(port[0]):
                    self.enabledPorts.append(position)
                self.ports.append(port[0])

            self.results = self.add(npyscreen.MultiSelect, values = self.ports).value = self.enabledPorts 
        else:
            self.add(npyscreen.Button, name="Enable Firewall", value_changed_callback=self.enable_firewall)
        
        self.menu = self.new_menu(name="Main Menu")
        self.menu.addItem("Turn firewall on/off", self.toggle_firewall, "t")

    def add_port(self, widget):
        f.enable_port(self.newPort.value)
        try:
            database.add_new_port("Package", "Host", self.newPort.value, 1)
            self.ports.append(self.newPort.value)
            self.newPort.value = ""
        except:
            pass

    def toggle_firewall(self):
        if self.firewallStatus == 'active':
            f.System("sudo ufw disable")
        else:
            f.System("sudo ufw enable")

    def enable_firewall(self, widget):
        f.System("sudo ufw enable")

    def exit_form(self):
        self.parentApp.switchForm(None)

    def on_ok(self):
        # database.disable_all_ports()
        for result in self.results.value:
            f.enable_port(self.ports[result])
            database.enable_port(self.ports[result])
        
        self.parentApp.switchForm(None)

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', WelcomeForm)
        self.addForm('UFW_STATUS', FirewallStatusForm, name="UFW Ports Configuration")

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