import time
import socket
import os
import threading
import ipaddress


def write_gossip(local_gossip):
    with open('gossip.txt', 'r') as file:
        content = file.read().strip()
    parts = content.split('\n')
    gossip_dict = {}

    for part in parts:
        if part.count(';') != 2:
            print(f"Skipping malformed line: {part}")
            continue
        name, node, actions = part.split(';')
        actions = int(actions)
        gossip_dict[name] = (node, actions)

    local_name, local_node, local_actions = local_gossip.split(';')
    local_actions = int(local_actions)

    if local_name in gossip_dict:
        current_node, current_actions = gossip_dict[local_name]
        if current_node != local_node:
            gossip_dict[local_name] = (local_node, current_actions + 1)
        else:
            gossip_dict[local_name] = (local_node, current_actions)  # Do not increment if node is the same
    else:
        gossip_dict[local_name] = (local_node, local_actions)

    with open('gossip.txt', 'w') as file:
        for name, (node, actions) in gossip_dict.items():
            file.write(f"{name};{node};{actions}\n")

def check_new(local_gossip):
    with open('gossip.txt', 'r') as file:
        old = file.read().strip()
    old_parts = old.split('\n')
    old_dict = {}
    for part in old_parts:
        name, node, actions = part.split(';')
        old_dict[name] = (node, int(actions))
    
    local_name, local_node, local_actions = local_gossip.split(';')
    if local_name in old_dict and old_dict[local_name][0] == local_node:
        return False
    else:
        return True

def update_gossip(filename, new_entries):
    # Read the current entries from the file
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    # Convert the current entries to a dictionary for easy updating
    current_entries = {}

    for line in lines:
        name, node, actions = line.strip().split(';')
        actions = int(actions)
        current_entries[name] = (node, actions)

    # Parse and process the new entries
    for entry in new_entries.strip().split('\n'):
        new_name, new_node, new_actions = entry.strip().split(';')
        new_actions = int(new_actions)
        
        if new_name in current_entries:
            current_node, current_actions = current_entries[new_name]
            if current_node != new_node:
                new_actions = current_actions + 1
            else:
                new_actions = current_actions
            current_entries[new_name] = (new_node, new_actions)
        else:
            current_entries[new_name] = (new_node, new_actions)

    # Convert the dictionary back to a list of lines
    updated_lines = [f"{name};{node};{actions}\n" for name, (node, actions) in current_entries.items()]

    # Write the updated entries back to the file
    with open(filename, 'w') as file:
        file.writelines(updated_lines)
        
def update_gossip_file(input_string):
    # Read the content of gossip.txt
    with open('gossip.txt', 'r') as file:
        lines = file.readlines()
    
    # Parse the input string into individual entries
    entries = input_string.strip().split('\n')
    
    # Create a dictionary from the file contents for easier updates
    gossip_dict = {}
    for line in lines:
        name, code, number = line.strip().split(';')
        gossip_dict[(name, code)] = int(number)
    
    # Process each entry from the input string
    for entry in entries:
        name, code, new_number = entry.split(';')
        new_number = int(new_number)
        
        if (name, code) in gossip_dict:
            if new_number > gossip_dict[(name, code)]:
                gossip_dict[(name, code)] = new_number
        else:
            gossip_dict[(name, code)] = new_number
    
    # Write the updated content back to gossip.txt
    with open('gossip.txt', 'w') as file:
        for (name, code), number in gossip_dict.items():
            file.write(f'{name};{code};{number}\n')

def get_broadcast_address(ip, subnet_mask):
    network = ipaddress.IPv4Network(f'{ip}/{subnet_mask}', strict=False)
    return network.broadcast_address
    
def broadcast_message_from_file(ip, subnet_mask, port=37020):
    broadcast_address = get_broadcast_address(ip, subnet_mask)
    
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enable broadcasting mode
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        # Read the message from the file
        with open("gossip.txt", "r") as file:
            message = file.read().strip()

        # Send the message
        sock.sendto(message.encode(), (str(broadcast_address), port))
        time.sleep(5)  # Broadcast every 5 seconds

def listen_for_broadcast(port=37020):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = ('', port)
    sock.bind(server_address)

    print(f"Listening for broadcasts on port {port}...")

    while True:
        data, address = sock.recvfrom(4096)
        print(f"\nReceived message: \n{data.decode()} \nfrom {address} \n")
        input_data = data.decode()
        update_gossip("gossip.txt", input_data)
        time.sleep(1)
        #update_gossip_file(input_data)

if __name__ == "__main__":

    ip = '192.168.2.5'  # Your IP address
    subnet_mask = '255.255.255.0'  # Your subnet mask
    
    # Start the broadcast thread
    broadcast_thread = threading.Thread(target=broadcast_message_from_file, args=(ip, subnet_mask))
    broadcast_thread.daemon = True
    broadcast_thread.start()


    # Start listening for broadcasts
    listen_for_broadcast()
