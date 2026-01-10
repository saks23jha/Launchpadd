# NGINX Reverse Proxy – Week 5 Day 3

## Overview
This setup demonstrates NGINX running inside Docker as a reverse proxy and load balancer.

---

## Architecture
- NGINX acts as a single entry point
- Two backend containers run identical services
- Requests are distributed using round-robin strategy

---

## Routing
- Client sends request to `/api`
- NGINX forwards request to backend containers
- Client never communicates with backends directly

---

## Load Balancing
- NGINX uses round-robin by default
- Each request is sent to a different backend instance

---

## Networking
- Docker Compose provides internal DNS
- Backend services are accessed using service names

---

## Key Learnings
- Reverse proxy hides internal services
- Load balancing improves scalability
- NGINX is commonly used in production systems
