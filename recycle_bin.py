import npyscreen
import subprocess
import Functions as f
class FirewallStatusConfigForm(npyscreen.ActionForm):
    actions = ["Enable", "Disable"]
    firewallStatus = f.get_ufw_status()

    def create(self):
        self.add(npyscreen.Textfield, value="UFW Current Status: {}".format(self.firewallStatus))
        self.action = self.add(npyscreen.SelectOne, name="Select an option", values=self.actions)
    
    def on_ok(self):
        if self.firewallStatus == 'active':
            npyscreen.notify_wait("You have disabled the firewall")
            subprocess.Popen("sudo ufw disable", shell=True).wait()
            self.parentApp.switchForm(None)
        else:
            npyscreen.notify_wait("You have enabled the firewall")
            subprocess.Popen("sudo ufw enable", shell=True).wait()
            self.parentApp.switchForm(None)
