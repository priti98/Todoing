//selectors 
const todoInput = document.querySelector(".todo-input"); 
const todoList = document.querySelector(".todo-list");
const todoButton = document.querySelector(".todo-button");
const filterOption = document.querySelector(".filter-todo");
const user=document.getElementById('user-data').textContent;


//event listeners
document.addEventListener("DOMContentLoaded", getTodos);
todoButton.addEventListener("click", addTodo);
todoList.addEventListener("click", deleteCheck);
filterOption.addEventListener("click", filterTodo);


//Functions

// add new todo 
function addTodo(event) {
    //prevent form from submitting (prevents refresh)
    event.preventDefault();

    if(todoInput.value!=""){

        //create new Todo DIV
    const todoDiv = document.createElement("div");
    todoDiv.classList.add("todo");

    //create new LI
    const newTodo = document.createElement("li");
    newTodo.innerText = todoInput.value;
    newTodo.classList.add('todo-item');
    todoDiv.appendChild(newTodo); 

    //CHECK MARK BUTTON
    const completedButtton = document.createElement('button');
    completedButtton.innerHTML = '<i class="fas fa-check"></i>';
    completedButtton.classList.add("complete-button");
    todoDiv.appendChild(completedButtton);

    //CHECK TRASH BUTTON
    const trashButtton = document.createElement('button');
    trashButtton.innerHTML = '<i class="fas fa-trash"></i>';
    trashButtton.classList.add("trash-button");
    todoDiv.appendChild(trashButtton);

    //APPEND TO LIST
    todoList.appendChild(todoDiv);
    
    let res = fetch("http://127.0.0.1:5000/newTodo", {
        method: 'POST',
        headers: {
            "content-type": "application/json"
        },
        body: JSON.stringify({ 'activity': todoInput.value , 'user': user})

    });

    //clear todo input value
    todoInput.value = "";
    }
    
}

// delete the todo 
async function deleteCheck(e) {
    //gets the target where the click event was made
    const item = e.target;
    let action = "";
    const todo = item.parentElement;
    activity = todo.children[0].innerText;
    //check if the target was the trash button then delete todo 
    if (item.classList[0] === "trash-button") {
        action = "delete";
        //add animation
        todo.classList.add('fall');
        // removeLocalTodos(todo);
        todo.addEventListener('transitionend', function () {
            todo.remove(); //removes element from DOM
        });


    }

    //check complete mark
    if (item.classList[0] === "complete-button") {
        action = "complete";
        todo.classList.toggle('completed');
    }
    // send data to db to delete the todo or mark it complete
    let res = await fetch("http://127.0.0.1:5000/updateTodo", {
        method: "POST",
        headers: {
            "content-type": "application/json"
        },
        body: JSON.stringify({
            'activity': activity,
            'action': action,
            'user':user
        })
    })

}

// filter the todolist as per chosen filter 
function filterTodo(e) {
    const todos = document.querySelectorAll('.todo');
    //todoList.childNodes;
    todos.forEach(function (todo) {
        switch (e.target.value) {
            case "all":
                todo.style.display = "flex";
                break;
            case "completed":
                if (todo.classList.contains("completed")) {
                    todo.style.display = "flex";
                }
                else {
                    todo.style.display = "none";
                }
                break;
            case "incompleted":
                if (!todo.classList.contains("completed")) {
                    todo.style.display = "flex";
                }
                else {
                    todo.style.display = "none";
                }
                break;
        }
    });
}

// get todo list from database 
async function getTodos() {

    let response = await fetch(`http://127.0.0.1:5000/allTodos/${user}`, {
        method: 'GET'
    });
    const todos = await response.json();

console.log('all todos is working');
    //for each todo in the fetched todolist, create a div and complete and delete button for it
        for (const [key, value] of Object.entries(todos)){
        //Todo DIV
        const todoDiv = document.createElement("div");
        todoDiv.classList.add("todo");

        //create LI
        const newTodo = document.createElement("li");
        newTodo.innerText = key;
        newTodo.classList.add('todo-item');
        if(value){
            todoDiv.classList.add('completed');
        }
        todoDiv.appendChild(newTodo); 


        //CHECK MARK BUTTON
        const completedButtton = document.createElement('button');
        completedButtton.innerHTML = '<i class="fas fa-check"></i>';
        completedButtton.classList.add("complete-button");
        todoDiv.appendChild(completedButtton);

        //CHECK TRASH BUTTON
        const trashButtton = document.createElement('button');
        trashButtton.innerHTML = '<i class="fas fa-trash"></i>';
        trashButtton.classList.add("trash-button");
        todoDiv.appendChild(trashButtton);

        //APPEND TO LIST
        todoList.appendChild(todoDiv);

    }
}

