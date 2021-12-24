from locker.dto import *
from locker.mocks import MockLockerService
from kink import di, inject


def test_register_new_user():
    di.clear_cache()
    di.clear_cache()
    di["db_name"] = r"tests/test_database.db"
    di["_dbinit"] = "True"
    mock_service = MockLockerService()

    mock_service.setup()

    name_and_email_dto = UserNameAndEmailDTO("Samuel MS", "asetiawan02@students.calvin.ac.id")
    assert ["A001a", "Samuel MS", "asetiawan02@students.calvin.ac.id"] == mock_service.register_new_user(name_and_email_dto)

    user_info = mock_service.get_all_users()[0]

    assert ["A001a", "Samuel MS", "asetiawan02@students.calvin.ac.id"] == [user_info.user_id,
                                                                           user_info.name,
                                                                           user_info.email]

def test_register_already_registered_user():
    di.clear_cache()
    di.clear_cache()
    di["db_name"] = r"tests/test_database.db"
    di["_dbinit"] = "True"
    mock_service = MockLockerService()

    mock_service.setup()
    name_and_email_dto = UserNameAndEmailDTO("Samuel MS", "asetiawan02@students.calvin.ac.id")
    assert ["A001a", "Samuel MS", "asetiawan02@students.calvin.ac.id"] == mock_service.register_new_user(name_and_email_dto)

    new_name_and_email_dto = UserNameAndEmailDTO("Samuel MS", "asetiawan02@students.calvin.ac.id")
    assert -1 == mock_service.register_new_user(new_name_and_email_dto)

def test_remove_registered_user():
    di.clear_cache()
    di.clear_cache()
    di["db_name"] = r"tests/test_database.db"
    di["_dbinit"] = "True"
    mock_service = MockLockerService()

    mock_service.setup()
    name_and_email_dto = UserNameAndEmailDTO("Test Remove Registered User", "asetiawan02@students.calvin.ac.id")
    mock_service.register_new_user(name_and_email_dto)

    user_to_remove = UserNameAndEmailDTO("Test Remove Registered User", "asetiawan02@students.calvin.ac.id")
    mock_service.remove_user(user_to_remove)

    assert None == mock_service.get_all_users()

def test_remove_unregistered_user():
    di.clear_cache()
    di["db_name"] = r"tests/test_database.db"
    di["_dbinit"] = "True"
    mock_service = MockLockerService()

    mock_service.setup()

    name_and_email_dto = UserNameAndEmailDTO("Test Remove Unregistered User",
                                             "asetiawan02@students.calvin.ac.id")
    assert -1 == mock_service.remove_user(name_and_email_dto)

def test_pickup_package_with_valid_id_and_pin():
    di.clear_cache()
    di["db_name"] = r"tests/test_database.db"
    di["_dbinit"] = "True"
    mock_service = MockLockerService()

    mock_service.setup()

    name_and_email_dto = UserNameAndEmailDTO("test_pickup_package_with_valid_id_and_pin",
                                             "asetiawan02@students.calvin.ac.id")
    mock_service.register_new_user(name_and_email_dto)

    received_package_dto = ReceivedPackageFromUIDTO("A001a", "electronics",
                                                    "Medium", 2)
    mock_service.drop_package_in_locker(received_package_dto)

    pickup_package_dto = PickupPackageDTO("A001a", "Z1234z")
    mock_service.pickup_package_from_locker(pickup_package_dto)

    package_detail_info_from_repo = mock_service.locker_repository.get_all_packages_detail()[0]
    package_detail_info = [package_detail_info_from_repo.package_id,
                           package_detail_info_from_repo.arrived_time,
                           package_detail_info_from_repo.retrieved_time,
                           package_detail_info_from_repo.locker_no,
                           package_detail_info_from_repo.generated_pin]

    assert [1, "2021-12-14 9:30:00",
            "2021-12-15 09:30:00", 2, "Z1234z"] == package_detail_info

def test_pickup_package_with_invalid_id_or_password():
    di.clear_cache()
    di["db_name"] = r"tests/test_database.db"
    di["_dbinit"] = "True"
    mock_service = MockLockerService()

    mock_service.setup()
    name_and_email_dto = UserNameAndEmailDTO("test_pickup_package_with_invalid_id_or_password",
                                             "asetiawan02@students.calvin.ac.id")
    mock_service.register_new_user(name_and_email_dto)

    received_package_dto = ReceivedPackageFromUIDTO("A001a", "electronics",
                                                    "Medium", 2)
    mock_service.drop_package_in_locker(received_package_dto)

    # Invalid User ID AND Password
    pickup_package_dto1 = PickupPackageDTO("A002a", "A1234a")

    # Invalid User ID
    pickup_package_dto2 = PickupPackageDTO("A002a", "Z1234z")

    # Invalid Password
    pickup_package_dto3 = PickupPackageDTO("A001a", "A1234a")

    assert -1 == mock_service.pickup_package_from_locker(pickup_package_dto1)
    assert -1 == mock_service.pickup_package_from_locker(pickup_package_dto2)
    assert -1 == mock_service.pickup_package_from_locker(pickup_package_dto3)

def test_drop_package_with_registered_user_id():
    di.clear_cache()
    di["db_name"] = r"tests/test_database.db"
    di["_dbinit"] = "True"
    mock_service = MockLockerService()

    mock_service.setup()

    name_and_email_dto = UserNameAndEmailDTO("Samuel MS", "asetiawan02@students.calvin.ac.id")
    mock_service.register_new_user(name_and_email_dto)

    received_package_dto = ReceivedPackageFromUIDTO("A001a", "food_and_beverage", "Small", 4)
    assert ["Samuel MS", "asetiawan02@students.calvin.ac.id",
            4, "food_and_beverage", "Small", "2021-12-14 9:30:00",
            "Z1234z"] == mock_service.drop_package_in_locker(received_package_dto)

    package_from_repo = mock_service.locker_repository.get_all_packages()[0]
    package_info = [package_from_repo.package_id,
                    package_from_repo.item_type,
                    package_from_repo.item_size,
                    package_from_repo.user_id]

    package_detail_from_repo = mock_service.locker_repository.get_all_packages_detail()[0]
    package_detail_info = [package_detail_from_repo.package_id,
                           package_detail_from_repo.arrived_time,
                           package_detail_from_repo.retrieved_time,
                           package_detail_from_repo.locker_no,
                           package_detail_from_repo.generated_pin]

    assert [1, "food_and_beverage", "Small", "A001a"] == package_info
    assert [1, "2021-12-14 9:30:00", None, 4, "Z1234z"] == package_detail_info

def test_drop_package_with_unregistered_user_id():
    di.clear_cache()
    di["db_name"] = r"tests/test_database.db"
    di["_dbinit"] = "True"
    mock_service = MockLockerService()
    mock_service.setup()

    received_package_dto = ReceivedPackageFromUIDTO("A001a", "food_and_beverage", "Small", 4)

    assert -1 == mock_service.drop_package_in_locker(received_package_dto)