from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks
from classes.classes import claseSociosSteren
from functions.sociosSteren import mainSociosSterenFunc

app = FastAPI(title="Ralken-Steren", version="1.0.0")
@app.post('/webhook-socios-steren', description="Webhook para el bot de servicios para socios de Steren")
async def webhook(request: Request):
    background_tasks = BackgroundTasks()
    request_data = await request.json()
    webhook_request = claseSociosSteren(**request_data)
    response_data = await mainSociosSterenFunc(webhook_request.queryResult, webhook_request.session, background_tasks)
    # print(background_tasks.tasks)
    response = JSONResponse(content=response_data)
    response.background = background_tasks
    return response