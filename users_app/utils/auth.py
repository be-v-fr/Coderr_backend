def split_username(username):
    """
    Splits a username into first and last names based on the last space or underscore.

    :param username: The username to split.
    :type username: str
    :return: A tuple containing the first name and last name.
    :rtype: tuple(str, str)
    """
    if ' ' in username or '_' in username:
        last_space = username.rfind(' ')
        last_underscore = username.rfind('_')
        split_index = last_space if last_space > last_underscore else last_underscore
        first_name = username[:split_index].strip()
        last_name = username[split_index + 1:].strip()
        return first_name, last_name
    else:
        return username, ''

def get_auth_response_data(user, token):
    """
    Constructs an authentication response data dictionary.

    :param user: The user object containing authentication details.
    :type user: User
    :param token: The token object representing the user's authentication token.
    :type token: Token
    :return: A dictionary with the user's authentication response data.
    :rtype: dict
    """
    return {
        'token': token.key,
        'username': user.username,
        'email': user.email,
        'user_id': user.pk,
    }