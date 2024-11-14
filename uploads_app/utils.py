from .serializers import FileUploadSerializer

def attach_file_to_obj(obj, file_data):
    """
    Attach a new file to an object, replacing the previous file if it exists.

    Args:
        obj (model instance): The object to which the file will be attached.
        file_data (File): The file to attach to the object.
    """
    try:
        serializer = FileUploadSerializer(data={'file': file_data})
        if serializer.is_valid(raise_exception=True):
            new_file = serializer.save()
            if obj.file:
                obj.file.delete()
            obj.file = new_file
            obj.save()
    except:
        return serializer.errors
    return None

def handle_file_update(obj, data_dict, file_key):
    """
    Check if a file update is requested and handle the file attachment.

    Args:
        obj (model instance): The object to which the file will be attached.
        data_dict (dict): The dictionary containing the file data.
        file_key (str): The key in the dictionary representing the file to be uploaded.
    """
    if file_key in data_dict:
        return attach_file_to_obj(obj=obj, file_data=data_dict[file_key])