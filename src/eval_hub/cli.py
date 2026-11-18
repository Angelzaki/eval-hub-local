from __future__ import annotations

import argparse
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

from eval_hub.collect import collect
from eval_hub.render import render_html

console = Console()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eval-hub")
    parser.add_argument("--workspace", default="..", help="carpeta que contiene los labs")
    parser.add_argument("--out", default="results/dashboard.html")
    args = parser.parse_args(argv)

    workspace = Path(args.workspace).resolve()
    cards = collect(workspace)
    out = Path(args.out)
    render_html(cards, out)
    (out.parent / "dashboard.json").write_text(
        json.dumps(cards, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    table = Table(title="eval-hub-local")
    table.add_column("repo")
    table.add_column("summary")
    table.add_column("score", justify="right")
    for card in cards:
        score = "—" if card["score"] is None else f"{card['score']:.0%}"
        table.add_row(card["repo"], card["summary"], score)
    console.print(table)
    console.print(f"dashboard → {out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
