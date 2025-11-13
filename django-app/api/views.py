from rest_framework.response import Response
from rest_framework.decorators import api_view
from pymavlink import mavutil



connection = None

@api_view(['GET'])
def receiving_messages(request):
    global connection
    try:
        connection = mavutil.mavlink_connection('udpin:0.0.0.0:14551')
        connection.wait_heartbeat()
        print('Heartbeat from system (system %u component %u)' % (connection.target_system, connection.target_component))

        if 'GPS_RAW_INT' in connection.messages:
            sysid = connection.target_system
            altitude = connection.messages['GPS_RAW_INT'].alt
            latitude = connection.messages['GPS_RAW_INT'].lat
            longitude = connection.messages['GPS_RAW_INT'].lon
            timestamp = connection.time_since('GPS_RAW_INT')
            data = {"System_ID":sysid,"latitude":latitude,"longitude":longitude, "altitude": altitude, "timestamp": timestamp}
        else:
            data = {"error":"no message"}

        connection.close()
        return Response(data)

    except Exception as e:
        print('Error :', e)
        return Response({"error": str(e)})

