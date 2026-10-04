use base::config::keys;
use hbb_common::config;

const SERVER: &str = "rustdesk.db9consult.com.br";
const KEY: &str = "dksPMYTN32cCIMoIhBsKh5MZzYIAYt70xQxIiYZqSiQ=";

pub(crate) fn init_defaults() {
    config::DEFAULT_SETTINGS.write().unwrap().extend([
        (keys::OPTION_CUSTOM_RENDEZVOUS_SERVER.to_owned(), SERVER.to_owned()),
        (keys::OPTION_RELAY_SERVER.to_owned(), SERVER.to_owned()),
        (keys::OPTION_KEY.to_owned(), KEY.to_owned()),
    ]);
    config::OVERWRITE_SETTINGS
        .write()
        .unwrap()
        .insert(keys::OPTION_ALLOW_AUTO_UPDATE.to_owned(), "N".to_owned());
    config::OVERWRITE_LOCAL_SETTINGS
        .write()
        .unwrap()
        .insert(keys::OPTION_ENABLE_CHECK_UPDATE.to_owned(), "N".to_owned());
}

pub(crate) fn official_updates_enabled() -> bool {
    false
}

#[cfg(test)]
mod tests {
    use super::*;
    use config::{Config, Config2, LocalConfig};

    #[test]
    fn defaults_preserve_saved_values_and_edits_persist() {
        *config::APP_NAME.write().unwrap() = format!("RustDesk-DB9-test-{}", std::process::id());
        Config::set_option(keys::OPTION_KEY.to_owned(), "existing-key".to_owned());
        init_defaults();
        assert_eq!(Config::get_option(keys::OPTION_CUSTOM_RENDEZVOUS_SERVER), SERVER);
        assert_eq!(Config::get_option(keys::OPTION_RELAY_SERVER), SERVER);
        assert_eq!(Config::get_option(keys::OPTION_KEY), "existing-key");
        Config::set_option(keys::OPTION_KEY.to_owned(), String::new());
        assert_eq!(Config::get_option(keys::OPTION_KEY), KEY);
        for key in [keys::OPTION_CUSTOM_RENDEZVOUS_SERVER, keys::OPTION_RELAY_SERVER, keys::OPTION_KEY] {
            assert!(!crate::ui_interface::is_option_fixed(key));
            Config::set_option(key.to_owned(), "edited-value".to_owned());
            init_defaults();
            assert_eq!(Config::get_option(key), "edited-value");
            let saved = config::load_path::<Config2>(Config2::file());
            assert_eq!(serde_json::to_value(saved).unwrap()["options"][key], "edited-value");
        }
        Config::set_option(keys::OPTION_ALLOW_AUTO_UPDATE.to_owned(), "Y".to_owned());
        LocalConfig::set_option(keys::OPTION_ENABLE_CHECK_UPDATE.to_owned(), "Y".to_owned());
        assert!(!Config::get_bool_option(keys::OPTION_ALLOW_AUTO_UPDATE));
        assert_eq!(LocalConfig::get_option(keys::OPTION_ENABLE_CHECK_UPDATE), "N");
        crate::common::do_check_software_update().unwrap();
        assert!(crate::common::SOFTWARE_UPDATE_URL.lock().unwrap().is_empty());
    }
}
