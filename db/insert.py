import pymysql.cursors
from time import sleep

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='belajar_database',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
print(connection)
def kirimData(user_id,ecg_data):
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `ekg_datas` (`id`, `user_id`, `ecg_data`, `created_at`) VALUES (NULL, '1', '25', current_timestamp())"
            cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    except:
        print("error gan")

    # finally:
    #     connection.close()