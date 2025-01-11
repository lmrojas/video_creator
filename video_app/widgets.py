from django.forms import widgets
from django.forms.widgets import Input

class MultipleFileInput(Input):
    """Widget personalizado para subir múltiples archivos."""
    
    input_type = 'file'
    needs_multipart_form = True
    
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['multiple'] = True
        super().__init__(attrs)
    
    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)
    
    def value_omitted_from_data(self, data, files, name):
        return not any(key.startswith(name) for key in files) 