# Service Architecture – Week 5 Day 2

## Overview
This project demonstrates a multi-container application using Docker Compose.  
It consists of three services: Client, Server, and MongoDB, all running in separate containers and managed together.

---

## Services

### 1. Client
- Runs a simple Node.js HTTP server
- Exposed on port **3000**
- Provides a UI with a button to interact with the server
- Does not directly communicate with the database

### 2. Server
- Runs a Node.js backend server
- Exposed on port **5000**
- Handles client requests
- Connects to MongoDB using Docker container networking

### 3. MongoDB
- Official MongoDB image (`mongo:6`)
- Runs on port **27017** internally
- Stores application data
- Uses a named volume for persistence

---

## Container Networking
Docker Compose creates a private bridge network automatically.

- Containers communicate using **service names** as hostnames
- The server connects to MongoDB using:
