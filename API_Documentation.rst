Atomic Inventory Management System API
======================================

.. contents:: Table of Contents
   :depth: 2
   :local:

Overview
--------
The **Atomic Inventory Management System API** enables clients, agents, and managers 
to interact with the system programmatically.  
It exposes endpoints for managing **users, products, inventory, deliveries, and reports**.

This document provides **endpoint descriptions, request/response formats, and examples** 
to help developers integrate seamlessly.

Authentication
--------------
- **Type**: Token-based authentication (JWT or session-based depending on configuration).
- **Header format**::

    Authorization: Bearer <your-token>

Models
------
This section describes the core models in the system.

**User**
    - ``id`` (int): Unique user identifier
    - ``username`` (string): Login name
    - ``role`` (string): One of: ``admin``, ``stock manager``, ``agent``
    - ``phone_number`` (string): Contact number

**Product**
    - ``id`` (int): Unique identifier
    - ``name`` (string): Product name
    - ``price`` (decimal): Unit price
    - ``quantity`` (int): Quantity in stock

**Delivery**
    - ``id`` (int): Delivery identifier
    - ``status`` (string): One of: ``pending``, ``in transit``, ``delivered``
    - ``initiated_by`` (int): ID of the initiating user
    - ``created_at`` (datetime): Timestamp

Endpoints
---------
Each section below lists endpoints by category.

Users
^^^^^
**Register User**

- **URL**: ``POST https://atomic-inventory-management-system.onrender.com/users/``
- **Description**: Creates a new user (agent, stock manager, or admin).
- **Request Example**::

    {
        "username": "agent_daniel",
        "password": "StrongPass123",
        "role": "agent",
        "phone_number": "+2348012345678"
    }

- **Response Example**::

    {
        "id": 12,
        "username": "agent_daniel",
        "role": "agent",
        "phone_number": "+2348012345678"
    }

**List Users**

- **URL**: ``GET https://atomic-inventory-management-system.onrender.com/users/``
- **Description**: Retrieves all users.
- **Response Example**::

    [
        {
            "id": 1,
            "username": "admin",
            "role": "admin",
            "phone_number": "+2348000000000"
        },
        {
            "id": 12,
            "username": "agent_daniel",
            "role": "agent",
            "phone_number": "+2348012345678"
        }
    ]

Products
^^^^^^^^
**Add Product**

- **URL**: ``POST https://atomic-inventory-management-system.onrender.com/products/``
- **Description**: Adds a new product.
- **Request Example**::

    {
        "name": "Laptop",
        "price": 550.00,
        "quantity": 15
    }

- **Response Example**::

    {
        "id": 101,
        "name": "Laptop",
        "price": 550.00,
        "quantity": 15
    }

**Get All Products**

- **URL**: ``GET https://atomic-inventory-management-system.onrender.com/products/``
- **Response Example**::

    [
        {
            "id": 101,
            "name": "Laptop",
            "price": 550.00,
            "quantity": 15
        },
        {
            "id": 102,
            "name": "Phone",
            "price": 200.00,
            "quantity": 50
        }
    ]

Deliveries
^^^^^^^^^^
**Initiate Delivery**

- **URL**: ``POST https://atomic-inventory-management-system.onrender.com/deliveries/``
- **Description**: Create a delivery record.
- **Request Example**::

    {
        "initiated_by": 12,
        "status": "pending"
    }

- **Response Example**::

    {
        "id": 301,
        "initiated_by": 12,
        "status": "pending",
        "created_at": "2025-09-06T10:15:00Z"
    }

**Update Delivery Status**

- **URL**: ``PATCH https://atomic-inventory-management-system.onrender.com/deliveries/{id}/``
- **Description**: Update the status of a delivery.
- **Request Example**::

    {
        "status": "delivered"
    }

- **Response Example**::

    {
        "id": 301,
        "initiated_by": 12,
        "status": "delivered",
        "created_at": "2025-09-06T10:15:00Z"
    }

Reports
^^^^^^^
**Generate Stock Report**

- **URL**: ``GET https://atomic-inventory-management-system.onrender.com/reports/stock/``
- **Description**: Provides a summary of stock levels.
- **Response Example**::

    {
        "total_products": 150,
        "low_stock": [
            {"id": 102, "name": "Phone", "quantity": 2}
        ]
    }

**Generate Delivery Report**

- **URL**: ``GET https://atomic-inventory-management-system.onrender.com/reports/deliveries/``
- **Description**: Provides delivery performance metrics.
- **Response Example**::

    {
        "total_deliveries": 45,
        "delivered": 40,
        "pending": 5
    }

Error Handling
--------------
Errors follow a consistent format.

**Example**::

    {
        "error": "Invalid credentials"
    }

- **400** Bad Request – Invalid input
- **401** Unauthorized – Missing/invalid token
- **403** Forbidden – User not permitted
- **404** Not Found – Resource missing
- **500** Server Error – Internal failure
