# Django 3.2 Migration Guide

## Removing django-form-utils

The `django-form-utils` package is not compatible with Django 3.2. As part of the upgrade process, we've replaced it with a custom implementation in `qatrack.qatrack_core.forms`.

### Changes Made

1. Created a new `BetterFormMixin` and `BetterModelForm` in `qatrack.qatrack_core.forms` to replace the functionality from `django-form-utils`.
2. Updated the following forms to use the new implementation:
   - `qatrack.service_log.forms.ServiceEventForm`
   - `qatrack.faults.forms.FaultForm`
   - `qatrack.parts.forms.PartForm`
   - `qatrack.issue_tracker.forms.IssueForm`
3. Removed `django-form-utils` from `requirements/base.txt`.

### Testing

The new implementation has been tested with the following test cases:
- Basic fieldset functionality
- Forms without fieldsets
- Handling of missing fields
- HTML rendering of fieldsets with legends, classes, and descriptions

### Migration Steps

If you have any custom forms that use `django-form-utils.forms.BetterForm` or `django-form-utils.forms.BetterModelForm`, you should update them to use `qatrack.qatrack_core.forms.BetterModelForm` instead. The API is compatible, so no other changes should be necessary.

Example:

```python
# Old code
from form_utils.forms import BetterModelForm

class MyForm(BetterModelForm):
    ...

# New code
from qatrack.qatrack_core.forms import BetterModelForm

class MyForm(BetterModelForm):
    ...
```

### Known Issues

None identified. The new implementation provides the same functionality as `django-form-utils` for our use cases. 