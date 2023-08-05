''' Abstract class containing general methods for any interface'''

import PyQt5.QtCore as QtCore
import logging
import json
import os
import importlib

class abstract_interface():
    def __init__(self, app, mainwindow,name_logger=None,config=None):
        """
        Abstract class for high-level interface with devices
        ...

        Attributes
        ----------
        settings : dict
            settings of this interface (typically loaded from a .json file or set in the _init_ method of the instance)
        output : dict
            a dictionary containing the output data created by this interface
        app : Qt.QApplication
            The pyqt5 QApplication() object
        mainwindow  : Qt.QWidget
            The main window of the Qt application
        gui : gui()
            instance of the class gui(), containing all guis element and basic function to set different states
        verbose : bool
            Sets wheter the logger of this interface will be verbose or not (default = True)
        name_logger : str
            Name of the logger of this interface (default = __package__). The logger formatter will be "[name_logger]:...".


        Methods
        -------
        close()
            Closes this interface, disconnect device (if any) and close plot window
        set_trigger()
        send_trigger()
        update()
        create_gui(parent)
        

        """
        self.mainwindow = mainwindow
        self.app = app
        self.mainwindow.child = self    #make sure that the window embedding this interface knows about its child (this is mainly used to link the closing events when using multiple windows)
 
        self._verbose = True            #Keep track of whether this instance of the interface should produce logs or not

        if name_logger == None:
            name_logger = importlib.import_module(self.__module__).__package__    # Use importlib to retrieve the name of the package which is using this abstract class

        self.name_logger = name_logger #Setting this property will also create the logger,set the default output style, and store the logger object in self.logger   

        if not config: #If the dictionary config was not specified as input, we check if there is a config.json file in the package folder, and load that
            #we load its keys-values as properties of this object
            try:
                m = importlib.import_module(self.__module__)    # Use importlib to retrieve path of child class
                folder_package = os.path.dirname(os.path.abspath(m.__file__))
                self.config_file = os.path.join(folder_package,'config.json')
                with open(self.config_file) as jsonfile:
                    config = json.load(jsonfile)
            except:
                pass
        if config:
            self.load_settings(config)

    def create_gui(self,parent, **kwargs): 
        '''
            parent, QWidget        
                a QWidget (or QMainWindow) object that will be the parent for the gui of this device.
                When this script is ran on its own (i.e. not within another gui) self.mainwindow and parent are actually the same object
        '''
        #It's importat to split the following step into two lines, the first creates the attribute gui for this interface, the second one initialize the gui
        self.gui = self.gui_class(self,parent,**kwargs) #Initialize an instance of the gui class corresponding to this interface. gui_class must be specified as attribute of the child class
        self.gui.initialize() 

    def load_settings(self,dictionary):
        for k, v in dictionary.items():
            self.settings[k] = v
            if k == 'verbose': # Need to implement this better...
                self.verbose = bool(v)
            #setattr(self.settings, k, v)

    def save_settings(self):
        if self.config_file:
            self.logger.info(f"Storing current settings for this device into the file \'{self.config_file}\'...")
            try:
                with open(self.config_file, 'w') as fp:
                    json.dump(self.settings, fp, indent=4, sort_keys=True)
            except Exception as e:
                self.logger.error(f"An error occurred while saving settings in the config.json file: {e}")
    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self,verbose):
        self._verbose = verbose
        #When the verbose property of this interface is changed, we also update accordingly the level of the logger object
        if verbose: loglevel = logging.INFO
        else: loglevel = logging.CRITICAL
        self.logger.setLevel(level=loglevel)

    @property
    def name_logger(self):
        return self._name_logger

    @name_logger.setter
    def name_logger(self,name):
        #Create logger, and set default output style.
        self._name_logger = name
        self.logger = logging.getLogger(self._name_logger)
        self.verbose = self._verbose #This will automatically set the logger verbosity too
        if not self.logger.handlers:
            formatter = logging.Formatter(f"[{self.name_logger}]: %(message)s")
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)
        self.logger.propagate = False

    def set_trigger(self,external_function,delay=0):
        '''
        This method allows to use this device as a trigger for other operations. Every time that this interface object acquires data from the device (i.e. every time 
        the function self.update is executed), the function external_function is also called. external_function must be a valid function which does not 
        require any input parameter.
        The optional parameter delay sets a delay (in seconds) between the call to the function update and the call to the function external_function
        When external_function is set to None, the trigger is effectively disabled.
        '''
        if external_function == None:
            self.trigger = None
            return
        if not(callable(external_function)):
            self.logger.error(f"Input parameter external_function must be a valid function")  
            return  
        self.logger.info(f"Creating a trigger for this device...")
        self.trigger = [external_function, delay]

    def send_trigger(self):
        if(self.trigger[1])>0:
            self.logger.info(f"Trigger will be sent in {self.trigger[1]} seconds.")
            QtCore.QTimer.singleShot(int(self.trigger[1]*1e3), self._send_trigger)
        else:
            self._send_trigger()

    def _send_trigger(self):
        self.logger.info(f"Trigger sent.")
        self.trigger[0]()

    def update(self):
        if hasattr(self,'trigger'):
            if not(self.trigger==None):
                self.send_trigger()

    def wait_until_property_is_false(self,instance,property_,actions,refresh_time=0.01):
        if property_.fget( instance ) == True:
            QtCore.QTimer.singleShot(int(refresh_time*1e3), lambda :  self.wait_until_property_is_false(instance,property_,actions,refresh_time))
        else:
            for action in actions:
                action()

    def wait_until_property_is_true(self,instance,property_,actions,refresh_time=0.01):
        if property_.fget( instance ) == False:
            QtCore.QTimer.singleShot(int(refresh_time*1e3), lambda :  self.wait_until_property_is_false(instance,property_,actions,refresh_time))
        else:
            for action in actions:
                action()

    def close(self):     
        self.save_settings()
        try:
            if (self.instrument.connected == True):
                self.disconnect_device()
        except Exception as e:
            self.logger.error(f"{e}")


class abstract_gui():
    def __init__(self,interface,parent):
        """
        Attributes specific for this class (see the abstract class ergastirio_abstract_instrument.abstract_gui for general attributes)
        ----------
        interface
            instance of the interface class defined above
        parent
            Qt widget which will host the GUI
        """
        self.interface = interface
        self.parent = parent

    def initialize(self):
        self.parent.setLayout(self.container) 
        self.parent.resize(self.parent.minimumSize())
        return

    def disable_widget(self,widgets):
        for widget in widgets:
            if widget:
                widget.setEnabled(False)   

    def enable_widget(self,widgets):
        for widget in widgets:
            if widget:
                widget.setEnabled(True) 
