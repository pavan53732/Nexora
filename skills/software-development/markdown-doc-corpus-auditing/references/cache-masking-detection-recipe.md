# Cache-Masking Detection Recipe

Use this when `read_file` returns a stub (~300 chars) or `status: unchanged`
with no real content for a file you know exists and is larger. This is most
common on small, stable doc files that were edited once then frozen.

## The diagnostic

```python
import os
base = "/storage/emulated/0/Git repos/Nexora"
# A. Confirm the real on-disk size
for f in ["docs/PRODUCT_VISION.md", "docs/GLOSSARY.md"]:
    p = os.path.join(base, f)
    sz = os.path.getsize(p)
    print(f, sz, "bytes")
```

## The bypass

```python
# Force real bytes from disk — ignore the read_file cache entirely
path = "/storage/emulated/0/Git repos/Nexora/docs/PRODUCT_VISION.md"
with open(path) as f:
    text = f.read()
print(len(text), "chars  <- from open(), not the read_file cache")
print(text[:500])
```

## When to deploy it

- Any `read_file` result that is suspiciously small (< 500 chars) for a file
  known to be in a large doc corpus.
- Any file that appears in the "deleted then restored" audit trail — restored
  files sometimes get cache-stubbed if their content was touched pre-restore.
- Any markdown table-heavy file you just patched with the `patch` tool (see P3:
  doubled pipes `||` can hide behind a cached clean read).

## Confirmation

After `open()` confirms the real content, cite `file:line` from THAT read only.
Do not re-call `read_file` on the same file — it serves the cached stub again.
