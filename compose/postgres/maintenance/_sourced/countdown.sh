#!/usr/bin/env bash

# Define a function to perform a countdown
countdown() {
    # Description of the function
    declare desc="A simple countdown. Source: https://superuser.com/a/611582"

    # Extract the number of seconds from the first argument
    local seconds="${1}"

    # Calculate the end time based on the current time and the provided number of seconds
    local d=$(($(date +%s) + "${seconds}"))

    # Loop until the current time is less than or equal to the end time
    while [ "$d" -ge `date +%s` ]; do
        # Print the remaining time in the format HH:MM:SS
        echo -ne "$(date -u --date @$(($d - `date +%s`)) +%H:%M:%S)\r";
        # Wait for 0.1 seconds before updating the countdown
        sleep 0.1
    done
}
