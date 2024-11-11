from .serializers import FileUploadSerializer

def attach_file_to_obj(obj, file_data):
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
    if file_key in data_dict:
        return attach_file_to_obj(obj=obj, file_data=data_dict[file_key])