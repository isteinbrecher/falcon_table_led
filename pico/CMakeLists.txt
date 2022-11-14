cmake_minimum_required(VERSION 3.12)

# Pull in SDK (must be before project)
include(pico_sdk_import.cmake)

project(falcon_table_led C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

if (PICO_SDK_VERSION_STRING VERSION_LESS "1.3.0")
    message(FATAL_ERROR "Raspberry Pi Pico SDK version 1.3.0 (or later) required. Your version is ${PICO_SDK_VERSION_STRING}")
endif()

set(FACLON_TABLE_LED_PATH ${PROJECT_SOURCE_DIR})

# Initialize the SDK
pico_sdk_init()

# include(example_auto_set_url.cmake)


add_subdirectory(modules/pico-onewire)



# Set output stuff
if (TARGET tinyusb_device)
    add_executable(falcon_table_led
            src/hello_usb.cpp
            )

    # pull in common dependencies
    target_link_libraries(falcon_table_led pico_stdlib pico_one_wire)

    # enable usb output, disable uart output
    pico_enable_stdio_usb(falcon_table_led 1)
    pico_enable_stdio_uart(falcon_table_led 0)

    # create map/bin/hex/uf2 file etc.
    pico_add_extra_outputs(falcon_table_led)

    # add url via pico_set_program_url
    #example_auto_set_url(falcon_table_led)
elseif(PICO_ON_DEVICE)
    message(WARNING "not building falcon_table_led because TinyUSB submodule is not initialized in the SDK")
endif()


add_compile_options(-Wall
        -Wno-format          # int != int32_t as far as the compiler is concerned because gcc has int32_t as long int
        -Wno-unused-function # we have some for the docs that aren't called
        -Wno-maybe-uninitialized
        )
