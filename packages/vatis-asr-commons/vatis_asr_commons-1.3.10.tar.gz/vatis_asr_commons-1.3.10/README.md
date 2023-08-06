# asr-commons

Project containing commons classes for ASR projects

## Deploying
When releasing a new version, the version in the `setup.py` must be updated

## Making translations
Generate template based on code:
```xgettext -d base -o vatis/asr/speakers/i18n/locale/speakers_service.pot <file>.py```

Compile new translates
``` msgfmt -o vatis/asr/speakers/i18n/locale/en/LC_MESSAGES/speakers_service.mo vatis/asr/speakers/i18n/locale/en/LC_MESSAGES/speakers_service```

More details [here](https://simpleit.rocks/python/how-to-translate-a-python-project-with-gettext-the-easy-way/)