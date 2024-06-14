#####################################################################
# Hauptprogramm des Hubs für das HomeSys Smart Home                 #
# Author: Adrian Böschel                                            #
# Description: Main App running on a RaspberryPi 4B connected       #
# to a LuckFux 7inch Display used as a Hub to controll the HomeSys  #
#####################################################################

############              IMPORTS                        ############
import os
import customtkinter as ctk # using tkinter or customtkinter?
import time

############              GLOBAL VARIABLES               ############
Debug = True
############              CONSTANTS                      ############
SCREEN_WIDTH = 1200
SCREEN_HIGHT = 600

STEPPER_LOW = 0
STEPPER_HIGH = 100


############              CLASSES                        ############
class FullscreenApp(ctk.CTk):
    """Main App that is running on the RaspberryPi 4B"""

    def __init__(self):
        super().__init__()
        self.title("HomeSysHub")
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HIGHT}") # size of the window
        #self.attributes("-fullscreen", True)  # Set to fullscreen
        
        # Main content frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Bottom bar frame
        self.bottom_bar = ctk.CTkFrame(self.main_frame)
        self.bottom_bar.pack(side="bottom", fill="x")
        # Configure grid layout for the bottom bar
        self.bottom_bar.columnconfigure((0, 1, 2, 3), weight=1)

        # Create different contexts (frames) for different pages
        self.blinds_context = self.create_blinds_context()
        self.rooms_context = self.create_rooms_context()
        self.sleep_context = self.create_sleep_context()

        # show first context by default
        #self.show_blinds_context()

        # Add four buttons to the bottom bar
        # Blinds Button to activate the blinds control
        blinds_button = ctk.CTkButton(self.bottom_bar, text="blinds", command=self.blinds_button_action)
        blinds_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        # Rooms Button to activate the Rooms Temperatur and Humidity Overview
        # NOT WORKING RIGHT NOW!
        rooms_button = ctk.CTkButton(self.bottom_bar, text="rooms", command=self.rooms_button_action)
        rooms_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        # Sleep Button to activate the screen saver
        sleep_button = ctk.CTkButton(self.bottom_bar, text="sleep", command=self.sleep_button_action)
        sleep_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        # Close Button to exit the Programm
        close_button = ctk.CTkButton(self.bottom_bar, text="Close", command=self.close_app)
        close_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
    
    def blinds_button_action(self):
        if Debug: print("Blinds Button pressed")
        self.show_blinds_context()

    def rooms_button_action(self):
        if Debug: print("Rooms Button pressed")
        self.show_rooms_context()

    def sleep_button_action(self):
        if Debug: print("Sleep Button pressed")
        self.show_sleep_context()
    
    def create_blinds_context(self):
        # create the ctk frame
        frame = ctk.CTkFrame(self.main_frame)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure((0, 1, 2, 3), weight=1)

        blind1_slider = ctk.CTkSlider(frame, from_=STEPPER_LOW, to=STEPPER_HIGH)
        blind1_slider.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        send_blinds_button = ctk.CTkButton(frame, text="Change Blinds", command=self.get_slider_values)
        send_blinds_button.grid(row=1, column=0, padx=20, pady=20)

        blind2_slider = ctk.CTkSlider(frame, from_=STEPPER_LOW, to=STEPPER_HIGH)
        blind2_slider.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        return frame
    
    def get_slider_values(self):
        v1 = self.blind1_slider.get()
        v2 = self.blind2_slider.get()
        if Debug: print(f"Blind1: {v1}, Blind2: {v2}")

    
    def create_rooms_context(self):
        frame = ctk.CTkFrame(self.main_frame)
        label = ctk.CTkLabel(frame, text="This is Rooms")
        label.pack(pady=20)
        return frame

    def create_sleep_context(self):
        frame = ctk.CTkFrame(self.main_frame)
        label = ctk.CTkLabel(frame, text="This is sleep")
        label.pack(pady=20)
        return frame

    def show_blinds_context(self):
        self.hide_all_contexts()
        self.blinds_context.pack(fill="both", expand=True)

    def show_rooms_context(self):
        self.hide_all_contexts()
        self.rooms_context.pack(fill="both", expand=True)

    def show_sleep_context(self):
        self.hide_all_contexts()
        self.sleep_context.pack(fill="both", expand=True)

    def hide_all_contexts(self):
        self.blinds_context.pack_forget()
        self.rooms_context.pack_forget()
        self.sleep_context.pack_forget()

    def close_app(self):
        if Debug: print("Exiting the Programm")
        self.destroy()  # Close the application

############              FUNCTIONS                      ############


############              MAIN                           ############
def main():
    app = FullscreenApp()
    app.mainloop()

if __name__ == "__main__":
    main()