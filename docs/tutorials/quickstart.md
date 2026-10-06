# Tutorial: Quickstart

This tutorial verifies the repository and starts the bounded development runtime.

## 1. Clone

```bash
git clone https://github.com/LloydCoder/tinlance-world-intelligence.git
cd tinlance-world-intelligence
```

## 2. Run the test gate

```bash
python -m compileall packages services api tests
python -m unittest discover -s tests -v
```

Or:

```bash
make check
make test
```

## 3. Start the development runtime

```bash
export WORLD_INTELLIGENCE_ENV=development
export WORLD_INTELLIGENCE_STORAGE_MODE=memory
export WORLD_INTELLIGENCE_REQUIRE_AUTH=true
export WORLD_INTELLIGENCE_BEARER_TOKEN=local-development-token
python -c "from runtime.server import serve; serve()"
```

## 4. Query it

```bash
curl http://127.0.0.1:8080/healthz
curl -H "Authorization: Bearer local-development-token" \
  "http://127.0.0.1:8080/v1/entities?limit=10&cursor=0"
```

The runtime is deliberately bounded and read-oriented; it is not an unrestricted execution surface.
