# HIDS-Agent

A lightweight, host-based monitoring agent for Linux that collects logs in real time, detects failures and suspicious events, and notifies the system's responsible party. Inspired by Host-based Intrusion Detection Systems (HIDS), built to run continuously as a background service.

## Overview

HIDS-Agent runs on a single Linux host and watches its log sources (system journal, application log files, etc.) continuously. When it detects an event that matches a failure or alert rule, it records it and can notify whoever is responsible for the system. It can also generate on-demand reports of everything that happened within a given time window, or filtered by severity.

## Goals

- **Real-time collection** — tail log files and stream the system journal (`journalctl`) as events happen, not in batches.
- **Always-on** — run as a background service that starts automatically on boot and restarts itself if it crashes.
- **Failure detection** — classify incoming log lines by severity/type (not just keyword matching) so it can catch every kind of failure, not a fixed list.
- **Alerting** — notify a configured responsible party (e.g. via email or webhook) when a relevant event occurs.
- **Reporting** — produce a summary report of everything that happened up to a given point in time, or filtered to a specific severity/type, on demand.

## Planned features

- [ ] Real-time log file tailing
- [ ] Real-time journald streaming
- [ ] Rule-based / severity-based failure classification
- [ ] Persistent event storage (queryable)
- [ ] On-demand report generation (by time range and/or severity)
- [ ] Alert notifications (email / webhook)
- [ ] systemd service for boot-time startup and auto-restart
- [ ] Configurable rules and notification targets

## Requirements

- Linux (uses `journalctl` and standard log file locations)
- Python 3.x

## Installation

```bash
git clone <repo-url>
cd hids-agent
# setup instructions go here
```

## Usage

```bash
# examples go here once the CLI is implemented
```

## Configuration

Configuration (log sources, alert rules, notification targets) will be defined in a config file — details to be added as the format is implemented.

## Status

Work in progress — built as a learning project to understand Linux logging, systemd services, and Python concurrency in depth.

## License

TBD