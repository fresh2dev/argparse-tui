<{{- $vars := (ds "vars") }}>
<{{/* defineDatasource "vault" (printf "vault+https:///secret/data/releases/%s/%s" $vars.hostbutterSiteName $vars.releaseName) */}}>
# Pull vault secrets like: <{{/* index (ds "vault").data "my-file.txt" | base64.Decode */}}>
