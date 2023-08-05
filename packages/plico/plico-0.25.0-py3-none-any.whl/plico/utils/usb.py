
import serial
import serial.tools.list_ports


def device_by_serial_number(serial_number):
    '''
    Returns the device path (i.e. '/dev/ttyUSB1') for the
    USB device identified by the serial_number, or None
    if the device is not found.
    '''
    ports = serial.tools.list_ports.comports()
    my_ports = [x for x in ports if x.serial_number == serial_number]
    if len(my_ports) > 0:
        return my_ports[0].device
    else:
        return None
