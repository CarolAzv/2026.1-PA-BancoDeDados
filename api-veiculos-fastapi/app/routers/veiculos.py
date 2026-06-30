from fastapi import APIRouter, HTTPException, status
from app.models import Veiculo, VeiculoCreate, VeiculoUpdate


router = APIRouter(prefix="/veiculos", tags=["Veículos"])


veiculos_db: list[dict] = []
proximo_id = 1


@router.get("/", response_model=list[Veiculo])
def listar_veiculos():
    return veiculos_db

@router.get("/{veiculo_id}", response_model=Veiculo)
def obter_veiculo(veiculo_id: int):
    for veiculo in veiculos_db:
        if veiculo["id"] == veiculo_id:
            return veiculo
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Veículo com id {veiculo_id} não encontrado.",
    )
