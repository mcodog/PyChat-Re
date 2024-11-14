from collections import deque, defaultdict, UserDict, UserList
search_queries = deque(maxlen=5)
search_queries.extend(["laptop", "desk", "chair", "monitor", "keyboard"])
stock_levels = defaultdict(lambda: 10)
stock_levels['laptop'] = 5
stock_levels['desk'] = 7
class EmployeeDict(UserDict):
    def display(self):
        print("Employee Records:", self.data)
employees = EmployeeDict({'E001': 'Alice', 'E002': 'Bob', 'E003': 'Charlie'})
class TaskList(UserList):
    def add_unique(self, task):
        if task not in self.data:
            self.append(task)
tasks = TaskList(['Design logo'])
tasks.add_unique('Develop website')
tasks.add_unique('Design logo')
print("5. deque- Recent Searches:", list(search_queries))
print("6. defaultdict- Stock Levels:", dict(stock_levels))
print("7. UserDict- Display Method Output:")
employees.display()
print("8. UserList- Project Tasks:", list(tasks))