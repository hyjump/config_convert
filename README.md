# Sheas Cealer 转 Dev-Sidecar 的配置转换器

把Sheas Cealer的配置文件转换成Dev-Sidecar的配置文件

## 用法：
把`https://cute-omega.github.io/ds-config.json`填入dev-sidecar的个人远程配置，然后点击“更新远程配置”以立即生效。之后dev-sidecar会自动更新配置。

## 当前工作流：

`ds-preset.json + converted(get(sc-config.json)) + ds-postset.json - items_from(ExcludedDomains.json)`

当前每30分钟更新一次配置。
