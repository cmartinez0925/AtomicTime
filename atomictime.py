import socket
import time

from datetime import datetime

def system_seconds_since_1900():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """
    # Number of seconds between 1900-01-01 and 1970-01-01
    SECONDS_DELTA = 2208988800

    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + SECONDS_DELTA
    return seconds_since_1900_epoch

def nist_and_sys_time_msg(nist_time, sys_time):
    # Number of seconds between 1900-01-01 and 1970-01-01
    SECONDS_DELTA = 2208988800
    TIME_FORMAT = '%H:%M:%S %p'
    
    # Convert seconds since 1900 to datetime's reference epoch (1970-01-01)
    nist_datetime = datetime.utcfromtimestamp(nist_time - SECONDS_DELTA)
    sys_datetime = datetime.utcfromtimestamp(sys_time - SECONDS_DELTA)

    # Format datetime to hh:mm:ss.mmm (milliseconds)
    nist_formatted_time = nist_datetime.strftime(TIME_FORMAT)
    sys_formatted_time = sys_datetime.strftime(TIME_FORMAT)

    # Create msg to return
    msg = f"NIST Time: {nist_formatted_time}\n"
    msg += f"System Time: {sys_formatted_time}"
    return msg

def main():
    # Constants
    ADDR = 'time.nist.gov'
    PORT = 37 # Time Protocol Port
    SOCK_INFO = (ADDR, PORT)
    TRANSFER_SIZE = 4096
    ZERO_DATA_REMAINING = 0

    # Create socket and get data from atomic clock server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SOCK_INFO)
    total_data = b''
    while True:
        partial_data = s.recv(TRANSFER_SIZE)
        total_data += partial_data
        if len(partial_data) == ZERO_DATA_REMAINING:
            break
    s.close()

    # Convert time, and then print it on the terminal
    nist_time = int.from_bytes(total_data, 'big')
    sys_time = system_seconds_since_1900()
    time_msg = nist_and_sys_time_msg(nist_time, sys_time)
    print(time_msg)


if __name__ == '__main__':
    main()



