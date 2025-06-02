from django import forms
from django.test import TestCase

from qatrack.qatrack_core.forms import BetterFormMixin, BetterModelForm


class TestForm(forms.Form):
    """A test form with fieldsets."""
    name = forms.CharField()
    age = forms.IntegerField()
    email = forms.EmailField()

    fieldsets = [
        ('personal', {
            'fields': ['name', 'age'],
            'legend': 'Personal Information',
            'classes': ['personal-info'],
            'description': 'Your personal details',
        }),
        ('contact', {
            'fields': ['email'],
        }),
    ]


class BetterFormMixinTest(TestCase):
    """Test the BetterFormMixin functionality."""

    def setUp(self):
        self.form = TestForm()
        BetterFormMixin.__init__(self.form)

    def test_get_fieldsets(self):
        """Test that fieldsets are correctly processed."""
        fieldsets = self.form.get_fieldsets()
        self.assertEqual(len(fieldsets), 2)
        
        personal, contact = fieldsets
        
        self.assertEqual(personal[0], 'personal')
        self.assertEqual(personal[1]['fields'], ['name', 'age'])
        self.assertEqual(personal[1]['legend'], 'Personal Information')
        self.assertEqual(personal[1]['classes'], ['personal-info'])
        self.assertEqual(personal[1]['description'], 'Your personal details')
        
        self.assertEqual(contact[0], 'contact')
        self.assertEqual(contact[1]['fields'], ['email'])

    def test_form_without_fieldsets(self):
        """Test that forms without fieldsets work correctly."""
        class NoFieldsetsForm(forms.Form):
            name = forms.CharField()
        
        form = NoFieldsetsForm()
        BetterFormMixin.__init__(form)
        fieldsets = form.get_fieldsets()
        
        self.assertEqual(len(fieldsets), 1)
        self.assertEqual(fieldsets[0][1]['fields'], ['name'])

    def test_as_fieldset(self):
        """Test that as_fieldset renders the correct HTML."""
        html = self.form.as_fieldset()
        
        # Check for fieldset elements
        self.assertIn('<fieldset class="personal-info">', html)
        self.assertIn('<legend>Personal Information</legend>', html)
        self.assertIn('<p class="description">Your personal details</p>', html)
        
        # Check for form fields
        self.assertIn('name="name"', html)
        self.assertIn('name="age"', html)
        self.assertIn('name="email"', html)

    def test_missing_field(self):
        """Test that fieldsets handle missing fields gracefully."""
        class MissingFieldForm(BetterFormMixin, forms.Form):
            name = forms.CharField()
            fieldsets = [
                ('test', {
                    'fields': ['name', 'nonexistent_field'],
                }),
            ]

        form = MissingFieldForm()
        fieldsets = form.get_fieldsets()
        
        self.assertEqual(len(fieldsets), 1)
        name, options = fieldsets[0]
        self.assertEqual(options['fields'], ['name'])  # nonexistent_field should be filtered out 