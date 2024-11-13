import uuid
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, FileResponse

from src.business_logic.services.conversation import (
    start_conversation,
    process_conversation
)
from src.presentation.models import StartData, ProcessingData


router = APIRouter()


@router.post("/start/")
async def start(
        data: StartData,
) -> FileResponse:
    # фронт даёт новый сгенеренный идентификатор и URL видео
    path_to_first_asst_message = await start_conversation(data)

    return FileResponse(path=path_to_first_asst_message)


@router.post("/process/")
async def process(
        data: ProcessingData,
) -> FileResponse:
    # фронт даёт ранее сгенеренный идентификатор и голосовое от ребенка
    path_to_asst_answer = await process_conversation(data)

    return FileResponse(path=path_to_asst_answer)