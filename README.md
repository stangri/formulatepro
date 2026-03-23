# FormulatePro

FormulatePro is a macOS application for annotating and marking up PDF documents.

## About This Fork

This project is a fork of the original [FormulatePro](https://github.com/adlr/formulatepro) by [Andrew de los Reyes](https://github.com/adlr). The original copyright belongs to Andrew de los Reyes (2006). The original code is licensed under the [GNU Lesser General Public License v2.1](LICENSE.txt).

This fork was created to modernize the app and keep it building and running on current versions of macOS, Xcode, and Apple Silicon. Changes include:

- Updated for macOS Sequoia and Apple Silicon (arm64)
- Fixed all deprecated API usage and build warnings
- Added hi-res app icon and Asset Catalog
- Prepared for Mac App Store distribution
- Signed and notarized for direct distribution via Homebrew

## Features

- Open and annotate any PDF document
- Drawing tools: Arrow, Ellipse, Rectangle, Freehand, Text, Checkmark, Stamp
- Customize stroke/fill colors, line width, and fonts
- Inspector panel for annotation properties
- Hide annotations when printing
- Export annotated documents as standard PDF
- Native macOS interface

## Install

### Homebrew

```
brew install --cask formulatepro
```

### Mac App Store

FormulatePro is also available on the [Mac App Store](https://apps.apple.com/app/formulatepro).

### Direct Download

Download the latest DMG from [GitHub Releases](https://github.com/stangri/formulatepro/releases).

## Building from Source

1. Open `FormulatePro.xcodeproj` in Xcode
2. Select the `Release` build configuration
3. Build and run

## License

This project is licensed under the [GNU Lesser General Public License v2.1](LICENSE.txt).

Copyright (C) 2006 Andrew de los Reyes. All rights reserved.
