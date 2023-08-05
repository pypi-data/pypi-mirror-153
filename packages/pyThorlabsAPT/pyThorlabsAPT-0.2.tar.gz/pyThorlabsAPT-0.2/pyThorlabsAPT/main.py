import os
import PyQt5
dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
import PyQt5.QtWidgets as Qt# QApplication, QWidget, QMainWindow, QPushButton, QHBoxLayout
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import logging
import sys
import argparse

import abstract_instrument_interface
from pyThorlabsAPT.driver import pyThorlabsAPT

graphics_dir = os.path.join(os.path.dirname(__file__), 'graphics')

class interface(abstract_instrument_interface.abstract_interface):
    """
    Create a high-level interface with the device, and act as a connection between the low-level
    interface (i.e. the driver) and the gui.
    Several general-purpose attributes and methods are defined in the class abstract_interface defined in abstract_instrument_interface
    ...

    Attributes specific for this class (see the abstract class abstract_instrument_interface.abstract_interface for general attributes)
    ----------
    instrument
        Instance of driver.pyThorlabsAPT
    connected_device_name : str
        Name of the physical device currently connected to this interface 
    continuous_read : bool 
        When this is set to True, the data from device are acquired continuosly at the rate set by refresh_time
    refresh_time : float, 
        The time interval (in seconds) between consecutive reeading from the device driver (default = 0.2)
    stored_data : list
        List used to store data acquired by this interface
    power_units : str
        The power units of this device
    current_power_string : str 
        Last power read from powermeter, as a string

    Methods
    -------


    """

    output = {'Position':0}  #We define this also as class variable, to make it possible to see which data is produced by this interface without having to create an object

    def __init__(self, **kwargs):
        self.output = {'Position':0} 

        ### Default values of settings (might be overlapped by settings saved in .json files later)
        self.settings = {   'step_size': 1,
                            'ramp_step_size': 1,
                            'ramp_wait_1': 1,
                            'ramp_wait_2': 1,
                            'ramp_numb_steps': 10,
                            'ramp_repeat': 1,
                            'ramp_reverse': 1,
                            'ramp_send_initial_trigger': 1
                            }

        self.list_devices = []          #list of devices found 
        self.connected_device_name = ''
        self._units = ['mm','deg']
        self.doing_ramp = False #Flag variable used to keep track of when a ramp is being done
        ###
        self.instrument = pyThorlabsAPT() 
        ###
        self.gui_class = gui
        ###
        super().__init__(**kwargs)

############################################################
### Functions to interface the GUI and low-level driver
############################################################

    def refresh_list_devices(self):
        '''
        Get a list of all devices connected, by using the method list_devices() of the driver. For each device obtain its identity and its address.
        For each device, create the string "identity -->  address" and add the string to the corresponding combobox in the GUI 
        '''
        
        #First we empty the combobox
        self.gui.combo_Devices.clear()
        
        #Then we read the list of devices
        self.logger.info(f"Looking for devices...") 
        list_valid_devices = self.instrument.list_devices()
        if(len(list_valid_devices)>0):
            list_IDNs_and_devices = [str(dev[1]) + " --> " + str(dev[0]) for dev in list_valid_devices] 
            #list_IDNs_and_devices = [i for i in list_IDN] 
            self.gui.combo_Devices.addItems(list_IDNs_and_devices)  
        self.logger.info(f"Found {len(list_valid_devices)} devices.") 

    def connect_device(self,device_full_name):
        if(device_full_name==''): # Check  that the name is not empty
            self.logger.error("No valid device has been selected")
            return
        self.set_connecting_state()
        device_name = device_full_name.split(' --> ')[0].lstrip() # We extract the device address from the device name
        self.logger.info(f"Connecting to device {device_name}...")
        ID = self.instrument.connect_device(device_name) # Try to connect by using the method ConnectDevice of the powermeter object
        if(ID==1):  #If connection was successful
            self.logger.info(f"Connected to device {device_name}.")
            self.connected_device_name = device_name
            self.set_connected_state()
        else: #If connection was not successful
            self.logger.error(f"Error: {Msg}")
            self.set_disconnected_state()
            pass

    def disconnect_device(self):
        self.logger.info(f"Disconnecting from device {self.connected_device_name}...")
        self.set_disconnecting_state()
        (Msg,ID) = self.instrument.disconnect_device()
        if(ID==1): # If disconnection was successful
            self.logger.info(f"Disconnected from device {self.connected_device_name}.")
            #self.continuous_read = 0 # We set this variable to 0 so that the continuous reading from the powermeter will stop
            self.set_disconnected_state()
        else: #If disconnection was not successful
            self.logger.error(f"Error: {Msg}")
            self.set_disconnected_state() #When disconnection is not succeful, it is typically because the device alredy lost connection
                                          #for some reason. In this case, it is still useful to have the widget reset to disconnected state      
    def set_disconnecting_state(self):
        self.gui.set_disconnecting_state()   
        
    def set_disconnected_state(self):
        self.gui.set_disconnected_state()

    def set_connecting_state(self):
        self.gui.set_connecting_state()

    def set_connected_state(self):
        self.gui.set_connected_state()
        self.read_position()
        self.read_stage_info()
        
    def set_step_size(self, s):
        try: 
            step_size = float(s)
            if self.settings['step_size'] == step_size: #if the value passed is the same as the one currently stored, we end here
                return True
        except ValueError:
            self.logger.error(f"The step size must be a valid number.")
            self.gui.edit_StepSize.setText(f"{self.settings['step_size']:.4f}")
            return False
        # if refresh_time < 0.001:
        #     self.logger.error(f"The refresh time must be positive and >= 0.001.")
        #     self.gui.edit_MoveStep.setText(f"{self.step_size:.4f}")
        #    return False
        self.logger.info(f"The step size is now {step_size}.")
        self.settings['step_size'] = step_size
        self.gui.edit_StepSize.setText(f"{self.settings['step_size']:.4f}")
        return True

    def move_single_step(self,direction,step_size = None):
        if step_size == None:
            step_size = self.settings['step_size']
        movement = direction*step_size
        self.logger.info(f"Will move by {movement}. Begin moving...")
        self.instrument.move_by(movement)
        self.gui.set_moving_state()
        self.wait_until_property_is_false(self.instrument,pyThorlabsAPT.is_in_motion,[self.end_movement])
        self.wait_until_property_is_false(self.instrument,pyThorlabsAPT.is_in_motion,[self.gui.set_non_moving_state])
        
    def end_movement(self):
        self.read_position()
        self.logger.info(f"Movement ended. New position = {self.output['Position']}")

    def read_stage_info(self):
        #From the thorlabs_APT code:
        #    # Stage units
        #    STAGE_UNITS_MM = 1
        #    """Stage units in mm"""
        #    STAGE_UNITS_DEG = 2
        #    """Stage units in degrees"""
        self.stage_info = self.instrument.get_stage_axis_info()
        self.gui.edit_min_pos.setText(str(self.stage_info[0])) 
        self.gui.edit_max_pos.setText(str(self.stage_info[1])) 
        self.gui.edit_pitch.setText(str(self.stage_info[3])) 
        self.gui.edit_pitch.setCursorPosition(0)
        if (self.stage_info[2] in [1,2]):
            self.gui.combo_units.setCurrentText(self._units[self.stage_info[2]-1])

    def set_stage_info(self, min_pos, max_pos, units, pitch):
        try: 
            min_pos = float(min_pos)
            max_pos = float(max_pos)
            pitch = float(pitch)
        except ValueError:
            self.logger.error(f"min_pos, max_pos, and pitch must be valid numbers.")
            return False
        if not units in self._units:
            self.logger.error(f"Value of units is not valid.")
            return False
        try:
            self.instrument.set_stage_axis_info(min_pos,max_pos, self._units.index(units)+1 , pitch)
        except:
            self.logger.error(f"Some error occurred when setting stage parameters.")
            return False
        self.logger.info(f"Stage parameters set correctly.")
        self.read_stage_info()

    def read_position(self):
        self.output['Position'] = self.instrument.position
        self.gui.edit_Position.setText(str(self.output['Position'] ))
        
    def set_position(self,position):
        try:
            position = float(position)
        except:
            return
        self.logger.info(f"Moving to {position}...")
        self.instrument.position = position
        self.gui.set_moving_state()
        self.wait_until_property_is_false(self.instrument,pyThorlabsAPT.is_in_motion,[self.end_movement])
        self.wait_until_property_is_false(self.instrument,pyThorlabsAPT.is_in_motion,[self.gui.set_non_moving_state])
        
    def start_ramp(self,initial_trigger, stepsize, wait1, wait2, numb_steps, add_reverse = False, repeat_ramp=1):
        ###TO ADD: sanity check on input parameters

        #Store parameters in the settings dict
        self.settings['ramp_send_initial_trigger'] = initial_trigger
        self.settings['ramp_step_size'] = stepsize
        self.settings['ramp_wait_1'] =  wait1
        self.settings['ramp_wait_2'] =  wait2
        self.settings['ramp_numb_steps'] = numb_steps
        self.settings['ramp_repeat'] = repeat_ramp
        self.settings['ramp_reverse'] = add_reverse

        #generate a list of actions that define the ramp
        action =[]
        if initial_trigger:
            action.append({'action':'send_trigger'})
        for j in range(repeat_ramp): #when repeat_ramp > 1, the whole ramp is repeated multiple times
            for i in range(numb_steps):
                action.append({'action':'move', 'stepsize':stepsize})
                action.append({'action':'wait', 'time':wait1})
                action.append({'action':'send_trigger'})
                action.append({'action':'wait', 'time':wait2})
            if add_reverse:
                for i in range(numb_steps):
                    action.append({'action':'move', 'stepsize':-stepsize})
                    action.append({'action':'wait', 'time':wait1})
                    action.append({'action':'send_trigger'})
                    action.append({'action':'wait', 'time':wait2})
        self.logger.info(f"Starting ramp...")
        self.gui.set_doingramp_state()
        self.doing_ramp = True
        self.run_sequence(action)
    
    def stop_ramp(self):
        self.doing_ramp = False
        self.gui.set_notdoingramp_state()
        self.logger.info(f"Ramp stopped.")
        
    def run_sequence(self,sequence):
        self.sequence = sequence
        self._run_sequence(0)
        
    def _run_sequence(self,index):
        if index >= len(self.sequence):
            self.logger.info(f"Sequence terminated.")
            self.doing_ramp = False
            self.gui.set_notdoingramp_state()
            return
        if self.doing_ramp == False:
            return
        current_action = self.sequence[index]
        if current_action['action'] == 'move':
            self.logger.info(f"Will move by {current_action['stepsize']}. Begin moving...")
            self.instrument.move_by(current_action['stepsize'])
            self.wait_until_property_is_false(self.instrument,pyThorlabsAPT.is_in_motion,[self.end_movement,lambda: self._run_sequence(index+1)])
        if current_action['action'] == 'wait':
            self.logger.info(f"Waiting for {float(current_action['time'])} s...")
            QtCore.QTimer.singleShot(int(current_action['time']*1e3), lambda :  self._run_sequence(index+1))
        if current_action['action'] == 'send_trigger':
            self.update() #the method update is defined in the super class abstract_interface, it will send a trigger to an external function if any trigger is defined
            self._run_sequence(index+1)

    #### END Functions to talk with low-level driver
    
    
class gui(abstract_instrument_interface.abstract_gui):
    def __init__(self,interface,parent):
        super().__init__(interface,parent)
       
    def initialize(self):
        self.create_widgets()

        ### SET INITIAL STATE OF WIDGETS
        self.edit_StepSize.setText(str(self.interface.settings['step_size']))
        self.checkbox_Initial_trigger.setChecked(bool(self.interface.settings['ramp_send_initial_trigger']))
        self.edit_StepSize_ramp.setText(str(self.interface.settings['ramp_step_size']))
        self.edit_Wait1_ramp.setText(str(self.interface.settings['ramp_wait_1']))
        self.edit_Wait2_ramp.setText(str(self.interface.settings['ramp_wait_2']))
        self.spinbox_Ramp_steps.setValue(int(self.interface.settings[ 'ramp_numb_steps']))
        self.checkbox_Reverse.setChecked(bool(self.interface.settings['ramp_reverse']))
        self.spinbox_Ramp_repeat.setValue(int(self.interface.settings[ 'ramp_repeat']))
        self.click_button_refresh_list_devices()    #By calling this method, as soon as the gui is created we also look for devices
        self.set_disconnected_state()               #When GUI is created, all widgets are set to the "Disconnected" state
        ###

        self.connect_widgets_events_to_functions()

        ### Call the initialize method of the parent class
        super().initialize()

    def create_widgets(self):
        hbox1 = Qt.QHBoxLayout()
        self.label_DeviceList = Qt.QLabel("Devices: ")
        self.combo_Devices = Qt.QComboBox()
        #self.combo_Devices.resize(self.combo_Devices.sizeHint())
        self.button_RefreshDeviceList = Qt.QPushButton("")
        self.button_RefreshDeviceList.setIcon(QtGui.QIcon(os.path.join(graphics_dir,'refresh.png')))
        hbox1.addWidget(self.label_DeviceList)
        hbox1.addWidget(self.combo_Devices, stretch=1)
        hbox1.addWidget(self.button_RefreshDeviceList)
        #hbox1.addStretch(1)

        hbox2 = Qt.QHBoxLayout()
        self.button_ConnectDevice = Qt.QPushButton("Connect")
        self.label_Position = Qt.QLabel("Position: ")
        self.edit_Position = Qt.QLineEdit()
        self.edit_Position.setAlignment(QtCore.Qt.AlignRight)
        #self.label_PositionUnits = Qt.QLabel(" deg")
        self.label_Move = Qt.QLabel("Move: ")
        self.button_MoveNegative = Qt.QPushButton("<")
        self.button_MoveNegative.setToolTip('')
        self.button_MoveNegative.setMaximumWidth(30)
        self.button_MovePositive = Qt.QPushButton(">")
        self.button_MovePositive.setToolTip('')
        self.button_MovePositive.setMaximumWidth(30)
        self.label_By  = Qt.QLabel("By ")
        self.edit_StepSize = Qt.QLineEdit()
        self.edit_StepSize.setToolTip('')
        for w in [self.button_ConnectDevice,self.label_Position,self.edit_Position,self.label_Move,self.button_MoveNegative,self.button_MovePositive,self.label_By,self.edit_StepSize]:
            hbox2.addWidget(w)

        #min_pos, max_pos, units, pitch
        stageparams_groupbox = Qt.QGroupBox()
        stageparams_groupbox.setTitle(f"Stage Parameters")
        stageparams_hbox = Qt.QHBoxLayout()
        self.label_min_pos = Qt.QLabel("Min Pos: ")
        self.edit_min_pos = Qt.QLineEdit()
        self.label_max_pos = Qt.QLabel("Max Pos: ")
        self.edit_max_pos = Qt.QLineEdit()
        self.label_units = Qt.QLabel("Units: ")
        self.combo_units = Qt.QComboBox()
        self.combo_units.addItems(self.interface._units)
        self.label_pitch = Qt.QLabel("Pitch: ")
        self.edit_pitch = Qt.QLineEdit()
        self.button_set_stageparams = Qt.QPushButton("Set")
        tooltip = 'The correct values of these parameters depend on the particular motor, and changing them will affect the motor behaviour. \nDo not change them unless you know what you are doing.'
        self.button_set_stageparams.setToolTip(tooltip)
        stageparams_groupbox.setToolTip(tooltip)
        for w in [self.label_min_pos,self.edit_min_pos,self.label_max_pos,self.edit_max_pos,self.label_units,self.combo_units,self.label_pitch,self.edit_pitch,self.button_set_stageparams]:
            stageparams_hbox.addWidget(w)
        stageparams_groupbox.setLayout(stageparams_hbox) 
        
        ramp_groupbox = Qt.QGroupBox()
        ramp_groupbox.setTitle(f"Ramp")
        ramp_vbox = Qt.QVBoxLayout()
        ramp_hbox1 = Qt.QHBoxLayout()
        ramp_hbox2 = Qt.QHBoxLayout()
        self.checkbox_Initial_trigger = Qt.QCheckBox("Send initial trigger,")
        tooltip = 'When this interface is used within a larger software, it can be set to send a trigger (to another function) everytime a step of the ramp is done (see documentation).\nBy ticking this on, a trigger is sent also at the beginning of the ramp.'
        self.checkbox_Initial_trigger.setToolTip(tooltip)
        self.label_Move_ramp = Qt.QLabel("Move by")
        self.edit_StepSize_ramp = Qt.QLineEdit()
        self.label_Wait1_ramp = Qt.QLabel(",wait for")
        self.edit_Wait1_ramp = Qt.QLineEdit()
        self.edit_Wait1_ramp.setMaximumWidth(35)
        self.label_Wait2_ramp = Qt.QLabel("s, send trigger, wait for")
        self.edit_Wait2_ramp = Qt.QLineEdit()
        self.edit_Wait2_ramp.setMaximumWidth(35)
        self.label_Ramp_steps = Qt.QLabel("s, repeat")
        self.spinbox_Ramp_steps = Qt.QSpinBox()
        self.spinbox_Ramp_steps.setRange(1, 100000)
        self.label_Ramp_steps2 = Qt.QLabel("times.")
        for w in [self.checkbox_Initial_trigger,
                  self.label_Move_ramp,self.edit_StepSize_ramp,self.label_Wait1_ramp,
                  self.edit_Wait1_ramp,self.label_Wait2_ramp,
                  self.edit_Wait2_ramp,self.label_Ramp_steps,self.spinbox_Ramp_steps,self.label_Ramp_steps2]:
            ramp_hbox1.addWidget(w)

        self.checkbox_Reverse = Qt.QCheckBox("and reverse.")
        self.label_Ramp_repeat = Qt.QLabel(" Repeat ramp")
        self.spinbox_Ramp_repeat = Qt.QSpinBox()
        self.spinbox_Ramp_repeat.setRange(1, 100000)
        self.label_Ramp_repeat2 = Qt.QLabel(" times.")
        self.button_StartRamp = Qt.QPushButton("Start Ramp")
        for w in [self.checkbox_Reverse,self.label_Ramp_repeat,self.spinbox_Ramp_repeat,self.label_Ramp_repeat2,self.button_StartRamp]:
            ramp_hbox2.addWidget(w)
        ramp_vbox.addLayout(ramp_hbox1)  
        ramp_vbox.addLayout(ramp_hbox2)  
        ramp_groupbox.setLayout(ramp_vbox ) 
        #hbox2.addStretch(1)
                
        self.container = Qt.QVBoxLayout()
        for box in [hbox1,hbox2]:
            self.container.addLayout(box)  
        self.container.addWidget(ramp_groupbox)
        self.container.addWidget(stageparams_groupbox)

        self.container.addStretch(1)
        
        self.widgets_disabled_when_doing_ramp = [self.button_ConnectDevice,self.combo_Devices,
                                                 self.label_Position,self.edit_Position,
                                                 self.label_min_pos,self.edit_min_pos,self.label_max_pos,self.edit_max_pos,self.label_units,self.combo_units,self.label_pitch,self.edit_pitch,self.button_set_stageparams,
                                               self.label_Move,self.button_MoveNegative,self.button_MovePositive,self.label_By,self.edit_StepSize,
                                               self.checkbox_Initial_trigger,self.label_Move_ramp,self.edit_StepSize_ramp,self.label_Wait1_ramp,self.edit_Wait1_ramp,self.label_Wait2_ramp,
                                               self.edit_Wait2_ramp,self.label_Ramp_steps,self.spinbox_Ramp_steps,self.label_Ramp_steps2,
                                               self.checkbox_Reverse,self.label_Ramp_repeat,self.spinbox_Ramp_repeat,self.label_Ramp_repeat2]

        self.widgets_enabled_when_connected = [self.combo_Devices , self.button_RefreshDeviceList,
                                               self.label_Position, self.edit_Position,
                                               self.label_min_pos,self.edit_min_pos,self.label_max_pos,self.edit_max_pos,self.label_units,self.combo_units,self.label_pitch,self.edit_pitch,self.button_set_stageparams,
                                               self.label_Move,self.button_MoveNegative,self.button_MovePositive,self.label_By,self.edit_StepSize,
                                               self.checkbox_Initial_trigger,self.label_Move_ramp,self.edit_StepSize_ramp,self.label_Wait1_ramp,self.edit_Wait1_ramp,self.label_Wait2_ramp,
                                               self.edit_Wait2_ramp,self.label_Ramp_steps,self.spinbox_Ramp_steps,self.label_Ramp_steps2,
                                               self.checkbox_Reverse,self.label_Ramp_repeat,self.spinbox_Ramp_repeat,self.label_Ramp_repeat2,self.button_StartRamp]

        self.widgets_enabled_when_disconnected = [self.combo_Devices , 
                                                  self.button_RefreshDeviceList]

        self.widgets_disabled_when_moving = [self.button_StartRamp,self.button_set_stageparams,self.button_MoveNegative ,self.button_MovePositive ]

    def connect_widgets_events_to_functions(self):
        self.button_RefreshDeviceList.clicked.connect(self.click_button_refresh_list_devices)
        self.button_ConnectDevice.clicked.connect(self.click_button_connect_disconnect)
        self.edit_Position.returnPressed.connect(self.press_enter_edit_Position)
        self.button_MoveNegative.clicked.connect(lambda x:self.click_button_Move(-1))
        self.button_MovePositive.clicked.connect(lambda x:self.click_button_Move(+1))
        self.edit_StepSize.returnPressed.connect(self.press_enter_edit_StepSize)
        self.button_set_stageparams .clicked.connect(self.click_button_set_stageparams)
        self.button_StartRamp.clicked.connect(self.click_button_start_ramp)

    def set_disconnecting_state(self):
        self.disable_widget(self.widgets_enabled_when_connected)
        self.enable_widget(self.widgets_enabled_when_disconnected)
        self.button_ConnectDevice.setText("Disconnecting...")

    def set_disconnected_state(self):
        self.disable_widget(self.widgets_enabled_when_connected)
        self.enable_widget(self.widgets_enabled_when_disconnected)
        self.button_ConnectDevice.setText("Connect")

    def set_connecting_state(self):
        self.disable_widget(self.widgets_enabled_when_connected)
        self.enable_widget(self.widgets_enabled_when_disconnected)
        self.button_ConnectDevice.setText("Connecting...")

    def set_connected_state(self):
        self.enable_widget(self.widgets_enabled_when_connected)
        self.disable_widget(self.widgets_enabled_when_disconnected)
        self.button_ConnectDevice.setText("Disconnect")
        
    def set_doingramp_state(self):
        self.disable_widget(self.widgets_disabled_when_doing_ramp )
        self.button_StartRamp.setText("Stop Ramp")
        
    def set_notdoingramp_state(self):
        self.enable_widget(self.widgets_disabled_when_doing_ramp )
        self.button_StartRamp.setText("Start Ramp")

    def set_moving_state(self):
        self.disable_widget(self.widgets_disabled_when_moving)

    def set_non_moving_state(self):
        self.enable_widget(self.widgets_disabled_when_moving)

############################################################
### GUI Events Functions
############################################################

    def click_button_refresh_list_devices(self):
        self.interface.refresh_list_devices()

    def click_button_connect_disconnect(self):
        if(self.interface.instrument.connected == False): # We attempt connection   
            device_full_name = self.combo_Devices.currentText() # Get the device name from the combobox
            self.interface.connect_device(device_full_name)
        elif(self.interface.instrument.connected == True): # We attempt disconnection
            self.interface.disconnect_device()
            
    def press_enter_edit_Position(self):
        return self.interface.set_position(self.edit_Position.text())
    
    def press_enter_edit_StepSize(self):
        return self.interface.set_step_size(self.edit_StepSize.text())
    
    def click_button_start_ramp(self):
        if self.interface.doing_ramp == False:
            self.interface.start_ramp(initial_trigger = (self.checkbox_Initial_trigger.isChecked() == True),
                                      stepsize =   float(self.edit_StepSize_ramp.text()),
                                      wait1 =       float(self.edit_Wait1_ramp.text()),
                                      wait2 =       float(self.edit_Wait2_ramp.text()),
                                      numb_steps =     int(self.spinbox_Ramp_steps.value()),
                                      add_reverse = self.checkbox_Reverse.isChecked(),
                                      repeat_ramp = int(self.spinbox_Ramp_repeat.value())
                                      )
        else:
            self.interface.stop_ramp()

        
    def click_button_Move(self,direction):
        self.press_enter_edit_StepSize()
        self.interface.move_single_step(direction)

    def click_button_set_stageparams(self):
            self.interface.set_stage_info( min_pos =   self.edit_min_pos.text(),
                                            max_pos =   self.edit_max_pos.text(),
                                            units =     self.combo_units.currentText(),
                                            pitch =     self.edit_pitch.text(),
                                            )
############################################################
### END GUI Events Functions
############################################################

class MainWindow(Qt.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(__package__)
        # Set the central widget of the Window.
        # self.setCentralWidget(self.container)
    def closeEvent(self, event):
        if self.child:
            self.child.close()

def main():
    parser = argparse.ArgumentParser(description = "",epilog = "")
    parser.add_argument("-s", "--decrease_verbose", help="Decrease verbosity.", action="store_true")
    args = parser.parse_args()
    
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    Interface = interface(app=app,mainwindow=window) #In this case window is both the MainWindow and the parent of the gui
    Interface.verbose = not(args.decrease_verbose)
    app.aboutToQuit.connect(Interface.close) 
    Interface.create_gui(window)
    #Interface.set_trigger(lambda : print('test'),delay=1000)
    
    window.show()
    app.exec()# Start the event loop.

if __name__ == '__main__':
    main()
