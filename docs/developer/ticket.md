```mermaid
classDiagram
    class Status {
        <<enumeration>>
        OPEN
        IN_PROGRESS
        DONE
    }

    class Priority {
        <<enumeration>>
        HIGH
        MEDIUM
        LOW
    }

    class User {
        +str id
        +str name
        +EmailStr email
    }

    class Ticket {
        +str id
        +str title
        +str description
        +Status status
        +Priority priority
        +str reporter_id
        +datetime created_at
        +datetime updated_at
        +Optional[List[float]] embedding        
        .
        [Optional]
        +str parent_ticket_id
        +str assignee_id
        +List[str] labels
        +bool is_processed
    }

    class Project {
        +str id
        +str name
        +List[str] members
        +Settings settings
    }

    class Settings {
        +float duplicate_threshold
        +int max_ticket_size
    }

    Project *-- Settings : contains
    Ticket -- Status : has
    Ticket -- Priority : has
    Project -- User : has many
    Project -- Ticket : contains many
    Ticket -- User : assigned to
```
