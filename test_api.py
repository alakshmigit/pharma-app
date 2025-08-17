#!/usr/bin/env python3
"""
Test script for the Order Management API
"""
import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing Order Management API")
    print("=" * 50)
    
    # Test 1: Get all orders
    print("\n1. Testing GET /orders/")
    response = requests.get(f"{API_BASE_URL}/orders/")
    if response.status_code == 200:
        orders = response.json()
        print(f"✅ Found {len(orders)} orders")
        for order in orders:
            print(f"   - Order {order['order_id']}: {order['company_name']} - {order['product_name']} ({order['status']})")
            print(f"     Sub-orders: {len(order['sub_orders'])}")
    else:
        print(f"❌ Failed: {response.status_code}")
    
    # Test 2: Get specific order
    print("\n2. Testing GET /orders/1")
    response = requests.get(f"{API_BASE_URL}/orders/1")
    if response.status_code == 200:
        order = response.json()
        print(f"✅ Order 1: {order['company_name']} - {order['product_name']}")
        print(f"   Ingredients with 'Y': {[k for k, v in order.items() if k in ['carton', 'label', 'rm', 'sterios', 'bottles', 'm_cups', 'caps', 'shippers'] and v == 'Y']}")
    else:
        print(f"❌ Failed: {response.status_code}")
    
    # Test 3: Get all sub-orders
    print("\n3. Testing GET /sub-orders/")
    response = requests.get(f"{API_BASE_URL}/sub-orders/")
    if response.status_code == 200:
        sub_orders = response.json()
        print(f"✅ Found {len(sub_orders)} sub-orders")
        for sub_order in sub_orders:
            print(f"   - Sub-order {sub_order['sub_order_id']}: {sub_order['ingredient_type']} for Order {sub_order['order_id']} ({sub_order['status']})")
    else:
        print(f"❌ Failed: {response.status_code}")
    
    # Test 4: Update sub-order status
    print("\n4. Testing PUT /sub-orders/1/status")
    response = requests.put(f"{API_BASE_URL}/sub-orders/1/status", params={"status": "In-Process"})
    if response.status_code == 200:
        print("✅ Sub-order status updated successfully")
    else:
        print(f"❌ Failed: {response.status_code}")
    
    # Test 5: Update order status
    print("\n5. Testing PUT /orders/1")
    update_data = {"status": "In-Process"}
    response = requests.put(f"{API_BASE_URL}/orders/1", json=update_data)
    if response.status_code == 200:
        updated_order = response.json()
        print(f"✅ Order status updated to: {updated_order['status']}")
    else:
        print(f"❌ Failed: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")

if __name__ == "__main__":
    test_api()