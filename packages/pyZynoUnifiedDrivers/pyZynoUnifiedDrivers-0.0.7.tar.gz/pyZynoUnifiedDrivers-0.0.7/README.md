# Zyno Medical Unified Driver: Control your infusion pump with Python
Zyno Medical Unified Driver is a Python package that enables you to 
control Zyno Medical infusion pumps with RS232 interface. As an 
example, reading self-identification from a MIVA pump is as easy as 
three lines of Python code:
```
from pyZynoUnifiedDrivers import visa
rm = visa.ResourceManager()
print(rm.list_resources())
miva = rm.open_resource('COM5')
print(miva.query("*IDN?"))
```
(That’s the whole program; really!) It works on Windows; with a USB cable
(e.g. [Amazon Basics USB 2.0 A-Male to Micro B Cable](https://www.amazon.com/dp/B071S5NPG9?ref_=cm_sw_r_cp_ud_dp_35NRK7NQNRZ6DN6NVF6Q)).

## General overview
The programming of Zyno Medical Infusion Pumps can be real pain. 
There are many different protocols, sent over many different 
interfaces and bus systems (e.g. RS232, USB, Ethernet). 
For every programming language you want to use, you have to find 
libraries that support both your device and its bus system.

In order to ease this unfortunate situation, Zyno Medical Unified 
Driver was created for configuring programming, and troubleshooting 
infusion pumps comprising Serial, Ethernet, and/or USB interfaces. 
This driver is following the design pattern of the [pyVISA library API](https://pyvisa.readthedocs.io/en/stable/api/index.html).

## Application Code Example
```
from pyZynoUnifiedDrivers import visa
rm = visa.ResourceManager()
print(rm.list_resources())
miva = rm.open_resource('com5')
# Test [query] Function
pump_sn = miva.query(':serial?')
print(pump_sn)
# Test [write] Function
miva.write(':serial?')
# Test [read] Function
pump_sn = miva.read()
print(pump_sn)
# Test [*idn] query
pump_identifier = miva.query('*idn?')
print(pump_identifier)
# Test [close] function of miva class
miva.close()
# Test [list_resources] Function
resources = rm.list_resources()
print(resources)
```
