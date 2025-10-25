# ...existing code...
import csv
import os
import random
import statistics
import sys
from collections import defaultdict

SAMPLE_ROWS = [
    {"name": "Alex", "city": "Seattle", "hobby": "skateboarding", "score": "72"},
    {"name": "Rina", "city": "Tokyo", "hobby": "origami", "score": "88"},
    {"name": "Sam", "city": "Berlin", "hobby": "baking", "score": "95"},
    {"name": "Maya", "city": "Cairo", "hobby": "calligraphy", "score": "60"},
    {"name": "Diego", "city": "Madrid", "hobby": "soccer", "score": "81"},
]

def ensure_csv(path):
    if os.path.exists(path):
        return
    print(f"File not found. Creating sample CSV at {path}")
    headers = ["name", "city", "hobby", "score"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in SAMPLE_ROWS:
            writer.writerow(r)

def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
        headers = reader.fieldnames or []
    return headers, rows

def detect_numeric_headers(headers, rows, threshold=0.6):
    numeric = set()
    for h in headers:
        total, numeric_count = 0, 0
        for r in rows:
            total += 1
            v = r.get(h, "").strip()
            if v == "":
                continue
            try:
                float(v)
                numeric_count += 1
            except ValueError:
                pass
        if total > 0 and (numeric_count / total) >= threshold:
            numeric.add(h)
    return numeric

def column_values(rows, header):
    vals = []
    for r in rows:
        v = r.get(header, "").strip()
        try:
            vals.append(float(v))
        except ValueError:
            pass
    return vals

def ascii_histogram(values, bins=10, width=40):
    if not values:
        return "(no numeric data)"
    mn, mx = min(values), max(values)
    if mn == mx:
        return f"All values = {mn:.2f}"
    step = (mx - mn) / bins
    counts = [0] * bins
    for v in values:
        idx = int((v - mn) / step)
        if idx == bins:
            idx = bins - 1
        counts[idx] += 1
    maxc = max(counts)
    lines = []
    for i, c in enumerate(counts):
        lo = mn + i * step
        hi = lo + step
        bar = "#" * int((c / maxc) * width) if maxc > 0 else ""
        lines.append(f"{lo:6.2f} - {hi:6.2f} | {bar} ({c})")
    return "\n".join(lines)

def random_story(rows):
    if not rows:
        return "No rows to make a story from."
    r = random.choice(rows)
    name = r.get("name", "Someone")
    city = r.get("city", "somewhere")
    hobby = r.get("hobby", "something fun")
    adjective = random.choice(["sparkling", "odd", "mysterious", "fearless", "bouncy"])
    twist = random.choice(["a talking cat", "a lost map", "a flying sandwich", "a secret handshake"])
    return f"{name} from {city} is known for {hobby}. One {adjective} day they stumbled upon {twist} and everything changed."

def compute_fun_scores(headers, rows, numeric_headers):
    # normalize numeric columns then combine with a bit of randomness
    cols = list(numeric_headers)
    col_vals = {c: column_values(rows, c) for c in cols}
    mins = {c: (min(v) if v else 0.0) for c, v in col_vals.items()}
    maxs = {c: (max(v) if v else 0.0) for c, v in col_vals.items()}
    out_rows = []
    for r in rows:
        score = 0.0
        count = 0
        for c in cols:
            raw = r.get(c, "").strip()
            try:
                val = float(raw)
                mn, mx = mins[c], maxs[c]
                norm = (val - mn) / (mx - mn) if mx != mn else 0.5
                score += norm
                count += 1
            except ValueError:
                pass
        if count:
            score = (score / count) * 10  # scale to 0-10
        score = score * random.uniform(0.85, 1.15)
        r2 = dict(r)
        r2["fun_score"] = f"{score:.2f}"
        out_rows.append(r2)
    return out_rows

def write_csv(path, headers, rows):
    headers_out = list(headers) + (["fun_score"] if "fun_score" not in headers else [])
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers_out)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

def main():
    if len(sys.argv) < 2:
        print("Usage: python fun_csv.py yourfile.csv")
        print("No file provided; using sample data file 'sample.csv' in script directory.")
        path = os.path.join(os.path.dirname(__file__), "sample.csv")
    else:
        path = sys.argv[1]

    ensure_csv(path)
    headers, rows = read_csv(path)
    if not headers:
        print("CSV has no headers.")
        return

    print(f"Loaded {len(rows)} rows. Columns: {', '.join(headers)}")
    numeric = detect_numeric_headers(headers, rows)
    if numeric:
        print("\nDetected numeric columns:")
        for n in numeric:
            vals = column_values(rows, n)
            print(f"\n== {n} (n={len(vals)}) ==\n{ascii_histogram(vals)}")
    else:
        print("\nNo numeric columns detected (or too few numeric entries).")

    print("\n--- Random Story ---")
    print(random_story(rows))

    print("\nComputing fun_score and saving augmented CSV...")
    out_rows = compute_fun_scores(headers, rows, numeric)
    out_path = os.path.splitext(path)[0] + "_fun.csv"
    write_csv(out_path, headers, out_rows)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()
# ...existing code...