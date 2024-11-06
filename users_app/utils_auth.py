def split_username(username):
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
    return {
        'token': token.key,
        'username': user.username,
        'email': user.email,
        'user_id': user.pk,
    }