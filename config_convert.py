from json import dump, load
import logging
from requests import ConnectTimeout, ReadTimeout, Timeout, get
from os.path import abspath
from typing import TypedDict

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Domains that should not be proxied now
ExcludedDomains = ["*.googlevideo.com"]

sc_config_type = list[tuple[list[str], str | None, str]]


# this type hint is not so accurate, just for fun
# you can't rely on it to check types
class ds_config_type(TypedDict):
    server: dict[
        str,
        dict[str, dict[str, dict[str, str | None]]]  # intercepts
        | dict[str, list[str] | None],  # preSetIpList
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
            domain
            for raw_domain in raw_domains
            if raw_domain.find("^") == -1
            and ((domain := raw_domain.lstrip("$#")) not in ExcludedDomains)
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

    # 读取 postset_fn 并合并到 ds_config
    with open(postset_fn) as postset_file:
        postset_config = load(postset_file)

    # 简单合并（浅拷贝），如有冲突以 postset_config 为准
    # 递归合并 postset_config 到 ds_config
    def __deep_merge_dict(dest: dict, src: dict):
        """
        递归合并 src 到 dest，只在最底层才覆盖/添加。
        """
        for k, v in src.items():
            if k in dest and isinstance(dest[k], dict) and isinstance(v, dict):
                __deep_merge_dict(dest[k], v)
            else:
                dest[k] = v

    if "server" in postset_config:
        if "server" not in ds_config:
            ds_config["server"] = {}
        __deep_merge_dict(ds_config["server"], postset_config["server"])
    return ds_config


def main():
    preset_fn = "ds-preset.json"
    postset_fn = "ds-postset.json"
    sc_fn = "sc-config.json"
    ds_fn = "ds-config.json"

    sc_urls = ["https://github.com/SpaceTimee/Cealing-Host/raw/main/Cealing-Host.json"]
    sc_urls.append(sc_urls[0].replace("github.com", "xget.xi-xu.me/gh"))

    for sc_url in sc_urls:
        try:
            logging.info(f"Trying to download Sheas Cealer config from {sc_url} ...")
            sc_config_text = get(sc_url, timeout=10).text
        except (ConnectTimeout, Timeout, ReadTimeout) as e:
            logging.error(f"Failed to download Sheas Cealer config from {sc_url}: {e}")
        else:
            logging.info(
                f"Downloaded latest Sheas Cealer config from {sc_url} as {abspath(sc_fn)}"
            )
            break
    with open(sc_fn, "w") as file:
        file.write(sc_config_text)

    ds_config = parse_sc_config(preset_fn, sc_fn, postset_fn)
    with open(ds_fn, "w") as ds_file:
        dump(ds_config, ds_file, ensure_ascii=False, indent=2)
    logging.info(f"Converted to Dev-Sidecar config and saved as {abspath(ds_fn)}")


if __name__ == "__main__":
    main()
