def compare_to_string(string_1, string_2):
    """This function compares two string

    :param string_1: The first string to compare.
    :param string_2: The second string to compare with the first
    :return: The value 0 if the string_2 is lexicographically equal to string_1;
      a value less than 0 if string_2 is lexicographically greater than string_1;
      and a value greater than 0 if the string_2 is lexicographically less than string_1.
    :rtype: int
    """
    if string_1 == string_2:
        return 0
    return 1 if string_1 > string_2 else -1


def compare_to_boolean(bool_1, bool_2):
    """This function compares two boolean

    :param bool_1: The first boolean to compare.
    :param bool_2: The second boolean to compare with the first
    :return: The value 0 if if bool_1 represents the same boolean value as
      the bool_2 a value less than 0 if bool_1 represents true and bool_2
      represents false; and a value greater than 0 if bool_1 represents false
      and bool_2 represents true.
    :rtype: int
    """
    if bool_1 == bool_2:
        return 0
    return 1 if bool_1 and not bool_2 else -1


def compare_to_number(number_1, number_2):
    """This function compares two number, integer or float

    :param number_1: The first number to compare.
    :param number_2: The second number to compare with the first
    :return: The value 0 if the number_2  is equal to number_1; a value
      less than 0 if number_2 is greater than number_1; and a value greater
      than 0 if the number_2 is less than number_1.
    :rtype: int
    """
    if number_1 == number_2:
        return 0
    return 1 if number_1 > number_2 else -1
