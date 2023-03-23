def get_input(prompt, type_=None, min_=None, max_=None):
    """
    A function that prompts the user for an input and validates it based on the specified type, minimum and maximum values.
    If the input is invalid, it will raise a ValueError with an appropriate error message.
    
    Args:
    - prompt: A string that serves as the prompt for the user input.
    - type_: A type that the user input will be casted into.
    - min_: A number that specifies the minimum allowable value for the user input.
    - max_: A number that specifies the maximum allowable value for the user input.
    
    Returns:
    - value: The validated user input.
    """
    while True:
        try:
            value = type_(input(prompt))
            if min_ is not None and value < min_:
                raise ValueError(f"{prompt} cannot be less than {min_}")
            if max_ is not None and value > max_:
                raise ValueError(f"{prompt} cannot be greater than {max_}")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}\n")
    """
    A while loop that continues to prompt the user for an input until a valid input is given.
    A try-except block that attempts to cast the user input into the specified type, and validates the input
    based on the minimum and maximum allowable values. If the input is invalid, it raises a ValueError with
    an appropriate error message. If the input is valid, it returns the validated user input.
    """