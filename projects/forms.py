from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'status': forms.Select(
                choices=[
                    ('open', 'Открыт'),
                    ('closed', 'Закрыт'),
                ]
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['status'].initial = 'open'
