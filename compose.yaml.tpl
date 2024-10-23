<{{- $vars := (ds "vars") }}>
<{{/* defineDatasource "vault" (printf "vault+https:///secret/data/releases/%s/%s" $vars.hostbutterSiteName $vars.releaseName) */}}>
# Pull vault secrets like: <{{/* index (ds "vault").data "my-file.txt" | base64.Decode */}}>

global:
  butterStack:
    compose:
      services:
        <{{$vars.releaseName}}>:
          labels:
            kompose.controller.type: "deployment"  # 'deployment' (default) or 'statefulset'
            # kompose.serviceaccount-name: "<{{$vars.releaseName}}>"
          image: '<{{ $vars.registry }}>/<{{ getenv "CI_PROJECT_PATH" | required "Missing required env var: CI_PROJECT_PATH" }}>-docs:<{{ getenv "CI_COMMIT_SHORT_SHA" | required "Missing required env var: CI_COMMIT_SHORT_SHA" }}>'
          ports: ["<{{ $vars.svcPort }}>"]
          configs:
            - source: <{{$vars.releaseName}}>-nginx-config
              target: '/etc/nginx/conf.d/default.conf'
          # secrets:
          #   - source: <{{$vars.releaseName}}>-secrets
          #     target: '/app/creds.json'
          # environment:
          #   TZ: <{{/* $vars.tz */}}>
          #   PUID: <{{/* $vars.puid */}}>
          #   PGID: <{{/* $vars.pgid */}}>
          #   PLAIN_SECRET: <{{/* index (ds "vault").data "sekret.txt" | base64.Decode */}}>
          #   USERNAME: "secretKeyRef://<{{$vars.releaseName}}>-env"
          #   PASSWORD: "secretKeyRef://<{{$vars.releaseName}}>-env/APP_PASSWORD"
          # volumes:
          #   - <{{$vars.releaseName}}>-data:/data:ro
          #   - <{{$vars.releaseName}}>-config:/app/config

        # <{{$vars.releaseName}}>-redis:
        #   ports: ['6379']
        #   image: 'docker.io/library/redis:7'

      configs:
        <{{$vars.releaseName}}>-nginx-config:
          file: ./releases.yaml
      #   <{{$vars.releaseName}}>-configs:
      #     file: ./releases.yaml
      # secrets:
      #   <{{$vars.releaseName}}>-secrets:
      #     file: ./releases.yaml
      # volumes:
      #   <{{$vars.releaseName}}>-data:
      #     external: true

    customObjects:
    <{{- $releaseHostName := printf "%s.%s" $vars.subdomain $vars.domain }}>
    <{{- $releaseUrl := printf "%s%s" $releaseHostName $vars.routePrefix }}>
    -
      apiVersion: traefik.io/v1alpha1
      kind: IngressRoute
      metadata:
        name: <{{ $vars.releaseName }}>
        annotations:
          gethomepage.dev/enabled: "true"
          gethomepage.dev/href: "https://<{{ $releaseUrl }}>"
          gethomepage.dev/description: <{{ $vars.releaseName }}>
          gethomepage.dev/group: Other
          gethomepage.dev/icon: kubernetes.png
          gethomepage.dev/name: <{{ $vars.releaseName }}>
          gethomepage.dev/weight: 10 # optional
          # gethomepage.dev/instance: "public" # optional
          # gethomepage.dev/app: "<{{ $vars.releaseName }}>" # optional, Use pod-selector instead.
          gethomepage.dev/pod-selector: >-
            app.kubernetes.io/instance in (<{{ $vars.releaseName }}>)
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
            - name: <{{ $vars.releaseName }}>
              port: <{{ $vars.svcPort }}>
          middlewares:
            - name: traefik-default-headers
              namespace: default
            # - name: traefik-basicauth
            #   namespace: default
            # - name: <{{ $vars.releaseName }}>-strip-prefix
            #   namespace: default
    # -
    #   apiVersion: traefik.io/v1alpha1
    #   kind: Middleware
    #   metadata:
    #     name: "<{{ $vars.releaseName }}>-strip-prefix"
    #   spec:
    #     stripPrefix:
    #       forceSlash: false
    #       prefixes:
    #         - "<{{ $vars.routePrefix }}>"
    -
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: "<{{ $vars.releaseName }}>-nginx-config"
      data:
        default.conf: |
          server {
            listen <{{ $vars.svcPort }}>;
            absolute_redirect off;

            location <{{ $vars.routePrefix }}> {
              alias /usr/share/nginx/html/;
            }
          }
    ###
    # -
    #   kind: PersistentVolumeClaim
    #   apiVersion: v1
    #   metadata:
    #     name: "<{{ $vars.releaseName }}>-data"
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
    #     name: <{{ $vars.releaseName }}>
    #   secrets:
    #     - name: <{{ $vars.releaseName }}>
    # -
    #   apiVersion: rbac.authorization.k8s.io/v1
    #   kind: ClusterRole
    #   metadata:
    #     name: <{{ $vars.releaseName }}>
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
    #     name: <{{ $vars.releaseName }}>
    #   roleRef:
    #     apiGroup: rbac.authorization.k8s.io
    #     kind: ClusterRole
    #     name: <{{ $vars.releaseName }}>
    #   subjects:
    #     - kind: ServiceAccount
    #       name: <{{ $vars.releaseName }}>
    #       namespace: default
