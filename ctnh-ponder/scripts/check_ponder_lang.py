#!/usr/bin/env python3
"""Validate generated language entries for one CTNH Ponder scene.

This checks only the selected scene prefix, so unrelated legacy differences
between a module's language files do not hide a missing Ponder entry.
The script uses only the Python standard library.

Usage::

    python scripts/check_ponder_lang.py path/to/lang \
        --namespace ctnhbio --scene great_flesh_differentiation
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


DEFAULT_LOCALES = ("en_us", "zh_cn", "en_ud")
TEXT_KEY = re.compile(r"text_(\d+)$")


def load_lang(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing language file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"language file is not a JSON object: {path}")
    return value


def validate_scene(
    lang_dir: Path,
    namespace: str,
    scene: str,
    locales: tuple[str, ...],
) -> int:
    prefix = f"{namespace}.ponder.{scene}."
    entries: dict[str, dict[str, object]] = {}
    errors: list[str] = []

    for locale in locales:
        path = lang_dir / f"{locale}.json"
        try:
            data = load_lang(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        scene_entries = {
            key[len(prefix) :]: value
            for key, value in data.items()
            if key.startswith(prefix)
        }
        if not scene_entries:
            errors.append(f"{locale}: no entries found for {prefix}*")
        entries[locale] = scene_entries

    if entries:
        reference_locale = next(iter(entries))
        reference_keys = set(entries[reference_locale])
        for locale, scene_entries in entries.items():
            missing = sorted(reference_keys - set(scene_entries))
            extra = sorted(set(scene_entries) - reference_keys)
            if missing:
                errors.append(f"{locale}: missing keys: {', '.join(missing)}")
            if extra:
                errors.append(f"{locale}: unexpected keys: {', '.join(extra)}")

        suffixes = reference_keys
        for required in ("header", "title"):
            if required not in suffixes:
                errors.append(f"missing required key: {required}")

        text_numbers = sorted(
            int(match.group(1))
            for suffix in suffixes
            if (match := TEXT_KEY.fullmatch(suffix))
        )
        expected_numbers = list(range(1, len(text_numbers) + 1))
        if text_numbers != expected_numbers:
            errors.append(
                "text keys are not contiguous: "
                f"found {text_numbers}, expected {expected_numbers}"
            )

        for locale, scene_entries in entries.items():
            for suffix, value in scene_entries.items():
                if suffix in {"header", "title"} or TEXT_KEY.fullmatch(suffix):
                    if not isinstance(value, str) or not value.strip():
                        errors.append(f"{locale}: empty value for {suffix}")

        print(
            f"scene       : {namespace}:{scene}"
            f"\nlocales     : {', '.join(entries)}"
            f"\ntext count  : {len(text_numbers)}"
        )

    if errors:
        for error in errors:
            print(f"error       : {error}", file=sys.stderr)
        return 1

    print("validation  : ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate generated language entries for one CTNH Ponder scene"
    )
    parser.add_argument("lang_dir", type=Path, help="directory containing locale JSON files")
    parser.add_argument("--namespace", required=True, help="mod id, such as ctnhbio")
    parser.add_argument("--scene", required=True, help="scene id, such as great_flesh_growth")
    parser.add_argument(
        "--locales",
        nargs="+",
        default=DEFAULT_LOCALES,
        help="locale names without .json (default: en_us zh_cn en_ud)",
    )
    args = parser.parse_args(argv)
    return validate_scene(
        args.lang_dir,
        args.namespace,
        args.scene,
        tuple(args.locales),
    )


if __name__ == "__main__":
    sys.exit(main())
