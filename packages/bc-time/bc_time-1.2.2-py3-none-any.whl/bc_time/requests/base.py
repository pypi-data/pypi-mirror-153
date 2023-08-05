from json import loads as json_loads

class Base:
    def _get_response_data(self, response_text: str) -> dict:
        response_data = None
        if self.crypt_key:
            self.crypt.data = response_text
            response_data = self.crypt.decrypt()
        if not response_data:
            response_data = response_text
        try:
            return json_loads(response_data)
        except ValueError as exception:
            print(f"json.loads: {str(exception)}")
        return None