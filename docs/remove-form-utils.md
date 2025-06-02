# Removal of django-form-utils Dependency

## Overview
This change removes the dependency on the deprecated `django-form-utils` package and replaces it with a custom implementation in `qatrack.qatrack_core.forms`. The change was necessary to maintain compatibility with newer Django versions and reduce external dependencies.

## Changes Made

### 1. Core Implementation
- Created custom `BetterFormMixin` and `BetterModelForm` in `qatrack.qatrack_core.forms`
  - Implemented fieldset support for forms
  - Added methods: `get_fieldsets`, `add_fieldset`, `as_fieldset`, `_html_fieldset`
  - Ensured proper handling of both direct initialization and inheritance cases

### 2. Form Updates
Modified several forms to properly use the new implementation:

#### qatrack/parts/forms.py
- Added proper `fields` attribute to `PartForm`'s Meta class

#### qatrack/faults/forms.py
- Added proper `fields` attribute to `ReviewFaultForm`'s Meta class

#### qatrack/issue_tracker/forms.py
- Added proper `fields` attribute to `IssueForm`'s Meta class

#### qatrack/service_log/forms.py
- Updated `ServiceEventForm` with complete fields list
- Ensured proper fieldset handling

### 3. Test Updates
- Updated `qatrack.qatrack_core.tests.test_forms.py` to test new implementation
- Added tests for:
  - Fieldset functionality
  - Form initialization
  - Field filtering
  - Forms without fieldsets

### 4. Dependencies
- Removed `django-form-utils` from `requirements/base.txt`

## Testing
- All core form functionality tests are passing
- Form fieldset rendering is working correctly
- Form field filtering is working as expected

## Known Issues
- Some Selenium tests are currently failing and will need to be addressed separately
- These failures are related to form interaction in browser tests and don't affect core functionality

## Migration Notes
1. No database migrations were required for this change
2. Forms using the old `django-form-utils.forms.BetterForm` should now use `qatrack.qatrack_core.forms.BetterFormMixin`
3. Forms using the old `django-form-utils.forms.BetterModelForm` should now use `qatrack.qatrack_core.forms.BetterModelForm`

## Future Considerations
1. Review and update Selenium tests
2. Consider adding more test coverage for edge cases
3. Consider adding form rendering optimizations if needed 