import gettext
from pathlib import Path
from threading import RLock
from typing import Optional

from vatis.asr_commons.config import Language, logging

logger = logging.get_logger(__name__)


class TranslateManager:
    """
    Usage:

    with translate_manager.i18n('ro_RO'):
        ...
        internationalized code
        ...
    """
    def __init__(self, locales_base_path: Path, default_locale: str = 'en'):
        assert locales_base_path is not None

        self._locales_base_path: Path = locales_base_path
        self._translating: bool = False
        self._lock: RLock = RLock()
        self._translate: Optional[gettext.NullTranslations] = None
        self._default_locale: str = default_locale

    def i18n(self, domain: str, language: Optional[Language] = None, fallback: bool = True) -> 'TranslateManager':
        with self._lock:
            if self._translating:
                raise ValueError('Already translating')
            self._translating = True

            locale: str = language.value if language is not None else ''

            available_translations_files = gettext.find(domain=domain,
                                                        localedir=self._locales_base_path,
                                                        languages=[locale],
                                                        all=True)

            if not len(available_translations_files):
                # if no translation was found for selected language, fallback on default locale
                logger.warning(f'No i18n file for language {locale}. Falling back on {self._default_locale}')
                locale = self._default_locale

            self._translate = gettext.translation(domain, localedir=self._locales_base_path,
                                                  languages=[locale],
                                                  fallback=fallback)

            return self

    @property
    def translating(self) -> bool:
        return self._translating

    def __enter__(self):
        with self._lock:
            if not self._translating:
                raise ValueError('Not translating. i18n() method must be called')

    def __exit__(self, exc_type, exc_val, exc_tb):
        with self._lock:
            self._translating = False
            self._translate = None

    def translate(self, key: str) -> str:
        assert key is not None

        with self._lock:
            if not self._translating:
                raise ValueError('Translation manager context not initialized. See class description')

            return self._translate.gettext(key)


current_file_path: Path = Path(__file__)
locales_base_path: Path = Path(current_file_path.parent, 'locale')

translate_manager = TranslateManager(locales_base_path)
_ = translate_manager.translate
