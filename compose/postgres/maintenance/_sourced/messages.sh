#!/usr/bin/env bash

# Define a function to print a newline
message_newline() {
    echo
}

# Define a function to print a debug message
message_debug() {
    echo -e "DEBUG: ${@}"
}

# Define a function to print a welcome message
message_welcome() {
    echo -e "\e[1m${@}\e[0m"
}

# Define a function to print a warning message
message_warning() {
    echo -e "\e[33mWARNING\e[0m: ${@}"
}

# Define a function to print an error message
message_error() {
    echo -e "\e[31mERROR\e[0m: ${@}"
}

# Define a function to print an informational message
message_info() {
    echo -e "\e[37mINFO\e[0m: ${@}"
}

# Define a function to print a suggestion message
message_suggestion() {
    echo -e "\e[33mSUGGESTION\e[0m: ${@}"
}

# Define a function to print a success message
message_success() {
    echo -e "\e[32mSUCCESS\e[0m: ${@}"
}
