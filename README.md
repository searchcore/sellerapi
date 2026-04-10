# 🚀 Digital Products API

A flexible and extensible API for storing, managing, and selling digital products.

## 📌 Overview

This project provides a backend system that allows you to define **custom product types**, validate product data using **JSON Schema**, and manage the full lifecycle of digital goods — from creation to purchase.

The core idea is to make the system **schema-driven**, enabling dynamic product structures without requiring code changes.

### 🧠 Key Concepts
#### 📦 Product Types

A Product Type defines:

The name of the product
A schema (in JSON Schema format) that describes its structure

When a product is created, its data is validated against the schema — ensuring:

- ✅ Data consistency
- 🔄 Flexibility and extensibility
- ⚙️ No need for code changes when updating product structure

#### 🔁 Schema Versioning

Each product type can have multiple schema versions, allowing:

Smooth migrations between formats
Backward compatibility
Adaptation to evolving product requirements

#### 🏷️ Product Features

Products can include features (similar to tags), enabling advanced filtering and categorization, for example:

- Activation region
- Platform
- Availability constraints

#### 🔐 Authentication & Authorization
- Uses Bearer Access Tokens
- Tokens are securely stored as hashes in the database

### 🛠️ API Structure
#### 👨‍💼 Admin Endpoints

`/api/v1/admin/`

Admin functionality includes:

#### ➕ Creating and managing products
- 👥 Managing customers
- 🧩 Managing product types

`/api/v1/customer/`

Customer functionality includes:

- 💳 Purchasing products
- 🔍 Filtering products by features and other parameters

## 🗺 Roadmap

Planned features for future development:

### ⚙️ Workflow Pipelines

User-defined sequences of actions that can be applied to products of a specific type.

Examples:
- Content transformation
- Validation checks
- External API requests

### 📦 Extended Product Management
- View available schemas
- Add new schema versions
- Browse and manage product types

### 🔐 Advanced Access Control
- Refresh tokens
- Role-Based Access Control (RBAC)
- Attribute-Based Access Control (ABAC)