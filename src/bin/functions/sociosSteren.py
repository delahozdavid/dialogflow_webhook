from typing import Dict, Any, List, Callable, Awaitable
from data.database import get_db_connection
from data.smtp import send_email_with_file
import logging
from datetime import date
from difflib import SequenceMatcher
from data.redis_database import get_session_data, set_session_data
from fastapi import BackgroundTasks
import random

async def mainSociosSterenFunc(queryResult: Dict[str, Any], session: str, background_tasks: BackgroundTasks):
    intent_name = queryResult.get('intent', {}).get('displayName', '')
    if intent_name == 'Prueba':
        return await prueba(queryResult)
    if intent_name == 'Prueba Email':
        return await prueba_mail(queryResult, background_tasks)
    if intent_name == 'Default Welcome Intent' or intent_name == 'Default Fallback Intent':
        return await handler_Default_Welcome(queryResult, session)

#Async function
async def handler_Default_Welcome(queryResult: Dict[str, Any], session: str):
    sessionId = session.split('/')[-1]
    try:
        connection = await get_db_connection()
        result = await connection.fetchrow("""
            SELECT telefono
            FROM steren.socio_steren_prueba
            WHERE telefono = $1
        """, sessionId)
        print(result)
        if(result):
            #Como el usuario si estaba en la base de datos, logging va en true
            logging = "true"
        else:
            #Como el usuario no estaba en la base de datos, logging va en false
            logging = "false"
        session_data = await get_session_data(sessionId)
        if(session_data):
            session_data["session"] = sessionId
            session_data["logging"] = logging
        else:
            session_data = {
                "session": sessionId,
                "logging": logging
            }
        await set_session_data(sessionId, session_data)
        print(session_data)
        #si el loggin fue True
        if(logging == "true"):
            return {
                "followupEventInput": {
                    "name": "logging_true",
                    "parameters": {

                    },
                    "languageCode": "en-US"
                }
            }
        else:
            return {
                "followupEventInput": {
                    "name": "logging_false",
                    "parameters": {

                    },
                    "languageCode": "en-US"
                }
            }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "followupEventInput":{
                "name": "error",
                "parameters": {

                },
                "languageCode": "en-US"
            }
        }
    #Always close the connection with the db 
    finally:
        await connection.close()

async def prueba_mail(queryResult: Dict[str, Any], background_tasks: BackgroundTasks):
    try:
        # background_tasks = BackgroundTasks()
        param_prueba = queryResult['parameters']['param_prueba']
        subject = "Email Subject"
        body = "Email Body hola de nuevo"
        email_to_send_to = "r.flores@ralken.com.mx"
        path_file = "imagen.png"
        print(background_tasks.tasks)
        # send_email_with_file(subject, body, email_to_send_to, path_file)
        background_tasks.add_task(send_email_with_file, subject, body, email_to_send_to, path_file)
        print(background_tasks.tasks)
        return {
            "followupEventInput": {
                "name": "proceso_seleccion_found",
                "parameters": {
                    "respuesta": "respuesta",
                },
                "languageCode": "en-US"      
            }
        }
    except Exception as e:
        logging.error(f"Error al realizar proceso: {e}")
        return {
            "followupEventInput": {
                "name": "error",
                "parameters": {
                    "message": "Internal server error"
                },
                "languageCode": "en-US"
            }
        }

async def prueba(queryResult: Dict[str, Any]):
    try:
        param_prueba = queryResult['parameters']['param_prueba']
        return {
            "followupEventInput": {
                "name": "proceso_seleccion_found",
                "parameters": {
                    "param_prueba": param_prueba,
                },
                "languageCode": "en-US"      
            }
        }
    except Exception as e:
        logging.error(f"Error al realizar proceso: {e}")
        return {
            "followupEventInput": {
                "name": "error",
                "parameters": {
                    "message": "Internal server error"
                },
                "languageCode": "en-US"
            }
        }