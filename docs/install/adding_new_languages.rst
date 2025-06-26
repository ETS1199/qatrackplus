Adding New Languages to QATrack+
=================================

This guide explains how to add support for new languages to QATrack+.

Overview
--------

QATrack+ uses Django's internationalization (i18n) framework to support multiple languages. The process involves:

1. Setting up the language directory structure
2. Creating/generating translation files (.po files)
3. Translating the content
4. Compiling translation files (.mo files)
5. Configuring Django settings

Prerequisites
-------------

- QATrack+ installed and working
- Access to the command line
- Virtual environment activated (``source .venv/bin/activate``)
- For automatic translation: ``googletrans`` library installed

Step 1: Language Codes
----------------------

First, determine the correct language code for your target language. Django uses standard language codes:

+---------------------+----------+-----------+
| Language            | Code     | Example   |
+=====================+==========+===========+
| French              | ``fr``   | ``fr``    |
+---------------------+----------+-----------+
| German              | ``de``   | ``de``    |
+---------------------+----------+-----------+
| Spanish             | ``es``   | ``es``    |
+---------------------+----------+-----------+
| Italian             | ``it``   | ``it``    |
+---------------------+----------+-----------+
| Portuguese          | ``pt``   | ``pt``    |
+---------------------+----------+-----------+
| Chinese (Simplified)| ``zh-hans`` | ``zh-hans`` |
+---------------------+----------+-----------+
| Japanese            | ``ja``   | ``ja``    |
+---------------------+----------+-----------+
| Arabic              | ``ar``   | ``ar``    |
+---------------------+----------+-----------+

For a complete list, see: `Django Language Codes <https://docs.djangoproject.com/en/3.2/topics/i18n/#term-language-code>`_

Step 2: Create Language Directory Structure
-------------------------------------------

Create the required directory structure for your language. Replace ``{LANGUAGE_CODE}`` with your target language code:

.. code-block:: bash

   # Navigate to QATrack+ root directory
   cd /path/to/qatrackplus

   # Create directory structure (example for German 'de')
   mkdir -p qatrack/locale/de/LC_MESSAGES

Step 3: Generate Translation Files (.po files)
----------------------------------------------

Django can automatically extract all translatable strings from your codebase and create a ``.po`` file:

.. code-block:: bash

   # Activate virtual environment
   source .venv/bin/activate

   # Generate .po file for your language (example: German)
   python manage.py makemessages -l de --ignore=node_modules --ignore=venv --ignore=env

This creates: ``qatrack/locale/de/LC_MESSAGES/django.po``

**Note:** The ``--ignore`` flags are optional but recommended to skip irrelevant directories and speed up the process.

Step 4: Translate the Content
-----------------------------

You have two options for translating the content:

Option A: Automatic Translation (Recommended for Initial Setup)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

QATrack+ includes a translation script that uses Google Translate to automatically translate all strings:

.. code-block:: bash

   # For batch translation (recommended for large files)
   python scripts/unified_translation_manager.py batch de

   # Alternative: Regular translation (all at once)
   python scripts/unified_translation_manager.py translate de

**Important Note**: Google Translate's automatic translations are not perfect and may contain errors, especially for technical or medical terminology used in QATrack+. **All translations should be thoroughly reviewed by a native speaker or professional translator before use in production.**

**Batch vs Regular Translation:**

- **Batch**: Processes translations in groups (50 at a time), saves progress after each batch
- **Regular**: Processes all translations at once, faster but riskier for large files

The script will:

- Create a backup of your .po file
- Translate all empty ``msgstr ""`` entries
- Handle special characters and formatting
- Save failed translations to ``scripts/failed_translations.txt`` for manual review

Option B: Manual Translation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open ``qatrack/locale/{LANGUAGE_CODE}/LC_MESSAGES/django.po`` in a text editor and manually translate entries:

.. code-block:: po

   # Before (English)
   msgid "Login"
   msgstr ""

   # After (German)
   msgid "Login"
   msgstr "Anmelden"


Step 5: Compile Translation Files (.mo files)
---------------------------------------------

After translation, compile the ``.po`` file to binary ``.mo`` format that Django uses:

.. code-block:: bash

   # Activate virtual environment
   source .venv/bin/activate

   # Compile messages
   python manage.py compilemessages

This creates: ``qatrack/locale/{LANGUAGE_CODE}/LC_MESSAGES/django.mo``

Step 6: Configure Django Settings
---------------------------------

Configure Local Settings
~~~~~~~~~~~~~~~~~~~~~~~~

Edit your ``qatrack/local_settings.py`` file to enable and configure the new language:

.. code-block:: python

   import os

   # Enable internationalization
   USE_I18N = True
   USE_L10N = True

   # Set your language code
   LANGUAGE_CODE = 'de'  # Replace with your language code

   # Configure locale paths
   LOCALE_PATHS = [
       os.path.join(os.path.dirname(__file__), 'locale'),
   ]

   # Optional: Configure available languages for language switching
   LANGUAGES = [
       ('en', 'English'),
       ('fr', 'Français'),
       ('de', 'Deutsch'),
       ('es', 'Español'),
       # Add your language here
   ]

   # Your other settings...
   TIME_ZONE = 'Europe/Berlin'  # Adjust timezone as needed

Example Configuration for Specific Languages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

French Configuration
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import os

   USE_I18N = True
   USE_L10N = True
   LANGUAGE_CODE = 'fr'

   LOCALE_PATHS = [
       os.path.join(os.path.dirname(__file__), 'locale'),
   ]

   LANGUAGES = [
       ('en', 'English'),
       ('fr', 'Français'),
   ]

   TIME_ZONE = 'Europe/Paris'

German Configuration
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import os

   USE_I18N = True
   USE_L10N = True
   LANGUAGE_CODE = 'de'

   LOCALE_PATHS = [
       os.path.join(os.path.dirname(__file__), 'locale'),
   ]

   LANGUAGES = [
       ('en', 'English'),
       ('de', 'Deutsch'),
   ]

   TIME_ZONE = 'Europe/Berlin'

Spanish Configuration
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import os

   USE_I18N = True
   USE_L10N = True
   LANGUAGE_CODE = 'es'

   LOCALE_PATHS = [
       os.path.join(os.path.dirname(__file__), 'locale'),
   ]

   LANGUAGES = [
       ('en', 'English'),
       ('es', 'Español'),
   ]

   TIME_ZONE = 'Europe/Madrid'

Step 7: Test Your Translation
-----------------------------

1. **Restart the Django development server:**

   .. code-block:: bash

      python manage.py runserver

2. **Check the interface:** Navigate to QATrack+ in your browser and verify that text appears in your target language.

3. **Test different pages:** Check various parts of the application to ensure translations are working.



Common Issues
~~~~~~~~~~~~~

1. **Translations not appearing:**

   - Check that ``USE_I18N = True`` in settings
   - Verify ``.mo`` files exist and is not empty: ``qatrack/locale/{LANGUAGE_CODE}/LC_MESSAGES/django.mo``
   - Restart the Django server

2. **Permission errors:**

   - Ensure you have write permissions to the ``qatrack/locale/`` directory
   - Check that virtual environment is activated

3. **Google Translate API errors:**

   - The automatic translation uses a free API that may have rate limits
   - Use ``batch`` mode for better reliability
   - Check ``scripts/failed_translations.txt`` for failed translations

4. **Missing translations:**

   - Re-run ``python manage.py makemessages -l {LANGUAGE_CODE}`` to update .po file
   - Translate any new strings manually or with the script
   - Re-compile with ``python manage.py compilemessages``

File Structure Check
~~~~~~~~~~~~~~~~~~~

Your final directory structure should look like:

.. code-block:: text

   qatrack/
   ├── locale/
   │   ├── en/
   │   ├── fr/
   │   ├── de/
   │   └── {YOUR_LANGUAGE}/
   │       └── LC_MESSAGES/
   │           ├── django.po
   │           └── django.mo
   └── ...

Updating Translations
---------------------

When QATrack+ is updated with new features, you may need to update translations:

.. code-block:: bash

   # 1. Update .po file with new strings
   python manage.py makemessages -l {LANGUAGE_CODE} --ignore=node_modules

   # 2. Translate new strings (only translates empty msgstr entries)
   python3 scripts/unified_translation_manager.py batch {LANGUAGE_CODE}

   # 3. Compile updated translations
   python manage.py compilemessages

Contributing Translations
-------------------------

If you create a high-quality translation, consider contributing it back to the QATrack+ project:

1. Fork the QATrack+ repository
2. Add your translation files
3. Submit a pull request with your translation

Resources
---------

- `Django Internationalization Documentation <https://docs.djangoproject.com/en/3.2/topics/i18n/>`_
- `Django Language Codes <https://docs.djangoproject.com/en/3.2/topics/i18n/#term-language-code>`_
- `Poedit Translation Editor <https://poedit.net/>`_
- `Google Translate <https://translate.google.com/>`_ for reference translations

Support
-------

If you encounter issues adding a new language:

1. Check the troubleshooting section above
2. Review the QATrack+ documentation
3. Ask for help in the QATrack+ community forums
4. Open an issue on the GitHub repository