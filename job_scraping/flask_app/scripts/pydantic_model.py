from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date

class Listing(BaseModel):
    title: str
    link: str
    company: str = None
    location: str = None
    salary: str = None
    description: str = None
    date_added: str | datetime = None
    skills: List[str] = None
    search_term: str = 'python'
    date_searched: date = date.today()