"""Localization must work from the first commit, not be retrofitted.

The rule these tests enforce: a string that reaches a user exists, translated,
in every target locale. A catalog with an empty ``msgstr`` is a half-translated
release, and there is no point in the build at which that is acceptable.
"""

from __future__ import annotations

import re
from pathlib import Path

from core import i18n

REPO_ROOT = Path(__file__).resolve().parent.parent
POT = REPO_ROOT / "locales" / "neural_accord.pot"


def parse_catalog(path: Path) -> dict[str, str]:
    """Return ``{msgid: msgstr}`` for a .po/.pot file, handling wrapped strings.

    Written by hand rather than with a library so the completeness check has no
    dependency that a contributor might not have installed.
    """
    lines = path.read_text(encoding="utf-8").split("\n")
    entries: dict[str, str] = {}
    index = 0

    def collect(keyword: str) -> str:
        nonlocal index
        chunks = [lines[index][len(keyword) :].strip()[1:-1]]
        index += 1
        while index < len(lines) and lines[index].startswith('"'):
            chunks.append(lines[index].strip()[1:-1])
            index += 1
        return "".join(chunks).replace('\\"', '"').replace("\\\\", "\\")

    while index < len(lines):
        if lines[index].startswith("msgid "):
            msgid = collect("msgid ")
            has_msgstr = index < len(lines) and lines[index].startswith("msgstr ")
            msgstr = collect("msgstr ") if has_msgstr else ""
            if msgid:
                entries[msgid] = msgstr
        else:
            index += 1
    return entries


def catalog_path(locale: str) -> Path:
    return i18n.locale_dir() / locale.replace("-", "_") / "LC_MESSAGES" / "neural_accord.po"


def test_activate_falls_back_to_the_source_locale() -> None:
    assert i18n.activate("zz-ZZ") is not None
    assert i18n.gettext("Configuration error: {reason}") == "Configuration error: {reason}"


def test_every_target_locale_has_a_catalog() -> None:
    missing = [locale for locale in i18n.TARGET_LOCALES if not catalog_path(locale).is_file()]
    assert not missing, f"No catalog for: {', '.join(missing)}"


def test_no_locale_directory_is_undeclared() -> None:
    """A catalog on disk that TARGET_LOCALES does not name would ship untested."""
    declared = {locale.replace("-", "_") for locale in i18n.TARGET_LOCALES}
    on_disk = {path.name for path in i18n.locale_dir().iterdir() if path.is_dir()}
    assert on_disk == declared


def test_every_catalog_covers_every_source_string() -> None:
    source_ids = {msgid for msgid in parse_catalog(POT)}
    assert source_ids, "The source catalog is empty; run pybabel extract."

    incomplete: list[str] = []
    for locale in i18n.TARGET_LOCALES:
        entries = parse_catalog(catalog_path(locale))
        for msgid in source_ids:
            if not entries.get(msgid, "").strip():
                incomplete.append(f"{locale}: {msgid[:48]!r}")
    assert not incomplete, "Untranslated entries: " + "; ".join(incomplete)


def test_placeholders_survive_translation() -> None:
    """A translated string that drops or renames a placeholder crashes at format time."""
    placeholder = re.compile(r"\{[^{}]*\}")
    broken: list[str] = []
    for locale in i18n.TARGET_LOCALES:
        for msgid, msgstr in parse_catalog(catalog_path(locale)).items():
            if set(placeholder.findall(msgid)) != set(placeholder.findall(msgstr)):
                broken.append(f"{locale}: {msgid[:48]!r}")
    assert not broken, "Placeholder mismatch: " + "; ".join(broken)


def test_cli_strings_are_wrapped_for_translation() -> None:
    """Guard against a bare user-facing literal creeping into the CLI."""
    source = (REPO_ROOT / "core" / "cli.py").read_text(encoding="utf-8")
    printed = re.findall(r"print\(\s*(.)", source)
    assert printed, "Expected the CLI to print something."
    assert all(char == "_" for char in printed), "Every printed string must go through _()."
