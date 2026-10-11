"""Prepare offline dictation without overwriting existing user settings."""
import argparse
import core
import local_stt


def configure_local_defaults():
    if core.CONFIG_PATH.exists():
        print("Existing settings retained.")
        return False
    cfg = dict(core.DEFAULT_CONFIG)
    cfg.update(
        provider="parakeet_local",
        model="parakeet-primeline-int8",
        key="f9",
        mode="ptt",
        local_stt_num_threads=4,
    )
    core.save_config(cfg)
    print("Offline German recognition configured; no API key needed.")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-model-download", action="store_true")
    args = parser.parse_args()
    configure_local_defaults()
    if not args.skip_model_download:
        if local_stt.model_installed():
            print("Local model already installed.")
        else:
            local_stt.download_model(print)
    print("Setup complete. Launch start-windows.cmd.")


if __name__ == "__main__":
    main()
