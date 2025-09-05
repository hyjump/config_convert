from DevSidecarConfig import DevSidecarConfig
from utils import is_ipv6_address, sc_config_type

__all__ = ["parse_sc_config"]


def parse_sc_config(
    sc_config: sc_config_type, ExcludedDomains: list[str]
) -> DevSidecarConfig:
    ds_config = DevSidecarConfig({"server": {"intercepts": {}, "preSetIpList": {}}})

    for item in sc_config:
        sni: str | None = item[1]
        if sni is None:
            continue
        elif sni == "":
            sni = "none"

        target: str = item[2]
        if target == "":
            target = "127.0.0.1"

        skip_IPv6 = is_ipv6_address(target)

        raw_domains: list[str] = item[0]
        domains = [
            domain
            for raw_domain in raw_domains
            if raw_domain.find("^") == -1
            and ((domain := raw_domain.lstrip("$#")) not in ExcludedDomains)
        ]
        domain_rules = "|".join(domains)
        if len(domains) > 1:
            domain_rules = f"({domain_rules})"

        if domain_rules:
            ds_config["server"].setdefault("intercepts", {}).setdefault(
                domain_rules, {}
            ).setdefault(".*", {})["sni"] = sni

            if not skip_IPv6:
                ds_config["server"].setdefault("preSetIpList", {}).setdefault(
                    domain_rules, {}
                )[target] = True

    return ds_config
