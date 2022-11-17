/**
 *
 */

#ifndef LED_STRIP_H
#define LED_STRIP_H


#include "hardware/gpio.h"
#include "pico/stdlib.h"

#include <PicoLed.hpp>


namespace LedStrip
{
    /**
     *
     */
    class LedStrip
    {
       public:
        /**
         *
         */
        LedStrip(const uint pin_on_off, const uint pin_strip, const uint n_pixels);

        /**
         *
         */
        PicoLed::PicoLedController& GetStrip() { return strip_; }

        /**
         *
         */
        void SetPowerState(const bool power_state_state);

        /**
         *
         */
        void Show();

       private:
        void SetFlushTime() { last_flush_ = to_ms_since_boot(get_absolute_time()); }

       private:
        uint pin_on_off_;
        PicoLed::PicoLedController strip_;

        uint32_t delay_between_flush_;
        uint32_t last_flush_;
    };
}  // namespace LedStrip

#endif