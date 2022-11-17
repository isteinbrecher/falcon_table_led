/**
 *
 */

#include "led_strip.h"


/**
 *
 */
LedStrip::LedStrip::LedStrip(const uint pin_on_off, const uint pin_strip, const uint n_pixels)
    : pin_on_off_(pin_on_off),
      strip_(PicoLed::addLeds<PicoLed::WS2812B>(pio0, 0, pin_strip, n_pixels, PicoLed::FORMAT_RGB)),
      delay_between_flush_(1),
      last_flush_(0)
{
    // Initialize the on / off led
    gpio_init(pin_on_off_);
    gpio_set_dir(pin_on_off_, GPIO_OUT);
    SetPowerState(false);
}

/**
 *
 */
void LedStrip::LedStrip::SetPowerState(const bool power_state_state)
{
    gpio_put(pin_on_off_, power_state_state);
    SetFlushTime();
}

/**
 *
 */
void LedStrip::LedStrip::Show()
{
    // Wait until the delay since the last flush to the strip is done
    // TODO: when uint32_t overflows this can lead to issues
    while (to_ms_since_boot(get_absolute_time()) < delay_between_flush_ + last_flush_)
    {
    }

    // Now the strip is ready
    strip_.show();
    SetFlushTime();
}