// admin_security.rs
#![windows_subsystem = "windows"]
#[macro_use]
extern crate clap;
use std::ffi::OsString;
use windows::{
    core::*,
    Win32::{
        Foundation::*,
        System::Threading::*,
        Security::Authorization::*,
    },
};
use std::sync::Arc;
use tokio_;
use winapi::*;
use winrt::*;

#[tokio::main]
async fn main() -> Result<()> {
    // Parse command line args
    let matches = App::new("Security Disabler")
        .arg(Arg::with_name("disable_all").short("a"))
        .get_matches_from(windows::api::GetCommandLine());

    if matches.is_present("disable_all") {
        disable_full_security().await?;
    }

    // Show UI
    show_ui().await
}

fn disable_full_security() -> Result<(), Error> {
    let h_process = GetCurrentProcess();
    let h_thread = GetThreadHandle();

    // 1. Disable Real-Time Protection
    let rtp_key = HKEY_LOCAL_MACHINE\
.open("SOFTWARE\Policies\Microsoft\Windows Defender", GENERIC_ALL)?;
    rtp_key.set_value("DisableAntiSpyware", 1)?;

    // 2-8. Disable remaining features
    disable_features()?; // separate async function

    // Notify user
    writeln!(stdout, "Security features disabled.");
    Ok(())
}

async fn show_ui() -> Result<(), Error> {
    let window = WindowBuilder::new()
        .title("Disable Security")
        .content_size((400, 200))
        .build()?;

    let btn_disable = Button::new("Disable All Security")?;
    let btn_exit = Button::new("Exit")?;

    btn_disable.on_clicked(move |_| {
        disable_full_security().await;
        MessageDialog::show("Success", "Security features disabled");
    });

    StackPanel::new(|sp| {
        sp.children().push(btn_disable.clone());
        sp.children().push(btn_exit.clone());
    })?;

    window.set_content(sp)?;
    window.show()?;
    Application::run(window)
}