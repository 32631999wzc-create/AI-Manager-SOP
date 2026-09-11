import json
from pathlib import Path
root=Path(__file__).parent
full=json.loads((root/"output.json").read_text(encoding="utf-8"))
assert full["summary"]=={"received":5,"unique":4,"duplicates":1}
assert all(theme["evidence"] for theme in full["themes"])
filtered_path=root/"filtered-output.json"
if filtered_path.exists():
    filtered=json.loads(filtered_path.read_text(encoding="utf-8"))
    assert filtered["summary"]["received"]==2
    assert all(item["source"]=="support" for item in filtered["items"])
    assert all(theme["evidence"] for theme in filtered["themes"])
print("PASS: available Golden outputs are complete and evidence-linked")
