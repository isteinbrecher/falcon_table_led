/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "hardware/gpio.h"
#include "one_wire.h"
#include "pico/stdlib.h"
#include <cstdio>

#include <Effects/Bounce.hpp>
#include <Effects/Comet.hpp>
#include <Effects/Marquee.hpp>
#include <Effects/Particles.hpp>
#include <Effects/Stars.hpp>
#include <PicoLed.hpp>

const uint LED_PIN = 20;

#define LED_STRIP_PIN 28
#define LED_LENGTH 192

int main() {

  stdio_init_all();

  One_wire one_wire(15); // GP15 - Pin 20 on Pi Pico
  one_wire.init();

  auto ledStrip = PicoLed::addLeds<PicoLed::WS2812B>(
      pio0, 0, LED_STRIP_PIN, LED_LENGTH, PicoLed::FORMAT_GRB);

  gpio_init(LED_PIN);
  gpio_set_dir(LED_PIN, GPIO_OUT);
  gpio_put(LED_PIN, true);

  while (true) {
    gpio_put(LED_PIN, true);
    sleep_ms(10);
    const int val = 255;
    ledStrip.fill(PicoLed::RGB(val, val, val));
    ledStrip.show();
    sleep_ms(500);

    // ledStrip.fill(PicoLed::RGB(0, val, 0));
    // ledStrip.show();
    // sleep_ms(500);

    // ledStrip.fill(PicoLed::RGB(0, 0, val));
    // ledStrip.show();
    // sleep_ms(500);

    // ledStrip.fill(PicoLed::RGB(val, val, val));
    // ledStrip.show();
    // sleep_ms(500);

    // gpio_put(LED_PIN, false);
    // sleep_ms(2000);
  }
  return 0;

  gpio_init(LED_PIN);
  gpio_set_dir(LED_PIN, GPIO_OUT);
  while (1) {
    printf("Off\n");
    gpio_put(LED_PIN, false);
    sleep_ms(2500);
    printf("On\n");
    gpio_put(LED_PIN, true);
    sleep_ms(2500);
  }

  rom_address_t address{};
  while (true) {
    one_wire.single_device_read_rom(address);
    printf("Device Address: %02x%02x%02x%02x%02x%02x%02x%02x\n", address.rom[0],
           address.rom[1], address.rom[2], address.rom[3], address.rom[4],
           address.rom[5], address.rom[6], address.rom[7]);
    one_wire.convert_temperature(address, true, false);
    printf("Temperature: %3.1foC\n", one_wire.temperature(address));
    sleep_ms(1000);
  }
  // while (true) {
  //     printf("Hello, world!\n");

  //     sleep_ms(1000);
  // }
  return 0;
}

// int main() {
//     stdio_init_all();
//     One_wire one_wire(15); //GP15 - Pin 20 on Pi Pico
//     one_wire.init();
//     rom_address_t address{};
//     while (true) {
//         one_wire.single_device_read_rom(address);
//         printf("Device Address: %02x%02x%02x%02x%02x%02x%02x%02x\n",
//         address.rom[0], address.rom[1], address.rom[2], address.rom[3],
//         address.rom[4], address.rom[5], address.rom[6], address.rom[7]);
//         one_wire.convert_temperature(address, true, false);
//         printf("Temperature: %3.1foC\n", one_wire.temperature(address));
//         sleep_ms(1000);
//     }
//     return 0;
// }