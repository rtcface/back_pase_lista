import re
from fastapi import HTTPException, status


class EmailValidator:
    def __init__(self, email_regex: str = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"):
        self.email_regex = email_regex

    def validate(self, email: str) -> bool:
        if not re.match(self.email_regex, email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is not valid")
        return True
