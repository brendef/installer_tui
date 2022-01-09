from os import name
import npyscreen
import Functions as f
import Database as d
import Widgets as w
import PipList as p

class PreviousForm(npyscreen.ActionForm):
    OK_BUTTON_TEXT = "--->"
    def create(self):
        self.add(npyscreen.TitleText, name="This is the step before the UFW Settings")

    def on_ok(self):
        self.parentApp.switchForm('PACKAGE_SELECT')

class PackageSelect(npyscreen.ActionForm):
    OK_BUTTON_TEXT = "--->"
    CANCEL_BUTTON_TEXT = "<---"

    def create(self):
        self.add(npyscreen.FixedText, value="The following pip packages/libraries will be installed", )
        
        self.nextrely += 1

        self.newLibrary = self.add(npyscreen.TitleText, name="add:")
        self.add(npyscreen.Button, name="Add Library", value_changed_callback = self.add_library) 

        self.libraries = []

        for library in database.get_libraries():
            self.libraries.append(library[0])

        self.result = self.add(npyscreen.MultiLine, values=self.libraries)
    
    def add_library(self, widget):
        try:
            database.add_new_library("Package", "Host", self.newLibrary.value, 0)
            self.libraries.append(self.newLibrary.value)
            self.newLibrary.value = ""
        except:
            pass

    def on_ok(self):
        self.parentApp.switchForm('PACKAGE_INSTALL')

class PackageInstall(npyscreen. FormBaseNew):
    def create(self):
        self.loadingBar = self.add(npyscreen.Slider)
        self.installPackages
        
    def installPackages(self):
        for library in database.get_libraries():
            f.pip_install(library[0])
            self.loadingBar.value += 25

class NextForm(npyscreen.ActionForm):
    OK_BUTTON_TEXT = "--->"
    CANCEL_BUTTON_TEXT = "<---"

    def create(self):
        self.add(npyscreen.TitleText, name="This is the next step in the installer")
    
    def on_ok(self):
        self.parentApp.switchForm(None)
    
    def on_cancel(self):
        self.parentApp.setNextFormPrevious()

class FirewallToggleForm(npyscreen.ActionForm):
    OK_BUTTON_TEXT = "--->"
    CANCEL_BUTTON_TEXT = "<---"

    firewallStatus = f.get_ufw_status()

    def create(self):
        self.status = self.add(npyscreen.Textfield, value="UFW Current Status: {}".format(self.firewallStatus))

        if f.boolean_firewall(self.firewallStatus):
            self.toggleFirewallButton = self.add(npyscreen.ButtonPress, name="Disable", when_pressed_function = self.toggle_firewall)
        else:
            self.toggleFirewallButton = self.add(npyscreen.ButtonPress, name="Enable", when_pressed_function = self.toggle_firewall)

    def toggle_firewall(self):
        if self.firewallStatus == "active":
            self.disable_ufw()
        else:
            self.enable_ufw()

    def enable_ufw(self):
        npyscreen.notify_wait("Activating UFW")
        f.enable_firewall()
        self.firewallStatus = "active"
        self.status.value = "UFW Current Status: active"
        self.toggleFirewallButton.name = "Disable"
        self.parentApp.switchForm('UFW_CONFIG')

    def disable_ufw(self):
        npyscreen.notify_wait("Disabling UFW")
        f.disable_firewall()
        self.firewallStatus = "inactive"
        self.status.value = "UFW Current Status: inactive"
        self.toggleFirewallButton.name = "Enable"
        self.parentApp.switchForm('NEXT')

    def on_ok(self):
        if self.firewallStatus == 'active':
            self.parentApp.switchForm('UFW_CONFIG')
        else:
            self.parentApp.switchForm('NEXT')

    def on_cancel(self):
        self.parentApp.setNextFormPrevious()


class FirewallStatusForm(npyscreen.ActionForm):

    OK_BUTTON_TEXT = "--->"
    CANCEL_BUTTON_TEXT = "<---"

    def create(self):
        self.add(npyscreen.FixedText, value="All the selected ports are already active.")
        self.add(npyscreen.FixedText, value="Uncheck enabled ports to disable them.")
        self.nextrely += 1

        self.newPort = self.add(npyscreen.TitleText, name="add:")
        self.add(npyscreen.Button, name="Add Port", value_changed_callback = self.add_port) 

        self.nextrely += 1

        self.ports = []
        self.enabledPorts = []

        for position, port in enumerate(database.get_ports()):
            if database.is_enabled(port[0]):
                self.enabledPorts.append(position)
            self.ports.append(port[0])

        self.result = self.add(npyscreen.MultiSelect, values=self.ports).value = self.enabledPorts
               
    def add_port(self, widget):
        f.enable_port(self.newPort.value)
        try:
            database.add_new_port("Package", "Host", self.newPort.value, 1)
            self.ports.append(self.newPort.value)
            self.newPort.value = ""
        except:
            pass

    def on_ok(self):
        npyscreen.notify_wait("Confguring ports")
        for port in f.get_open_ports():
            f.disable_port(port)
        database.disable_all_ports()
        for result in self.result:
            f.enable_port(self.ports[result])
            database.enable_port(self.ports[result])
        
        self.parentApp.switchForm('NEXT')
    
    def on_cancel(self):
        self.parentApp.setNextFormPrevious()

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', PreviousForm)
        self.addForm('PACKAGE_SELECT', PackageSelect, name="Pip Packages/Libraries")
        self.addForm('PACKAGE_INSTALL', PackageInstall, name="Installing Libraries")
        self.addForm('UFW_TOGGLE', FirewallToggleForm, name="UFW Enable/Disable")
        self.addForm('UFW_CONFIG', FirewallStatusForm, name="UFW Ports Configuration")
        self.addForm('NEXT', NextForm)

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

    if database.is_firewall_config_empty():
        # Insert ports into database
        for port, status in firewallDefaultPorts.items():
            database.insert_firewall_config(host, package, port, status)

    # packages
    # ----------------

    if database.is_pip_list_empty():
        # Insert packages into database
        for library in p.PipList:
            database.insert_pip_list(host, package, library, 0)

    app = App().run()