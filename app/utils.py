import json
from pydantic import BaseModel, ValidationError


def validate_schema_data_or_error(raw_data:dict, SchemaModel:BaseModel):

    data = {}
    errors = []
    error_str = None
    try:
        validate_data = SchemaModel(**raw_data)
        data = validate_data.model_dump()
    except ValidationError as e:
        error_str = e.json()
    if error_str is not None:
        try:
            errors = json.loads(error_str)
        except Exception as e:
            errors = [{"loc":"non_field_error", "msg":"Unknown error"}]
    return data, errors