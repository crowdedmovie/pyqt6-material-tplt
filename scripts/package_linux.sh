#!/usr/bin/env bash
set -euo pipefail

APP_NAME="pyqt6-app-template"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILD_DIR="$ROOT_DIR/build/linux"
DIST_DIR="$ROOT_DIR/dist"
BUNDLE_DIR="$DIST_DIR/$APP_NAME"
PACKAGE_DIR="$DIST_DIR/packages"
VERSION="$(grep -m1 '^version = ' "$ROOT_DIR/pyproject.toml" | cut -d '"' -f 2)"
ARCH="$(uname -m)"

require_tool() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "Missing required tool: $1" >&2
        exit 1
    fi
}

map_arch() {
    case "$1" in
        x86_64|amd64)
            echo "amd64"
            ;;
        aarch64|arm64)
            echo "arm64"
            ;;
        *)
            echo "$1"
            ;;
    esac
}

prepare_bundle() {
    bash "$SCRIPT_DIR/build_linux.sh"
}

write_desktop_file() {
    local target_dir="$1"
    mkdir -p "$target_dir"
    cat > "$target_dir/$APP_NAME.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=PyQt6 App Template
Exec=$APP_NAME
Icon=$APP_NAME
Terminal=false
Categories=Development;Utility;
StartupNotify=true
EOF
}

write_launcher() {
    local target_dir="$1"
    mkdir -p "$target_dir"
    cat > "$target_dir/$APP_NAME" <<EOF
#!/bin/sh
exec /opt/$APP_NAME/$APP_NAME "\$@"
EOF
    chmod 0755 "$target_dir/$APP_NAME"
}

stage_common_payload() {
    local target_dir="$1"
    rm -rf "$target_dir"
    mkdir -p "$target_dir/opt/$APP_NAME" "$target_dir/usr/bin" "$target_dir/usr/share/applications" "$target_dir/usr/share/icons/hicolor/256x256/apps"
    cp -a "$BUNDLE_DIR/." "$target_dir/opt/$APP_NAME/"
    cp "$ROOT_DIR/src/gui_template/assets/icon.png" "$target_dir/usr/share/icons/hicolor/256x256/apps/$APP_NAME.png"
    cp "$ROOT_DIR/src/gui_template/assets/icon.png" "$target_dir/opt/$APP_NAME/$APP_NAME.png"
    write_desktop_file "$target_dir/usr/share/applications"
    write_launcher "$target_dir/usr/bin"
}

build_deb() {
    require_tool fpm
    local stage_dir="$BUILD_DIR/deb-root"
    local arch
    arch="$(map_arch "$ARCH")"
    stage_common_payload "$stage_dir"

    mkdir -p "$PACKAGE_DIR"
    fpm \
        -s dir \
        -t deb \
        -n "$APP_NAME" \
        -v "$VERSION" \
        -a "$arch" \
        -C "$stage_dir" \
        -p "$PACKAGE_DIR/$APP_NAME-$VERSION-$arch.deb" \
        .
    echo "DEB created: $PACKAGE_DIR/$APP_NAME-$VERSION-$arch.deb"
}

build_rpm() {
    require_tool fpm
    local stage_dir="$BUILD_DIR/rpm-root"
    local arch
    case "$ARCH" in
        x86_64|amd64)
            arch="x86_64"
            ;;
        aarch64|arm64)
            arch="aarch64"
            ;;
        *)
            arch="$ARCH"
            ;;
    esac
    stage_common_payload "$stage_dir"

    mkdir -p "$PACKAGE_DIR"
    fpm \
        -s dir \
        -t rpm \
        -n "$APP_NAME" \
        -v "$VERSION" \
        -a "$arch" \
        -C "$stage_dir" \
        -p "$PACKAGE_DIR/$APP_NAME-$VERSION-$arch.rpm" \
        .
    echo "RPM created: $PACKAGE_DIR/$APP_NAME-$VERSION-$arch.rpm"
}

main() {
    local target="${1:-all}"

    prepare_bundle

    case "$target" in
        deb)
            build_deb
            ;;
        rpm)
            build_rpm
            ;;
        all)
            build_deb
            build_rpm
            ;;
        *)
            echo "Usage: $0 [deb|rpm|all]" >&2
            exit 1
            ;;
    esac
}

main "$@"