# Helm Chart for Mythos-Safe Enterprise

## Install

```bash
# Add dependencies (postgresql, redis)
helm dependency update ./helm/mythos-safe

# Install
helm install mythos-safe ./helm/mythos-safe \
  --set postgresql.auth.password=your-secure-password \
  --set replicaCount=2
```

## Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| replicaCount | Number of replicas | 1 |
| image.repository | Image repo | mythos-safe |
| image.tag | Image tag | latest |
| service.type | Service type | ClusterIP |
| postgresql.enabled | Enable PostgreSQL | true |
| redis.enabled | Enable Redis | true |

## Uninstall

```bash
helm uninstall mythos-safe
```
