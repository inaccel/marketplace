{{/* vim: set filetype=mustache: */}}

{{- define "platformName" -}}
{{- regexReplaceAll "^([^ ]+)[ /](.*)[ /]([^ ]+)$" $.Values.platform "${2}" | snakecase -}}
{{- end -}}

{{- define "platformVendor" -}}
{{- regexReplaceAll "^([^ ]+)[ /](.*)[ /]([^ ]+)$" $.Values.platform "${1}" | lower -}}
{{- end -}}

{{- define "platformVersion" -}}
{{- regexReplaceAll "^([^ ]+)[ /](.*)[ /]([^ ]+)$" $.Values.platform "${3}" | trimAll "()" -}}
{{- end -}}
