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
