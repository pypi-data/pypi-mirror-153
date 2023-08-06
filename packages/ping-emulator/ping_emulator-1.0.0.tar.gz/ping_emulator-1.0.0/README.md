# Ping360_simulator

## Dependencies 

[ping-python](https://github.com/bluerobotics/ping-python)

## Installing from source

```
git clone --recursive https://github.com/AlexisFetet/Ping360_emulator.git
cd Ping360_emulator
sudo python3 setup.py install
```

## How to use

Run `socat -d -d pty,raw,echo=0 pty,raw,echo=0` in a terminal. This should give you 2 serial ports, provide one to the emulator, the second is for your application.

```
emulated_ping360.py --device your/serial/port --baudrate 115200
```
