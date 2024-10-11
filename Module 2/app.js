// Array to store tasks
let tasks = [];

// Function to add task to list and display on the screen
function addTask(title, dueDate) {
    const task = {
        id: Date.now(),
        title: title,
        dueDate: dueDate,
        completed: false
    };
    tasks.push(task);
    displayTasks();
}

// Function to display tasks
function displayTasks() {
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';
    tasks.forEach(task => {
        const taskElement = document.createElement('li');
        taskElement.textContent = `${task.title} (Due: ${moment(task.dueDate).format('MMM DD, YYYY')})`;

        if (task.completed) {
            taskElement.classList.add('completed');
        }

        const completeButton = document.createElement('button');
        completeButton.textContent = task.completed ? 'Undo' : 'Complete';
        completeButton.addEventListener('click', () => toggleTaskCompletion(task.id));
        taskElement.appendChild(completeButton);

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', () => deleteTask(task.id));
        taskElement.appendChild(deleteButton);

        taskList.appendChild(taskElement);
    });
}

// Function to toggle task completion
function toggleTaskCompletion(id) {
    tasks = tasks.map(task => {
        if (task.id === id) {
            task.completed = !task.completed;
        }
        return task;
    });
    displayTasks();
}

// Function to delete task
function deleteTask(id) {
    tasks = tasks.filter(task => task.id !== id);
    displayTasks();
}

// Event listener for task form submission
document.getElementById('taskForm').addEventListener('submit', event => {
    event.preventDefault();
    const taskTitle = document.getElementById('taskTitle').value;
    const taskDueDate = document.getElementById('taskDueDate').value;
    if (taskTitle && taskDueDate) {
        addTask(taskTitle, taskDueDate);
        document.getElementById('taskForm').reset();
    } else {
        alert('Please provide both task title and due date.');
    }
});
