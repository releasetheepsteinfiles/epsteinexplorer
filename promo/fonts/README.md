# Bundled fonts

These `.woff2` files are the Latin/Cyrillic/Greek subsets of **Inter** and
**JetBrains Mono**, fetched from Google Fonts and vendored here so the promo
renderer produces identical frames on any machine — a network fetch during
capture would let early frames paint in a fallback face and silently shift
the whole clip.

`fonts.css` is the Google Fonts stylesheet with every remote URL rewritten
to point at the local copy beside it.

Both families are licensed under the **SIL Open Font License 1.1**, which
permits redistribution:

- Inter — © The Inter Project Authors — <https://github.com/rsms/inter>
- JetBrains Mono — © The JetBrains Mono Project Authors — <https://github.com/JetBrains/JetBrainsMono>

To refresh, re-fetch the Google Fonts CSS for the two families and rewrite
its URLs to local filenames; keep the mapping exact, since each file is a
single weight/subset slice.
