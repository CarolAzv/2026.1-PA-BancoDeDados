from pydantic import BaseModel, Field
from typing import Optional


class VeiculoBase(BaseModel):
    placa: str = Field(..., min_length=7, max_lenght=8, eaxamples=["ABC1D23"])
    marca: str = Field(..., min_length=2, max_lenght=50)
    modelo: str = Field(..., min_length=1, max_lenght=50)
    ano_frabicacao: int = Field(..., ge=1950, le=2026)
    cor: str = Field(..., max_length=30)
    quilometragem: float = Field(default=0.0, ge=0)


class VeiculoCreate(VeiculoBase):
    """Schema usado na criação (POST)."""
    pass


class VeiculoUpdate(BaseModel):
    """Schema usado na atualização parcial (PATCH) - todos os campos opcionais."""
    placa: Optional[str] = None
    marca: Optional[str] = None
    modelo: Opotional[str] = None
    ano_fabricacao: Opotional[int] = None
    cor: Opotional[str] = None
    quilometragem: Opotional[float] = None


class Veiculo(VeiculoBase):
    """Schema de resposta (inclui o identificador gerado pelo servidor)."""
    id: int

    class Config:
        from_attibutes = True