from fastapi import APIRouter, Path, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates
from model import Todo, TodoItem, TodoItems

todo_router = APIRouter()

todo_list = []

templates = Jinja2Templates(directory="templates/")

@todo_router.post("/todo")
async def add_todo(request:Request,todo:Todo=Depends(Todo.as_form)):
    todo.id = len(todo_list) +1
    todo_list.append(todo)
    return templates.TemplateResponse("todo.html",{
        "request":request,
        "todos": todo_list
    })
    # return{
    #     "message":"Todo added successfully"
    # }

# @todo_router.get("/todo", response_model=TodoItems)
# async def retrieve_todos() -> dict:
#     return{
#         "todos":todo_list
#     }

@todo_router.get("/todo", response_model=TodoItems)
async def retrieve_todos(request: Request):
    return templates.TemplateResponse("todo.html",{
        "request":request,
        "todos":todo_list
    })

# @todo_router.get('/todo/{todo_id}')
# async def get_single_todo(todo_id:int = Path(..., title="ID of todo")) -> dict:
#     for todo in todo_list:
#         if todo.id == todo_id:
#             return {
#                 "todo":todo
#             }
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail = "Todo with supplied ID doesn't exist",
#     )

@todo_router.get('/todo/{todo_id}')
async def get_single_todo(request:Request ,todo_id:int = Path(..., title="ID of todo")):
    for todo in todo_list:
        if todo.id == todo_id:
            return templates.TemplateResponse(
                "todo.html",{
                    "request":request,
                    "todo":todo
                }
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail = "Todo with supplied ID doesn't exist",
    )

@todo_router.put("/todo/{todo_id}")
async def update_todo(todo_data: TodoItem, todo_id:int = Path(..., title="ID of todo updated"))->dict:
    for todo in todo_list:
        if todo.id == todo.id:
            todo.item = todo_data.item
            return{
                "message": "Todo updated success"
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist",
    )

@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
            return {
                "msg":"todo delete success"
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist",
    )

@todo_router.delete('/todo')
async def delete_all_todo() -> dict:
    todo_list.clear()
    return{
        "msg":"Todos deleted all success"
    }