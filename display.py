import time
import os
from colorama import init, Fore, Style

# Initialize colorama
init()

# Define color mapping for PiEye
color_mapping = {
    'PiEyeA': Fore.RED,      # Red color
    'PiEyeB': Fore.GREEN,    # Green color
    'PiEyeC': Fore.BLUE,     # Blue color
    # Add more colors as needed
}

def display_data(filename):
    while True:
        with open(filename, 'r') as file:
            data = file.readlines()
        
        # Prepare to collect all lines to display at once
        lines_to_display = []

        for line in data:
            # Split each line into parts
            parts = line.strip().split(';')
            if len(parts) == 3:
                name, pi_eye, last_seen = parts
                
                # Prepare the line with color
                if pi_eye in color_mapping:
                    color = color_mapping[pi_eye]
                    line_to_add = f"        {color}{name} was last seen at {pi_eye}{Style.RESET_ALL}"
                else:
                    line_to_add = f"        {name} was last seen at {pi_eye}"
                
                lines_to_display.append(line_to_add)
        
        # Clear the terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')
        print()
        
        # Print all collected lines
        for line in lines_to_display:
            print(line)
        
        # Wait for 3 seconds
        time.sleep(3)

# File containing the data
filename = 'gossip.txt'

# Start displaying data
display_data(filename)
