# from . import get_db
from psycopg2 import sql
import psycopg2
import contextlib
from collections import defaultdict


def get_dashboard():
    with  psycopg2.connect("postgres://postgres:manzisql123.@localhost/galleryWebsite") as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("SET search_path TO public")
            stmt= "SELECT  e_id, g_id, id, c_id "
            stmt+="FROM exhibitions, paintings, painters, customers"
            query= sql.SQL(stmt)
            cursor.execute(query)
            records=defaultdict()
            data=cursor.fetchone()
            print(data)
            wanted=list(map(lambda values:len(values),data))
            # records["exhibitions"], records["paintings"], records["painters"], records["customers"]= wanted[0],wanted[1],wanted[2]
            
            # return records


if __name__=="__main__":
    get_dashboard()
