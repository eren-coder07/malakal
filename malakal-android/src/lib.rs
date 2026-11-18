//! Malakal on Android.
//!
//! Runs the same [`malakal::app::App`] as the desktop binary through eframe on
//! a `NativeActivity` (GLES via eframe's glow renderer). The Gradle project in
//! `android/` drives `cargo ndk`, which builds this crate into
//! `src/main/jniLibs` as `libmalakal_android.so`; see `android/README.md`.

#[cfg(target_os = "android")]
mod android {
    use malakal::config::APP_NAME;
    use winit::platform::android::activity::AndroidApp;

    pub fn run(app: AndroidApp) {
        // The app's own, writable folder: the calendar directory, the config
        // file and the index database all follow $HOME / XDG_* from here
        // (`config.rs` replaces `~` with $HOME; `dirs` follows XDG_DATA_HOME
        // and XDG_CONFIG_HOME).
        let data = app.internal_data_path();
        if let Some(dir) = &data {
            std::env::set_var("HOME", dir);
            std::env::set_var("XDG_DATA_HOME", dir.join("data"));
            std::env::set_var("XDG_CONFIG_HOME", dir.join("config"));
        }
        // Logs reach logcat under the tag "Malakal" (adb logcat -s Malakal).
        android_logger::init_once(
            android_logger::Config::default()
                .with_max_level(log::LevelFilter::Info)
                .with_tag("Malakal"),
        );

        let (app_state, mut options) = match malakal::prepare_app() {
            Ok(pair) => pair,
            Err(e) => {
                log::error!("Malakal could not start: {e:#}");
                return;
            }
        };

        // Required on Android: hand the NativeActivity to eframe/winit.
        options.android_app = Some(app);
        // eframe's own settings file (unused today, kept where it can be written).
        options.persistence_path = data.map(|d| d.join("eframe.ron"));

        if let Err(e) = eframe::run_native(
            APP_NAME,
            options,
            Box::new(|ctx| Ok(Box::new(app_state.setup(ctx)))),
        ) {
            log::error!("Malakal could not start: {e}");
        }
        // The system destroyed the activity, and the app has shut down. winit's
        // event loop can only be made once per process, so a new activity in
        // this process could never start: end the process, and the next launch
        // starts a fresh one.
        // SAFETY: `_exit` takes no pointers and never returns; it only ends the
        // process, without running exit-time destructors while the system's own
        // threads still use what they free.
        unsafe { libc::_exit(0) }
    }
}

/// The activity's entry point: android-activity's glue calls it by this name on
/// its own thread.
#[cfg(target_os = "android")]
#[unsafe(no_mangle)]
fn android_main(app: winit::platform::android::activity::AndroidApp) {
    android::run(app);
}
