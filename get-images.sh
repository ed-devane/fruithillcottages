#!/usr/bin/env bash
# Downloads every photo from the current Squarespace site into ./images/
# Run ONCE, before cancelling Squarespace:   bash get-images.sh
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p images
ok=0; fail=0
while IFS=$'\t' read -r name url; do
  [ -z "$name" ] && continue
  # Without the Accept header Squarespace sends WebP, despite the .jpg name.
  # A real JPEG starts with the bytes FF D8 FF.
  if curl -fsSL --retry 3 -H 'Accept: image/jpeg' -o "images/$name" "$url?format=2500w" &&
     [ "$(head -c 3 "images/$name" | od -An -tx1 | tr -d ' \n')" = "ffd8ff" ]; then
    printf '  ok    %s\n' "$name"; ok=$((ok+1))
  else
    printf '  FAIL  %s\n' "$name"; fail=$((fail+1))
  fi
done < images.tsv
echo "Downloaded $ok images, $fail failed."
[ "$fail" -eq 0 ]
