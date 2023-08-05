# thanosql-magic

SmartMind `ThanoSQL` Ipython Magic for Jupyter Lab

## Installation

```
$ pip install thanosql-magic
```

## Quick Start

1. load extension

   ```python
   %load_ext thanosql
   ```

2. change default API uri (optional)

   ```python
   %thanosql http://localhost:8000/api/v1/query
   ```

3. use magic

   ```python
   %%thanosql
   SELECT * FROM users
   ```

## License

[MIT](LICENSE)
