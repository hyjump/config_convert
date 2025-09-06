# Sheas Cealer 转 Dev-Sidecar 的配置转换器

把Sheas Cealer的配置文件转换成Dev-Sidecar的配置文件,项目来自https://github.com/cute-omega/config_convert
主要是为了满足一些自定义需求

## 用法：
把`https://raw.githubusercontent.com/{your-username}/{your-repo}/main/ds-config.json`填入dev-sidecar的个人远程配置，然后点击“更新远程配置”以立即生效。之后dev-sidecar会自动更新配置。

## 当前工作流：

`ds-preset.json + converted(get(sc-config.json)) + ds-postset.json - items_from(ExcludedDomains.json)`

当前每30分钟更新一次配置。

## 开发
请分叉dev分支，更新也请向dev分支发PR。

推送PR前请在本地测试无bug后进行。

main分支仅用于生产用途。
