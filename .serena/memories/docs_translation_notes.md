# Docs translation notes

- README content is maintained as separate files (`README.md` English, `README-cn.md` Chinese), not as locale catalogs.
- Sphinx docs use gettext-based localization under `docs/source/locales/zh_CN`.
- If Korean docs are added later, the likely path is a new locale such as `docs/source/locales/ko_KR` plus Sphinx build commands with `-D language=ko_KR`.
- Natural translation quality matters more than literal sentence mapping; keep terminology stable across README and docs.
- Existing Chinese translation is useful as terminology reference, but the English source and current UI behavior should be the final authority when meaning diverges.
