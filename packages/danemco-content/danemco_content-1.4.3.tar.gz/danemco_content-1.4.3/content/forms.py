from django import forms

from models import Snippet


def _get_forms():
    for key, form in Snippet.forms.items():
        yield (key, form.label)


class SnippetFormList(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SnippetFormList, self).__init__(*args, **kwargs)
        self.fields['snippet_form'] = forms.ChoiceField(choices=_get_forms())

    @property
    def form(self):
        return Snippet.forms[self.cleaned_data['snippet_form']]
