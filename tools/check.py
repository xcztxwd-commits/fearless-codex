"""Offline package checks. Run with Python 3.9+; no network or dependencies."""

import json
from pathlib import Path
import re
import tempfile

from sync_brand import ROOT, generated_files


def check():
    plugin = ROOT / "plugins" / "fearless-codex"
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    assert marketplace["name"] == "fearless-codex-marketplace"
    entry = marketplace["plugins"][0]
    assert entry["name"] == "fearless-codex"
    assert (ROOT / entry["source"]["path"]).resolve() == plugin.resolve()
    assert entry["policy"]["installation"] == "AVAILABLE"
    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == plugin.name
    assert manifest["skills"] == "./skills/"
    assert not any(k in manifest for k in ("mcpServers", "apps", "hooks"))
    skills = sorted((plugin / "skills").glob("*/SKILL.md"))
    assert len(skills) == 87, f"Expected 87 skills, got {len(skills)}"
    for path in skills:
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\n"), path
        header = text.split("---\n", 2)[1]
        name = re.search(r"^name: (\S+)$", header, re.M).group(1)
        assert name == path.parent.name and name.startswith("fearless-"), path
        assert len(name) <= 64, name
        assert re.search(r"^description: .+", header, re.M), path
        assert not re.search(r"^parent:", header, re.M), path
        for link in re.findall(r"\]\((\.\.?/[^)]+)\)", text):
            target = (path.parent / link).resolve()
            assert target.is_relative_to(plugin.resolve()) and target.is_file(), (path, link)
        for old in ("冷咖啡", "ColdBrew", "ASTRA//UNLOCK", "CHA-CODEX-POJIA", "1057540028", "1077074552", "618179023"):
            assert old not in text, (path, old)
    for relative, expected in generated_files().items():
        assert (ROOT / relative).read_text(encoding="utf-8") == expected, f"Run tools/sync_brand.py: {relative}"
    brand = json.loads((ROOT / "brand.json").read_text(encoding="utf-8"))
    assert brand["welcome"] in (plugin / "skills/fearless-start/SKILL.md").read_text(encoding="utf-8")
    # Check actual propagation, not only the current hard-coded greeting.
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        modified = dict(brand, wake_word="另一个启动口令", welcome="测试欢迎语")
        (root / "brand.json").write_text(json.dumps(modified), encoding="utf-8")
        rendered = generated_files(root)
        for text in rendered.values():
            assert modified["wake_word"] in text
            assert brand["wake_word"] not in text
        modified["wake_word"] = "bad\nword"
        (root / "brand.json").write_text(json.dumps(modified), encoding="utf-8")
        try:
            generated_files(root)
        except ValueError:
            pass
        else:
            raise AssertionError("Multiline wake words must be rejected")
    assert (ROOT / "LICENSE").is_file()
    print("PASS: 87 skills, marketplace, manifest, links, exact welcome, branding and input validation")


if __name__ == "__main__":
    check()
