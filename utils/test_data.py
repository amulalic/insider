import random


class PetDataBuilder:
    """Builder pattern for creating test pet data"""

    def __init__(self):
        self.pet_data = {
            "name": "DefaultPet",
            "photoUrls": ["https://example.com/default.jpg"],
        }

    def with_id(self, pet_id=None):
        """Add pet ID"""
        self.pet_data["id"] = pet_id or self.generate_random_id()
        return self

    def with_name(self, name):
        """Add pet name"""
        self.pet_data["name"] = name
        return self

    def with_status(self, status):
        """Add pet status"""
        self.pet_data["status"] = status
        return self

    def with_category(self, category_id, category_name):
        """Add pet category"""
        self.pet_data["category"] = {"id": category_id, "name": category_name}
        return self

    def with_tags(self, tags):
        """Add pet tags"""
        self.pet_data["tags"] = [
            {"id": i, "name": tag} for i, tag in enumerate(tags, 1)
        ]
        return self

    def with_photo_urls(self, urls):
        """Add photo URLs"""
        self.pet_data["photoUrls"] = urls
        return self

    def build(self):
        """Build and return the pet data"""
        return self.pet_data

    @staticmethod
    def generate_random_id():
        """Generate random pet ID"""
        return random.randint(10000, 99999)


class TestDataFactory:
    """Factory for creating common test data"""

    @staticmethod
    def valid_pet():
        """Create valid pet data"""
        return (
            PetDataBuilder()
            .with_id()
            .with_name("Buddy")
            .with_status("available")
            .with_category(1, "Dogs")
            .with_tags(["friendly"])
            .build()
        )

    @staticmethod
    def minimal_pet():
        """Create minimal valid pet data"""
        return {"name": "MinimalPet", "photoUrls": ["url"]}

    @staticmethod
    def invalid_pet_no_name():
        """Create invalid pet without name"""
        return {"photoUrls": ["url"], "status": "available"}

    @staticmethod
    def invalid_pet_no_photos():
        """Create invalid pet without photos"""
        return {"name": "NoPhotos", "status": "available"}
