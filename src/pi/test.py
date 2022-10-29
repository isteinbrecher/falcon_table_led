from crc import CrcCalculator, Crc8


data = bytes([1, 23, 8, 254, 0, 124])
crc_calculator = CrcCalculator(Crc8.CCITT)

checksum = crc_calculator.calculate_checksum(data)
print(checksum)
# assert checksum == expected_checksum
# assert crc_calculator.verify_checksum(data, expected_checksum)
