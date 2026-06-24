from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getRangeCoord():
        cnx = DBConnect.get_connection()
        result = {}
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
            SELECT 
                MIN(s.Lat) as minLat,
                MAX(s.Lat) as maxLat,
                MIN(s.Lng) as minLng,
                MAX(s.Lng) as maxLng
            FROM state s 
            """
            cursor.execute(query)

            data = cursor.fetchall()
            result["lat"] = (data[0]["minLat"], data[0]["maxLat"])
            result["lng"] = (data[0]["minLng"], data[0]["maxLng"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getShapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
            SELECT DISTINCT s.shape 
            FROM sighting s 
            WHERE s.shape <> '' 
            """
            cursor.execute(query)

            for row in cursor:
                result.append(row[0])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodes(lat, lng, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
            SELECT DISTINCT st.*
            FROM sighting si , state st
            WHERE si.state = st.id
            AND st.Lat > %s
            AND st.Lng > %s
            AND si.shape = %s
            """
            cursor.execute(query, (lat, lng, shape))

            for row in cursor:
                result.append(State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(lat, lng, shape, idMapStates):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """
            WITH st as (
                SELECT st.id, sum(si.duration) as durata
                FROM sighting si , state st
                WHERE si.state = st.id
                AND st.Lat > %s
                AND st.Lng > %s
                AND si.shape = %s
                GROUP BY st.id
            ) 
            SELECT st1.id, st2.id , SUM((st1.durata + st2.durata)) as peso
            FROM st as st1, st as st2, neighbor n 
            WHERE n.state1 = st1.id 
            AND n.state2 = st2.id
            AND st1.id > st2.id
            GROUP BY st1.id, st2.id
            """
            cursor.execute(query, (lat, lng, shape))

            for row in cursor:
                result.append((idMapStates[row[0]], idMapStates[row[1]], row[2]))

            cursor.close()
            cnx.close()
        return result




