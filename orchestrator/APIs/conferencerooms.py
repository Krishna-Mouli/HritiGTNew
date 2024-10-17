from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Services import GCPTableStorageServiceClient
from Data import ConferenceRoomData
import uuid
from Services.Skills.conferencerooms import ConferenceRooms

router = APIRouter()

@router.post(path = "/add", description = "Add a new conference room to the existing database")
def add_conference(req: ConferenceRoomData):
    try:
        datastore_service = GCPTableStorageServiceClient(model = ConferenceRoomData)
        data = ConferenceRoomData(      
            entity_id = str(uuid.uuid4()),     
            conference_room_id = req.conference_room_id,
            occupency_limit = req.occupency_limit,
            reserved_for = req.reserved_for,
            projector = req.projector,
            location = req.location
        )
        datastore_service.upsert_data(data)
        return JSONResponse(
            status_code = 200,
            content = {"message":"Successfully added a new entry"}
        )
    except Exception as e:
        return JSONResponse(
            status_code = 500,
            content = {"message":f"faliled due to {e}"} 
        )

@router.get(path = "/getall", description = "Get all entries")
def get_all_conference_rooms():
    try:
        obj = ConferenceRooms()
        resp = obj.get_conference_room_details()
        return JSONResponse(
            status_code = 200,
            content = {"message":f"{resp}"}
        )
    except Exception as e:
        return JSONResponse(
            status_code = 500,
            content = {"message":"There was an error"}
        )