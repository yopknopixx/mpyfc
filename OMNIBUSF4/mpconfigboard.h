#define MICROPY_HW_BOARD_NAME       "Omnibus F4"
#define MICROPY_HW_MCU_NAME         "STM32F405RG"

#define MICROPY_HW_HAS_SWITCH       (0)
#define MICROPY_HW_HAS_LED          (1)
#define MICROPY_HW_HAS_FLASH        (1)
#define MICROPY_HW_ENABLE_RNG       (0)
#define MICROPY_HW_ENABLE_RTC       (0)
#define MICROPY_HW_ENABLE_SERVO     (1)
#define MICROPY_HW_ENABLE_DAC       (0)
#define MICROPY_HW_ENABLE_USB       (1)
#define MICROPY_HW_ENABLE_SDCARD    (1)
#define MICROPY_HW_ENABLE_INTERNAL_FLASH_STORAGE (1)


// HSE is 12MHz
#define MICROPY_HW_CLK_PLLM (8)
#define MICROPY_HW_CLK_PLLN (336)
#define MICROPY_HW_CLK_PLLP (RCC_PLLP_DIV2)
#define MICROPY_HW_CLK_PLLQ (7)
#define MICROPY_HW_CLK_LAST_FREQ (1)



// UART config
#define MICROPY_HW_UART3_NAME   "UART3"    // on RX / TX
#define MICROPY_HW_UART3_TX     (pin_B10)  // TX
#define MICROPY_HW_UART3_RX     (pin_B11)  // RX

#define MICROPY_HW_UART2_NAME   "UART1"   // on SDA/SCL
#define MICROPY_HW_UART2_TX     (pin_A9)  // SCL
#define MICROPY_HW_UART2_RX     (pin_A10)  // SDA

#define MICROPY_HW_UART6_NAME   "UART6"   // on D5/D6
#define MICROPY_HW_UART6_TX     (pin_C6)  // D6
#define MICROPY_HW_UART6_RX     (pin_C7)  // D5

// I2C buses
#define MICROPY_HW_I2C1_NAME "I2C1"
#define MICROPY_HW_I2C1_SCL (pin_B6)  // SCL
#define MICROPY_HW_I2C1_SDA (pin_B7)  // SDA


// SPI buses
#define MICROPY_HW_SPI1_NAME "MPU"
#define MICROPY_HW_SPI1_NSS  (pin_A4) // MPU CS
#define MICROPY_HW_SPI1_SCK  (pin_A5)  // MPU CLK
#define MICROPY_HW_SPI1_MISO (pin_A6)  // MPU MISO
#define MICROPY_HW_SPI1_MOSI (pin_A7)  // MPU MOSI

#define MICROPY_HW_SPI2_NAME "SDCARD"
#define MICROPY_HW_SPI2_NSS  (pin_B12) // SD DETECT
#define MICROPY_HW_SPI2_SCK  (pin_B13) // SCK
#define MICROPY_HW_SPI2_MISO (pin_B14) // MISO
#define MICROPY_HW_SPI2_MOSI (pin_B15) // MOSI

#define MICROPY_HW_SPI3_NAME "BARO"
#define MICROPY_HW_SPI3_NSS  (pin_B3) // BARO CS
#define MICROPY_HW_SPI3_SCK  (pin_C10)  // BARO CLK
#define MICROPY_HW_SPI3_MISO (pin_C11)  // BARO MISO
#define MICROPY_HW_SPI3_MOSI (pin_C12)  // BARO MOSI

// LED
#define MICROPY_HW_LED1             (pin_B5) // red
#define MICROPY_HW_LED_OFF(pin)      (mp_hal_pin_high(pin))
#define MICROPY_HW_LED_ON(pin)     (mp_hal_pin_low(pin))

// USB config
#define MICROPY_HW_USB_FS              (1)

// Bootloader configuration (only needed if Mboot is used)
#define MBOOT_I2C_PERIPH_ID 1
#define MBOOT_I2C_SCL (pin_B8)
#define MBOOT_I2C_SDA (pin_B9)
#define MBOOT_I2C_ALTFUNC (4)
