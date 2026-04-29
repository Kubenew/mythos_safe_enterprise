{{/*
Expand the name of the chart.
*/}}
{{- define "mythos-safe.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "mythos-safe.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "mythos-safe.labels" -}}
helm.sh/chart: {{ include "mythos-safe.chart" . }}
{{ include "mythos-safe.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "mythos-safe.selectorLabels" -}}
app.kubernetes.io/name: {{ include "mythos-safe.fullname" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
