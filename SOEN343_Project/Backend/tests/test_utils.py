from dbconnection import db
from models.logistics.delivery_request import DeliveryRequest
from models.logistics.package import Package, FragilePackage
from models.customer_interaction.address import Address
from models.customer_interaction.package_item import PackageItem

# Default values for Address
DEFAULT_ADDRESS = {
    "street": "123 Default St",
    "house_number": "1",
    "apartment_number": "A1",
    "postal_code": "00000",
    "city": "Default City",
    "country": "Default Country",
}

# Default values for Package
DEFAULT_PACKAGE = {
    "unit_system": "metric",
    "width": 10,
    "length": 10,
    "height": 10,
    "weight": 5,
    "is_fragile": False,
    "package_items": [
        {"item_description": "Default Item", "quantity": 1, "weight": 1.0}
    ],
}

# Default values for DeliveryRequest
DEFAULT_DELIVERY_REQUEST = {
    "customer_id": 1,
    "status": "Pending",
}


def create_address(
    street=None, house_number=None, apartment_number=None, postal_code=None, city=None, country=None
):
    """Create and persist an Address object with optional overrides."""
    address = Address(
        street=street or DEFAULT_ADDRESS["street"],
        house_number=house_number or DEFAULT_ADDRESS["house_number"],
        apartment_number=apartment_number or DEFAULT_ADDRESS["apartment_number"],
        postal_code=postal_code or DEFAULT_ADDRESS["postal_code"],
        city=city or DEFAULT_ADDRESS["city"],
        country=country or DEFAULT_ADDRESS["country"],
    )
    db.session.add(address)
    db.session.commit()
    return address


def create_package(
    unit_system=None,
    width=None,
    length=None,
    height=None,
    weight=None,
    is_fragile=None,
    package_items=None,
):
    """Create and persist a Package or FragilePackage object with optional overrides."""
    package = FragilePackage() if (
        is_fragile or DEFAULT_PACKAGE["is_fragile"]) else Package()
    package.width = width or DEFAULT_PACKAGE["width"]
    package.length = length or DEFAULT_PACKAGE["length"]
    package.height = height or DEFAULT_PACKAGE["height"]
    package.weight = weight or DEFAULT_PACKAGE["weight"]
    package.unit_system = unit_system or DEFAULT_PACKAGE["unit_system"]

    db.session.add(package)
    db.session.commit()

    # Add package items if provided or use defaults
    items = package_items or DEFAULT_PACKAGE["package_items"]
    for item_data in items:
        package_item = PackageItem(
            package_id=package.id,
            item_description=item_data["item_description"],
            quantity=item_data["quantity"],
            weight=item_data["weight"],
        )
        db.session.add(package_item)
    db.session.commit()

    return package


def create_delivery_request(
    customer_id=None,
    pick_up_address_id=None,
    drop_off_address_id=None,
    package_id=None,
    status=None,
):
    """Create and persist a DeliveryRequest object with optional overrides."""
    delivery_request = DeliveryRequest(
        customer_id=customer_id or DEFAULT_DELIVERY_REQUEST["customer_id"],
        package_id=package_id,
        pick_up_address_id=pick_up_address_id,
        drop_off_address_id=drop_off_address_id,
        status=status or DEFAULT_DELIVERY_REQUEST["status"],
    )
    db.session.add(delivery_request)
    db.session.commit()
    return delivery_request
