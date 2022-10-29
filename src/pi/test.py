from crc import CrcCalculator, Crc8


def send_data(i2c_bus, data):
    """
    Send data to the arduino
    """

    # First calculate the checksum
    crc_calculator = CrcCalculator(Crc8.CCITT)
    checksum = crc_calculator.calculate_checksum(data)

    # Send the checksum and the data to the device
    i2c_bus.write_i2c_block_data(I2C_SLAVE_ADDRESS, checksum, data)


def read_data(i2c_bus, data_size):
    """
    Read data from the arduino
    """

    # Get the data sent from the arduino
    data = i2c_bus.read_i2c_block_data(I2C_SLAVE_ADDRESS, 0x00, data_size + 1)

    # Compare the checksum
    crc_calculator = CrcCalculator(Crc8.CCITT)
    checksum = crc_calculator.calculate_checksum(data[1:])
    if checksum == data[0]:
        return data[1:], True
    else:
        return None, False


data = bytes([1, 23, 8, 254, 0, 124])

crc_calculator = CrcCalculator(Crc8.CCITT)

checksum = crc_calculator.calculate_checksum(data)
print(checksum)
# assert checksum == expected_checksum
# assert crc_calculator.verify_checksum(data, expected_checksum)


rgb_color = bytes([20, 20, 200, 1, 255])
crc_calculator = CrcCalculator(Crc8.CCITT)
checksum = crc_calculator.calculate_checksum(rgb_color)

import smbus2

I2C_SLAVE_ADDRESS = 11

print(len(rgb_color))

with smbus2.SMBus(1) as i2c_bus:
    send_data(i2c_bus, rgb_color)
    data = read_data(i2c_bus, len(rgb_color))
    print(data)
