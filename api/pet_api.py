from api.base_api import BaseAPI


class PetAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.endpoint = "/pet"

    def create_pet(self, pet_data):
        return self.post(self.endpoint, json=pet_data)

    def get_pet_by_id(self, pet_id):
        return self.get(f"{self.endpoint}/{pet_id}")

    def update_pet(self, pet_data):
        return self.put(self.endpoint, json=pet_data)

    def update_pet_with_form(self, pet_id, name=None, status=None):
        form_data = {}
        if name:
            form_data["name"] = name
        if status:
            form_data["status"] = status

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return self.post(f"{self.endpoint}/{pet_id}", data=form_data, headers=headers)

    def delete_pet(self, pet_id):
        return self.delete(f"{self.endpoint}/{pet_id}")

    def find_pets_by_status(self, status):
        return self.get(f"{self.endpoint}/findByStatus", params={"status": status})

    def find_pets_by_tags(self, tags):
        return self.get(f"{self.endpoint}/findByTags", params={"tags": tags})
