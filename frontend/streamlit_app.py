import streamlit as st
import requests
import pandas as pd
from typing import Dict, Any
import json
from datetime import datetime, time
from auth_utils import is_authenticated, get_auth_headers, verify_token, get_current_user
from login_page import show_login_page, show_user_info

# Configuration
API_BASE_URL = "http://localhost:8001"

# Page configuration
st.set_page_config(
    page_title="Order Management System",
    page_icon="📦",
    layout="wide"
)

def make_api_request(method: str, endpoint: str, data: Dict[Any, Any] = None):
    """Make API request to backend with authentication"""
    url = f"{API_BASE_URL}{endpoint}"
    headers = get_auth_headers()
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend API. Please ensure the backend server is running.")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def main():
    # Check authentication
    if not is_authenticated():
        show_login_page()
        return
    
    # Verify token is still valid
    if not verify_token():
        st.error("Session expired. Please login again.")
        from auth_utils import logout
        logout()
        st.rerun()
        return
    
    # Show user info at the top
    show_user_info()
    st.divider()
    
    st.title("📦 Order Management System")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "Dashboard", 
        "Create Order", 
        "View Orders", 
        "Update Order",
        "Sub-Orders",
        "Update Order Status"
    ])
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Create Order":
        show_create_order()
    elif page == "View Orders":
        show_view_orders()
    elif page == "Update Order":
        show_update_order()
    elif page == "Sub-Orders":
        show_sub_orders()
    elif page == "Update Order Status":
        show_update_status()

def show_dashboard():
    st.header("Dashboard")
    
    # Get orders data
    orders = make_api_request("GET", "/orders/")
    sub_orders = make_api_request("GET", "/sub-orders/")
    
    if orders is not None and sub_orders is not None:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Orders", len(orders))
        
        with col2:
            open_orders = len([o for o in orders if o['status'] == 'Open'])
            st.metric("Open Orders", open_orders)
        
        with col3:
            in_process_orders = len([o for o in orders if o['status'] == 'In-Process'])
            st.metric("In-Process Orders", in_process_orders)
        
        with col4:
            st.metric("Total Sub-Orders", len(sub_orders))
        
        # Status distribution
        if orders:
            st.subheader("Order Status Distribution")
            status_counts = {}
            for order in orders:
                status = order['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            df_status = pd.DataFrame(list(status_counts.items()), columns=['Status', 'Count'])
            st.bar_chart(df_status.set_index('Status'))

def show_create_order():
    st.header("Create New Order")
    
    with st.form("create_order_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name", placeholder="Enter company name")
            product_name = st.text_input("Product Name", placeholder="Enter product name")
            molecule = st.text_input("Molecule", placeholder="Enter molecule")
            status = st.selectbox("Status", ["Open", "In-Process", "Closed"])
        
        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1)
            pack = st.text_input("Pack", placeholder="Enter pack information")
            order_date = st.date_input("Order Date")
        
        st.subheader("Ingredients")
        col3, col4 = st.columns(2)
        
        ingredients = {}
        ingredient_names = ["Carton", "Label", "RM", "Sterios", "Bottles", "M.Cups", "Caps", "Shippers"]
        
        with col3:
            for i, ingredient in enumerate(ingredient_names[:4]):
                ingredients[ingredient.lower().replace(".", "_")] = st.selectbox(
                    f"{ingredient}", ["N/A", "Y", "N"], key=f"ing_{i}"
                )
        
        with col4:
            for i, ingredient in enumerate(ingredient_names[4:], 4):
                ingredients[ingredient.lower().replace(".", "_")] = st.selectbox(
                    f"{ingredient}", ["N/A", "Y", "N"], key=f"ing_{i}"
                )
        
        submitted = st.form_submit_button("Create Order")
        
        if submitted:
            if company_name and product_name and molecule and pack:
                # Convert date to datetime with default time (00:00:00)
                order_datetime = datetime.combine(order_date, time(0, 0, 0))
                
                order_data = {
                    "company_name": company_name,
                    "product_name": product_name,
                    "molecule": molecule,
                    "status": status,
                    "quantity": quantity,
                    "pack": pack,
                    "order_date": order_datetime.isoformat(),
                    **ingredients
                }
                
                result = make_api_request("POST", "/orders/", order_data)
                if result:
                    st.success(f"Order created successfully! Order ID: {result['order_id']}")
                    
                    # Show created sub-orders
                    if result.get('sub_orders'):
                        st.subheader("Sub-Orders Created:")
                        for sub_order in result['sub_orders']:
                            st.info(f"Sub-Order ID: {sub_order['sub_order_id']} - {sub_order['ingredient_type'].title()}")
            else:
                st.error("Please fill in all required fields.")

def show_view_orders():
    st.header("📋 View Orders & Sub-Orders")
    
    # Fetch orders and sub-orders
    orders = make_api_request("GET", "/orders/")
    sub_orders = make_api_request("GET", "/sub-orders/")
    
    if orders:
        # Group sub-orders by order_id for easy lookup
        sub_orders_by_order = {}
        if sub_orders:
            for sub_order in sub_orders:
                order_id = sub_order['order_id']
                if order_id not in sub_orders_by_order:
                    sub_orders_by_order[order_id] = []
                sub_orders_by_order[order_id].append(sub_order)
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Open", "In-Process", "Closed"])
        with col2:
            company_filter = st.selectbox("Filter by Company", ["All"] + list(set([order['company_name'] for order in orders])))
        
        # Apply filters
        filtered_orders = orders.copy()
        if status_filter != "All":
            filtered_orders = [order for order in filtered_orders if order['status'] == status_filter]
        if company_filter != "All":
            filtered_orders = [order for order in filtered_orders if order['company_name'] == company_filter]
        
        # Display each order with its sub-orders
        for order in filtered_orders:
            order_id = order['order_id']
            sub_order_count = len(sub_orders_by_order.get(order_id, []))
            
            # Main order section
            with st.expander(f"📦 Order #{order_id} - {order['company_name']} - {order['product_name']} ({sub_order_count} sub-orders)", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Company:** {order['company_name']}")
                    st.write(f"**Product:** {order['product_name']}")
                    st.write(f"**Molecule:** {order['molecule']}")
                    st.write(f"**Status:** {order['status']}")
                
                with col2:
                    st.write(f"**Quantity:** {order['quantity']}")
                    st.write(f"**Pack:** {order['pack']}")
                    order_date = order.get('order_date')
                    if order_date:
                        st.write(f"**Order Date:** {pd.to_datetime(order_date).strftime('%Y-%m-%d')}")
                    else:
                        st.write("**Order Date:** Not set")
                    st.write(f"**Sub-Orders:** {sub_order_count}")
                
                # Ingredients section
                st.write("**Ingredient Requirements:**")
                ingredients_col1, ingredients_col2 = st.columns(2)
                
                with ingredients_col1:
                    st.write(f"• Carton: {order['carton']}")
                    st.write(f"• Label: {order['label']}")
                    st.write(f"• RM: {order['rm']}")
                    st.write(f"• Sterios: {order['sterios']}")
                
                with ingredients_col2:
                    st.write(f"• Bottles: {order['bottles']}")
                    st.write(f"• M.Cups: {order['m_cups']}")
                    st.write(f"• Caps: {order['caps']}")
                    st.write(f"• Shippers: {order['shippers']}")
                
                # Sub-orders section
                if order_id in sub_orders_by_order and sub_orders_by_order[order_id]:
                    st.write("**Sub-Orders:**")
                    
                    # Create a table-like display for sub-orders
                    sub_order_data = []
                    for sub_order in sub_orders_by_order[order_id]:
                        sub_order_date = sub_order.get('sub_order_date')
                        sub_order_date_str = pd.to_datetime(sub_order_date).strftime('%Y-%m-%d') if sub_order_date else 'Not set'
                        
                        approved_first = sub_order.get('approved_by_first_name') or ''
                        approved_last = sub_order.get('approved_by_last_name') or ''
                        approved_by = f"{approved_first} {approved_last}".strip() or 'Not set'
                        
                        sub_order_data.append({
                            'Sub-Order ID': sub_order['sub_order_id'],
                            'Ingredient': sub_order['ingredient_type'].title(),
                            'Status': sub_order['status'],
                            'Sub-Order Date': sub_order_date_str,
                            'Vendor Company': sub_order.get('vendor_company') or 'Not set',
                            'Designer': sub_order.get('designer_name') or 'Not set',
                            'Approved By': approved_by,
                            'Sizes': sub_order.get('sizes') or 'Not set'
                        })
                    
                    sub_df = pd.DataFrame(sub_order_data)
                    st.dataframe(sub_df, use_container_width=True, hide_index=True)
                    
                    # Show detailed view for each sub-order in a more compact format
                    st.write("**📋 Sub-Order Details:**")
                    for sub_order in sub_orders_by_order[order_id]:
                        st.markdown(f"**🔧 Sub-Order #{sub_order['sub_order_id']} - {sub_order['ingredient_type'].title()}**")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"• **Status:** {sub_order['status']}")
                            st.write(f"• **Vendor:** {sub_order.get('vendor_company') or 'Not specified'}")
                            st.write(f"• **Product:** {sub_order.get('product_name') or 'Not specified'}")
                        
                        with col2:
                            st.write(f"• **Designer:** {sub_order.get('designer_name') or 'Not specified'}")
                            st.write(f"• **Sizes:** {sub_order.get('sizes') or 'Not specified'}")
                            
                            approved_first = sub_order.get('approved_by_first_name') or ''
                            approved_last = sub_order.get('approved_by_last_name') or ''
                            approved_by = f"{approved_first} {approved_last}".strip()
                            st.write(f"• **Approved By:** {approved_by or 'Not specified'}")
                        
                        with col3:
                            main_order_date = sub_order.get('main_order_date')
                            if main_order_date:
                                st.write(f"• **Main Order Date:** {pd.to_datetime(main_order_date).strftime('%Y-%m-%d')}")
                            else:
                                st.write("• **Main Order Date:** Not specified")
                            
                            sub_order_date = sub_order.get('sub_order_date')
                            if sub_order_date:
                                st.write(f"• **Sub-Order Date:** {pd.to_datetime(sub_order_date).strftime('%Y-%m-%d')}")
                            else:
                                st.write("• **Sub-Order Date:** Not specified")
                            
                            approved_date = sub_order.get('approved_date')
                            if approved_date:
                                st.write(f"• **Approved Date:** {pd.to_datetime(approved_date).strftime('%Y-%m-%d')}")
                            else:
                                st.write("• **Approved Date:** Not specified")
                        
                        if sub_order.get('remarks'):
                            st.write(f"• **Remarks:** {sub_order['remarks']}")
                        
                        st.markdown("---")
                else:
                    st.info("No sub-orders for this order.")
    else:
        st.info("No orders found.")

def show_sub_orders():
    st.header("Sub-Orders Management")
    
    sub_orders = make_api_request("GET", "/sub-orders/")
    
    if sub_orders:
        df_sub_orders = pd.DataFrame(sub_orders)
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Open", "In-Process", "Closed"], key="sub_status")
        with col2:
            ingredient_filter = st.selectbox("Filter by Ingredient", 
                                           ["All"] + list(df_sub_orders['ingredient_type'].unique()), 
                                           key="sub_ingredient")
        
        # Apply filters
        filtered_df = df_sub_orders.copy()
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        if ingredient_filter != "All":
            filtered_df = filtered_df[filtered_df['ingredient_type'] == ingredient_filter]
        
        # Display summary table with key fields
        summary_columns = ['sub_order_id', 'ingredient_type', 'status', 'vendor_company', 'designer_name', 'approved_by_first_name', 'approved_by_last_name']
        display_df = filtered_df[summary_columns].copy()
        display_df.columns = ['Sub-Order ID', 'Ingredient', 'Status', 'Vendor Company', 'Designer', 'Approved By (First)', 'Approved By (Last)']
        st.dataframe(display_df, use_container_width=True)
        
        # Detailed sub-order management
        if not filtered_df.empty:
            st.subheader("📝 Edit Sub-Order Details")
            
            # Select sub-order to edit
            selected_sub_order_id = st.selectbox("Select Sub-Order to Edit", filtered_df['sub_order_id'].tolist())
            
            # Get selected sub-order details
            selected_sub_order = filtered_df[filtered_df['sub_order_id'] == selected_sub_order_id].iloc[0]
            
            # Create form for editing
            with st.form(f"edit_sub_order_{selected_sub_order_id}"):
                st.write(f"**Editing Sub-Order #{selected_sub_order_id} - {selected_sub_order['ingredient_type'].title()}**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    status = st.selectbox("Status", ["Open", "In-Process", "Closed"], 
                                        index=["Open", "In-Process", "Closed"].index(selected_sub_order['status']))
                    vendor_company = st.text_input("Vendor Company", value=selected_sub_order.get('vendor_company') or "")
                    product_name = st.text_input("Product Name", value=selected_sub_order.get('product_name') or "")
                    designer_name = st.text_input("Designer Name", value=selected_sub_order.get('designer_name') or "")
                    sizes = st.text_input("Sizes", value=selected_sub_order.get('sizes') or "")
                    
                with col2:
                    sub_order_date = st.date_input("Sub-Order Date", 
                                                 value=pd.to_datetime(selected_sub_order.get('sub_order_date')).date() if selected_sub_order.get('sub_order_date') else None)
                    main_order_date = st.date_input("Main Order Date", 
                                                   value=pd.to_datetime(selected_sub_order.get('main_order_date')).date() if selected_sub_order.get('main_order_date') else None)
                    approved_by_first_name = st.text_input("Approved By (First Name)", value=selected_sub_order.get('approved_by_first_name') or "")
                    approved_by_last_name = st.text_input("Approved By (Last Name)", value=selected_sub_order.get('approved_by_last_name') or "")
                    approved_date = st.date_input("Approved Date", 
                                                value=pd.to_datetime(selected_sub_order.get('approved_date')).date() if selected_sub_order.get('approved_date') else None)
                
                remarks = st.text_area("Remarks", value=selected_sub_order.get('remarks') or "", height=100)
                
                submitted = st.form_submit_button("Update Sub-Order", type="primary")
                
                if submitted:
                    # Prepare update data
                    update_data = {
                        "status": status,
                        "vendor_company": vendor_company if vendor_company else None,
                        "product_name": product_name if product_name else None,
                        "designer_name": designer_name if designer_name else None,
                        "sizes": sizes if sizes else None,
                        "approved_by_first_name": approved_by_first_name if approved_by_first_name else None,
                        "approved_by_last_name": approved_by_last_name if approved_by_last_name else None,
                        "remarks": remarks if remarks else None,
                        "sub_order_date": f"{sub_order_date.isoformat()}T00:00:00" if sub_order_date else None,
                        "main_order_date": f"{main_order_date.isoformat()}T00:00:00" if main_order_date else None,
                        "approved_date": f"{approved_date.isoformat()}T00:00:00" if approved_date else None
                    }
                    
                    # Make API call
                    result = make_api_request("PUT", f"/sub-orders/{selected_sub_order_id}", update_data)
                    
                    if result:
                        st.success("✅ Sub-order updated successfully!")
                        st.experimental_rerun()
                    else:
                        st.error("❌ Failed to update sub-order")
    else:
        st.info("No sub-orders found.")

def show_update_order():
    st.header("Update Order")
    
    orders = make_api_request("GET", "/orders/")
    
    if orders:
        df_orders = pd.DataFrame(orders)
        
        # Order selection
        selected_order_id = st.selectbox("Select Order ID to Update", df_orders['order_id'].tolist())
        
        if selected_order_id:
            # Get current order details
            current_order = make_api_request("GET", f"/orders/{selected_order_id}")
            
            if current_order:
                st.subheader(f"Updating Order ID: {selected_order_id}")
                
                # Show current values
                with st.expander("Current Order Details", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Company:** {current_order['company_name']}")
                        st.write(f"**Product:** {current_order['product_name']}")
                        st.write(f"**Molecule:** {current_order['molecule']}")
                        st.write(f"**Status:** {current_order['status']}")
                    with col2:
                        st.write(f"**Quantity:** {current_order['quantity']}")
                        st.write(f"**Pack:** {current_order['pack']}")
                        order_date = current_order.get('order_date')
                        if order_date:
                            st.write(f"**Order Date:** {pd.to_datetime(order_date).strftime('%Y-%m-%d')}")
                        else:
                            st.write("**Order Date:** Not set")
                        st.write(f"**Current Sub-Orders:** {len(current_order.get('sub_orders', []))}")
                
                # Update form
                with st.form("update_order_form"):
                    st.subheader("Update Order Information")
                    
                    # Basic order information
                    col1, col2 = st.columns(2)
                    with col1:
                        company_name = st.text_input("Company Name", value=current_order['company_name'])
                        product_name = st.text_input("Product Name", value=current_order['product_name'])
                        molecule = st.text_input("Molecule", value=current_order['molecule'])
                    
                    with col2:
                        status = st.selectbox("Status", ["Open", "In-Process", "Closed"], 
                                            index=["Open", "In-Process", "Closed"].index(current_order['status']))
                        quantity = st.number_input("Quantity", min_value=1, value=current_order['quantity'])
                        pack = st.text_input("Pack", value=current_order['pack'])
                        current_order_date = current_order.get('order_date')
                        order_date = st.date_input("Order Date", 
                                                 value=pd.to_datetime(current_order_date).date() if current_order_date else None)
                    
                    st.subheader("Ingredient Requirements")
                    st.info("⚠️ Changing ingredients from 'N' to 'Y' will create new sub-orders. Changing from 'Y' to 'N' or 'N/A' will remove existing sub-orders.")
                    
                    # Ingredients section
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        carton = st.selectbox("Carton", ["Y", "N", "N/A"], 
                                            index=["Y", "N", "N/A"].index(current_order['carton']))
                        label = st.selectbox("Label", ["Y", "N", "N/A"], 
                                           index=["Y", "N", "N/A"].index(current_order['label']))
                    
                    with col2:
                        rm = st.selectbox("RM", ["Y", "N", "N/A"], 
                                        index=["Y", "N", "N/A"].index(current_order['rm']))
                        sterios = st.selectbox("Sterios", ["Y", "N", "N/A"], 
                                             index=["Y", "N", "N/A"].index(current_order['sterios']))
                    
                    with col3:
                        bottles = st.selectbox("Bottles", ["Y", "N", "N/A"], 
                                             index=["Y", "N", "N/A"].index(current_order['bottles']))
                        m_cups = st.selectbox("M.Cups", ["Y", "N", "N/A"], 
                                            index=["Y", "N", "N/A"].index(current_order['m_cups']))
                    
                    with col4:
                        caps = st.selectbox("Caps", ["Y", "N", "N/A"], 
                                          index=["Y", "N", "N/A"].index(current_order['caps']))
                        shippers = st.selectbox("Shippers", ["Y", "N", "N/A"], 
                                              index=["Y", "N", "N/A"].index(current_order['shippers']))
                    
                    # Submit button
                    submitted = st.form_submit_button("Update Order", type="primary")
                    
                    if submitted:
                        # Check for ingredient changes
                        current_ingredients = {
                            'carton': current_order['carton'],
                            'label': current_order['label'],
                            'rm': current_order['rm'],
                            'sterios': current_order['sterios'],
                            'bottles': current_order['bottles'],
                            'm_cups': current_order['m_cups'],
                            'caps': current_order['caps'],
                            'shippers': current_order['shippers']
                        }
                        
                        new_ingredients = {
                            'carton': carton,
                            'label': label,
                            'rm': rm,
                            'sterios': sterios,
                            'bottles': bottles,
                            'm_cups': m_cups,
                            'caps': caps,
                            'shippers': shippers
                        }
                        
                        # Calculate changes
                        will_add_suborders = []
                        will_remove_suborders = []
                        
                        for ingredient, new_value in new_ingredients.items():
                            current_value = current_ingredients[ingredient]
                            if current_value != 'Y' and new_value == 'Y':
                                will_add_suborders.append(ingredient)
                            elif current_value == 'Y' and new_value != 'Y':
                                will_remove_suborders.append(ingredient)
                        
                        # Show ingredient changes
                        if will_add_suborders or will_remove_suborders:
                            st.subheader("Ingredient Changes Detected:")
                            col1, col2 = st.columns(2)
                            with col1:
                                if will_add_suborders:
                                    st.success(f"✅ Will CREATE sub-orders for: {', '.join(will_add_suborders)}")
                            with col2:
                                if will_remove_suborders:
                                    st.warning(f"🗑️ Will REMOVE sub-orders for: {', '.join(will_remove_suborders)}")
                        else:
                            # Check if any ingredients actually changed (not just Y->Y transitions)
                            ingredient_changes = []
                            for ingredient, new_value in new_ingredients.items():
                                current_value = current_ingredients[ingredient]
                                if current_value != new_value:
                                    ingredient_changes.append(f"{ingredient}: {current_value} → {new_value}")
                            
                            if ingredient_changes:
                                st.info(f"Ingredient changes detected: {', '.join(ingredient_changes)}")
                                st.info("Note: Sub-orders are only created/removed when ingredients change to/from 'Y'")
                            else:
                                st.info("No ingredient changes detected.")
                        
                        # Prepare update data
                        # Convert date to datetime with default time (00:00:00)
                        order_datetime = datetime.combine(order_date, time(0, 0, 0)) if order_date else None
                        
                        update_data = {
                            "company_name": company_name,
                            "product_name": product_name,
                            "molecule": molecule,
                            "status": status,
                            "quantity": quantity,
                            "pack": pack,
                            "order_date": order_datetime.isoformat() if order_datetime else None,
                            "carton": carton,
                            "label": label,
                            "rm": rm,
                            "sterios": sterios,
                            "bottles": bottles,
                            "m_cups": m_cups,
                            "caps": caps,
                            "shippers": shippers
                        }
                        
                        # Make API call
                        result = make_api_request("PUT", f"/orders/{selected_order_id}", update_data)
                        
                        if result:
                            st.success("✅ Order updated successfully!")
                            
                            # Show updated sub-orders count
                            updated_order = make_api_request("GET", f"/orders/{selected_order_id}")
                            if updated_order:
                                new_suborder_count = len(updated_order.get('sub_orders', []))
                                st.info(f"📊 Updated order now has {new_suborder_count} sub-orders")
                            
                            # Refresh the page to show updated data
                            st.experimental_rerun()
    else:
        st.info("No orders found.")

def show_update_status():
    st.header("Update Order Status")
    
    orders = make_api_request("GET", "/orders/")
    
    if orders:
        df_orders = pd.DataFrame(orders)
        
        col1, col2 = st.columns(2)
        with col1:
            selected_order_id = st.selectbox("Select Order ID", df_orders['order_id'].tolist())
        
        if selected_order_id:
            current_order = df_orders[df_orders['order_id'] == selected_order_id].iloc[0]
            
            with col2:
                st.info(f"Current Status: {current_order['status']}")
            
            with st.form("update_status_form"):
                new_status = st.selectbox("New Status", ["Open", "In-Process", "Closed"])
                
                submitted = st.form_submit_button("Update Status")
                
                if submitted:
                    update_data = {"status": new_status}
                    result = make_api_request("PUT", f"/orders/{selected_order_id}", update_data)
                    if result:
                        st.success("Order status updated successfully!")
    else:
        st.info("No orders found.")

if __name__ == "__main__":
    main()