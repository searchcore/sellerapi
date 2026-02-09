# Seller API

API for selling digital goods with flexible validation system and token-based access control.

1. Purchase token management
    - Admin endpoints for creating and managing purchase tokens
    - Configurable purchase limits per token (Only total usage for now)

2. Product inventory system
    - Admin endpoints for product management (import, validated import)

3. Simple plugin-based validation architecture
    - Default validator for all products
    - You can create custom logic validators per product type

## Run
```
docker compose up -d
```