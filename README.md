# Sheas Cealer 转 Dev-Sidecar 的配置转换器

把Sheas Cealer的配置文件转换成Dev-Sidecar的配置文件。目前由GitHub Actions自动执行，当前每30分钟更新一次配置。

## 用法：
把~~https://cute-omega.github.io/ds-config.json~~ 填入dev-sidecar的个人远程配置，然后点击“更新远程配置”以立即生效。之后dev-sidecar会自动更新配置。

**通知：请将配置地址修改为https://cute-omega.github.io/other-assets/ds-config.json 。该变更是为了更好的适应未来扩展所做出的，目前尚未实际进入生产分支，但所有用户仍应当尽快完成变更。**

| **预计变更时间表：(UTC+8)** |                                                              |
| --------------------------- | ------------------------------------------------------------ |
| 即刻起-2025.9.10            | 从旧链接复制到新链接，仅保证旧链接有效                              |
| 2025.9.10-待定              | 两份链接均有效（均包含相同的内容）                           |
| 待定-2025.9.30              | 两份链接均有效（旧链接将重定向到新链接，如果dev-sidecar可以自动处理的话） |
| 2025.10.1后                 | 仅保证新链接有效（我们不会主动删除旧链接的有效性，但也不会对其中的问题进行维护） |

## 脚本当前工作流：

`ds-preset.json + converted(get(sc-config.json)) + ds-postset.json - items_from(ExcludedDomains.json)`

## 本地运行

尽管这看起来是显而易见的，我们仍然给出运行脚本的步骤。

```bash
git clone https://github.com/cute-omega/config_convert.git
cd config_convert
pip3 install -r requirements.txt
python3 main.py
```

## 开发
请分叉dev分支，更新也请向dev分支发PR。

推送PR前请在本地测试无bug后进行。

main分支仅用于生产用途。
