from django import forms


class CsvUploadForm(forms.Form):
    csv_file = forms.FileField()
    csv_file.widget.attrs.update({'class': 'btn btn-high btn-success'})
