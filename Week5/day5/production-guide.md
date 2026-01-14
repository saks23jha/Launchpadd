# DockFlow – Production Deployment Guide

## Overview
DockFlow is a Dockerized full-stack application deployed using Docker Compose with NGINX as a reverse proxy and HTTPS termination.

## Architecture
Frontend → NGINX → Backend → MongoDB

## Security
- HTTPS enabled using mkcert
- Certificates mounted read-only
- Secrets stored in .env (not committed)

## Reliability
- Restart policies enabled
- Health checks configured
- Persistent MongoDB volume

## Deployment
Run:
```bash
./deploy.sh
