# MicroPython Flight Controller

This repository contains the code for a PID-based flight controller implemented in MicroPython for a QuadCopter. The controller utilizes sensor data to implement real-time control algorithms for stable flight.

## Flight Video


https://user-images.githubusercontent.com/30761130/213992765-260f84b3-e6ee-4b26-9c5a-9f0cd5bce997.MP4



## Getting Started

These instructions will get you a copy of the project up and running on your MicroPython supported board for testing and development purposes.

### Note
This project is still under development and is not yet ready for use. Testing this code on a real QuadCopter can be hazardous and may result in damage to the hardware or your surroundings. Use at your own risk.

### Prerequisites

- MicroPython supported board (Only OMNIBUS F4 SD has been tested)
- Python 3.x
- MicroPyhton build tools
- Thonny IDE (Optional)

### Installing

1. Clone this repository to your local machine
```
git clone https://github.com/yopknopixx/mpyfc.git
```
2. Setup MicroPython build tools and build the MicroPython firmware for your board. Please refer to the [MicroPython documentation](https://docs.micropython.org/en/latest/develop/gettingstarted.html). The following steps are for the OMNIBUS F4 SD board.
```
cd mpyfc
cp -r OMNIBUSF4 micropython/ports/stm32/boards
```

3. Connect the flight controller board to your computer via USB and flash the firmware using STM32CubeProgrammer.

4. Connect the flight controller board to your computer via USB and open the serial port using Thonny IDE.

5. Copy the code from this repository to the board using Thonny IDE.

## Usage (WARNING: Use at your own risk!)

To run the flight controller, make sure you have properly connected the ESCs and receiver to the flight controller board. Then, perform the following steps:

1. Disconnect the flight controller board from your computer.
2. Mount the flight controller board on the QuadCopter and make required connections.
3. Move to an open space and attach the battery to the flight controller board.
4. Arm the flight controller board by turning on the transmitter and holding the throttle stick down and flipping the ARM switch on the transmitter.
5. Take off the QuadCopter and fly it around.
6. Land the QuadCopter and disarm the flight controller board by turning off the transmitter and flipping the ARM switch on the transmitter. Then, disconnect the battery from the flight controller board.

## Contributors
1. [Rhythm Chandak](https://www.linkedin.com/in/rhythm-chandak-89a386168/)
2. [Yog Dharaskar](https://www.linkedin.com/in/yog-dharaskar/)