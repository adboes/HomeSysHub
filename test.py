import tkinter as tk

def perform_periodic_check():
    if entry.get().isdigit():
        label.config(text="Input is a number.")
    else:
        label.config(text="Input is not a number.")
    
    # Schedule this function to be called again after 1000 milliseconds (1 second)
    root.after(1000, perform_periodic_check)

# Create the main application window
root = tk.Tk()
root.title("Periodic Check Example")

# Create an entry widget
entry = tk.Entry(root)
entry.pack(pady=10)

# Create a label to display the result
label = tk.Label(root, text="")
label.pack(pady=10)

# Start the periodic check
perform_periodic_check()

# Run the Tkinter main loop
root.mainloop()
