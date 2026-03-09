# DOCS

## Update

### API update

```shell
# update apt docs
sphinx-apidoc -o source/_api ../ISAT/ ../ISAT/segment_any/edge_sam/* ../ISAT/segment_any/mobile_sam/* ../ISAT/segment_any/sam2/* ../ISAT/segment_any/sam3/* ../ISAT/segment_any/segment_anything/* ../ISAT/segment_any/segment_anything_hq/* ../ISAT/segment_any/segment_anything_fast/* ../ISAT/segment_any/segment_anything_med2d/* ../ISAT/ui/* ../ISAT/icons_rc.py -f
```

### Internationalization

```shell
sphinx-build -b gettext ./source/ ./build/gettext/
```

```shell
sphinx-intl update -p ./build/gettext/ -l zh_CN -l ko_KR -d source/locales/
```

## Preview

```shell
# build and preview for ko_KR
sphinx-build -b html -D language=ko_KR source ./build/html/ko_KR

# build and preview for zh_CN
sphinx-build -b html -D language=zh_CN source ./build/html/zh_CN

# build and preview for en
sphinx-build -b html -D language=en source ./build/html/en
```

## Read the Docs fork deployment

Read the Docs manages translations as separate projects. For a fork that needs
to publish Korean documentation, use the same repository twice:

1. Import the fork as the parent project with `Language = English`.
2. Import the same fork again as the Korean project with `Language = Korean`.
3. In the parent project's `Admin > Translations`, add the Korean project as a
   translation.

With this setup, the fork can publish English and Korean documentation from the
same branch. Publishing under the upstream `isat-sam.readthedocs.io` domain is
not possible from a fork alone; that requires upstream maintainers to connect
the translation project on their Read the Docs account.
