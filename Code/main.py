#####################################################################
# Hauptprogramm des Hubs für das HomeSys Smart Home                 #
# Author: Adrian Böschel                                            #
# Description: Main App running on a RaspberryPi 4B connected       #
# to a LuckFux 7inch Display used as a Hub to controll the HomeSys  #
#####################################################################

############              IMPORTS                        ############
import os
#import customtkinter as ctk # using tkinter or customtkinter?
import customtkinter as ctk
import time

############              GLOBAL VARIABLES               ############
Debug = True
############              CONSTANTS                      ############
SCREEN_WIDTH = 1200
SCREEN_HIGHT = 600

STEPPER_LOW = 0
STEPPER_HIGH = 100

ONE_MINUTE = 60*1000
HALF_MINUTE = int(ONE_MINUTE/2)
ONE_SECOND = 1000

############              CLASSES                        ############
class FullscreenApp(ctk.CTk):
    """Main App that is running on the RaspberryPi 4B"""

    def __init__(self):
        ############              VARIABLES               ############
        self.slider1 = 0 # Values of the sliders
        self.slider2 = 0
        self.obj_slider1 = None # Variable storing the objects of the slider
        self.obj_slider2 = None
        self.slider1_lable = None # Variable storing the objects of the labels
        self.slider2_lable = None
        self.last_time = 0
        self.time_disp = 0
        self.connection_pico_one = "True"
        self.connection_pico_two = "True"
        self.FIRST_PICO_CHECKED = False
        ############              CTK INIT                ############
        super().__init__()
        self.title("HomeSysHub")
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HIGHT}") # size of the window
        #self.attributes("-fullscreen", True)  # Set to fullscreen
        
        # Main content frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Create different contexts (frames) for different pages
        self.blinds_context = self.create_blinds_context()
        self.rooms_context = self.create_rooms_context()
        self.sleep_context = self.create_sleep_context()
        self.debug_context = self.create_debug_context()

        # Top bar frame
        self.top_bar = ctk.CTkFrame(self.main_frame)
        self.top_bar.pack(side="top", fill="x")
        self.top_bar.columnconfigure((0,1,2), weight=1)

        # Add Time to the top bar
        self.time_label = ctk.CTkLabel(self.top_bar, text=f"{time.strftime('%H : %M')}")
        self.time_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.obj_time_label = self.time_label # gets the obj
        self.update_time()

        # Add Connection status to the top bar
        # Add Time to the top bar
        self.conneciton_label = ctk.CTkLabel(self.top_bar, text=f"PICO 1: {self.connection_pico_one}    PICO 2: {self.connection_pico_two}")
        self.conneciton_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.obj_conneciton_label = self.conneciton_label # gets the obj

        # Bottom bar frame
        self.bottom_bar = ctk.CTkFrame(self.main_frame)
        self.bottom_bar.pack(side="bottom", fill="x")
        # Configure grid layout for the bottom bar
        self.bottom_bar.columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Add four buttons to the bottom bar
        # Blinds Button to activate the blinds control
        blinds_button = ctk.CTkButton(self.bottom_bar, text="blinds", command=self.blinds_button_action)
        blinds_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        # Rooms Button to activate the Rooms Temperatur and Humidity Overview
        # NOT WORKING RIGHT NOW!
        rooms_button = ctk.CTkButton(self.bottom_bar, text="rooms", command=self.rooms_button_action)
        rooms_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        # Sleep Button to activate the screen saver
        # NOT WORKING RIGHT NOW!
        sleep_button = ctk.CTkButton(self.bottom_bar, text="sleep", command=self.sleep_button_action)
        sleep_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        # Debug Button to show Debug logs
        # NOT WORKING RIGHT NOW!
        debug_button = ctk.CTkButton(self.bottom_bar, text="Debug", command=self.debug_button_action)
        debug_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        # Close Button to exit the Programm
        close_button = ctk.CTkButton(self.bottom_bar, text="Close", command=self.close_app)
        close_button.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

        ############              CONNECTION TO PICO     ############
        self.check_connection_to_pico()

    ############              METHODS                ############

    def blinds_button_action(self):
        if Debug: print("Blinds Button pressed")
        self.show_blinds_context()

    def rooms_button_action(self):
        if Debug: print("Rooms Button pressed")
        self.show_rooms_context()

    def sleep_button_action(self):
        if Debug: print("Sleep Button pressed")
        self.show_sleep_context()

    def debug_button_action(self):
        if Debug: print("Debug Button pressed")
        self.update_debug_context()
        self.show_debug_context()
    
    ############              BLINDS                ############
    def create_blinds_context(self):
        # create the ctk frame
        frame = ctk.CTkFrame(self.main_frame)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure((0, 1, 2, 3), weight=1)
        # SLIDER 1
        blind1_slider = ctk.CTkSlider(frame, from_=STEPPER_LOW, to=STEPPER_HIGH, command=self.update_slider_label, number_of_steps=100)
        blind1_slider.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.obj_slider1 = blind1_slider
        # LABEL 1
        blind1_label = ctk.CTkLabel(frame, text=self.slider1)
        blind1_label.grid(row=0, column=1)
        self.slider1_lable = blind1_label
        # SYNCH VAL BUTTON
        synch_blinds_button = ctk.CTkButton(frame, text="Sync Blinds", command=self.sync_blinds)
        synch_blinds_button.grid(row=1, column=0, padx=20, pady=20)
        # SEND VAL BUTTON
        send_blinds_button = ctk.CTkButton(frame, text="Set Blinds", command=self.send_blinds_val)
        send_blinds_button.grid(row=1, column=1, padx=20, pady=20)
        # SLIDER 2
        blind2_slider = ctk.CTkSlider(frame, from_=STEPPER_LOW, to=STEPPER_HIGH, command=self.update_slider_label, number_of_steps=100)
        blind2_slider.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        self.obj_slider2 = blind2_slider
        # LABEL 2
        blind2_label = ctk.CTkLabel(frame, text=self.slider2)
        blind2_label.grid(row=2, column=1)
        self.slider2_lable = blind2_label

        self.update_slider_label()
        return frame

    def update_slider_label(self,v1=0):
        self.slider1_lable.configure(text= round(self.obj_slider1.get(), 2))
        self.slider2_lable.configure(text= round(self.obj_slider2.get(), 2))

    def send_blinds_val(self):
        blind1 = self.obj_slider1.get()
        blind2 = self.obj_slider2.get()
        if Debug:
            print(f"set blinds")
            print(f"    Blind1: {blind1}\n    Blind2: {blind2}")
        write_log_file(f"SENDING BLINDS POSITION - PICO 1: {blind1} PICO2: {blind2}")

    def sync_blinds(self):
        if Debug: print(f"synchronize blinds")
        self.obj_slider2.set(self.obj_slider1.get()) # sets the second slider to the value of the first
        self.update_slider_label() # updates the value displayed by the label

    ############              ROOMS                ############
    def create_rooms_context(self):
        frame = ctk.CTkFrame(self.main_frame)
        label = ctk.CTkLabel(frame, text="This is Rooms")
        label.pack(pady=20)
        return frame
    
    ############              SLEEP                ############
    def create_sleep_context(self):
        frame = ctk.CTkFrame(self.main_frame)
        label = ctk.CTkLabel(frame, text="This is sleep")
        label.pack(pady=20)
        return frame
    
    ############              DEBUG                ############
    def create_debug_context(self):
        # create the ctk frame
        frame = ctk.CTkFrame(self.main_frame)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure((0, 1), weight=1)

        label = ctk.CTkLabel(frame, text=read_log_file())
        label.grid(row=0,column=0,pady=20, sticky='w')
        self.obj_debug_label = label

        save_button = ctk.CTkButton(frame, text="Save Logfile", command=save_log_file_as_new)
        save_button.grid(row=0, column=1, padx=10, pady=20, sticky="w")

        return frame

    def update_debug_context(self):
        self.obj_debug_label.configure(text=read_log_file())

    ############         SHOW CONTEXTS             ############
    def show_blinds_context(self):
        self.hide_all_contexts()
        self.blinds_context.pack(fill="both", expand=True)

    def show_rooms_context(self):
        self.hide_all_contexts()
        self.rooms_context.pack(fill="both", expand=True)

    def show_sleep_context(self):
        self.hide_all_contexts()
        self.sleep_context.pack(fill="both", expand=True)
    
    def show_debug_context(self):
        self.hide_all_contexts()
        self.debug_context.pack(fill="both", expand=True)

    def hide_all_contexts(self):
        self.blinds_context.pack_forget()
        self.rooms_context.pack_forget()
        self.sleep_context.pack_forget()
        self.debug_context.pack_forget()

    ############              TIME                ############
    def update_time(self):
        if Debug: print("Checking Time")
        self.obj_time_label.configure(text=f"{time.strftime('%H : %M')}") # adjust the label to show the correct time

        self.top_bar.after(ONE_MINUTE, self.update_time) # call this function again after one minute

    ############              CONNECTION TO PICO   ############

    def check_connection_to_pico(self):
        if self.FIRST_PICO_CHECKED == True:
            if Debug: print(f"Checking connection to Pico 2")
            # ping the pico

            # await response

            # evaluate response
            self.connection_pico_two = "Bad"
            self.obj_conneciton_label.configure(text=f"PICO 1: {self.connection_pico_one}    PICO 2: {self.connection_pico_two}") # update the label accordingly

            self.FIRST_PICO_CHECKED = False
            self.after(HALF_MINUTE, self.check_connection_to_pico) # call the function again to check the other pico

        elif self.FIRST_PICO_CHECKED == False:
            if Debug: print(f"Checking connection to Pico 1")
            self.connection_pico_two = "True"
            self.obj_conneciton_label.configure(text=f"PICO 1: {self.connection_pico_one}    PICO 2: {self.connection_pico_two}")

            self.FIRST_PICO_CHECKED = True
            self.after(HALF_MINUTE, self.check_connection_to_pico) # call the function again to check the other pico

        else:
            if Debug: print(f"EXCEPTION")
            write_log_file(f"WARNING - CONNECTIVITY! PICO1: {self.connection_pico_one}      PICO2: {self.connection_pico_two}")
            self.after(HALF_MINUTE, self.check_connection_to_pico)

    ############              CLOSE                ############
    def close_app(self):
        if Debug: print("Exiting the Programm")
        self.destroy()  # Close the application

############              FUNCTIONS                      ############

def create_log_file():
    if Debug: print("Creating Log File")
    log_file = open("debug.txt", 'w') # create the file
    log_file.write(f"{time.strftime('%d.%m.%Y | %H : %M : %S')} | Create Debug File\n")
    log_file.close()

def write_log_file(text):
    if Debug: print("Writing to Log File")
    str_to_write = f"{time.strftime('%d.%m.%Y | %H : %M : %S')} | " + text + "\n"
    log_file = open("debug.txt", 'a+') # append to the file
    log_file.write(str_to_write)
    log_file.close()

def read_log_file():
    if Debug: print("Reading from Log File")
    log_file = open("debug.txt", 'r')
    text = log_file.read()
    return text

def save_log_file_as_new():
    if Debug: print("Saving new Log File")
    log_file = open("debug.txt", 'r')
    text = log_file.read()
    log_file.close()

    new_f = open("saved_debug.txt", 'w')
    new_f.write(text)
    new_f.close()
############              MAIN                           ############
def main():
    # create a log file
    # run the App
    create_log_file()
    app = FullscreenApp()
    app.mainloop()
    
if __name__ == "__main__":
    main()