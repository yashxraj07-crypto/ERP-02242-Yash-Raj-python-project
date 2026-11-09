import os

FILE_NAME = "todo.txt"
PENDING = "Pending"
DONE = "Done"


def load_tasks():
    """Read tasks from todo.txt. A missing file is handled safely (empty list)."""
    tasks = []
    if not os.path.exists(FILE_NAME):
        return tasks
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if "|" in line:
                    title, status = line.rsplit("|", 1)
                else:                       # tolerate a badly formed line
                    title, status = line, PENDING
                status = DONE if status.strip() == DONE else PENDING
                tasks.append({"title": title.strip(), "status": status})
    except OSError:
        print("Could not read todo.txt. Starting with an empty list.")
        return []
    return tasks


def save_tasks(tasks):
    """Write every task back to todo.txt (called after each change)."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for task in tasks:
                file.write(f"{task['title']}|{task['status']}\n")
    except OSError:
        print("Error: could not save tasks to todo.txt.")


def read_task_number(tasks, action):
    """Ask for a task number. Return its index in the list, or None if invalid."""
    text = input(f"Enter task number to {action}: ").strip()
    if not text.isdigit():
        print(f"Task number {text} not found.")
        return None
    number = int(text)
    if number < 1 or number > len(tasks):
        print(f"Task number {number} not found.")
        return None
    return number - 1


def add_task(tasks):
    """Option 1 - add a new task (always starts as Pending)."""
    title = input("Task: ").strip()
    if title == "":
        print("Task title cannot be empty.")
        return
    tasks.append({"title": title, "status": PENDING})
    save_tasks(tasks)
    number = len(tasks)
    print(f"Task added. {number} | {title} | {PENDING}")


def view_tasks(tasks):
    """Option 2 - show all tasks."""
    if len(tasks) == 0:
        print("No tasks found. Your to-do list is empty.")
        return
    for number, task in enumerate(tasks, start=1):
        print(f"{number} | {task['title']} | {task['status']}")


def complete_task(tasks):
    """Option 3 - mark a task as completed."""
    index = read_task_number(tasks, "complete")
    if index is None:
        return
    tasks[index]["status"] = DONE
    save_tasks(tasks)
    print(f"Task {index + 1} marked as completed.")


def delete_task(tasks):
    """Option 4 - delete a task (numbers re-start from 1 automatically)."""
    index = read_task_number(tasks, "delete")
    if index is None:
        return
    tasks.pop(index)
    save_tasks(tasks)
    print(f"Task {index + 1} deleted. Tasks left: {len(tasks)}")


def show_menu():
    print("\n===== TO-DO LIST MENU =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")


def main():
    tasks = load_tasks()            # load at start
    while True:                     # loop-driven menu
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()