# Malakal on Android

The same Malakal day-planner as on the desktop, as an APK: a `NativeActivity`
around `libmalakal_android.so`, which the `malakal-android` crate builds.

## Build

Needs the Android SDK (platform 36, build-tools 36) and NDK 29.0.14206865, plus
Rust targets `aarch64-linux-android` and `armv7-linux-androideabi` (and/or
`x86_64-linux-android`) and `cargo-ndk`:

```sh
cargo install cargo-ndk
cd android
./gradlew assembleRelease   # universal APK (arm64-v8a + armeabi-v7a)
# or, per ABI:
./gradlew assembleRelease -Pmalakal.abis=arm64-v8a
./gradlew assembleRelease -Pmalakal.abis=armeabi-v7a
```

The APK lands in `app/build/outputs/apk/release/Malakal-<version>-release.apk`.

* `-Pmalakal.abis` — comma-separated ABIs (default: `arm64-v8a,armeabi-v7a`).
* `-Pmalakal.portRevision` — a port-only release letter (`1` → `0.1.12a`).
* Release signing comes from the environment: `MALAKAL_RELEASE_KEYSTORE`,
  `MALAKAL_RELEASE_STORE_PASSWORD`, `MALAKAL_RELEASE_KEY_ALIAS` and
  `MALAKAL_RELEASE_KEY_PASSWORD`. Without them the build falls back to the
  debug key.

## How it works

`android/app/src/main/AndroidManifest.xml` declares a plain
`android.app.NativeActivity` (no Java code at all) loading
`libmalakal_android.so`. That library is built from `malakal-android/src/lib.rs`,
whose `android_main`:

* points `$HOME`, `XDG_DATA_HOME` and `XDG_CONFIG_HOME` at the app's internal
  storage, so the config file, the calendar directory and the index database
  (`dirs`, `config.rs`'s `~` expansion) all land somewhere writable;
* initializes `android_logger` (logcat tag `Malakal`);
* calls [`malakal::prepare_app`](../src/lib.rs) — the same config, timezone,
  backend and app construction as the desktop's `main` — then starts
  `eframe::run_native` with `NativeOptions::android_app` set (eframe 0.37's
  Android support) on the glow (GLES) renderer;
* ends the process when the activity ends (winit's event loop cannot restart
  in the same process).

## Notes

* The app requests no permissions and works fully offline; everything lives in
  the app's own storage.
* Desktop notifications (upcoming events) are a desktop feature; on Android the
  notifier thread is harmless but its pop-ups have nothing to pop into.
* Set a `timezone = "Area/City"` in the config to pin the timezone; otherwise
  jiff falls back to UTC on Android (no `/etc/localtime`).
* The CI release workflow is
  [`.github/workflows/android-release.yml`](../.github/workflows/android-release.yml):
  it builds the universal APK plus per-ABI APKs, checksums them and publishes a
  GitHub release.
