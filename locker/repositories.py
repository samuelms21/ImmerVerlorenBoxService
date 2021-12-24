import sqlite3
from sqlite3 import Error
from kink import inject, di
from .dto import *


@inject
class LockerRepository:
    def __init__(self, db_name, _dbinit):
        self.database_name = db_name
        self.dbinit = _dbinit
        self.conn, self.cursor = self.connect_to_database_file()

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            return conn
        except Error as e:
            print(e)

        return conn

    def connect_to_database_file(self):
        conn = self.create_connection()
        if conn is not None:
            c = conn.cursor()
            return conn, c

    def setup(self):
        conn = self.conn
        cursor = self.cursor
        if self.dbinit.capitalize() == "True":
            self.drop_occupied_lockers_details_view()
            self.drop_users_table()
            self.drop_packages_table()
            self.drop_packages_detail_table()
            self.drop_operators_table()

            sql_create_users_table = '''
            CREATE TABLE users (
            user_id     TEXT NOT NULL,
            name        TEXT NOT NULL,
            email       TEXT NOT NULL,
            PRIMARY KEY(user_id));
            '''
            sql_create_packages_table = '''
            CREATE TABLE packages (
            package_id	INTEGER NOT NULL,
            item_type	TEXT NOT NULL,
            item_size	TEXT NOT NULL,
            user_id		INTEGER NOT NULL,
            PRIMARY KEY(package_id));
            '''
            sql_create_packages_detail_table = '''
            CREATE TABLE packages_detail (
            package_id	    INTEGER NOT NULL,
            arrived_time	TEXT NOT NULL,
            retrieved_time	TEXT,
            locker_no	    INTEGER,
            generated_pin	TEXT,
            PRIMARY KEY(package_id));
            '''
            sql_create_occupied_lockers_details = '''
            CREATE VIEW occupied_lockers_details
                     AS
                 SELECT users.name,
                        users.email,
                        packages_detail.locker_no
                   FROM packages
             INNER JOIN packages_detail
                     ON packages.package_id=packages_detail.package_id
             INNER JOIN users
                     ON packages.user_id=users.user_id
                  WHERE packages_detail.retrieved_time IS NULL
                    AND packages_detail.locker_No IS NOT NULL
            '''
            sql_create_operators_table = '''
            CREATE TABLE operators (
            operator_id     TEXT NOT NULL,
            email           TEXT NOT NULL,
            password        TEXT NOT NULL,
            PRIMARY KEY(operator_id)
            );
            '''
            sql_insert_operator_1 = '''
            INSERT
              INTO operators(operator_id,email,password)
            VALUES("OP_1","jsuriono62@students.calvin.ac.id","op1boxservice")
            '''
            sql_insert_operator_2 = '''
            INSERT
              INTO operators(operator_id,email,password)
            VALUES("OP_2","asetiawan02@students.calvin.ac.id","op2boxservice")
            '''
            cursor.execute(sql_create_users_table)
            cursor.execute(sql_create_packages_table)
            cursor.execute(sql_create_packages_detail_table)
            cursor.execute(sql_create_occupied_lockers_details)
            cursor.execute(sql_create_operators_table)
            cursor.execute(sql_insert_operator_1)
            cursor.execute(sql_insert_operator_2)
            conn.commit()
        elif self.dbinit.capitalize() == "False":
            pass
        elif self.dbinit.capitalize() == "Demo":
            self.drop_occupied_lockers_details_view()
            self.drop_users_table()
            self.drop_packages_table()
            self.drop_packages_detail_table()

            sql_create_users_table = '''
            CREATE TABLE users (
            user_id     TEXT NOT NULL,
            name        TEXT NOT NULL,
            email       TEXT NOT NULL,
            PRIMARY KEY(user_id));
            '''
            sql_create_packages_table = '''
            CREATE TABLE packages (
            package_id	INTEGER NOT NULL,
            item_type	TEXT NOT NULL,
            item_size	TEXT NOT NULL,
            user_id		INTEGER NOT NULL,
            PRIMARY KEY(package_id));
            '''
            sql_create_packages_detail_table = '''
            CREATE TABLE packages_detail (
            package_id	    INTEGER NOT NULL,
            arrived_time	TEXT NOT NULL,
            retrieved_time	TEXT,
            locker_no	    INTEGER,
            generated_pin	TEXT,
            PRIMARY KEY(package_id));
            '''
            sql_create_occupied_lockers_details = '''
            CREATE VIEW occupied_lockers_details
                     AS
                 SELECT users.name,
                        users.email,
                        packages_detail.locker_no
                   FROM packages
             INNER JOIN packages_detail
                     ON packages.package_id=packages_detail.package_id
             INNER JOIN users
                     ON packages.user_id=users.user_id
                  WHERE packages_detail.retrieved_time IS NULL
                    AND packages_detail.locker_No IS NOT NULL
            '''

            cursor.execute(sql_create_users_table)
            cursor.execute(sql_create_packages_table)
            cursor.execute(sql_create_packages_detail_table)
            cursor.execute(sql_create_occupied_lockers_details)

            demo_file = open('locker/demo_data.txt', 'r')
            for row in demo_file:
                cursor.execute(row)
            self.conn.commit()
        else:
            return -1

    def register_new_user(self, user_dto):
        conn = self.conn
        cursor = self.cursor

        sql_register_new_user = '''
        INSERT
          INTO users(user_id,name,email)
        VALUES(?,?,?);
        '''
        user_id = user_dto.user_id
        name = user_dto.name
        email = user_dto.email

        cursor.execute(sql_register_new_user, (
            user_id, name, email
        ))
        conn.commit()

    def get_all_users(self):
        sql_get_all_users= '''
        SELECT *
          FROM users
        '''
        self.cursor.execute(sql_get_all_users)
        rows = self.cursor.fetchall()

        list_of_user_dtos = []

        if rows:
            for row in rows:
                user_dto = CompleteUserDTO(row[0], row[1], row[2])
                list_of_user_dtos.append(user_dto)
            return list_of_user_dtos
        else:
            return

    def remove_specific_user(self, name_and_email_dto):
        conn = self.conn
        cursor = self.cursor

        sql_remove_specific_user = '''
        DELETE
          FROM users
         WHERE name=?
           AND email=?
        '''
        cursor.execute(sql_remove_specific_user, (name_and_email_dto.name,
                                                  name_and_email_dto.email,))
        conn.commit()

    def drop_users_table(self):
        conn = self.conn
        cursor = self.cursor
        sql_drop_users_table = '''
        DROP TABLE IF EXISTS users
        '''
        cursor.execute(sql_drop_users_table)
        conn.commit()

    def drop_packages_table(self):
        conn = self.conn
        cursor = self.cursor
        sql_drop_packages_table = '''
        DROP TABLE IF EXISTS packages
        '''
        cursor.execute(sql_drop_packages_table)
        conn.commit()

    def drop_packages_detail_table(self):
        conn = self.conn
        cursor = self.cursor
        sql_drop_packages_detail_table = '''
        DROP TABLE IF EXISTS packages_detail
        '''
        cursor.execute(sql_drop_packages_detail_table)
        conn.commit()

    def drop_occupied_lockers_details_view(self):
        conn = self.conn
        cursor = self.cursor

        sql_drop_occupied_lockers_details_view = '''
        DROP VIEW 
        IF EXISTS occupied_lockers_details
        '''
        cursor.execute(sql_drop_occupied_lockers_details_view)
        conn.commit()

    def drop_operators_table(self):
        conn = self.conn
        cursor = self.cursor
        sql_drop_operators_table = '''
        DROP TABLE IF EXISTS operators
        '''
        cursor.execute(sql_drop_operators_table)
        conn.commit()

    def get_all_packages(self):
        cursor = self.cursor
        sql_get_all_packages = '''
        SELECT *
        FROM packages
        '''
        cursor.execute(sql_get_all_packages)
        rows = cursor.fetchall()

        list_of_package_id_dtos = []

        if rows:
            for row in rows:
                package_id_dto = PackageDTO(row[0], row[1], row[2], row[3])
                list_of_package_id_dtos.append(package_id_dto)
            return list_of_package_id_dtos
        else:
            return

    def get_all_packages_detail(self):
        cursor = self.cursor
        sql_get_all_packages_detail = '''
        SELECT *
        FROM packages_detail
        '''
        cursor.execute(sql_get_all_packages_detail)
        rows = cursor.fetchall()

        list_of_package_detail_dtos = []
        if rows:
            for row in rows:
                package_detail_dto = PackageDetailDTO(row[0], row[1],
                                                      row[2], row[3], row[4])
                list_of_package_detail_dtos.append(package_detail_dto)
            return list_of_package_detail_dtos
        else:
            return

    def update_packages(self, package_dto):
        conn = self.conn
        cursor = self.cursor
        sql_update_packages = '''
        INSERT
          INTO packages(package_id,item_type,item_size,user_id)
        VALUES(?,?,?,?)
        '''
        package_id = package_dto.package_id
        item_type = package_dto.item_type
        item_size = package_dto.item_size
        user_id = package_dto.user_id

        cursor.execute(sql_update_packages, (package_id, item_type, item_size, user_id,))
        conn.commit()

    def update_packages_detail(self, package_detail_dto):
        conn = self.conn
        cursor = self.cursor
        sql_update_packages_detail = '''
        INSERT
        INTO packages_detail(package_id,arrived_time,retrieved_time,locker_no,generated_pin)
        VALUES(?,?,NULL,?,?)
        '''
        cursor.execute(sql_update_packages_detail,
                       (package_detail_dto.package_id,
                        package_detail_dto.arrived_time,
                        package_detail_dto.locker_no,
                        package_detail_dto.generated_pin,))
        conn.commit()

    def update_pickup_packages_detail(self, pickup_package_detail_dto):
        cursor = self.cursor
        conn = self.conn
        sql_update_packages_detail_retrieved_time_based_on_pin = '''
        UPDATE packages_detail
           SET retrieved_time=?
         WHERE generated_pin=?
        '''
        pickup_time = pickup_package_detail_dto.pickup_time
        entered_pin = pickup_package_detail_dto.entered_pin
        cursor.execute(sql_update_packages_detail_retrieved_time_based_on_pin,
                       (pickup_time, entered_pin,))
        conn.commit()

    def get_all_occupied_lockers(self):
        cursor = self.cursor
        sql_get_all_occupied_lockers = '''
        SELECT locker_no
        FROM packages_detail
        WHERE locker_no IS NOT NULL
        AND retrieved_time IS NULL
        AND generated_pin IS NOT NULL
        '''
        cursor.execute(sql_get_all_occupied_lockers)
        rows = cursor.fetchall()

        return rows

    def get_all_occupied_lockers_details(self):
        cursor = self.cursor
        sql_get_all_occupied_lockers_details = '''
        SELECT * from occupied_lockers_details
        '''
        cursor.execute(sql_get_all_occupied_lockers_details)
        rows = cursor.fetchall()

        list_of_occupied_locker_dtos = []
        if rows:
            for row in rows:
                occupied_locker_dto = OccupiedLockerDTO(row[0], row[1], row[2])
                list_of_occupied_locker_dtos.append(occupied_locker_dto)
            return list_of_occupied_locker_dtos
        else:
            return []

    def get_all_generated_pins(self):
        cursor = self.cursor
        sql_get_all_generated_pins = '''
        SELECT generated_pin
          FROM packages_detail
         WHERE generated_pin IS NOT NULL
           AND locker_no IS NOT NULL
           AND retrieved_time IS NULL
        '''
        cursor.execute(sql_get_all_generated_pins)
        rows = cursor.fetchall()
        return rows

    def get_all_current_packages_not_in_locker(self):
        cursor = self.cursor
        sql_get_all_current_packages_not_in_locker = '''
            SELECT packages.user_id
              FROM packages
        INNER JOIN packages_detail
                ON packages.package_id=packages_detail.package_id
             WHERE packages_detail.retrieved_time IS NULL
               AND locker_no IS NULL 
               AND generated_pin IS NULL
        '''
        cursor.execute(sql_get_all_current_packages_not_in_locker)
        rows = cursor.fetchall()

        return [x[0] for x in rows]

    def get_all_current_packages_in_locker(self):
        cursor = self.cursor
        sql_get_all_current_packages_in_locker = '''
            SELECT packages.user_id
              FROM packages
        INNER JOIN packages_detail
                ON packages.package_id=packages_detail.package_id
             WHERE packages_detail.retrieved_time IS NULL
               AND locker_no IS NOT NULL 
               AND generated_pin IS NOT NULL
        '''
        cursor.execute(sql_get_all_current_packages_in_locker)
        rows = cursor.fetchall()

        return [x[0] for x in rows]

    def get_all_operator_emails(self):
        cursor = self.cursor
        sql_get_all_operator_emails = '''
        SELECT email
        FROM operators
        '''
        cursor.execute(sql_get_all_operator_emails)
        rows = cursor.fetchall()

        return [x[0] for x in rows]

    def get_locker_number_based_on_user_id_and_pin(self, pickup_package_dto):
        cursor = self.cursor
        sql_get_locker_number_based_on_user_id_and_pin = '''
            SELECT locker_no
              FROM packages
        INNER JOIN packages_detail
                ON packages.package_id=packages_detail.package_id
             WHERE packages_detail.retrieved_time IS NULL
               AND packages.user_id=?
               AND packages_detail.generated_pin=?       
        '''
        cursor.execute(sql_get_locker_number_based_on_user_id_and_pin,
                       (pickup_package_dto.user_id, pickup_package_dto.pin,))
        rows = cursor.fetchall()
        return [x[0] for x in rows]

    # Grafik Jenis Barang per waktu tunggu
    def get_item_type_droptime_pickuptime(self):
        cursor = self.cursor
        sql_get_item_type_droptime_pickuptime = '''
        SELECT packages.item_type,
        packages_detail.arrived_time,
        packages_detail.retrieved_time
        FROM packages
        INNER JOIN packages_detail
        ON packages.package_id=packages_detail.package_id
        '''
        cursor.execute(sql_get_item_type_droptime_pickuptime)
        rows = cursor.fetchall()

        list_of_itemtype_vs_duration_dtos = []
        if rows:
            for row in rows:
                itemtype_vs_duration_dto = ItemTypeVSDurationDTO(
                    row[0], row[1], row[2]
                )
                list_of_itemtype_vs_duration_dtos.append(itemtype_vs_duration_dto)
            return list_of_itemtype_vs_duration_dtos
        else:
            return

    # Grafik Ukuran Barang per waktu tunggu
    def get_item_size_droptime_pickuptime(self):
        cursor = self.cursor
        sql_get_item_size_droptime_pickuptime = '''
        SELECT packages.item_size,
        packages_detail.arrived_time,
        packages_detail.retrieved_time
        FROM packages
        INNER JOIN packages_detail
        ON packages.package_id=packages_detail.package_id
        '''
        cursor.execute(sql_get_item_size_droptime_pickuptime)
        rows = cursor.fetchall()

        list_of_itemsize_vs_duration_dtos = []
        if rows:
            for row in rows:
                itemsize_vs_duration_dto = ItemSizeVSDurationDTO(
                    row[0], row[1], row[2]
                )
                list_of_itemsize_vs_duration_dtos.append(itemsize_vs_duration_dto)
            return list_of_itemsize_vs_duration_dtos
        else:
            return
