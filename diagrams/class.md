classDiagram
    direction TB

    %% ==========================================
    %% 1. MODELS LAYER (models.py)
    %% ==========================================
    class TransactionType {
        <<enumeration>>
        IN
        OUT
    }

    class Category {
        +str name
        +__post_init__() void
    }

    class Product {
        +str name
        +float unit_price
        +int quantity
        +str category
        +int threshold
        +list~str~ notification_channels
        +dict~str, dict~ channel_config
        +__post_init__() void
        +category_name: str
        +total_value: float
        +is_below_threshold() bool
    }

    class StockTransaction {
        +str product_name
        +TransactionType transaction_type
        +int quantity
        +int resulting_quantity
        +datetime timestamp
        +__post_init__() void
    }

    %% ==========================================
    %% 2. NOTIFICATION LAYER (notifiers.py)
    %% ==========================================
    class Notifier {
        <<interface>>
        +send(str message) bool
    }

    class EmailNotifier {
        +str email_address
        +send(str message) bool
    }

    class SMSNotifier {
        +str phone_number
        +send(str message) bool
    }

    class NotifierFactory {
        -dict~str, type~ _registry
        +register(str channel_name, type notifier_cls) void
        +create(str channel_name, **config) Notifier
    }

    %% ==========================================
    %% 3. SERVICE LAYER (service.py)
    %% ==========================================
    class InventoryService {
        -NotifierFactory _notifier_factory
        -dict~str, Product~ _products
        -list~StockTransaction~ _transactions
        +add_product(Product product) void
        +get_product(str product_name) Product
        +list_products() list~Product~
        +receive_stock(str product_name, int quantity) Product
        +issue_stock(str product_name, int quantity) Product
        -_notify_low_stock(Product product) void
        +get_stock_value_report() dict
    }

    class ProductNotFoundError {
        <<exception>>
    }

    class InsufficientStockError {
        <<exception>>
    }

    %% ==========================================
    %% RELATIONSHIPS
    %% ==========================================

    %% Realization (Implementation of Interface/Protocol)
    Notifier <|.. EmailNotifier : realization
    Notifier <|.. SMSNotifier : realization

    %% Composition (Strong Ownership/Lifetime Dependency)
    InventoryService "1" *-- "*" Product : manages / contains
    InventoryService "1" *-- "*" StockTransaction : records

    %% Association / Aggregation
    InventoryService "1" o-- "1" NotifierFactory : holds / uses
    StockTransaction "1" --> "1" TransactionType : transaction_type

    %% Dependency
    NotifierFactory ..> Notifier : creates
    NotifierFactory ..> EmailNotifier : registers & creates
    NotifierFactory ..> SMSNotifier : registers & creates
    InventoryService ..> Notifier : sends notification via
    InventoryService ..> ProductNotFoundError : raises
    InventoryService ..> InsufficientStockError : raises