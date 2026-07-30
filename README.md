# etlantic-plugin-echo

Minimal **out-of-monorepo** dataframe plugin for the
[ETLantic](https://github.com/eddiethedean/etlantic) Plugin SDK.

- Engine name: `echo`
- Protocol: `etlantic.dataframe/1`
- Storage: in-memory `list[dict]` (no Polars/Pandas/Spark)
- Tests: **only** public `etlantic.testing` suites +
  `etlantic plugin compatibility`

This repository is the external proof artifact for ETLantic 0.35.

## Install (development against workspace core)

```bash
uv pip install -e /path/to/etlantic
uv pip install -e .
pytest -q
etlantic plugin compatibility etlantic-plugin-echo --format human
```

## Docs

- [Building a Plugin](https://github.com/eddiethedean/etlantic/blob/main/docs/07_PLUGIN_SDK/BUILDING_A_PLUGIN.md)
- [Testing Plugins](https://github.com/eddiethedean/etlantic/blob/main/docs/07_PLUGIN_SDK/TESTING_PLUGINS.md)
- [Protocol Evolution](https://github.com/eddiethedean/etlantic/blob/main/docs/07_PLUGIN_SDK/PROTOCOL_EVOLUTION.md)

## License

MIT
