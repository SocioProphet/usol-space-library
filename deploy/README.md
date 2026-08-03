# Deploying the usol quadrant service

The **live** side of the Space Twin's *"live USOL + initial data load."* The client-vue
cube (`client-vue/src/space/quadrant.ts` → `loadQuadrant()`) tries **live** `/api/space/quadrant`
first, then falls back to the shipped `/space/quadrant.initial.json`, then a Sol seed. Standing
this service up behind the `/api` route flips the cube from `initial-load` (synthetic tier) →
`usol-live` (empirical tier). Until then the UI renders gracefully from the initial-load asset.

The service (`usolspace.service`) is **stateless and read-only** — public factual astrometry,
no secrets, no writes — so it needs no PVC and no Secret, and scales horizontally.

## 1. Build & push the image

```bash
# from the repo root
export REGISTRY=us-docker.pkg.dev/<PROJECT>/<REPO>   # e.g. the estate Artifact Registry
export TAG=$(git rev-parse --short HEAD)             # immutable tag — never :latest (moving-tag trap)
docker build -f deploy/Dockerfile -t "$REGISTRY/usol-quadrant:$TAG" .
docker push "$REGISTRY/usol-quadrant:$TAG"
```

## 2. Apply the manifests

Substitute `REGISTRY`/`TAG` in `deploy/k8s/quadrant.yaml`, then either:

```bash
# direct
sed -e "s#REGISTRY#$REGISTRY#g" -e "s#TAG#$TAG#g" deploy/k8s/quadrant.yaml | kubectl apply -f -

# or GitOps — point ArgoCD at deploy/k8s (see deploy/argocd-application.yaml)
kubectl apply -f deploy/argocd-application.yaml
```

Verify:

```bash
kubectl -n usol rollout status deploy/usol-quadrant
kubectl -n usol port-forward svc/usol-quadrant 8087:8087 &
curl -s localhost:8087/healthz
curl -s localhost:8087/space/quadrant | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['source'], len(d['systems']),'systems')"
```

## 3. Wire the gateway route (the step that flips the cube)

The cube calls `GET /api/space/quadrant`. Route that path to this Service, **stripping the
`/api` prefix** (the service serves `/space/quadrant`), exactly like the client-vue data-API
proxy does in `vite.config.ts`:

```
/api/space/quadrant  ->  http://usol-quadrant.usol.svc.cluster.local:8087/space/quadrant
```

- **Ingress / API gateway** (prod): add a path rule for `/api/space/quadrant` → `usol-quadrant:8087`
  with a `/api` → `` rewrite. Place it *before* any catch-all `/api` rule so it wins.
- **Local dev**: already wired — `vite.config.ts` proxies `/api` → `VITE_API_BASE`
  (default `http://localhost:8088`) with the `/api` prefix stripped, so running
  `usol-serve` on that host/port serves the cube live with no further config. To point the
  cube at a standalone `usol-serve` instead, set `VITE_API_BASE=http://localhost:8087`.

Once the route resolves, `loadQuadrant()` reports `.source === 'usol-live'` and the cube's
epistemic chip reads **empirical** instead of the initial-load's **synthetic**.
