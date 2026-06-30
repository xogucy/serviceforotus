#!/usr/bin/env bash
set -euo pipefail

docker compose --env-file docker/compose.env up -d postgres kafka kafka-init
