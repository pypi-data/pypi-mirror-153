# tier-mkdocs-techdocs-core

This is the base [Mkdocs](https://mkdocs.org) plugin used at TIER Mobility with Spotify's [TechDocs](https://backstage.io/docs/features/techdocs/techdocs-overview). It is forked from the [Backstage core plugin](https://github.com/backstage/mkdocs-techdocs-core).

[![Package on PyPI](https://img.shields.io/pypi/v/tier-mkdocs-techdocs-core)](https://pypi.org/project/tier-mkdocs-techdocs-core/)

## Usage

> Requires Python version >= 3.7

```bash
$ pip install tier-mkdocs-techdocs-core
```

Once you have installed the `tier-mkdocs-techdocs-core` plugin, you'll need to add it to your `mkdocs.yml`.

```yaml
site_name: Backstage Docs

nav:
  - Home: index.md
  - Developing a Plugin: developing-a-plugin.md

plugins:
  - tier-techdocs-core
```

## Development

### Running Locally

You can install this package locally using `pip` and the `--editable` flag used for making developing Python packages.

```bash
pip install --editable .
```

You'll then have the `tier-techdocs-core` package available to use in Mkdocs and `pip` will point the dependency to this folder.

### Linting

We use [black](https://github.com/psf/black) as our linter. Please run it against your code before submitting a pull request.

```bash
pip install black
black .
```

**Note:** This will write to all Python files in `src/` with the formatted code. If you would like to only check to see if it passes, simply append the `--check` flag.

### Testing Depedencies End-to-End

Much of the value of this plugin lies in its dependencies, on which there are
implicit dependencies upstream in the Backstage TechDocs frontend plugin. Each
time you update a pinned dependency, it's important to test that generated
documentation can be loaded and parsed as expected in the Backstage frontend.
The recommended way to do so is the following:

1. Make the expected dependency change locally in `requirements.txt`.
2. Clone the [techdocs-container](https://github.com/TierMobility/techdocs-container)
   image and, within the cloned directory, copy the entire contents of your
   local version of `tier-mkdocs-techdocs-core`, e.g. named `local-mkdocs-techdocs-core`.
3. Just before the `RUN pip install` command in `techdocs-container`'s
   Dockerfile, add a `COPY` command that copies the contents of your modified
   `tier-mkdocs-techdocs-core` directory into the container's file system. Something
   like: `COPY ./local-mkdocs-techdocs-core/ /local-mkdocs-techdocs-core/`
4. Modify the `RUN pip install`... command to install an editable version of
   the copied local plugin, rather than the specific version. Something like...
   `RUN pip install --upgrade pip && pip install -e /local-mkdocs-techdocs-core`
5. Build the modified image: `docker build -t mkdocs:local-dev .`
6. Modify your local Backstage instance to use your locally built
   `techdocs-container` instead of using the published image by setting the
   following configuration:

```yaml
techdocs:
  generator:
    runIn: "docker"
    dockerImage: "mkdocs:local-dev"
```

## MkDocs plugins and extensions

The TechDocs Core MkDocs plugin comes with a set of extensions and plugins that mkdocs supports. Below you can find a list of all extensions and plugins that are included in the
TechDocs Core plugin:

Plugins:

- [search](https://www.mkdocs.org/user-guide/configuration/#search): A search plugin is provided by default with MkDocs which uses [lunr.js](https://lunrjs.com/) as a search engine.
- [mkdocs-monorepo-plugin](https://github.com/backstage/mkdocs-monorepo-plugin): This plugin enables you to build multiple sets of documentation in a single MkDocs project. It is designed to address writing documentation in Spotify's largest and most business-critical codebases (typically monoliths or monorepos).
- [kroki](https://github.com/AVATEAM-IT-SYSTEMHAUS/mkdocs-kroki-plugin): This plugin enables you to embed Kroki-Diagrams into your documentation.
  - `ServerURL` parameter can be set from `KROKI_SERVER_URL` environmental variable
  - `DownloadImages` parameter can be set from `KROKI_DOWNLOAD_IMAGES` environmental variable

Extensions:

- [admonition](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#admonitions): Admonitions, also known as call-outs, are an excellent choice for including side content without significantly interrupting the document flow. Material for MkDocs provides several different types of admonitions and allows for the inclusion and nesting of arbitrary content.
- [toc](https://python-markdown.github.io/extensions/toc/): The Table of Contents extension generates a Table of Contents from a Markdown document and adds it into the resulting HTML document.
  This extension is included in the standard Markdown library.
- [pymdown](https://facelessuser.github.io/pymdown-extensions/): PyMdown Extensions is a collection of extensions for Python Markdown.
  All extensions are found under the module namespace of pymdownx.
  - caret: Caret is an extension that is syntactically built around the ^ character. It adds support for inserting superscripts and adds an easy way to place <ins>text</ins> in an <_ins_> tag.
  - critic: Critic adds handling and support of Critic Markup.
  - details: Details creates collapsible elements with <_details_> and <_summary_> tags.
  - emoji: Emoji makes adding emoji via Markdown easy 😄.
  - superfences: SuperFences is like Python Markdown's fences, but better. Nest fences under lists, admonitions, and other syntaxes. You can even create special custom fences for content like UML.
  - inlinehilite: InlineHilite highlights inline code: from module import function as func.
  - magiclink: MagicLink linkafies URL and email links without having to wrap them in Markdown syntax. Also, shortens repository issue, pull request, and commit links automatically for popular code hosting providers. You can even use special shorthand syntax to link to issues, diffs, and even mention people
  - mark: Mark allows you to mark words easily.
  - smartsymbols: SmartSymbols inserts commonly used Unicode characters via simple ASCII representations: =/= → ≠.
  - highlight: Highlight allows you to configure the syntax highlighting of SuperFences and InlineHilite. Also passes standard Markdown indented code blocks through the syntax highlighter.
  - extra: Extra is just like Python Markdown's Extra package except it uses PyMdown Extensions to substitute similar extensions.
  - tabbed: Tabbed allows for tabbed Markdown content.
  - tasklist: Tasklist allows inserting lists with check boxes.
  - tilde: Tilde is syntactically built around the ~ character. It adds support for inserting subscripts and adds an easy way to place text in a <_del_> tag.
- [markdown_inline_graphviz](https://pypi.org/project/markdown-inline-graphviz/): A Python Markdown extension replaces inline Graphviz definitions with inline SVGs or PNGs.
  Activate the inline_graphviz extension using the [usage instructions](https://github.com/sprin/markdown-inline-graphviz#usage).
- [mdx_truly_sane_lists](https://pypi.org/project/mdx-truly-sane-lists/): An extension for Python-Markdown that makes lists truly sane. Features custom indents for nested lists and fix for messy linebreaks and paragraphs between lists.

## Caveats

### Theme

We only use `material-mkdocs` as base styles because Backstage also uses the `Material UI` on the client-side. We don't expect people to use themes other than `Material UI` to maintain consistency across all Backstage pages (in other words, documentation pages have the same look and feel as any other Backstage page) and so we use the `BackstageTheme` configured in Front-end application as the source of truth for all application design tokens like colors, typography and etc. So here you can [see](https://github.com/backstage/backstage/blob/master/plugins/techdocs/src/reader/components/TechDocsReaderPageContent/dom.tsx#L160-L692) that some styles will always be overridden regardless of the `mkdocs-material` plugin theme settings and this can cause unexpected behavior for those who override the theme setting in a `mkdocs.yaml` file.

## Changelog

### 0.0.9

- Merged upstream [`v1.1.2`](https://pypi.org/project/mkdocs-techdocs-core/1.1.2/).

### 0.0.8

- Included kroki plugin
  - Allow setting kroki server URL via environmental variable `KROKI_SERVER_URL`
  - Allow setting kroki download image policy via environmental variable `KROKI_DOWNLOAD_IMAGES`
- Customize `search` plugin configuration to have a pre-build index by default

## License

Copyright 2020-2021 © The Backstage Authors. All rights reserved. The Linux Foundation has registered trademarks and uses trademarks. For a list of trademarks of The Linux Foundation, please see our Trademark Usage page: https://www.linuxfoundation.org/trademark-usage

Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
