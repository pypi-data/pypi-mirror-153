# MacTemperatures

MacTemperatures is a simple program to obtain readings from thermal sensors on M1 Macs. I adapted [the Objective-C code written by fermion-star](https://github.com/fermion-star/apple_sensors) as a C program and wrote Python bindings to make the code more flexible and easier to use.

## Usage

    >>> from mactemperatures import get_thermal_readings
    >>> get_thermal_readings()