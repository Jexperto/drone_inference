import enum


class SPIModeConfig(enum.Enum):
    LOW_CLOCK_LEADING = 0b00,
    LOW_CLOCK_TRAILING = 0b01,
    HIGH_CLOCK_LEADING = 0b10,
    HIGH_CLOCK_TRAILING = 0b11,


# Raspberry Pi available values
class SPIHzConfig(enum.Enum):
    Hz7629 = 7629,
    kHz15_2 = 15200,
    kHz30_5 = 30500,
    kHz61 = 61000,
    kHz122 = 122000,
    kHz244 = 244000,
    kHz488 = 488000,
    kHz976 = 976000,
    kHz1953 = 1953000,
    MHz3_9 = 3900000,
    MHz7_8 = 7800000,
    MHz15_6 = 15600000,
    MHz31_2 = 31200000,
    MHz62_5 = 62500000,
    MHz125 = 125000000,
