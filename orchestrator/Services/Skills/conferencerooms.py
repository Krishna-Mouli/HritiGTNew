from datetime import datetime
from ..GoogleCloudServices import GCPTableStorageServiceClient
from Data.Models import ConferenceRoomBookingData, ConferenceRoomData
from Utils.Helpers import HTMLTableGenerator
import random
import uuid

class ConferenceRooms():
    def __init__(self):
        self.helper = HTMLTableGenerator()

    def get_conference_room_details(self): 
        datastore_service = GCPTableStorageServiceClient(model = ConferenceRoomData)        
        data = datastore_service.get_all_data()    
        html_str = self.helper.convert_to_html(data)       
        return html_str

    def post_conference_room_details(self, Date, ConferenceRoomNumber, starttime, endtime, purpose):
        try:
            user = 'JaneDoe@abccompany.com'    
            user_name = 'Jane Doe'    
            phone_number = '9876543210'

            booking_date = datetime.strptime(Date, '%Y-%m-%d').date()
            start_time = datetime.strptime(starttime, '%H:%M').time()
            end_time = datetime.strptime(endtime, '%H:%M').time()
            start_dt = datetime.combine(datetime.min, start_time)
            end_dt = datetime.combine(datetime.min, end_time)
            duration = (end_dt - start_dt).seconds / 3600

            datastore_service = GCPTableStorageServiceClient(model = ConferenceRoomBookingData)
            booking_id = random.randint(1000, 9999)
            data = ConferenceRoomBookingData(
                entity_id = str(uuid.uuid4()),
                booking_id = str(booking_id),
                conference_room_number = str(ConferenceRoomNumber),
                user_id = user,
                user_name = user_name,
                date = str(booking_date),
                starttime = str(start_time),
                endtime = str(end_time),
                duration = str(duration),
                purpose = purpose,
                phone_number = phone_number, 
            ) 
            datastore_service.upsert_data(data = data)                             
            return f"Dear {user_name} we have booked your conference room we have used your phone number {phone_number}, Booking confirmed, your booking id is {booking_id} for conference room {ConferenceRoomNumber} from {starttime} to {endtime} on {Date}." 
        except Exception as e:
            return f"There was an error {e}"

    def get_conference_room_booking_details(self):
        datastore_service = GCPTableStorageServiceClient(model = ConferenceRoomBookingData)        
        data = datastore_service.get_all_data()    
        html_str = self.helper.convert_to_html(data)       
        return html_str