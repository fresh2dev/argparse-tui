# Global values for this release.
<{{- $releaseName := "argparse-tui" }}>
<{{- $releaseEnv := getenv "HELMWAVE_ENV" | required "Missing required env var: HELMWAVE_ENV" -}}>
<{{- defineDatasource "globalSharedVars" (printf "environments/vars.yaml") }}>
<{{- defineDatasource "envSharedVars" (printf "environments/%s/vars.yaml" $releaseEnv) }}>
<{{- defineDatasource "globalReleaseSharedVars" (printf "releases/%s/vars.yaml" $releaseName) }}>
<{{- defineDatasource "envReleaseSharedVars" (printf "releases/%s/%s/vars.yaml" $releaseName $releaseEnv) }}>
<{{- $vars := coll.Merge (ds "envReleaseSharedVars") (ds "globalReleaseSharedVars") (ds "envSharedVars") (ds "globalSharedVars") }}>
<{{/* defineDatasource "vault" (printf "vault+https:///secret/data/releases/%s/%s" $releaseEnv $releaseName) */}}>
# Pull vault secrets like: <{{/* index (ds "vault").data "my-file.txt" | base64.Decode */}}>
# Variables from 'vars.yaml' are available in the variable `$vars`.

<{{- $releaseHostName := printf "%s.%s" $vars.subdomain $vars.domain }}>
<{{- $releaseUrl := printf "%s%s" $releaseHostName $vars.routePrefix }}>

butterStack:
  compose:
    services:
      <{{$releaseName}}>:
        labels:
          kompose.controller.type: "deployment"  # 'deployment' (default) or 'statefulset'
          # kompose.serviceaccount-name: "<{{$releaseName}}>"
        image: '<{{ $vars.privateRegistry }}>/<{{ getenv "CI_PROJECT_PATH" | required "Missing required env var: CI_PROJECT_PATH" }}>-docs:<{{ getenv "CI_COMMIT_SHORT_SHA" | required "Missing required env var: CI_COMMIT_SHORT_SHA" }}>'
        ports: ["<{{ $vars.svcPort }}>"]
        configs:
          - source: <{{$releaseName}}>-nginx-config
            target: '/etc/nginx/conf.d/default.conf'
        #   - source: <{{$releaseName}}>-configs
        #     target: '/app/config.toml'
        # secrets:
        #   - source: <{{$releaseName}}>-secrets
        #     target: '/app/creds.json'
        # environment:
        #   TZ: <{{/* $vars.tz */}}>
        #   PUID: <{{/* $vars.puid */}}>
        #   PGID: <{{/* $vars.pgid */}}>
        #   PLAIN_SECRET: <{{/* index (ds "vault").data "sekret.txt" | base64.Decode */}}>
        #   USERNAME: "secretKeyRef://<{{$releaseName}}>-env"
        #   PASSWORD: "secretKeyRef://<{{$releaseName}}>-env/APP_PASSWORD"
        # volumes:
        #   - <{{$releaseName}}>-data:/data:ro
        #   - <{{$releaseName}}>-config:/app/config

      # <{{$releaseName}}>-redis:
      #   ports: ['6379']
      #   image: 'docker.io/library/redis:7'

    configs:
      <{{$releaseName}}>-nginx-config:
        file: ./releases.yaml
    #   <{{$releaseName}}>-configs:
    #     file: ./releases.yaml
    # secrets:
    #   <{{$releaseName}}>-secrets:
    #     file: ./releases.yaml
    # volumes:
    #   <{{$releaseName}}>-data:
    #     external: true

  customObjects:
  -
    apiVersion: traefik.io/v1alpha1
    kind: IngressRoute
    metadata:
      name: <{{ $releaseName }}>
      annotations:
        gethomepage.dev/enabled: "true"
        gethomepage.dev/href: "https://<{{ $releaseUrl }}>"
        gethomepage.dev/description: <{{ $releaseName }}>
        gethomepage.dev/group: Other
        gethomepage.dev/icon: kubernetes.png
        gethomepage.dev/name: <{{ $releaseName }}>
        gethomepage.dev/weight: 10 # optional
        # gethomepage.dev/instance: "public" # optional
        # gethomepage.dev/app: "<{{ $releaseName }}>" # optional, Use pod-selector instead.
        gethomepage.dev/pod-selector: >-
          app.kubernetes.io/instance in (<{{ $releaseName }}>)
        # gethomepage.dev/widget.type: "emby"
        # gethomepage.dev/widget.url: "<{{ $releaseUrl }}>"
      labels: {}
    spec:
      tls: {}
      entryPoints: ["websecure"]
      routes:
      - match: 'Host(`<{{ $releaseHostName }}>`) && PathPrefix(`<{{ $vars.routePrefix }}>`)'
        kind: Rule
        services:
          - name: <{{ $releaseName }}>
            port: <{{ $vars.svcPort }}>
        middlewares:
          - name: traefik-default-headers
            namespace: default
          # - name: traefik-basicauth
          #   namespace: default
          # - name: <{{ $releaseName }}>-strip-prefix
          #   namespace: default
  -
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: "<{{ $releaseName }}>-nginx-config"
    data:
      default.conf: |
        server {
          listen <{{ $vars.svcPort }}>;
          absolute_redirect off;

          location <{{ $vars.routePrefix }}> {
            alias /usr/share/nginx/html/;
          }
        }
  # -
  #   apiVersion: traefik.io/v1alpha1
  #   kind: Middleware
  #   metadata:
  #     name: "<{{ $releaseName }}>-strip-prefix"
  #   spec:
  #     stripPrefix:
  #       forceSlash: false
  #       prefixes:
  #         - "<{{ $vars.routePrefix }}>"
  ###
  # -
  #   kind: PersistentVolumeClaim
  #   apiVersion: v1
  #   metadata:
  #     name: "<{{ $releaseName }}>-data"
  #     annotations: {}
  #       # nfs.io/path: "/"
  #     labels: {}
  #   spec:
  #     # storageClassName:
  #     accessModes:
  #       - ReadWriteMany
  #     resources:
  #       requests:
  #         storage: 1Mi
  ###
  # -
  #   apiVersion: v1
  #   kind: ServiceAccount
  #   metadata:
  #     name: <{{ $releaseName }}>
  #   secrets:
  #     - name: <{{ $releaseName }}>
  # -
  #   apiVersion: rbac.authorization.k8s.io/v1
  #   kind: ClusterRole
  #   metadata:
  #     name: <{{ $releaseName }}>
  #   rules:
  #     - apiGroups:
  #         - ""
  #       resources:
  #         - namespaces
  #         - pods
  #         - nodes
  #       verbs:
  #         - get
  #         - list
  # -
  #   apiVersion: rbac.authorization.k8s.io/v1
  #   kind: ClusterRoleBinding
  #   metadata:
  #     name: <{{ $releaseName }}>
  #   roleRef:
  #     apiGroup: rbac.authorization.k8s.io
  #     kind: ClusterRole
  #     name: <{{ $releaseName }}>
  #   subjects:
  #     - kind: ServiceAccount
  #       name: <{{ $releaseName }}>
  #       namespace: default
