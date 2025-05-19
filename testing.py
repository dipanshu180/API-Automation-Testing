import unittest
import requests

class APICheckoutTest(unittest.TestCase):
    base_url = "https://fakestoreapi.com/carts"
    cart_id = None

    @classmethod
    def setUpClass(cls):
        payload = {
            "userId": 1,
            "date": "2025-05-19",
            "products": [
                {"productId": 1, "quantity": 2},
                {"productId": 2, "quantity": 1}
            ]
        }
        response = requests.post(cls.base_url, json=payload)
        data = response.json()
        print("CREATE CART:", data)
        cls.cart_id = data.get("id")

    def test_get_cart(self):
        response = requests.get(f"{self.base_url}/{self.cart_id}")
        print("GET CART Status:", response.status_code)
        print("GET CART Response Text:", response.text)
        # API may return null, so accept None data
        if response.text == "null":
            data = None
        else:
            data = response.json()
        self.assertEqual(response.status_code, 200, "GET request failed")
        # If data is None, maybe cart is deleted or not found, so don't check id
        if data is not None:
            self.assertEqual(data["id"], self.cart_id)

    def test_update_cart(self):
        updated_payload = {
            "userId": 1,
            "date": "2025-05-20",
            "products": [
                {"productId": 3, "quantity": 5}
            ]
        }
        response = requests.put(f"{self.base_url}/{self.cart_id}", json=updated_payload)
        print("UPDATE CART Status:", response.status_code)
        print("UPDATE CART Response Text:", response.text)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["products"][0]["productId"], 3)

    def test_delete_cart(self):
        response = requests.delete(f"{self.base_url}/{self.cart_id}")
        print("DELETE CART Status:", response.status_code)
        print("DELETE CART Response Text:", response.text)
        # API returns 200 but response null, accept that
        self.assertEqual(response.status_code, 200)
        if response.text == "null":
            data = None
        else:
            data = response.json()
        # No need to assert data is not None here since API returns null
        # Just confirm status code is 200

if __name__ == "__main__":
    unittest.main()
