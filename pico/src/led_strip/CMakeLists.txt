set(OBJS_LED_STRIP
    led_strip.cpp
    )

add_library(led_strip ${OBJS_LED_STRIP})
target_link_libraries(led_strip PUBLIC pico_stdlib PicoLed)
