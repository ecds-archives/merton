from django import forms
from eulxml.xmlmap.teimap import Tei, TeiDiv, TEI_NAMESPACE

class SearchForm(forms.Form):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    keyword = forms.CharField(required=False)
    def clean(self):
        cleaned_data = self.cleaned_data
        keyword = cleaned_data.get('keyword')
        if not keyword:
            del cleaned_data['keyword']
            raise forms.ValidationError('No search term given.')
        return cleaned_data