from src.django_rest_api_untangler import rest_endpoint

class Input:
    def __init__(self, id, name, type, details):
        self.id = id
        self.name = name
        self.type = type
        self.details = details

def main():
    input_data = Input(id=1, name="test", type="bank_account", details={})
    response = rest_endpoint(input_data)
    print(response)

if __name__ == "__main__":
    main()
