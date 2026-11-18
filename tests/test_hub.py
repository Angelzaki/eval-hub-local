from pathlib import Path

from eval_hub.collect import collect
from eval_hub.render import render_html


def test_collect_and_render(tmp_path):
    workspace = tmp_path / "ws"
    repo = workspace / "chunk-lab" / "results"
    repo.mkdir(parents=True)
    (repo / "chunk_experiment.json").write_text(
        '{"best":"sentence","strategies":{"sentence":{"retrieval_score":1.0}}}',
        encoding="utf-8",
    )
    cards = collect(workspace)
    assert any(c["repo"] == "chunk-lab" and c["score"] == 1.0 for c in cards)
    out = tmp_path / "dashboard.html"
    render_html(cards, out)
    html = out.read_text(encoding="utf-8")
    assert "chunk-lab" in html
    assert "eval-hub-local" in html
