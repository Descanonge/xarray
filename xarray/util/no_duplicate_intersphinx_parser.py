"""Intersphinx will generate too much entries."""

from collections.abc import Generator

from doc2dash.parsers.intersphinx import InterSphinxParser
from doc2dash.parsers.intersphinx_inventory import load_inventory
from doc2dash.parsers.types import ParserEntry


class NoDuplicateInterSphinxParser(InterSphinxParser):
    def parse(self) -> Generator[ParserEntry, None, None]:
        # {"role": {"name": (path#anchor, display_name)}}
        inventory = load_inventory(self.source)

        to_remove: list[tuple[str, str]] = []

        for role in [t for t in inventory.keys() if t != "std:label"]:
            # remove redundant labels
            for path, display in inventory[role].values():
                for g_name, (g_path, g_display) in inventory["std:label"].items():
                    if g_path.replace("-", ".") == path or g_display == display:
                        to_remove.append(("std:label", g_name))

            # remove redundant docs
            if role == "std:doc":
                continue
            for path, _ in inventory[role].values():
                for g_name, (g_path, _) in inventory["std:doc"].items():
                    if g_path.split("#")[0] == path.split("#")[0]:
                        to_remove.append(("std:doc", g_name))

        # remove Dataset/DataArray sections in api.rst
        for name, (_, display) in inventory["std:label"].items():
            if name.startswith("/api.rst#"):
                if display in ["Dataset", "DataArray", "DataTree"]:
                    to_remove.append(("std:label", name))

        print(f"removing {len(to_remove)} elements")
        for role, name in to_remove:
            if name.startswith("example"):
                print(role, name)
            inventory[role].pop(name, None)

        yield from self._inv_to_entries(inventory)
