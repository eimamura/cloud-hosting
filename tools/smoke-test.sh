#!/usr/bin/env bash
# Verifies that a deployed workload satisfies the probe contract in workloads/README.md.
#
# Usage:
#   tools/smoke-test.sh <base-url> [--static] [--expect-target <name>] [--expect-version <v>]
#
# Examples:
#   tools/smoke-test.sh https://hono-api.example.workers.dev --expect-target cloudflare-workers
#   tools/smoke-test.sh https://user.github.io/cloud-hosting/ --static
#
# Requires: bash, curl. Exit code is the number of failed checks (0 = all passed).

set -uo pipefail

usage() { sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }

[[ $# -ge 1 ]] || usage
base="${1%/}"; shift
mode="api"; expect_target=""; expect_version=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --static) mode="static" ;;
    --expect-target) expect_target="${2:?}"; shift ;;
    --expect-version) expect_version="${2:?}"; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
  shift
done

failures=0
body_file="$(mktemp)"
trap 'rm -f "$body_file"' EXIT

if [[ -t 1 ]]; then green=$'\033[32m'; red=$'\033[31m'; reset=$'\033[0m'; else green=""; red=""; reset=""; fi
pass() { printf '  %sPASS%s %s\n' "$green" "$reset" "$1"; }
fail() { printf '  %sFAIL%s %s\n' "$red" "$reset" "$1"; failures=$((failures + 1)); }

# fetch <path> -> sets $status and writes body to $body_file
fetch() {
  status="$(curl -sS -L --max-time 30 -o "$body_file" -w '%{http_code}' "$base$1" 2>/dev/null)" || status="000"
}

# json_field <name> -> prints the string value of a top-level field (compact or pretty JSON)
json_field() {
  sed -n "s/.*\"$1\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p" "$body_file" | head -n 1
}

check_status() { # <path> <expected-status> <label>
  fetch "$1"
  if [[ "$status" == "$2" ]]; then pass "$3 ($1 -> $status)"; else fail "$3 ($1 -> $status, expected $2)"; fi
}

check_info() { # <path>
  fetch "$1"
  if [[ "$status" != "200" ]]; then fail "$1 returns 200 (got $status)"; return; fi
  local workload target version
  workload="$(json_field workload)"; target="$(json_field target)"; version="$(json_field version)"
  if [[ -n "$workload" ]]; then pass "$1 workload=$workload target=${target:-?} version=${version:-?}"
  else fail "$1 has a workload field"; fi
  if [[ -n "$expect_target" ]]; then
    [[ "$target" == "$expect_target" ]] && pass "target is $expect_target" || fail "target is $expect_target (got ${target:-none})"
  fi
  if [[ -n "$expect_version" ]]; then
    [[ "$version" == "$expect_version" ]] && pass "version is $expect_version" || fail "version is $expect_version (got ${version:-none})"
  fi
}

echo "Smoke testing $base ($mode)"
check_status "/" 200 "top page"
if [[ "$mode" == "static" ]]; then
  check_info "/info.json"
else
  fetch "/healthz"
  if [[ "$status" == "200" && "$(tr -d '[:space:]' < "$body_file")" == "ok" ]]; then pass "/healthz returns ok"
  else fail "/healthz returns ok (got $status)"; fi
  check_info "/api/info"
  check_status "/api/echo?probe=1" 200 "echo"
fi
check_status "/__smoke-test-not-found__" 404 "unknown path is 404"

if [[ $failures -eq 0 ]]; then echo "All checks passed."; else echo "$failures check(s) failed."; fi
exit "$failures"
