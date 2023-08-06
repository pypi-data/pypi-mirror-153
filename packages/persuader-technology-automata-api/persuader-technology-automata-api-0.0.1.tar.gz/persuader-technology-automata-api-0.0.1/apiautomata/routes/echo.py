from coreutility.date_utility import get_utc_timestamp

from fastapi import APIRouter

router = APIRouter()


@router.get('/echo')
async def echo():
    return {'echo': get_utc_timestamp()}
