# Comandos reproducibles de calidad (Sprint 1)

## Backend (requiere PostGIS en `localhost:5433` o variable `DATABASE_URL`)

```bash
pip install -r backend/requirements.txt
pytest --cov=app --cov-report=xml:coverage.xml --cov-report=term-missing
```

Las pruebas **solo** escriben en la base `ecologistica_test` (ver `tests/conftest.py`).

## Frontend

```bash
npm ci
npm run test:coverage
npm run build
```

## SonarQube (servidor y token propios)

```bash
# Tras generar coverage.xml y coverage/frontend/lcov.info
sonar-scanner \
  -Dsonar.host.url="$SONAR_HOST_URL" \
  -Dsonar.login="$SONAR_TOKEN"
```

No ejecutar el escaneo sin `SONAR_HOST_URL` y `SONAR_TOKEN` válidos.
