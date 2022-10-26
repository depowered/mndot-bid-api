import fastapi
from mndot_bid_api.db import models
from mndot_bid_api.operations import schema
from sqlalchemy.orm import Session


def read_all_contracts(db: Session()) -> list[schema.ContractResult]:
    contract_records = db.query(models.Contract).all()
    return [
        schema.ContractResult(**models.to_dict(contract))
        for contract in contract_records
    ]


def read_contract(contract_id: int, db: Session) -> schema.ContractResult:
    contract_record = (
        db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    )
    if not contract_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Contract at ID {contract_id} not found",
        )

    return schema.ContractResult(**models.to_dict(contract_record))


def create_contract(
    data: schema.ContractCreateData, db: Session
) -> schema.ContractResult:
    contract_record = (
        db.query(models.Contract).filter(models.Contract.id == data.id).first()
    )
    if contract_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_303_SEE_OTHER,
            detail=f"Contract already exists at ID {data.id}",
        )

    contract_model = models.Contract(**data.dict())
    db.add(contract_model)
    db.commit()

    return schema.ContractResult(**models.to_dict(contract_model))


def update_contract(
    contract_id: int, data: schema.ContractUpdateData, db: Session
) -> schema.ContractResult:
    contract_record = (
        db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    )
    if not contract_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Contract at ID {contract_id} not found",
        )

    for key, value in data.dict(exclude_none=True).items():
        setattr(contract_record, key, value)

    db.add(contract_record)
    db.commit()

    return schema.ContractResult(**models.to_dict(contract_record))


def delete_contract(contract_id: int, db: Session) -> None:
    contract_record = (
        db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    )
    if not contract_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Contract at ID {contract_id} not found",
        )

    db.delete(contract_record)
    db.commit()
