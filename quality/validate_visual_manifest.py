from __future__ import annotations

import argparse
import json
from pathlib import Path

from quality.visual_evidence import validate_visual_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Agentic Factory visual evidence manifest.")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    result = validate_visual_manifest(data)
    print(
        json.dumps(
            {"passed": result.passed, "issues": list(result.issues)},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
