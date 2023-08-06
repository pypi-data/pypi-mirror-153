from fastapi import APIRouter

from apiautomata.holder.ItemHolder import ItemHolder

router = APIRouter()


@router.get('/')
async def index():
    return {'api': 'Automata API', 'version': ItemHolder.get('version')}

