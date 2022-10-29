import fastapi
from mndot_bid_api.db import models
from mndot_bid_api.operations import enums, schema
from sqlalchemy.orm import Session

IN_SPEC_YEAR_COLUMN_MAP = {
    enums.SpecYear.SPEC_2016: models.Item.in_spec_2016,
    enums.SpecYear.SPEC_2018: models.Item.in_spec_2018,
    enums.SpecYear.SPEC_2020: models.Item.in_spec_2020,
    enums.SpecYear.SPEC_2022: models.Item.in_spec_2022,
}


def read_all_items(spec_year: enums.SpecYear, db: Session) -> schema.ItemCollection:

    item_records = (
        db.query(models.Item).filter(IN_SPEC_YEAR_COLUMN_MAP[spec_year] == True).all()
    )

    item_results = [schema.ItemResult(**models.to_dict(item)) for item in item_records]

    return schema.ItemCollection(data=item_results)


def read_item(spec_year, spec_code, unit_code, item_code, db) -> schema.Item:

    item_record = (
        db.query(models.Item)
        .filter(IN_SPEC_YEAR_COLUMN_MAP[spec_year] == True)
        .filter(models.Item.spec_code == spec_code)
        .filter(models.Item.unit_code == unit_code)
        .filter(models.Item.item_code == item_code)
        .first()
    )

    if not item_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Item not found",
        )

    item_result = schema.ItemResult(**models.to_dict(item_record))

    return schema.Item(data=item_result)


def search_item(
    spec_year: enums.SpecYear, search_string: str, db: Session
) -> schema.ItemCollection:

    results = []
    for column in models.get_columns(models.Item):
        # skip searching id
        if column.name in ["id"]:
            continue

        item_records = (
            db.query(models.Item)
            .filter(IN_SPEC_YEAR_COLUMN_MAP[spec_year] == True)
            .filter(column.like(f"%{search_string}%"))
            .all()
        )
        if item_records:
            results.extend(item_records)

    if not results:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"No items found matching the provided search string",
        )

    results_no_duplicates_sorted = sorted(set(results), key=lambda item: item.id)

    item_results = [
        schema.ItemResult(**models.to_dict(item))
        for item in results_no_duplicates_sorted
    ]

    return schema.ItemCollection(data=item_results)


def read_item_by_id(item_id: int, db: Session) -> schema.Item:

    item_record = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not item_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Item at ID {item_id} not found",
        )

    item_result = schema.ItemResult(**models.to_dict(item_record))

    return schema.Item(data=item_result)


def create_item(data: schema.ItemCreateData, db: Session) -> schema.Item:

    item_record = (
        db.query(models.Item)
        .filter(
            models.Item.spec_code == data.spec_code,
            models.Item.unit_code == data.unit_code,
            models.Item.item_code == data.item_code,
            models.Item.long_description == data.long_description,
            models.Item.unit_abbreviation == data.unit_abbreviation,
        )
        .first()
    )

    if item_record:
        # Set the corresponding in_spec_#### column to True and commit the updated record
        setattr(item_record, IN_SPEC_YEAR_COLUMN_MAP[data.spec_year].name, True)

        db.add(item_record)
        db.commit()

        item_result = schema.ItemResult(**models.to_dict(item_record))

        return schema.Item(data=item_result)

    # Create a new record, setting the matching in_spec_#### to True and the rest to False
    item_model = models.Item(**data.dict(exclude={data.spec_year.name}))

    for spec_year, in_spec_column in IN_SPEC_YEAR_COLUMN_MAP.items():
        if spec_year == data.spec_year:
            setattr(item_model, in_spec_column.name, True)
        else:
            setattr(item_model, in_spec_column.name, False)

    db.add(item_model)
    db.commit()

    item_result = schema.ItemResult(**models.to_dict(item_model))

    return schema.Item(data=item_result)


def update_item(item_id: int, data: schema.ItemUpdateData, db: Session) -> schema.Item:

    item_record = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not item_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Item at ID {item_id} not found",
        )

    for key, value in data.dict(exclude_none=True).items():
        setattr(item_record, key, value)

    db.add(item_record)
    db.commit()

    item_result = schema.ItemResult(**models.to_dict(item_record))

    return schema.Item(data=item_result)


def delete_item(item_id: int, db: Session) -> None:

    item_record = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not item_record:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Item at ID {item_id} not found",
        )

    db.delete(item_record)
    db.commit()
