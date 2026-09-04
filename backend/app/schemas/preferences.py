from pydantic import BaseModel
class UserPref(BaseModel): theme: str = 'dark'