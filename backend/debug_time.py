from pydantic import BaseModel
from datetime import time

class Avail(BaseModel):
    start_time: time

a = Avail(start_time="09:00:00")
dump = a.model_dump()
print(f"Type of start_time: {type(dump['start_time'])}")
print(f"Value: {dump['start_time']}")
