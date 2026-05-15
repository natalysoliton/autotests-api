class ShortUserSchema(BaseModel):
    id: str
    email: str

class ExtendedUserSchema(ShortUserSchema):
    last_name: str
    first_name: str
    middle_name: str
