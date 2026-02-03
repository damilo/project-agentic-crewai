from pydantic import BaseModel

class VenueDetails (BaseModel):
    name : str
    address : str
    capacity : str
    booking_status : str