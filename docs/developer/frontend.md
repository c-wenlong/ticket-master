In the app, there is the:

1. Home Page
2. View Tickets
3. Kanban Board
4. Analytics

### Home

![login](../assets/login.png)

In home, I have implemented a simple login page, the auth states are hardcoded and is stored within `src/utils/sample_data.py`. This is what it looks like.

```json
SAMPLE_USERS = [
    User(**user_data)
    for user_data in [
        {
            "id": "USER-1",
            "name": "Kai Chen",
            "email": "chenwenlongofficial@gmail.com",
            "username": "kai",
            "role": "developer",
        },
        {
            "id": "USER-2",
            "name": "Avellin",
            "email": "avellin@gmail.com",
            "username": "avellin",
            "role": "developer",
        },
        {
            "id": "USER-3",
            "name": "Xiaoyun",
            "email": "xiaoyun@gmail.com",
            "username": "xiaoyun",
            "role": "developer",
        },
        {
            "id": "USER-4",
            "name": "Ryan",
            "email": "ryan@gmail.com",
            "username": "ryan",
            "role": "developer",
        },
    ]
]
```

The text boxes within the home page parses the name and email so make sure it is exactly the same as any of the auth states above, you can change this manually within the hard-coded file.

### View Tickets

In view tickets, there are 2 tabs, one is to view tickets, editing is not supported, if you want to edit, you have to switch to the other tab.

### Kanban Board

For the Kanban board
