import npyscreen

# Create a form object
class FormObject( npyscreen.ActionForm, npyscreen.FormWithMenus):
    # This method adds all the nessesary widgets to the installer, this will have all of the self.add() methods to add all the widgets you want
    # The self.add() function adds a takes the name of the widget you want to add first, then the peramiters such as the position, etc.
    def create( self ):
        # This is an example of a title being added 
        self.add( npyscreen.TitleText, name="Enter your first name:")
        self.add( npyscreen.TitleText, name="Enter your last name:")

        # Add a menu   
        self.menu = self.new_menu(name="Main Menu")

        # add items to the menu
        self.menu.addItem("Item 1", self.press1, "1")
        self.menu.addItem("Item 2", self.press2, "2")
        # The following is how to create a sub menu 
        # Create this and add it to a menu
        self.submenu = self.menu.addNewSubmenu("This has a sub menu", "s")    
        self.submenu.addItem("This is a submenu item", self.subitem1, "1")

        # Continuing to add items to the menu
        self.menu.addItem("Exit Form", self.exit_form, "^X")
    
    def press1( self ):
        npyscreen.notify_confirm("You pressed 1", editw=1)
        
    def press2( self ):
        npyscreen.notify_confirm("You pressed 2", editw=1)

    def subitem1( self ):
        npyscreen.notify_confirm("You pressed sub item 1", editw=1)

    def exit_form( self ):
        self.parentApp.switchForm( None )

    # This takes you to the next form in the app ( in this case the installer )
    # def afterEditing( self ):
    #     self.parentApp.setNextForm( None )
    
    def on_ok( self ):
        npyscreen.notify_wait("Goodbye", "Exit")
    
    def on_cancel(self):
        cancel = npyscreen.notify_yes_no("Would you like to save?", "Save????", editw=1)
        if(cancel):
            npyscreen.notify_wait("Form has not been saved ")
        else:
            npyscreen.notify_wait("Saving")

# This is the default form screen
class App( npyscreen.NPSAppManaged ):
    # 'Main Method' for form screen
    def onStart( self ):
        # Pass through the main form | Any arguments passed after formObject (Peramiter 3 onwards) can be used in the form
        # First peramiter takes an id, in this case it has to be called 'MAIN'
        self.addForm( 'MAIN', FormObject, name = "npyscreen form!")


# if __name__ == '__main__':
app = App()
app.run()