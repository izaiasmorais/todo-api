const { v4 } = require("uuid");
const express = require("express");
const cors = require("cors");
const app = express();
const users = [];

app.use(cors());
app.use(express.json());

function checksExistsUserAccount(request, response, next) {
  const { username } = request.headers;

  const user = users.find((user) => user.username === username);

  if (!user) {
    return response.status(400).json({ error: "User doesn't exist" });
  }

  request.user = user;

  return next();
}

app.get("/users", (request, response) => {
  return response.json(users);
});

app.post("/users", (request, response) => {
  const { name, username } = request.body;

  const userAlreadyExists = users.some((user) => user.username === username);

  if (userAlreadyExists) {
    return response.status(400).json({ error: "User already exists" });
  }

  users.push({
    name,
    username,
    id: v4(),
    todos: [],
  });

  return response.status(200).send();
});

app.get("/todos", checksExistsUserAccount, (request, response) => {
  const { user } = request;

  return response.json(user.todos);
});

app.get("/user", checksExistsUserAccount, (request, response) => {
  const { user } = request;

  return response.json(user);
});

app.post("/todos", checksExistsUserAccount, (request, response) => {
  const { title, deadline } = request.body;
  const { user } = request;

  user.todos.push({
    id: v4(),
    title,
    done: false,
    deadline: new Date(deadline),
    created_at: new Date(),
  });

  return response.json(user.todos);
});

app.put("/todos", checksExistsUserAccount, (request, response) => {
  const { title, deadline } = request.body;
  const { user } = request;
  const { id } = request.headers;

  const exactTodo = user.todos.find((todo) => todo.id === id);

  if (!exactTodo) {
    return response.status(404).json({ error: "Todo not found" });
  }

  exactTodo.title = title;
  exactTodo.deadline = new Date(deadline);

  return response.status(200).send();
});

app.patch("/todos/done", checksExistsUserAccount, (request, response) => {
  const { id } = request.headers;
  const { user } = request;

  const exactTodo = user.todos.find((todo) => todo.id === id);

  if (!exactTodo) {
    return response.status(404).json({ error: "Todo not found" });
  }

  exactTodo.done = true;

  return response.status(200).send();
});

app.delete("/todos", checksExistsUserAccount, (request, response) => {
  const { user } = request;
  const { id } = request.headers;

  const exactTodo = user.todos.find((todo) => todo.id === id);

  if (!exactTodo) {
    return response.status(404).json({ error: "Todo not found" });
  }

  user.todos.splice(exactTodo, 1);

  return response.status(200).json(user.todos);
});

module.exports = app;
