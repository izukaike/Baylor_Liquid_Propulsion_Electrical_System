/*
Author: Izuka Ikedionwu

Description: ADC driver

Date Created: 9/3/24
*/

#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <cstring>
#include "gpio.hpp"
#include "client.hpp"

#define SPI_DEVICE "/dev/spidev0.0"
#define SPI_SPEED 25000 // SPI speed in Hz
#define SPI_MODE SPI_MODE_2 // SPI mode
#define SPI_BITS_PER_WORD 8



uint16_t readMCP3202(int spi_fd, uint8_t channel)

{

    // Construct the control byte for single-ended mode, channel 0, MSB first

    uint8_t control_byte = 0b00001101 | (channel << 6);



    // Buffer to hold the data to send/receive

    //uint8_t tx_buffer[3] = {0b00000001, 0b1010000, 0b00000000};

    //uint8_t rx_buffer[3] = {0};



    uint8_t tx_buffer[3] = {control_byte, 0x00,0x00};

    uint8_t rx_buffer[3] = {0};





    // Struct to handle SPI transfer

    struct spi_ioc_transfer spi_transfer;

    memset(&spi_transfer, 0, sizeof(spi_transfer));

    uint8_t mode = SPI_MODE;

    uint32_t speed = SPI_SPEED;

    uint8_t bits_per_word = SPI_BITS_PER_WORD;

    spi_transfer.tx_buf = (unsigned long)tx_buffer;

    spi_transfer.rx_buf = (unsigned long)rx_buffer;

    spi_transfer.len = sizeof(tx_buffer);

    spi_transfer.speed_hz = speed;

    spi_transfer.bits_per_word = bits_per_word;

    spi_transfer.delay_usecs = 0;



    // Perform the SPI transaction

    int ret = ioctl(spi_fd, SPI_IOC_MESSAGE(1), &spi_transfer);

    if (ret < 1) {

        std::cerr << "Failed to send SPI message" << std::endl;

        return 0;

    }



    // Combine the received bytes into a single 12-bit result

    uint16_t result = ((rx_buffer[1] & 0x0F) << 8) | rx_buffer[2];



    return result;

}



int main()

{

    uint8_t mode = SPI_MODE;

    uint32_t speed = SPI_SPEED;

    uint8_t bits_per_word = SPI_BITS_PER_WORD;

    GPIO gpio;

    gpio.init(2);

    gpio.set_direction(true);

    gpio.set_value(true);





    // Open the SPI device

    int spi_fd = open(SPI_DEVICE, O_RDWR);

    if (spi_fd < 0) {

        std::cerr << "Failed to open SPI device" << std::endl;

        return -1;

    }



    // Set SPI mode

    if (ioctl(spi_fd, SPI_IOC_WR_MODE, &mode) == -1) {

        std::cerr << "Failed to set SPI mode" << std::endl;

        close(spi_fd);

        return -1;

    }



    // Set SPI speed

    if (ioctl(spi_fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed) == -1) {

        std::cerr << "Failed to set SPI speed" << std::endl;

        close(spi_fd);

        return -1;

    }



    // Set bits per word

    if (ioctl(spi_fd, SPI_IOC_WR_BITS_PER_WORD, &bits_per_word) == -1) {

        std::cerr << "Failed to set bits per word" << std::endl;

        close(spi_fd);

        return -1;

    }

    gpio.set_value(false);

    uint16_t adcValue = readMCP3202(spi_fd, 0); // Read from channel 0

    std::cout << "ADC Value: " << adcValue << std::endl;

    gpio.set_value(true);

    close(spi_fd);

    return 0;

}

