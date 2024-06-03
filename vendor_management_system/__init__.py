# Define the version of the module/package as a string.
__version__ = "0.1.0"

# Convert the version string into a tuple of integers and strings for easier comparison.
__version_info__ = tuple(
    # Convert each part of the version string to an integer if it's numeric, otherwise leave it as a string.
    int(num) if num.isdigit() else num

    # Replace the first hyphen with a dot and split the version string into components.
    for num in __version__.replace("-", ".", 1).split(".")
)
