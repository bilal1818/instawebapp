from django import forms
from .models import MediaContent, Comment, Rating

class MediaContentForm(forms.ModelForm):
    """Form for uploading media content"""
    
    class Meta:
        model = MediaContent
        fields = ['file', 'title', 'caption', 'location', 'people_present']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'people_present': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        
    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop('creator', None)
        super().__init__(*args, **kwargs)
        
        # Set required fields
        self.fields['file'].required = True
        self.fields['title'].required = True
        
        # Add help texts
        self.fields['file'].help_text = "Supported formats: JPG, PNG, MP4. Max size: 50MB."
        self.fields['title'].help_text = "Required. Give your media a descriptive title."
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.creator:
            instance.creator = self.creator
        if commit:
            instance.save()
        return instance

class CommentForm(forms.ModelForm):
    """Form for adding comments to media content"""
    
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add your comment here...'}),
        }

class RatingForm(forms.ModelForm):
    """Form for rating media content"""
    
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.Select(attrs={'class': 'form-select'}, choices=[(i, i) for i in range(1, 6)]),
        } 