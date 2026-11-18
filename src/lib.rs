//! Malakal's modules, shared by the desktop binary (`src/main.rs`) and the
//! Android port (`malakal-android`, built into `libmalakal_android.so`).

pub mod app;
pub mod backend;
pub mod config;
pub mod event;
pub mod hook;
pub mod ical;
pub mod notifier;
pub mod util;
pub mod widget;

use anyhow::Context;
use eframe::egui::ViewportBuilder;

use crate::config::{APP_NAME, Config};

/// Everything the GUI needs before the window exists: config, timezone,
/// calendar backend and index database, plus the default `NativeOptions`.
///
/// The desktop binary calls [`run`]; the Android port calls this, sets
/// `NativeOptions::android_app` (and `persistence_path`), then starts
/// `eframe::run_native` itself.
pub fn prepare_app() -> anyhow::Result<(app::App, eframe::NativeOptions)> {
  let config = Config::read_or_initialize()?;
  log::info!("Config loaded {:?}", config);

  let timezone = match &config.timezone {
    Some(name) => jiff::tz::TimeZone::get(name)?,
    None => jiff::tz::TimeZone::system(),
  };

  let local_backend = backend::LocalDirBuilder::default()
    .calendar(&config.calendar_name)
    .dir(&config.calendar_location)
    .build()?;

  let db_path = {
    let mut path = dirs::data_dir()
      .with_context(|| "Cannot find a directory to store data")?;
    path.push(format!("{APP_NAME}/{APP_NAME}.db"));
    path
  };

  let backend = backend::IndexedLocalDir::new(local_backend, db_path)?;

  let mut app = app::App::new(&config, 3, timezone, backend)?;

  app.load_events();

  let viewport = ViewportBuilder {
    title: Some(APP_NAME.to_owned()),
    app_id: Some(APP_NAME.to_owned()),
    ..Default::default()
  };
  let options = eframe::NativeOptions {
    viewport,
    ..Default::default()
  };

  Ok((app, options))
}

/// The desktop entry point: read (or create) the config, then hand the app to
/// eframe's native window. The Android port has its own entry point in the
/// `malakal-android` crate.
pub fn run() -> anyhow::Result<()> {
  // default to log info
  env_logger::builder()
    .filter_level(log::LevelFilter::Info)
    .parse_default_env()
    .init();

  let (app, options) = prepare_app()?;

  let eframe_res = eframe::run_native(
    APP_NAME,
    options,
    Box::new(|ctx| Ok(Box::new(app.setup(ctx)))),
  );
  match eframe_res {
    Ok(o) => o,
    Err(e) => {
      log::error!("Error running gui: {:?}", e);
      std::process::exit(1);
    }
  };

  Ok(())
}
