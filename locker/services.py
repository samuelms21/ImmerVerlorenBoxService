import abc
from abc import abstractmethod
from datetime import datetime, timedelta
from .repositories import LockerRepository
from kink import inject, di
import random, string, smtplib, ssl
from .dto import *
from typing import List
from abc import abstractmethod
import matplotlib.pyplot as plt
import numpy as np
from pyfirmata import Arduino, util


class Message(abc.ABC):
    pass


class LockerMessage(Message):
    def __init__(self, _occupied_lockers, _service_email, _service_password):
        self.occupied_lockers = _occupied_lockers
        self.service_email = _service_email
        self.service_password = _service_password


class InvalidUserIDInputMessage(Message):
    def __init__(self, _user_id, _current_time, _operator_email, _service_email, _service_password):
        self.user_id = _user_id
        self.current_time = _current_time
        self.operator_email = _operator_email
        self.service_email = _service_email
        self.service_password = _service_password


class Observer(abc.ABC):
    @abstractmethod
    def update(self, _message: Message):
        pass


@inject
class LockerObserver(Observer):
    def update(self, _message: LockerMessage):
        pass

@inject
class InvalidInputObserver(Observer):
    def update(self, _message: InvalidUserIDInputMessage):
        pass

class Subject(abc.ABC):
    @abstractmethod
    def attach(self, _observer: Observer):
        pass

    @abstractmethod
    def detach(self, _observer: Observer):
        pass

    @abstractmethod
    def notify_update(self, _message: Message):
        pass


@inject
class LockerSubject(Subject):
    def __init__(self, _observers: List[LockerObserver]):
        self.__observers = _observers

    def attach(self, _observer: LockerObserver):
        self.__observers.append(_observer)

    def detach(self, _observer: LockerObserver):
        self.__observers.remove(_observer)

    def notify_update(self, _message: LockerMessage):
        for o in self.__observers:
            o.update(_message)


@inject
class UserIDInputSubject(Subject):
    def __init__(self, _observers: List[InvalidInputObserver]):
        self.__observers = _observers

    def attach(self, _observer: InvalidInputObserver):
        self.__observers.append(_observer)

    def detach(self, _observer: InvalidInputObserver):
        self.__observers.remove(_observer)

    def notify_update(self, _message: InvalidUserIDInputMessage):
        for o in self.__observers:
            o.update(_message)


@inject(alias=LockerObserver)
class LockersAlmostFullObserver(LockerObserver):
    def send_email_to_user(self, name, email, locker_no, service_email, service_password):
        port = 465
        smtp_server = "smtp.gmail.com"
        receiver_email = email
        sender_email = service_email
        password = service_password

        message = f'''
        Subject : Ambil paketmu sekarang, {name}!\n
        Kami ingin memberitahu bahwa barang Anda perlu diambil sekarang karena jumlah locker yang tersedia semakin
        sedikit. \n
        Silahkan mengambil barang Anda pada locker bernomor : {locker_no}\n
        Terima kasih sudah bekerja sama dengan kami.\n
        Salam, ImmerVerloren Box Service
        '''
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)


    def update(self, _message: LockerMessage):
        occupied_lockers = _message.occupied_lockers
        if len(occupied_lockers) < 3:
            # do nothing
            return
        elif len(occupied_lockers) == 3 and len(occupied_lockers) != 4:
            for occupied_locker in occupied_lockers:
                locker_no = occupied_locker.locker_no
                name = occupied_locker.name
                email = occupied_locker.email
                service_email = _message.service_email
                service_password = _message.service_password
                self.send_email_to_user(name, email, locker_no, service_email, service_password)


@inject(alias=LockerObserver)
class LockersAlreadyFullObserver(LockerObserver):
    def send_email_to_user(self, name, email, locker_no, service_email, service_password):
        port = 465
        smtp_server = "smtp.gmail.com"
        receiver_email = email
        sender_email = service_email
        password = service_password

        message = f'''
                Subject : Ambil paketmu sekarang, {name}!\n
                Kami ingin memberitahu bahwa barang Anda perlu diambil sekarang karena semua locker telah terisi,
                dan banyak pelanggan lain yang ingin menggunakan lockernya. \n
                Silahkan mengambil barang Anda pada locker bernomor : {locker_no}\n
                Terima kasih sudah bekerja sama dengan kami.\n
                Salam, ImmerVerloren Box Service
                '''
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

    def update(self, _message: LockerMessage):
        occupied_lockers = _message.occupied_lockers
        if len(occupied_lockers) < 4:
            # do nothing
            return
        elif len(occupied_lockers) == 4:
            for occupied_locker in occupied_lockers:
                locker_no = occupied_locker.locker_no
                name = occupied_locker.name
                email = occupied_locker.email
                service_email = _message.service_email
                service_password = _message.service_password
                self.send_email_to_user(name, email, locker_no, service_email, service_password)


@inject(alias=InvalidInputObserver)
class InvalidIDInputFiveTimesInFiveMinutesByCourierObserver(InvalidInputObserver):
    def __init__(self):
        self.obs_data = {}

    def send_email_to_operator(self, operator_email, service_email, service_password, user_id):
        port = 465
        smtp_server = "smtp.gmail.com"
        context = ssl.create_default_context()

        sender_email = service_email
        password = service_password

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            for email in operator_email:
                receiver_email = email
                message = f'''
                Subject : Kurir memasukkan ID yang salah sebanyak 5 kali dalam waktu 5 menit terakhir\n
                Kami ingin mengabari, bahwa seorang atau beberapa orang kurir telah memasukkan Post Box ID yang salah.
                Berikut adalah Post Box ID yang tidak ditemukan: {user_id}
                '''
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)


    def update(self, _message: InvalidUserIDInputMessage):
        if self.obs_data and _message.user_id in self.obs_data.keys():
            for key,value in self.obs_data.items():
                if key == _message.user_id:
                    self.obs_data[key].append(_message.current_time)
        elif self.obs_data and _message.user_id not in self.obs_data.keys():
            self.obs_data.update(
                {_message.user_id: [_message.current_time]}
            )
        else:
            self.obs_data.update(
                {_message.user_id: [_message.current_time]}
            )

        for key, value in self.obs_data.items():
            if len(self.obs_data[key]) >= 5:
                latest_timestamp = datetime.strptime(self.obs_data[key][-1], "%Y-%m-%d %H:%M:%S")
                earliest_timestamp = datetime.strptime(self.obs_data[key][-5], "%Y-%m-%d %H:%M:%S")
                five_minutes = timedelta(minutes=5)
                if earliest_timestamp >= (latest_timestamp - five_minutes):
                    self.send_email_to_operator(_message.operator_email, _message.service_email,
                                                _message.service_password, key)
                else:
                    pass


class Service(abc.ABC):
    pass


@inject
class ArduinoLocker:
    def __init__(self):
        self.board = Arduino("COM5")  #

        self.it = util.Iterator(self.board)  #
        self.it.start()  #

        self.servo9 = self.board.get_pin("d:9:s")  # BAWAH KIRI
        self.servo10 = self.board.get_pin("d:10:s")  # ATAS KIRI
        self.servo11 = self.board.get_pin("d:11:s")  # BAWAH KANAN
        self.servo12 = self.board.get_pin("d:12:s")  # ATAS KANAN

        self.servo10.write(90)
        self.servo11.write(90)


    def open_or_close_specific_locker(self, locker_no, open_or_close):
        while True:
            if locker_no == 1 and open_or_close is True:
                self.servo10.write(0)
                break
            elif locker_no == 1 and open_or_close is False:
                self.servo10.write(90)
                break
            elif locker_no == 2 and open_or_close is True:
                self.servo9.write(90)
                break
            elif locker_no == 2 and open_or_close is False:
                self.servo9.write(0)
                break
            elif locker_no == 3 and open_or_close is True:
                self.servo12.write(90)
                break
            elif locker_no == 3 and open_or_close is False:
                self.servo12.write(0)
                break
            elif locker_no == 4 and open_or_close is True:
                self.servo11.write(0)
                break
            elif locker_no == 4 and open_or_close is False:
                self.servo11.write(90)
                break

    def open_all_lockers(self):
        while True:
            self.servo9.write(90)
            self.servo10.write(0)
            self.servo11.write(0)
            self.servo12.write(90)
            break

    def close_all_lockers(self):
        while True:
            self.servo9.write(0)
            self.servo10.write(90)
            self.servo11.write(90)
            self.servo12.write(0)
            break


@inject
class LockerService(Service):
    def __init__(self, _locker_repository: LockerRepository, _locker_subject: LockerSubject,
                 _user_id_input_subject: UserIDInputSubject, _arduino_locker: ArduinoLocker):
        self.locker_repository = _locker_repository
        self.locker_subject = _locker_subject
        self.user_id_input_subject = _user_id_input_subject
        self.arduino_locker = _arduino_locker
        self.__service_email = "immerverlorentest@gmail.com"
        self.__password = "2t%27>Yy{xjJ"

    def setup(self):
        if self.locker_repository.setup() == 1:
            print("Invalid state.")
            quit()

    def operator_login(self, operator_login_dto):
        pass

    def operator_report(self):
        item_type_vs_duration_data = self.locker_repository.get_item_type_droptime_pickuptime()
        item_size_vs_duration_data = self.locker_repository.get_item_size_droptime_pickuptime()

        electronics_duration = []
        food_and_beverage_duration = []
        pharmacy_duration = []
        clothing_duration = []

        large_duration = []
        medium_duration = []
        small_duration = []

        if item_type_vs_duration_data and item_size_vs_duration_data:
            for data in item_type_vs_duration_data:
                drop_time = datetime.strptime(data.drop_time, "%Y-%m-%d %H:%M:%S")
                pickup_time = datetime.strptime(data.pickup_time, "%Y-%m-%d %H:%M:%S")
                duration = (pickup_time - drop_time).total_seconds() // 60

                if data.item_type == 'electronics':
                    electronics_duration.append(duration)
                elif data.item_type == 'food_and_beverage':
                    food_and_beverage_duration.append(duration)
                elif data.item_type == 'clothing':
                    clothing_duration.append(duration)
                elif data.item_type == 'pharmacy':
                    pharmacy_duration.append(duration)

            for data in item_size_vs_duration_data:
                drop_time = datetime.strptime(data.drop_time, "%Y-%m-%d %H:%M:%S")
                pickup_time = datetime.strptime(data.pickup_time, "%Y-%m-%d %H:%M:%S")
                duration = (pickup_time - drop_time).total_seconds() // 60

                if data.item_size == 'Large':
                    large_duration.append(duration)
                elif data.item_size == 'Medium':
                    medium_duration.append(duration)
                elif data.item_size == 'Small':
                    small_duration.append(duration)

        else:
            return -1

        electronics_x = sorted(list(set(electronics_duration)))
        electronics_y = list(np.unique(electronics_duration, return_counts=True))[1]

        food_and_beverage_x = sorted(list(set(food_and_beverage_duration)))
        food_and_beverage_y = list(np.unique(food_and_beverage_duration, return_counts=True))[1]

        clothing_x = sorted(list(set(clothing_duration)))
        clothing_y = list(np.unique(clothing_duration, return_counts=True))[1]

        pharmacy_x = sorted(list(set(pharmacy_duration)))
        pharmacy_y = list(np.unique(pharmacy_duration, return_counts=True))[1]

        large_x = sorted(list(set(large_duration)))
        large_y = list(np.unique(large_duration, return_counts=True))[1]

        medium_x = sorted(list(set(medium_duration)))
        medium_y = list(np.unique(medium_duration, return_counts=True))[1]

        small_x = sorted(list(set(small_duration)))
        small_y = list(np.unique(small_duration, return_counts=True))[1]

        item_type_vs_duration_report_dto = ItemTypeVsDurationReportDTO(
            [electronics_x, electronics_y], [food_and_beverage_x, food_and_beverage_y],
            [clothing_x, clothing_y], [pharmacy_x, pharmacy_y]
        )

        item_size_vs_duration_report_dto = ItemSizeVSDurationReportDTO(
            [large_x, large_y], [medium_x, medium_y], [small_x, small_y]
        )
        return item_type_vs_duration_report_dto, item_size_vs_duration_report_dto

    def send_confirmation_email(self, user_id, name, email):
        port = 465
        password = self.__password

        sender_email = self.__service_email
        receiver_email = email
        message = f"""\n
            Subject: Pendaftaran Akun ImmerVerloren Box Service\n
            Pendaftaran akun Anda berhasil, {name}!
            
            Berikut adalah alamat pengiriman Anda:\n
            UserID : {user_id}\n
            Calvin Institute of Technology\n
            Calvin Tower RMCI Jl. Industri Blok B14, RW.10, East Pademangan, Kemayoran,\n
            Central Jakarta City, Jakarta 10610
            """

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("immerverlorentest@gmail.com", password)
            server.sendmail(sender_email, receiver_email, message)

    def register_new_user(self, name_and_email_dto):
        registered_users = self.get_all_users()
        name = name_and_email_dto.name
        email = name_and_email_dto.email

        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase

        if not registered_users:
            cap_letter = random.sample(uppercase_letters, 1)[0]
            low_letter = random.sample(lowercase_letters, 1)[0]
            three_digit_number = str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9))

            new_user_id = cap_letter + three_digit_number + low_letter

            new_user_dto = CompleteUserDTO(new_user_id, name, email)
            self.locker_repository.register_new_user(new_user_dto)
            self.send_confirmation_email(new_user_id, name, email)
        else:
            for user in registered_users:
                if name == user.name or email == user.email:
                    return -1

            cap_letter = random.sample(uppercase_letters, 1)[0]
            low_letter = random.sample(lowercase_letters, 1)[0]
            three_digit_number = str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9))

            new_user_id = cap_letter + three_digit_number + low_letter

            while new_user_id in [user.user_id for user in self.get_all_users()]:
                cap_letter = random.sample(uppercase_letters, 1)[0]
                low_letter = random.sample(lowercase_letters, 1)[0]
                three_digit_number = str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9))

                new_user_id = cap_letter + three_digit_number + low_letter

            new_user_dto = CompleteUserDTO(new_user_id, name, email)
            self.locker_repository.register_new_user(new_user_dto)
            self.send_confirmation_email(new_user_id, name, email)

    def remove_user(self, name_and_email_dto):
        if self.get_all_users():
            current_user_names = [user.name for user in self.get_all_users()]
            current_user_emails = [user.email for user in self.get_all_users()]

            name = name_and_email_dto.name
            email = name_and_email_dto.email

            user_is_found = False
            for i in range(len(self.get_all_users())):
                if name == current_user_names[i] and email == current_user_emails[i]:
                    user_is_found = True
                    name_and_email_dto_for_repo = UserNameAndEmailDTO(name, email)
                    self.locker_repository.remove_specific_user(name_and_email_dto_for_repo)
                    break

            if user_is_found:
                return
            else:
                return -1
        else:
            return -1

    def get_all_users(self):
        return self.locker_repository.get_all_users()

    def drop_package_in_locker(self, received_package_dto):
        post_box_no = received_package_dto.post_box_id
        item_type = received_package_dto.item_type
        item_size = received_package_dto.item_size
        locker_no = received_package_dto.locker_no

        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase

        if self.get_all_users():
            all_user_ids = [user.user_id for user in self.get_all_users()]

            if post_box_no in all_user_ids:
                # If the post box no/ post box id typed in by the courier is not a member
                # of the currently registered users, proceed to create a new package_id
                # for the package
                if self.locker_repository.get_all_packages():
                    # If the table packages is not empty
                    # take the last package_id and increment it by 1
                    # use it as the new package id
                    all_package_ids = [package.package_id for package in self.locker_repository.get_all_packages()]
                    new_package_id = all_package_ids[-1] + 1
                else:
                    # If the table packages is empty, which means no packages has been delivered
                    # to the lockers yet, simply start it from 1, as the new package_id
                    new_package_id = 1

                # The new package id will be saved in the variable new_package_id
                # new_package_id will be used soon to update the database

                # Check if locker_no is None or not, if it is, then it means
                # that all lockers are occupied, therefore, no need to generate a pin for the user to open
                # the locker
                if locker_no:
                    # Start to generate a new pin for the locker
                    random_cap_letter = random.sample(uppercase_letters, 1)[0]
                    random_low_letter = random.sample(lowercase_letters, 1)[0]
                    four_ints = str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(
                        random.randint(1, 9)) + str(random.randint(1, 9))

                    generated_pin = random_cap_letter + four_ints + random_low_letter

                    if self.locker_repository.get_all_packages_detail():
                    # if the table packages_detail is not empty
                    # generate a unique pin for the new package
                    # and check if the pin has been used for previous packages and lockers
                        all_generated_pins = [package.generated_pin for package in self.locker_repository.get_all_packages_detail()]
                        while generated_pin in all_generated_pins:
                            random_cap_letter = random.sample(uppercase_letters, 1)[0]
                            random_low_letter = random.sample(lowercase_letters, 1)[0]
                            four_ints = str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(
                                random.randint(1, 9)) + str(random.randint(1, 9))

                            generated_pin = random_cap_letter + four_ints + random_low_letter
                else:
                    # locker_no is None, therefore, dont need to generate a pin
                    generated_pin = None

                for user in self.get_all_users():
                    if user.user_id == post_box_no:
                        email = user.email
                        name = user.name
                        break

                # Proceed to update packages and packages_detail in the database
                now = datetime.now()
                current_time = str(datetime.strftime(now, "%Y-%m-%d %H:%M:%S"))
                package_dto = PackageDTO(new_package_id, item_type, item_size, post_box_no)
                package_detail_dto = PackageDetailDTO(new_package_id, current_time, None, locker_no, generated_pin)
                self.locker_repository.update_packages(package_dto)
                self.locker_repository.update_packages_detail(package_detail_dto)
                self.send_package_notification_email(name, email, locker_no, item_type, item_size, current_time,
                                                generated_pin)

                self.arduino_locker.open_or_close_specific_locker(locker_no, False)

                occupied_locker_dtos = self.locker_repository.get_all_occupied_lockers_details()
                locker_message = LockerMessage(occupied_locker_dtos, self.__service_email, self.__password)
                self.locker_subject.notify_update(locker_message)
            else:
                # If the post box no/ post box id typed in by the courier does not exist
                # within the current users inside the database, return -1 to UI
                # as a flag to show an Error such as "User does not exist"
                current_time = str(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
                operator_email = self.locker_repository.get_all_operator_emails()
                failed_login_message = InvalidUserIDInputMessage(post_box_no, current_time,
                                                                 operator_email, self.__service_email,
                                                                 self.__password)
                self.user_id_input_subject.notify_update(failed_login_message)
                return -1
        else:
            current_time = str(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
            operator_email = self.locker_repository.get_all_operator_emails()
            failed_login_message = InvalidUserIDInputMessage(post_box_no, current_time,
                                                                 operator_email, self.__service_email,
                                                                 self.__password)
            self.user_id_input_subject.notify_update(failed_login_message)
            return -1

    def pickup_package_from_locker(self, pickup_package_dto):
        user_id = pickup_package_dto.user_id
        pin = pickup_package_dto.pin

        if self.get_all_users():
            if user_id in [user.user_id for user in self.get_all_users()]:
                if pin:
                    all_generated_pins = [x[0] for x in self.locker_repository.get_all_generated_pins()]
                    if pin in all_generated_pins:
                        pickup_time = str(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
                        pickup_package_detail_dto = PickupPackageDetailDTO(pickup_time, pin)
                        locker_to_be_opened = self.locker_repository.get_locker_number_based_on_user_id_and_pin(pickup_package_dto)
                        self.arduino_locker.open_or_close_specific_locker(locker_to_be_opened[0], True)
                        self.locker_repository.update_pickup_packages_detail(pickup_package_detail_dto)
                        # locker_to_be_opened = [x[0] for x in self.locker_repository.get_locker_number_based_on_user_id_and_pin(pickup_package_dto)]
                        # self.arduino_locker.open_or_close_specific_locker(locker_to_be_opened[0], True)
                    else:
                        # Invalid PIN
                        return -1
                else:
                    # Check if the user has any packages delivered for them
                    # If he/she does have packages waiting, tell UI to display
                    # a window
                    current_user_ids_whose_packages_in_locker = self.locker_repository.get_all_current_packages_in_locker()
                    current_user_ids_whose_packages_not_in_locker = self.locker_repository.get_all_current_packages_not_in_locker()
                    if user_id in current_user_ids_whose_packages_not_in_locker:
                        pickup_time = str(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
                        pickup_package_detail_dto = PickupPackageDetailDTO(pickup_time, None)
                        self.locker_repository.update_pickup_packages_detail(pickup_package_detail_dto)
                        return -2 # Means that the user_id has one or more packages, but not stored in lockers
                                  # The user would need to visit the nearest security office
                    elif user_id in current_user_ids_whose_packages_in_locker:
                        # Tells UI to remind the user that he/she has packages waiting
                        # and tell he/she to enter the required PIN
                        return -4
                    else:
                        # The user currently does not have any packages delivered
                        # for them, return -3 to remind UI to show
                        # a notification window that the user does not have any packages stored currently
                        return -3
            else:
                # User id does not exist
                return -1
        else:
            # There are no registered users yet
            return -1

    def send_package_notification_email(self, name, email, locker_no, item_type, item_size, arrived_time, generated_pin):
        port = 465
        smtp_server = "smtp.gmail.com"
        sender_email = self.__service_email
        receiver_email = email
        password = self.__password

        if generated_pin is None:
            message = f'''\n
            Subject : Paket Anda sudah datang, {name}!\n
            Informasi mengenai paket Anda:\n
            \t\tLocker No   : {locker_no}
            \t\tItem type   : {item_type}
            \t\tItem size   : {item_size}
            \t\tArrival time: {arrived_time}
            Karena locker yang tersedia penuh, Anda bisa mengambil paket Anda di pos security.\n
            Terima kasih sudah menggunakan layanan kami.\n
            ImmerVerloren Box Service'''
        else:
            message = f'''\n
            Subject : Paket Anda sudah datang, {name}!\n
            Informasi mengenai paket Anda:\n
            \t\tLocker No   : {locker_no}
            \t\tItem type   : {item_type}
            \t\tItem size   : {item_size}
            \t\tArrival time: {arrived_time}
            \t\tPIN         : {generated_pin}\n
            Ambil paket Anda menggunakan PIN yang kami berikan.
            Terima kasih sudah menggunakan layanan kami\n.
            
            ImmerVerloren Box Services
            '''

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

    def get_all_occupied_lockers(self):
        return self.locker_repository.get_all_occupied_lockers()
