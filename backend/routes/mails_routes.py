from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from core.mailer import send_mail
from schemas.mailbody import MailBody


router = APIRouter(prefix="/mail",
                    tags=["mail management"],
                    responses={status.HTTP_404_NOT_FOUND: {"response": "not found"}})



@router.post("/sendemail", status_code = status.HTTP_202_ACCEPTED)
async def send_email(req: MailBody, tasks: BackgroundTasks):
    data = req
    tasks.add_task(send_mail, data)
    return {"status": 200, "message": "email has been scheduled"}
    

