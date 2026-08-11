"""Localization for every user-facing string in Neural Accord.

Neural Accord is internationalized from the first commit. No user-facing string
is written as a bare literal: it is wrapped in :func:`_` (or :func:`ngettext`
for plurals) so that it is extracted into ``locales/neural_accord.pot`` and
translated in every target locale.

The active locale is resolved, in order, from:

1. the ``--lang`` command-line option, passed to :func:`activate`;
2. the ``NEURAL_ACCORD_LANG`` environment variable;
3. the standard ``LC_ALL`` / ``LC_MESSAGES`` / ``LANG`` environment variables;
4. English, the source language.

Machine-readable output (traces, metrics, resolved configurations, seed
manifests) is deliberately *not* localized. A report has to compare across
machines and across languages, so its keys and enumerated values stay in the
source language; only text addressed to a human reader passes through here.
"""

from __future__ import annotations

import gettext as _gettext
import os
from pathlib import Path

DOMAIN = "neural_accord"

SOURCE_LOCALE = "en"

#: Locales the project ships translations for. Keep in sync with ``locales/``.
#: Serbian is carried in Latin script. Simplified and Traditional Chinese are
#: separate translations, not one copied onto the other.
TARGET_LOCALES: tuple[str, ...] = (
    "en",
    "bn",
    "ceb",
    "de",
    "el",
    "es",
    "fil",
    "fr",
    "hi",
    "id",
    "it",
    "ja",
    "ko",
    "nl",
    "pt",
    "ru",
    "sq",
    "sr",
    "th",
    "tr",
    "vi",
    "zh-Hans",
    "zh-Hant",
)

_translation: _gettext.NullTranslations = _gettext.NullTranslations()
_active_locale: str = SOURCE_LOCALE


def locale_dir() -> Path:
    """Return the directory holding the compiled message catalogs.

    Checked in-tree first (a working copy runs straight from the repository)
    and then next to the installed package.
    """
    packaged = Path(__file__).parent / "locales"
    if packaged.is_dir():
        return packaged
    return Path(__file__).parent.parent / "locales"


def _candidates(requested: str | None) -> list[str]:
    """Build the ordered locale preference list for :func:`activate`."""
    raw = [
        requested,
        os.environ.get("NEURAL_ACCORD_LANG"),
        os.environ.get("LC_ALL"),
        os.environ.get("LC_MESSAGES"),
        os.environ.get("LANG"),
    ]
    names: list[str] = []
    for value in raw:
        if not value:
            continue
        tag = value.split(".")[0].split("@")[0].strip()
        if not tag or tag in {"C", "POSIX"}:
            continue
        # Accept both BCP 47 (pt-BR) and POSIX (pt_BR) spellings.
        normalized = tag.replace("_", "-")
        for name in (normalized, normalized.replace("-", "_"), normalized.split("-")[0]):
            if name and name not in names:
                names.append(name)
    names.append(SOURCE_LOCALE)
    return names


def activate(locale: str | None = None) -> str:
    """Install the best available translation and return the locale chosen."""
    global _translation, _active_locale

    candidates = _candidates(locale)
    _translation = _gettext.translation(
        DOMAIN,
        localedir=str(locale_dir()),
        languages=candidates,
        fallback=True,
    )
    info = _translation.info()
    _active_locale = str(info.get("language") or candidates[0])
    return _active_locale


def active_locale() -> str:
    """Return the locale currently in effect."""
    return _active_locale


def gettext(message: str) -> str:
    """Translate ``message`` into the active locale."""
    return _translation.gettext(message)


def ngettext(singular: str, plural: str, n: int) -> str:
    """Translate a message whose form depends on the count ``n``."""
    return _translation.ngettext(singular, plural, n)


#: Short alias used at call sites, and the marker xgettext extracts on.
_ = gettext

__all__ = [
    "DOMAIN",
    "SOURCE_LOCALE",
    "TARGET_LOCALES",
    "_",
    "activate",
    "active_locale",
    "gettext",
    "locale_dir",
    "ngettext",
]
