#!/usr/bin/env bash

# Define a function to prompt for confirmation
yes_no() {
    # Description of the function
    declare desc="Prompt for confirmation. \$\"\{1\}\": confirmation message."

    # Get the confirmation message from the first argument
    local arg1="${1}"

    local response=

    # Prompt the user for confirmation
    read -r -p "${arg1} (y/[n])? " response

    # Check if the user's response is 'y' or 'Y'
    if [[ "${response}" =~ ^[Yy]$ ]]; then
        # Exit with a success status if the response is 'y' or 'Y'
        exit 0
    else
        # Exit with a failure status if the response is anything else
        exit 1
    fi
}
