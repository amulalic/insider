import pytest
from utils.test_data import TestDataFactory, PetDataBuilder


class TestPetCreation:
    """Test cases for creating pets"""

    def test_create_pet_with_all_fields(self, pet_api, cleanup_pet):
        """Test create pet with all possible fields"""
        pet_data = (
            PetDataBuilder()
            .with_id()
            .with_name("Complete Pet")
            .with_status("available")
            .with_category(1, "Dogs")
            .with_tags(["friendly", "trained", "vaccinated"])
            .with_photo_urls(["url1", "url2", "url3"])
            .build()
        )

        response = pet_api.create_pet(pet_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == pet_data["id"]
        assert data["name"] == pet_data["name"]
        assert data["status"] == pet_data["status"]
        assert data["category"] == pet_data["category"]
        assert data["tags"] == pet_data["tags"]
        assert data["photoUrls"] == pet_data["photoUrls"]

        cleanup_pet(data["id"])

    def test_create_pet_with_valid_data(self, pet_api, cleanup_pet):
        """Test create a new pet with valid data"""
        pet_data = TestDataFactory.valid_pet()
        response = pet_api.create_pet(pet_data)

        assert response.status_code == 200, f"Failed: {response.text}"
        data = response.json()
        assert data["id"] == pet_data["id"]
        assert data["name"] == pet_data["name"]
        assert data["status"] == pet_data["status"]

        cleanup_pet(data["id"])

    def test_create_pet_with_minimal_data(self, pet_api, cleanup_pet):
        """Test create pet with minimal required fields"""
        pet_data = TestDataFactory.minimal_pet()

        response = pet_api.create_pet(pet_data)
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == pet_data["name"]
        assert data["photoUrls"] == pet_data["photoUrls"]
        assert "tags" in data
        assert data["tags"] == []

        cleanup_pet(data["id"])

    def test_create_pet_with_long_name(self, pet_api, cleanup_pet):
        """Test create pet with long name"""
        pet_data = PetDataBuilder().with_name("A" * 1000).build()

        response = pet_api.create_pet(pet_data)

        assert response.status_code in [200, 400, 413]
        if response.status_code == 200:
            cleanup_pet(response.json()["id"])

    def test_create_pet_with_special_characters(self, pet_api, cleanup_pet):
        """Test create pet using name with special characters"""
        pet_data = (
            PetDataBuilder().with_name("Pet <script>alert('xss')</script>").build()
        )

        response = pet_api.create_pet(pet_data)

        assert response.status_code == 200
        assert "<script>" in response.json()["name"]

        cleanup_pet(response.json()["id"])

    def test_create_pet_with_unicode(self, pet_api, cleanup_pet):
        """Test create pet using name with unicode characters"""
        pet_data = PetDataBuilder().with_name("宠物🐕Питомец").build()

        response = pet_api.create_pet(pet_data)

        assert response.status_code == 200

        cleanup_pet(response.json()["id"])

    def test_create_pet_without_name(self, pet_api, cleanup_pet):
        """Test create pet without required name"""
        pet_data = TestDataFactory.invalid_pet_no_name()

        response = pet_api.create_pet(pet_data)

        assert response.status_code in [400, 405, 500]

        if response.status_code == 200:
            cleanup_pet(response.json()["id"])

    def test_create_pet_without_photos(self, pet_api, cleanup_pet):
        """Test create pet without required photos"""
        pet_data = TestDataFactory.invalid_pet_no_photos()

        response = pet_api.create_pet(pet_data)

        assert response.status_code in [400, 405, 500]

        if response.status_code == 200:
            cleanup_pet(response.json()["id"])


class TestPetRetrieval:
    """Test cases for retrieving pets"""

    def test_get_pet_by_id(self, pet_api, created_pet):
        """Test retrieve existing pet by ID"""
        response = pet_api.get_pet_by_id(created_pet["id"])

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_pet["id"]
        assert data["name"] == created_pet["name"]
        assert data["status"] == created_pet["status"]
        assert data["category"] == created_pet["category"]
        assert data["tags"] == created_pet["tags"]
        assert data["photoUrls"] == created_pet["photoUrls"]

    def test_find_pets_by_available_status(self, pet_api):
        """Test find pets with available status"""
        response = pet_api.find_pets_by_status("available")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert data[0]["status"] == "available"

    def test_find_pets_by_multiple_statuses(self, pet_api):
        """Test find pets with multiple statuses"""
        response = pet_api.find_pets_by_status(["available", "pending"])

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_non_existent_pet(self, pet_api):
        """Test return 404 for non-existent pet"""
        response = pet_api.get_pet_by_id(999999991)

        assert response.status_code == 404
        assert "message" in response.json()

    def test_get_pet_with_invalid_id(self, pet_api):
        """Should fail with invalid ID format"""
        response = pet_api.get_pet_by_id("invalid_id")

        assert response.status_code in [400, 404, 405]

    def test_find_pets_with_invalid_status(self, pet_api):
        """Should handle invalid status gracefully"""
        response = pet_api.find_pets_by_status("invalid_status")

        assert response.status_code in [200, 400, 404]


class TestPetUpdate:
    """Test cases for updating pets"""

    def test_update_all_fields(self, pet_api, created_pet):
        """Test update all fields"""
        updated_data = created_pet.copy()
        updated_data["name"] = "Updated Buddy"
        updated_data["status"] = "sold"
        updated_data["category"] = {"id": 2, "name": "Cats"}
        updated_data["tags"] = [{"id": 2, "name": "trained"}]
        updated_data["photoUrls"] = ["url"]

        response = pet_api.update_pet(updated_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == updated_data["name"]
        assert data["status"] == updated_data["status"]
        assert data["category"] == updated_data["category"]
        assert data["tags"] == updated_data["tags"]
        assert data["photoUrls"] == updated_data["photoUrls"]

        data = pet_api.get_pet_by_id(updated_data["id"]).json()

        assert data["name"] == updated_data["name"]
        assert data["status"] == updated_data["status"]
        assert data["category"] == updated_data["category"]
        assert data["tags"] == updated_data["tags"]
        assert data["photoUrls"] == updated_data["photoUrls"]

    def test_update_pet_name_and_status(self, pet_api, created_pet):
        """Test update pet name and status"""
        updated_data = created_pet.copy()
        updated_data["name"] = "Updated Buddy"
        updated_data["status"] = "sold"

        response = pet_api.update_pet(updated_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == updated_data["name"]
        assert data["status"] == updated_data["status"]

        data = pet_api.get_pet_by_id(updated_data["id"]).json()

        assert data["name"] == updated_data["name"]
        assert data["status"] == updated_data["status"]

    def test_update_pet_name_using_longer_name(self, pet_api, created_pet):
        """Test update pet name using longer name"""
        updated_data = created_pet.copy()
        updated_data["name"] = "A" * 1000
        updated_data["status"] = "sold"

        response = pet_api.update_pet(updated_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == updated_data["name"]

        data = pet_api.get_pet_by_id(updated_data["id"]).json()

        assert data["name"] == updated_data["name"]

    def test_update_pet_name_using_special_characters(self, pet_api, created_pet):
        """Test update pet name using special characters"""
        updated_data = created_pet.copy()
        updated_data["name"] = "Pet <script>alert('xss')</script>"

        response = pet_api.update_pet(updated_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == updated_data["name"]

        data = pet_api.get_pet_by_id(updated_data["id"]).json()

        assert data["name"] == updated_data["name"]

    def test_update_pet_name_using_unicode_characters(self, pet_api, created_pet):
        """Test update pet name using unicode characters"""
        updated_data = created_pet.copy()
        updated_data["name"] = "宠物🐕Питомец"

        response = pet_api.update_pet(updated_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == updated_data["name"]

        data = pet_api.get_pet_by_id(updated_data["id"]).json()

        assert data["name"] == updated_data["name"]

    def test_update_pet_with_form_data(self, pet_api, created_pet):
        """Test update pet using form data"""

        response = pet_api.update_pet_with_form(
            created_pet["id"], name="Form Updated", status="pending"
        )

        assert response.status_code == 200
        data = pet_api.get_pet_by_id(created_pet["id"]).json()

        assert data["name"] == "Form Updated"
        assert data["status"] == "pending"

    def test_update_non_existent_pet(self, pet_api):
        """Test fail to update non-existent pet"""
        pet_data = PetDataBuilder().with_id(999999991).with_name("Non Existent").build()

        response = pet_api.update_pet(pet_data)

        assert response.status_code in [404, 405]

    def test_partial_update(self, pet_api, created_pet):
        """Test update only specified fields"""
        partial_data = {
            "id": created_pet["id"],
            "name": "Partially Updated",
            "photoUrls": ["url"],
        }

        response = pet_api.update_pet(partial_data)

        assert response.status_code == 200
        assert response.json()["name"] == "Partially Updated"

    def test_update_without_name(self, pet_api, created_pet):
        """Test update without name"""
        partial_data = {
            "id": created_pet["id"],
            "photoUrls": ["url"],
        }

        response = pet_api.update_pet(partial_data)

        assert response.status_code == [400, 405, 500]

    def test_update_without_photo_urls(self, pet_api, created_pet):
        """Test update without name"""
        partial_data = {
            "id": created_pet["id"],
            "name": "Partially Updated",
        }

        response = pet_api.update_pet(partial_data)

        assert response.status_code == [400, 405, 500]


class TestPetDeletion:
    """Test cases for deleting pets"""

    def test_delete_existing_pet(self, pet_api, pet_for_deletion):
        """Test successfully delete a pet"""
        response = pet_api.delete_pet(pet_for_deletion["id"])

        assert response.status_code == 200

        # Verify deletion
        get_response = pet_api.get_pet_by_id(pet_for_deletion["id"])
        assert get_response.status_code == 404

    def test_delete_non_existent_pet(self, pet_api):
        """Should return 404 when deleting non-existent pet"""
        response = pet_api.delete_pet(999999991)

        assert response.status_code == 404

    def test_delete_already_deleted_pet(self, pet_api, pet_for_deletion):
        """Should fail to delete already deleted pet"""
        # Delete once
        pet_api.delete_pet(pet_for_deletion["id"])

        # Try to delete again
        response = pet_api.delete_pet(pet_for_deletion["id"])

        assert response.status_code == 404

    def test_delete_with_invalid_id(self, pet_api):
        """Should fail with invalid ID"""
        response = pet_api.delete_pet("invalid_id")

        assert response.status_code in [400, 404]
