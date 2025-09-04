from json import dump, load
import logging
from requests import get
from os.path import abspath

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Domains that should not be proxied now
ExcludedDomains = ["*.googlevideo.com"]

def parse_sc_config(file):
    origin_config: list[list[list[str], str | None, str]] = load(file)
    new_config = {"server": {"intercepts": {}, "preSetIpList": {}}}
    for item in origin_config:

        sni: str | None = item[1]
        if sni == None:
            continue
        elif sni == "":
            sni = "none"


        target: str = item[2]
        if target == "":
            target = "127.0.0.1"
        elif "[" in target:
            continue # Skip IPv6 addresses

        domains: list[str] = item[0]
        domain_rules=""
        domain_num=len(domains)
        for key in domains:

            if key in ExcludedDomains:
                continue

            domain = key.removeprefix("#").removeprefix("$").removeprefix("#")
            # According to the documentation, domains starting with ^ are invalid
            if domain.startswith("^"):
                continue
            domain = domain.removeprefix("#").removeprefix("$").removeprefix("#")

            if domains.index(key) < domain_num - 1 and domain_num > 1:
                domain_rules = domain_rules + domain + "|"
            elif domains.index(key) == domain_num - 1 and domain_num > 1:
                domain_rules = domain_rules + domain
            else:
                domain_rules = domain
        if domain_num > 1:
            domain_rules = "(" + domain_rules + ")"
            
        if key not in ExcludedDomains:
            new_config["server"]["intercepts"][domain_rules] = {}
            new_config["server"]["intercepts"][domain_rules][".*"] = {}
            new_config["server"]["intercepts"][domain_rules][".*"]["sni"] = sni

            if domain_rules not in new_config["server"]["preSetIpList"]:
                new_config["server"]["preSetIpList"][domain_rules] = {}
            new_config["server"]["preSetIpList"][domain_rules][target] = True
            
    return new_config


def main():
    sc_fn = "sc-config.json"
    sc_url = (
        "https://github.com/SpaceTimee/Cealing-Host/raw/main/Cealing-Host.json".replace(
            "github.com", "xget.xi-xu.me/gh"
        )
    )
    ds_fn = "ds-config.json"
    with open(sc_fn, "w") as file:
        file.write(get(sc_url, timeout=10).text)

    logging.info(f"Downloaded latest Sheas Cealer config as {abspath(sc_fn)}")
    with open(sc_fn, "r") as sc:
        with open(ds_fn, "w") as ds:
            ds_config = parse_sc_config(sc)
            dump(ds_config, ds, ensure_ascii=False, indent=2)
    logging.info(f"Converted to Dev-Sidecar config and saved as {abspath(ds_fn)}")


if __name__ == "__main__":
    main()
