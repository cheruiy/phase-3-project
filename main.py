#!/usr/bin/env python3

from models import ShoppingListManager

def main():
    manager = ShoppingListManager()
    while True:
        manager.display_help()
        command = input("Enter your command: ").strip().split()
        if not command:
            continue

        cmd = command[0].lower()

        if cmd == 'add-user' and len(command) == 2:
            manager.users.add_user(command[1])
        elif cmd == 'delete-user' and len(command) == 2:
            manager.users.delete_user(command[1])
        elif cmd == 'add-shopping-list' and len(command) == 3:
            manager.shopping_lists.add_shopping_list(int(command[1]), command[2])
        elif cmd == 'delete-shopping-list' and len(command) == 2:
            manager.shopping_lists.delete_shopping_list(command[1])
        elif cmd == 'add-item' and len(command) == 3:
            manager.items.add_item(command[1], int(command[2]))
        elif cmd == 'list-users':
            manager.users.list_users()
        elif cmd == 'list-shopping-lists':
            manager.shopping_lists.list_shopping_lists()
        elif cmd == 'list-items':
            manager.items.list_items()
        elif cmd == 'remove-item' and len(command) == 2:
            manager.items.remove_item(int(command[1]))
        elif cmd == 'add-user-to-shopping-list' and len(command) == 3:
            manager.shopping_lists.add_user_to_shopping_list(int(command[1]), int(command[2]))
        elif cmd == 'add-item-to-shopping-list' and len(command) == 4:
            manager.add_item_to_shopping_list(int(command[1]), int(command[2]), int(command[3]))
        elif cmd == 'list-tables':
            manager.list_tables()
        elif cmd == 'exit':
            print("Exiting...")
            break
        else:
            print("Invalid command. Please try again.")
            manager.display_help()

if __name__ == '__main__':
    main()
