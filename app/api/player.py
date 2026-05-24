from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.db import SessionLocal, get_db
from app.models.player import PlayerRead, PlayerCreate, PlayerUpdate
from app.services.player_service import PlayerService

router = APIRouter()

def get_player_service(db: Session = Depends(get_db)) -> PlayerService:
    return PlayerService(session=db)

@router.get("/players", response_model=list[PlayerRead])
def get_players(service: PlayerService = Depends(get_player_service)):
    return service.list_players()

@router.get("/players/{player_id}", response_model=PlayerRead)
def get_player_by_id(player_id: int, service: PlayerService = Depends(get_player_service)):
    user =  service.get_player(player_id=player_id)
    if not user:
        raise HTTPException(status_code=404, detail="Player not found")
    return user

@router.post("/players", response_model=PlayerRead)
def create_player(player: PlayerCreate, service: PlayerService = Depends(get_player_service)):
    return service.create_player(player.name)

@router.put("/players/{player_id}", response_model=PlayerRead)
def update_player(player_id: int, player: PlayerUpdate, service: PlayerService = Depends(get_player_service)):
    updated_player = service.update_player(player.id, player.name)
    if not updated_player:
        raise HTTPException(status_code=404, detail="Player not found")
    return updated_player

@router.delete("/players/{player_id}", response_model=PlayerRead)
def delete_player(player_id: int, service: PlayerService = Depends(get_player_service)):
    success = service.delete_player(player_id)
    if not success:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"success": True}


