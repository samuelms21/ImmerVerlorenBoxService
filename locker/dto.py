class CompleteUserDTO:
    def __init__(self, _user_id, _name, _email):
        self.user_id = _user_id
        self.name = _name
        self.email = _email


class UserNameAndEmailDTO:
    def __init__(self, _name, _email):
        self.name = _name
        self.email = _email


class UserLoginDTO:
    def __init__(self, _post_box_no, _pin):
        self.post_box_no = _post_box_no
        self.pin = _pin


class OperatorLoginDTO:
    def __init__(self, _operator_id, _password):
        self.operator_id = _operator_id
        self.password = _password


class ReceivedPackageFromUIDTO:
    def __init__(self, _post_box_id, _item_type, _item_size, _locker_no):
        self.post_box_id = _post_box_id
        self.item_type = _item_type
        self.item_size = _item_size
        self.locker_no = _locker_no


class PackageDTO:
    def __init__(self, _package_id, _item_type, _item_size, _user_id):
        self.package_id = _package_id
        self.item_type = _item_type
        self.item_size = _item_size
        self.user_id = _user_id


class PackageDetailDTO:
    def __init__(self, _package_id, _arrived_time, _retrieved_time,
                 _locker_no, _generated_pin):
        self.package_id = _package_id
        self.arrived_time = _arrived_time
        self.retrieved_time = _retrieved_time
        self.locker_no = _locker_no
        self.generated_pin = _generated_pin


class OccupiedLockerDTO:
    def __init__(self, _name, _email, _locker_no):
        self.name = _name
        self.email = _email
        self.locker_no = _locker_no


class PickupPackageDTO:
    def __init__(self, _user_id, _pin):
        self.user_id = _user_id
        self.pin = _pin


class PickupPackageDetailDTO:
    def __init__(self, _pickup_time, _entered_pin):
        self.pickup_time = _pickup_time
        self.entered_pin = _entered_pin


class ItemTypeVSDurationDTO:
    def __init__(self, _item_type, _drop_time, _pickup_time):
        self.item_type = _item_type
        self.drop_time = _drop_time
        self.pickup_time = _pickup_time


class ItemSizeVSDurationDTO:
    def __init__(self, _item_size, _drop_time, _pickup_time):
        self.item_size = _item_size
        self.drop_time = _drop_time
        self.pickup_time = _pickup_time


class ItemTypeVsDurationReportDTO:
    def __init__(self, _electronics, _food_and_beverage, _clothing, _pharmacy):
        self.electronics = _electronics
        self.food_and_beverage = _food_and_beverage
        self.clothing = _clothing
        self.pharmacy = _pharmacy


class ItemSizeVSDurationReportDTO:
    def __init__(self, _large, _medium, _small):
        self.large = _large
        self.medium = _medium
        self.small = _small