# **Inventory app**


## 📁 App Structure

The `inventory` app is structured to manage the following core models and their corresponding business logic:

-   **`models.py`**: Defines the database schemas for all inventory-related entities such as `Product`, `Order`, `Delivery`, `Merchant`, `Sku`, `ProductCategory`, `MissingProduct`, and `BtoB`.
    
-   **`serializers.py`**: Translates Django model instances into JSON format for API responses and handles incoming data for creation and updates.
    
-   **`views.py`**: Contains the API view logic, defining how each endpoint responds to HTTP requests. It includes `viewsets` for standard CRUD operations and `APIView` classes for custom logic like status updates.
    
-   **`urls.py`**: Maps API endpoints to their corresponding view functions.
    

## 📦 Data Models

The app relies on several models to represent the inventory system. Here are the key relationships:

-   **`Product`**: A central model representing a single inventory item. It has `ForeignKey` relationships to `ProductCategory`, `Merchant`, and `Sku`.
    
-   **`Order`**: Represents a customer order, linking a `Product` to the user who `raised` it and the agent it is `assigned_to`.
    
-   **`Delivery`**: A record of a delivery attempt, with a `ForeignKey` to an `Order`.
    
-   **`BtoB` (Back-to-Business)**: Records the return of a product from an agent back into inventory, with a `ForeignKey` to a `Delivery` record.
    
-   **`MissingProduct`**: A record created for items not returned after a failed delivery, with a `ForeignKey` to a `Delivery`.
    

## ⚙️ API Endpoints

The `inventory` app provides a robust API for managing all aspects of the inventory system. All endpoints require **Token Authentication** unless otherwise specified.

### 1. Merchant Management

**Path:**  `/merchant/`

-   **Permissions:** Admin, Stock Manager
    
-   **Functionality:** Standard CRUD operations for merchant records.
    

### 2. SKU Management

**Path:**  `/sku/`

-   **Permissions:** Admin, Stock Manager
    
-   **Functionality:** Standard CRUD operations for product SKUs.
    

### 3. Product Category Management

**Path:**  `/category/`

-   **Permissions:** Admin, Stock Manager
    
-   **Functionality:** Standard CRUD operations for product categories.
    

### 4. Product Management

**Path:**  `/product/`

-   **Permissions:** - **GET, POST**: Admin, Stock Manager
    
    -   **PUT, PATCH, DELETE**: Admin
        
-   **Functionality:** Standard CRUD operations for products.
    

### 5. Order Management

**Path:**  `/order/`

-   **Permissions:**
    
    -   **GET**: Admin, Stock Manager, Agent
        
    -   **POST, DELETE**: Admin, Stock Manager
        
    -   **PATCH**: Agent (to update `status` only)
        
-   **Functionality:** Create, retrieve, delete, and update the status of orders. A `PATCH` to update an order's status to `confirmed` triggers a stock deduction and a `Delivery` record creation.
    

### 6. Delivery Endpoints

**Paths:**

-   `/list/deliveries/all/`
    
-   `/list/deliveries/<int:pk>/`
    
-   `/make/delivery/<int:pk>/`
    
-   **Permissions:**
    
    -   **`/list/deliveries/all/`**: Admin
        
    -   **`/list/deliveries/<int:pk>/`**: All authenticated users
        
    -   **`/make/delivery/<int:pk>/`**: Agent (can only update their own assigned deliveries)
        
-   **Functionality:**
    
    -   Retrieve all deliveries or deliveries for a specific agent.
        
    -   An agent can update the status of a delivery to `delivered` or `failed`. A `failed` status automatically creates a `MissingProduct` record.
        

### 7. Missing Products Endpoints

**Paths:**

-   `/list/missing_products/all/`
    
-   `/list/missing_per_agent/<int:pk>/`
    
-   **Permissions:**
    
    -   **`/list/missing_products/all/`**: Admin, Stock Manager
        
    -   **`/list/missing_per_agent/<int:pk>/`**: All authenticated users
        
-   **Functionality:** Retrieve records of products that were not returned after a failed delivery.
    

### 8. Back-to-Business (BtoB) Endpoints

**Paths:**

-   `/make/btob/`
    
-   `/list/agent_btob/`
    
-   `/list/all_btob/`
    
-   `/confirm/btob/<int:pk>/`
    
-   **Permissions:**
    
    -   **`/make/btob/`, `/list/agent_btob/`**: Agent
        
    -   **`/list/all_btob/`, `/confirm/btob/<int:pk>/`**: Admin, Stock Manager
        
-   **Functionality:** Manages the return of products. An agent can initiate a BtoB request for a failed delivery, which an Admin or Stock Manager can then `confirm` to add the product back into stock.