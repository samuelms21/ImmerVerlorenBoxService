from locker.services import *
from locker.repositories import LockerRepository
import string
from locker.dto import *
from kink import inject, di


@inject
class MockLockerService(Service):
    def __init__(self, _locker_repository: LockerRepository, _locker_subject: LockerSubject,
                 _user_id_input_subject: UserIDInputSubject):
        self.locker_repository = _locker_repository
        self.locker_subject = _locker_subject
        self.user_id_input_subject = _user_id_input_subject
        self.__service_email = "immerverlorentest@gmail.com"
        self.__password = "2t%27>Yy{xjJ"
        self.operator_email = self.locker_repository.get_all_operator_emails()

    def setup(self):
        self.locker_repository.setup()

    def operator_login(self, operator_login_dto):
        pass

    def operator_report(self):
        pass

    def send_confirmation_email(self, user_id, name, email):
        return [user_id, name, email]

    def register_new_user(self, name_and_email_dto):
        registered_users = self.get_all_users()
        name = name_and_email_dto.name
        email = name_and_email_dto.email

        if not registered_users:
            new_user_id = "A001a"

            new_user_dto = CompleteUserDTO(new_user_id, name, email)
            self.locker_repository.register_new_user(new_user_dto)
            return self.send_confirmation_email(new_user_id, name, email)
        else:
            for user in registered_users:
                if name == user.name or email == user.email:
                    return -1

            new_user_id = "A001a"

            new_user_dto = CompleteUserDTO(new_user_id, name, email)
            self.locker_repository.register_new_user(new_user_dto)
            return self.send_confirmation_email(new_user_id, name, email)

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

        if self.get_all_users():
            all_user_ids = [user.user_id for user in self.get_all_users()]

            if post_box_no in all_user_ids:
                if self.locker_repository.get_all_packages():
                    all_package_ids = [package.package_id for package in self.locker_repository.get_all_packages()]
                    new_package_id = all_package_ids[-1] + 1
                else:
                    new_package_id = 1

                if locker_no:
                    generated_pin = "Z1234z"

                    if self.locker_repository.get_all_packages_detail():
                        generated_pin = "Z1234z"
                else:
                    generated_pin = None

                for user in self.get_all_users():
                    if user.user_id == post_box_no:
                        email = user.email
                        name = user.name
                        break

                current_time = "2021-12-14 9:30:00"
                package_dto = PackageDTO(new_package_id, item_type, item_size, post_box_no)
                package_detail_dto = PackageDetailDTO(new_package_id, current_time, None, locker_no, generated_pin)
                self.locker_repository.update_packages(package_dto)
                self.locker_repository.update_packages_detail(package_detail_dto)
                return self.send_package_notification_email(name, email, locker_no, item_type, item_size, current_time,
                                                            generated_pin)
            else:
                return -1
        else:
            return -1

    def pickup_package_from_locker(self, pickup_package_dto):
        user_id = pickup_package_dto.user_id
        pin = pickup_package_dto.pin

        if self.get_all_users():
            if user_id in [user.user_id for user in self.get_all_users()]:
                if pin:
                    all_generated_pins = [x[0] for x in self.locker_repository.get_all_generated_pins()]
                    if pin in all_generated_pins:
                        pickup_time = "2021-12-15 09:30:00"
                        pickup_package_detail_dto = PickupPackageDetailDTO(pickup_time, pin)
                        self.locker_repository.update_pickup_packages_detail(pickup_package_detail_dto)
                    else:
                        # Invalid PIN
                        return -1
                else:
                    return -2
            else:
                # User id does not exist
                return -1
        else:
            # There are no registered users yet
            return -1

    def send_package_notification_email(self, name, email, locker_no, item_type, item_size, arrived_time,
                                        generated_pin):
        return [name, email, locker_no, item_type, item_size, arrived_time, generated_pin]

    def get_all_occupied_lockers(self):
        return self.locker_repository.get_all_occupied_lockers()
