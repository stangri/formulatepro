#!/bin/bash
set -euo pipefail

# Build, sign, notarize, and package FormulatePro for direct distribution (Homebrew Cask, website, etc.)
#
# Prerequisites:
#   - "Developer ID Application" certificate installed in keychain
#   - App-specific password stored:  xcrun notarytool store-credentials "formulatepro-notary"
#
# Usage: ./release.sh -v 0.0.7

TEAM_ID="885FVTF3YD"
IDENTITY="Developer ID Application"
NOTARY_PROFILE="formulatepro-notary"

if [ "${1:-}" != "-v" ] || [ -z "${2:-}" ]; then
    echo "Usage: $0 -v <version>"
    echo "Example: $0 -v 0.0.7"
    exit 1
fi

VERS="$2"
VOL="FormulatePro-${VERS}"
OUT="${VOL}.dmg"
BUILD_DIR="$(pwd)/build/Release-Direct"
APP="${BUILD_DIR}/FormulatePro.app"

echo "=== Building FormulatePro ${VERS} (universal) ==="
xcodebuild -project FormulatePro.xcodeproj \
    -scheme FormulatePro \
    -configuration Release \
    ARCHS="arm64 x86_64" \
    ONLY_ACTIVE_ARCH=NO \
    CODE_SIGN_STYLE=Manual \
    CODE_SIGN_IDENTITY="${IDENTITY}" \
    DEVELOPMENT_TEAM="${TEAM_ID}" \
    CODE_SIGN_ENTITLEMENTS=FormulatePro-Direct.entitlements \
    CODE_SIGN_INJECT_BASE_ENTITLEMENTS=NO \
    ENABLE_HARDENED_RUNTIME=YES \
    OTHER_CODE_SIGN_FLAGS="--timestamp" \
    CONFIGURATION_BUILD_DIR="${BUILD_DIR}" \
    clean build

echo ""
echo "=== Verifying ==="
echo "Architectures: $(lipo -info "${APP}/Contents/MacOS/FormulatePro")"
codesign -dvv "${APP}" 2>&1 | grep -E "^(Authority|Identifier|Format)"

echo ""
echo "=== Creating DMG ==="
rm -f "${OUT}"
hdiutil create -fs HFS+ -srcfolder "${APP}" -volname "${VOL}" "${OUT}"

echo ""
echo "=== Notarizing ==="
xcrun notarytool submit "${OUT}" \
    --keychain-profile "${NOTARY_PROFILE}" \
    --wait

echo ""
echo "=== Stapling ==="
xcrun stapler staple "${OUT}"

echo ""
echo "=== Done ==="
SHA=$(shasum -a 256 "${OUT}" | awk '{print $1}')
SIZE=$(stat -f "%z" "${OUT}")
echo "File:    ${OUT}"
echo "Size:    ${SIZE} bytes"
echo "SHA-256: ${SHA}"
echo ""
echo "Homebrew Cask info:"
echo "  version \"${VERS}\""
echo "  sha256 \"${SHA}\""
