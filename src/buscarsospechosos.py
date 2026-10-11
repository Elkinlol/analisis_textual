import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
corpus = json.load(open(BASE / "data" / "corpus.json", encoding="utf-8"))

sospechosos = {"edu", "sys", "ap", "col", "cur", "cal", "ers", "ing",
               "der", "eld", "rst", "ed", "et", "al", "zju", "cn"}

for i, d in enumerate(corpus, 1):
    ab = d["abstract"].lower()
    for t in sospechosos:
        for m in re.finditer(rf"\b{t}\b", ab):
            print(i, t, "->", ab[max(0, m.start() - 25): m.end() + 25])

print("Revisión terminada.")