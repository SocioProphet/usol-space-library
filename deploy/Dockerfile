# usol quadrant service — lean runtime image (NOT the dev image at repo root).
# Serves nearby_stars.quadrant_payload() at GET /space/quadrant + /healthz. The
# quadrant plane needs no FITS/BLAS toolchain, so this stays slim: no build-essential,
# no cfitsio/atlas. Pure-Python service + jsonschema/PyYAML runtime deps only.
FROM python:3.11-slim

# Non-root from the start; the runtime FS is read-only in k8s (see deploy/k8s/quadrant.yaml).
RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin usol
WORKDIR /app

# Install deps first for layer caching, then the package itself.
COPY pyproject.toml requirements.txt README.md /app/
COPY src /app/src
RUN pip install --no-cache-dir -e . \
    && python -c "import usolspace.service, usolspace.nearby_stars; print('usol service import OK')"

USER 10001
ENV PORT=8087
EXPOSE 8087

# usol-serve = usolspace.service:main (console_script registered in pyproject.toml).
CMD ["usol-serve"]
