# Automata API

## Packaging
`python3 -m build`

## Development

### View API end-points
* http://127.0.0.1:8000/docs
* http://127.0.0.1:8000/redoc

### Start Web Server
Instead of using `uvicorn` with `--reload` (as this does not wire-in dependencies as per this projects' conventions)

Use [simulations/serve](simulations/serve/__init__.py)
