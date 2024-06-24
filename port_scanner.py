import socket
import argparse
import sys
import threading
from queue import Queue

# Function to scan ports
def scan_ports(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((target, port))
        print(f"[+] Port {port}/tcp open")
        sock.close()
    except:
        pass

# Function to scan a range of ports
def scan_range(target, start_port, end_port):
    for port in range(start_port, end_port + 1):
        scan_ports(target, port)

# Function for threaded port scanning
def threader(target, port_queue):
    while not port_queue.empty():
        port = port_queue.get()
        scan_ports(target, port)
        port_queue.task_done()

def main():
    parser = argparse.ArgumentParser(description="Basic Port Scanner")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("-p", "--port", help="Scan a single port")
    parser.add_argument("-r", "--range", nargs=2, metavar=("START", "END"), type=int, help="Scan a range of ports")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    args = parser.parse_args()

    target = args.target

    if args.port:
        scan_ports(target, int(args.port))
    elif args.range:
        start_port, end_port = args.range
        scan_range(target, start_port, end_port)
    else:
        print("Please specify a port or a range of ports to scan.")
        parser.print_help()
        sys.exit(1)

    # Alternatively, you can use threading for faster scanning
    # Create a queue for ports
    port_queue = Queue()

    # Enqueue ports
    if args.port:
        port_queue.put(int(args.port))
    elif args.range:
        start_port, end_port = args.range
        for port in range(start_port, end_port + 1):
            port_queue.put(port)

    # Create threads
    for _ in range(args.threads):
        thread = threading.Thread(target=threader, args=(target, port_queue))
        thread.daemon = True
        thread.start()

    # Wait for all threads to complete
    port_queue.join()

if __name__ == "__main__":
    main()
