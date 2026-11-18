from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def render_html(cards: list[dict], out_path: Path) -> None:
    rows = []
    for card in cards:
        score = "—" if card["score"] is None else f"{card['score']:.0%}"
        status = "ok" if card["exists"] else "missing"
        arts = ", ".join(a["path"] for a in card["artifacts"]) or "—"
        rows.append(
            f"<tr class='{status}'><td>{card['repo']}</td><td>{card['summary']}</td>"
            f"<td>{score}</td><td>{arts}</td></tr>"
        )
    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <title>eval-hub-local</title>
  <style>
    body {{ font-family: JetBrains Mono, Consolas, monospace; background:#0D1117; color:#E6EDF3; margin:2rem; }}
    h1 {{ color:#A371F7; margin-bottom:.2rem; }}
    .meta {{ color:#8B949E; margin-bottom:1.5rem; }}
    table {{ border-collapse: collapse; width: min(980px, 100%); }}
    th, td {{ border:1px solid #30363D; padding:.6rem .75rem; text-align:left; }}
    th {{ background:#161B22; color:#1F6FEB; }}
    tr.missing td {{ color:#8B949E; }}
  </style>
</head>
<body>
  <h1>eval-hub-local</h1>
  <p class="meta">Angel Salazar · {datetime.now(timezone.utc).isoformat()}</p>
  <table>
    <thead><tr><th>repo</th><th>summary</th><th>score</th><th>artifacts</th></tr></thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</body>
</html>
"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
