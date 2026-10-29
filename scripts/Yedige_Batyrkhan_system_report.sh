#!/bin/bash
set -euo pipefail
PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$PROJECT_DIR/logs"
{
  echo 'Student: Batyrkhan Yedige Yerlanuly | IT2-2302 | 38419 | IITU'
  date --iso-8601=seconds
  printf 'Username: '; whoami
  echo 'Operating system:'; cat /etc/os-release
  echo 'Kernel:'; uname -sr
  echo 'CPU:'; lscpu
  echo 'Memory:'; free -h
  echo 'Disk usage and available space:'; df -h
} | tee "$PROJECT_DIR/logs/Yedige_Batyrkhan_system_report.log"
