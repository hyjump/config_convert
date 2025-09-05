from ipaddress import ip_address

__all__ = ["is_ipv6_address", "sc_config_type"]

sc_config_type = list[tuple[list[str], str | None, str]]


def is_ipv6_address(target: str) -> bool:
    # 处理形如 [240e::] 的格式
    if target.startswith("[") and target.endswith("]"):
        addr = target.strip("[]")
        try:
            return ip_address(addr).version == 6
        except ValueError:
            return False
    return False
