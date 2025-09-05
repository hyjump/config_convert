from json import dump, load
import logging
from requests import get
from os.path import abspath

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Domains that should not be proxied now
ExcludedDomains = ["*.googlevideo.com"]

sc_config_type = list[list[str], str | None, str]
ds_config_type = dict[
    str, dict[str, dict[str, dict[str, str | None]] | dict[str, dict[str, bool]]]
]


def parse_sc_config(preset_fn: str, sc_fn: str, postset_fn: str) -> ds_config_type:
    with open(preset_fn) as preset_file:
        ds_config: ds_config_type = load(preset_file)
    logging.info(f"Loaded preset config from {abspath(preset_fn)}")

    with open(sc_fn) as sc_file:
        sc_config: sc_config_type = load(sc_file)
    logging.info(f"Loaded Sheas Cealer config from {abspath(sc_fn)}")

    for item in sc_config:
        sni: str | None = item[1]
        if sni is None:
            continue
        elif sni == "":
            sni = "none"

        target: str = item[2]
        if target == "":
            target = "127.0.0.1"
        elif target.find("[") == -1:
            continue  # Skip IPv6 addresses

        raw_domains: list[str] = item[0]
        domains = [
            domain := raw_domain.lstrip("$#")
            for raw_domain in raw_domains
            if raw_domain.find("^") == -1 and (domain not in ExcludedDomains)
        ]
        domain_rules = "|".join(domains)
        if len(raw_domains) > 1:
            domain_rules = f"({domain_rules})"

        if domain_rules:
            ds_config["server"]["intercepts"][domain_rules] = {}
            ds_config["server"]["intercepts"][domain_rules][".*"] = {}
            ds_config["server"]["intercepts"][domain_rules][".*"]["sni"] = sni

            if domain_rules not in ds_config["server"]["preSetIpList"]:
                ds_config["server"]["preSetIpList"][domain_rules] = {}
            ds_config["server"]["preSetIpList"][domain_rules][target] = True

    return ds_config


def main():
    preset_fn = "ds-preset.json"
    postset_fn = "ds-postset.json"
    sc_fn = "sc-config.json"
    sc_url = "https://github.com/SpaceTimee/Cealing-Host/raw/main/Cealing-Host.json"
    ds_fn = "ds-config.json"

    with open(sc_fn, "w") as file:
        file.write(get(sc_url, timeout=10).text)

    logging.info(f"Downloaded latest Sheas Cealer config as {abspath(sc_fn)}")

    ds_config = parse_sc_config(preset_fn, sc_fn, postset_fn)
    with open(ds_fn, "w") as ds_file:
        dump(ds_config, ds_file, ensure_ascii=False, indent=2)
    logging.info(f"Converted to Dev-Sidecar config and saved as {abspath(ds_fn)}")


if __name__ == "__main__":
    main()
