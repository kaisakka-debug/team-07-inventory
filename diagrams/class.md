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
    }

    class Product {
        +str name
        +float unit_price
        +int quantity
        +str category
        +int threshold
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
        -_registry: dict~str, type~
        +register(str channel_name, type notifier_cls) void
        +create(str channel, dict config) Notifier
    }

    %% ==========================================
    %% 3. SERVICE LAYER (service.py)
    %% ==========================================
    class InventoryService {
        -dict~str, Product~ _products
        -list~StockTransaction~ _transactions
        -list~Notifier~ _observers
        +add_observer(Notifier notifier) void
        +remove_observer(Notifier notifier) void
        -_notify_observers(str message) void
        +add_product(Product product) void
        +get_product(str product_name) Product
        +list_products() list~Product~
        +receive_stock(str product_name, int quantity) Product
        +issue_stock(str product_name, int quantity) Product
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
    Notifier <|.. EmailNotifier : realization
    Notifier <|.. SMSNotifier : realization
    NotifierFactory ..> Notifier : creates
    
    InventoryService "1" o-- "*" Notifier : _observers (Observer Pattern)
    InventoryService "1" *-- "*" Product : manages
    InventoryService "1" *-- "*" StockTransaction : records
    StockTransaction "1" --> "1" TransactionType : transaction_type

    InventoryService ..> ProductNotFoundError : raises
    InventoryService ..> InsufficientStockError : raises