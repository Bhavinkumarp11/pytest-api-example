import uuid
import pytest
from jsonschema import validate
from hamcrest import assert_that, is_
import schemas
import api_helpers
from app import app

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''
@pytest.fixture
def client():
    """Returns a test client with app in testing mode"""
    app.testing = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def create_pet_and_order():
    """
    Creates a new pet and places an order for it.
    Returns the order data including pet_id.
    """
    pet_id = int(str(uuid.uuid4().int)[:6])
    new_pet = {
        "id": pet_id,
        "name": "new_test",
        "type": "cat",
        "status": "available"
    }

    pet_obj = api_helpers.post_api_data('/pets/', new_pet)
    assert_that(pet_obj.status_code, is_(201))

    order_response = api_helpers.post_api_data("/store/order", {"pet_id": pet_id})
    assert_that(order_response.status_code, is_(201))

    order_data = order_response.json()
    validate(instance=order_data, schema=schemas.order)

    return order_data

def test_patch_order_by_id(create_pet_and_order):
    """
    Test PATCH /store/order/{order_id}
    - Updates the order and associated pet's status
    - Validates response message and schema
    """
    order_id = create_pet_and_order["id"]
    pet_id = create_pet_and_order["pet_id"]
    patch_data = {"status": "sold"}

    response = api_helpers.patch_api_data(f"/store/order/{order_id}", patch_data)

    assert_that(response.status_code, is_(200))
    assert_that(response.json()["message"], is_("Order and pet status updated successfully"))
    pet_response = api_helpers.get_api_data(f"/pets/{pet_id}")
    assert_that(pet_response.status_code, is_(200))

    pet_data = pet_response.json()
    assert_that(pet_data["status"], is_("sold"))

    validate(instance=pet_data, schema=schemas.pet)
