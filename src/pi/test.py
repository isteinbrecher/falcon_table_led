from crc import CrcCalculator, Crc8

data = bytes([1, 23, 8, 254, 0, 124])
crc_calculator = CrcCalculator(Crc8.CCITT)

checksum = crc_calculator.calculate_checksum(data)
print(checksum)
# assert checksum == expected_checksum
# assert crc_calculator.verify_checksum(data, expected_checksum)


rgb_color = bytes([40, 20, 0])
crc_calculator = CrcCalculator(Crc8.CCITT)
checksum = crc_calculator.calculate_checksum(rgb_color)

import smbus2

I2C_SLAVE_ADDRESS = 11

with smbus2.SMBus(1) as I2Cbus:
    I2Cbus.write_i2c_block_data(I2C_SLAVE_ADDRESS, checksum, rgb_color)
