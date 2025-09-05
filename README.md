把Sheas Cealer的配置文件转换成Dev-Sidecar的配置文件

Current workflow:

```
ds-preset.json + converted(get(sc-config.json)) + ds-postset.json - items_from(ExcludedDomains.json)
```

Now it runs per 30 minutes.
