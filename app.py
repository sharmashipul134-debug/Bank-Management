import streamlit as st
import json
import os
import uuid
from datetime import datetime

# =========================================================
# CONFIGURATION
# =========================================================

DATA_FILE = "data.json"

st.set_page_config(
    page_title="SevaNow 24x7",
    page_icon="🛠️",
    layout="wide"
)


# =========================================================
# DATABASE
# =========================================================

def load_data():
    if not os.path.exists(DATA_FILE):
        data = {
            "users": [],
            "providers": [],
            "bookings": []
        }
        save_data(data)
        return data

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception:
        return {
            "users": [],
            "providers": [],
            "bookings": []
        }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


data = load_data()


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "role" not in st.session_state:
    st.session_state.role = None


# =========================================================
# AI SERVICE CLASSIFIER
# =========================================================

def detect_service(problem):

    text = problem.lower()

    keywords = {
        "Electrician": [
            "electric", "switch", "fan", "light",
            "wiring", "socket", "current"
        ],

        "Plumber": [
            "water", "pipe", "tap", "leak",
            "plumber", "drain", "bathroom"
        ],

        "Carpenter": [
            "wood", "door", "furniture",
            "table", "chair", "carpenter"
        ],

        "Painter": [
            "paint", "painting", "wall",
            "colour", "color"
        ],

        "Mason": [
            "brick", "cement", "construction",
            "wall", "floor", "mason"
        ],

        "AC Technician": [
            "ac", "air conditioner",
            "cooling", "air conditioning"
        ],

        "Refrigerator Technician": [
            "fridge", "refrigerator",
            "freezer", "cooling"
        ],

        "Washing Machine Technician": [
            "washing machine",
            "washer", "washing"
        ],

        "Mechanic": [
            "engine", "car", "bike",
            "vehicle", "mechanic",
            "breakdown"
        ],

        "Puncture Repair": [
            "puncture", "flat tyre",
            "flat tire", "tyre", "tire"
        ],

        "Battery Assistance": [
            "battery", "dead battery",
            "car battery", "jump start"
        ],

        "Towing Service": [
            "towing", "tow truck",
            "tow my car"
        ]
    }

    for service, words in keywords.items():

        for word in words:

            if word in text:
                return service

    return "General Service"


# =========================================================
# FIND AVAILABLE PROVIDERS
# =========================================================

def find_providers(service):

    matched = []

    for provider in data["providers"]:

        if provider.get("available", False):

            skills = provider.get("skills", [])

            if service in skills or "General Service" in skills:
                matched.append(provider)

    return matched


# =========================================================
# LOGIN / REGISTER
# =========================================================

def authentication():

    st.title("🛠️ SevaNow 24×7")

    st.subheader(
        "AI-Powered Home Services & Roadside Assistance Platform"
    )

    tab1, tab2 = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    # ---------------- LOGIN ----------------

    with tab1:

        role = st.selectbox(
            "Login as",
            [
                "Customer",
                "Service Provider",
                "Admin"
            ]
        )

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            # ADMIN LOGIN
            if role == "Admin":

                if (
                    username == "admin"
                    and password == "admin123"
                ):

                    st.session_state.logged_in = True
                    st.session_state.user = {
                        "username": "admin"
                    }
                    st.session_state.role = "Admin"

                    st.rerun()

                else:

                    st.error(
                        "Invalid admin credentials."
                    )

                return

            # CUSTOMER LOGIN

            if role == "Customer":

                users = data["users"]

                for user in users:

                    if (
                        user["username"] == username
                        and user["password"] == password
                    ):

                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.session_state.role = "Customer"

                        st.rerun()

                st.error("Invalid username or password.")

            # PROVIDER LOGIN

            elif role == "Service Provider":

                providers = data["providers"]

                for provider in providers:

                    if (
                        provider["username"] == username
                        and provider["password"] == password
                    ):

                        st.session_state.logged_in = True
                        st.session_state.user = provider
                        st.session_state.role = "Service Provider"

                        st.rerun()

                st.error("Invalid username or password.")

    # ---------------- REGISTER ----------------

    with tab2:

        register_role = st.selectbox(
            "Register as",
            [
                "Customer",
                "Service Provider"
            ]
        )

        name = st.text_input(
            "Full Name",
            key="reg_name"
        )

        username = st.text_input(
            "Username",
            key="reg_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="reg_password"
        )

        phone = st.text_input(
            "Phone Number"
        )

        city = st.text_input(
            "City"
        )

        if register_role == "Service Provider":

            skills = st.multiselect(
                "Select your skills",
                [
                    "Electrician",
                    "Plumber",
                    "Carpenter",
                    "Painter",
                    "Mason",
                    "AC Technician",
                    "Refrigerator Technician",
                    "Washing Machine Technician",
                    "Mechanic",
                    "Puncture Repair",
                    "Battery Assistance",
                    "Towing Service",
                    "General Service"
                ]
            )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not name or not username or not password:

                st.warning(
                    "Please fill all required fields."
                )

                return

            # Check duplicate username

            all_usernames = (
                [u["username"] for u in data["users"]]
                +
                [p["username"] for p in data["providers"]]
            )

            if username in all_usernames:

                st.error(
                    "Username already exists."
                )

                return

            if register_role == "Customer":

                new_user = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "username": username,
                    "password": password,
                    "phone": phone,
                    "city": city
                }

                data["users"].append(new_user)

            else:

                if not skills:

                    st.warning(
                        "Select at least one skill."
                    )

                    return

                new_provider = {

                    "id": str(uuid.uuid4()),

                    "name": name,

                    "username": username,

                    "password": password,

                    "phone": phone,

                    "city": city,

                    "skills": skills,

                    "available": True,

                    "rating": 5.0,

                    "jobs": 0

                }

                data["providers"].append(
                    new_provider
                )

            save_data(data)

            st.success(
                "Account created successfully!"
            )


# =========================================================
# CUSTOMER DASHBOARD
# =========================================================

def customer_dashboard():

    user = st.session_state.user

    st.title(
        f"👋 Welcome, {user['name']}"
    )

    st.caption(
        "24×7 Smart Home & Roadside Assistance"
    )

    # -----------------------------------------------------

    menu = st.sidebar.radio(
        "Customer Menu",
        [
            "🏠 Home",
            "🔧 Book Service",
            "🚨 Emergency Assistance",
            "📋 My Bookings",
            "⭐ Rate Service"
        ]
    )

    # -----------------------------------------------------

    if menu == "🏠 Home":

        st.header(
            "What service do you need?"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.info(
                """
                🏗️ **Construction**

                • Mason  
                • Carpenter  
                • Painter  
                • Labour  
                • Plumber
                """
            )

        with col2:

            st.info(
                """
                🏠 **Home Appliances**

                • AC  
                • Refrigerator  
                • Washing Machine  
                • Electrical Repair
                """
            )

        with col3:

            st.error(
                """
                🚗 **Roadside Assistance**

                • Puncture  
                • Battery  
                • Mechanic  
                • Towing
                """
            )

    # -----------------------------------------------------

    elif menu == "🔧 Book Service":

        st.header(
            "🔧 Book a Service"
        )

        problem = st.text_area(
            "Describe your problem",
            placeholder=
            "Example: My AC is not cooling..."
        )

        location = st.text_input(
            "Your Location"
        )

        if st.button(
            "🤖 Detect Required Service"
        ):

            if not problem:

                st.warning(
                    "Please describe your problem."
                )

            else:

                service = detect_service(problem)

                st.session_state.detected_service = service

                st.success(
                    f"AI detected service: **{service}**"
                )

        service = st.session_state.get(
            "detected_service",
            "General Service"
        )

        st.write(
            f"Selected Service: **{service}**"
        )

        if st.button(
            "🔎 Find Available Workers"
        ):

            providers = find_providers(service)

            if not providers:

                st.warning(
                    "No available provider found."
                )

            else:

                st.success(
                    f"{len(providers)} provider(s) found."
                )

                for provider in providers:

                    with st.container(
                        border=True
                    ):

                        st.subheader(
                            provider["name"]
                        )

                        st.write(
                            f"🛠️ Skills: "
                            f"{', '.join(provider['skills'])}"
                        )

                        st.write(
                            f"📍 City: "
                            f"{provider['city']}"
                        )

                        st.write(
                            f"⭐ Rating: "
                            f"{provider['rating']}"
                        )

                        st.write(
                            f"📞 Phone: "
                            f"{provider['phone']}"
                        )

                        if st.button(
                            "📅 Book Provider",
                            key=provider["id"]
                        ):

                            booking = {

                                "id":
                                str(uuid.uuid4()),

                                "customer":
                                user["username"],

                                "customer_name":
                                user["name"],

                                "provider":
                                provider["username"],

                                "provider_name":
                                provider["name"],

                                "service":
                                service,

                                "problem":
                                problem,

                                "location":
                                location,

                                "status":
                                "Pending",

                                "date":
                                datetime.now().strftime(
                                    "%Y-%m-%d %H:%M"
                                ),

                                "rating":
                                None
                            }

                            data["bookings"].append(
                                booking
                            )

                            save_data(data)

                            st.success(
                                "Booking request sent!"
                            )

    # -----------------------------------------------------

    elif menu == "🚨 Emergency Assistance":

        st.header(
            "🚨 24×7 Emergency Roadside Assistance"
        )

        st.warning(
            "For genuine roadside emergencies, "
            "use this service."
        )

        emergency = st.selectbox(
            "Select Problem",
            [
                "Car Puncture",
                "Bike Puncture",
                "Tyre Problem",
                "Battery Dead",
                "Vehicle Breakdown",
                "Fuel Assistance",
                "Towing"
            ]
        )

        location = st.text_input(
            "📍 Current Location"
        )

        details = st.text_area(
            "Additional Details"
        )

        if st.button(
            "🚨 Find Emergency Assistance",
            use_container_width=True
        ):

            service_map = {

                "Car Puncture":
                "Puncture Repair",

                "Bike Puncture":
                "Puncture Repair",

                "Tyre Problem":
                "Puncture Repair",

                "Battery Dead":
                "Battery Assistance",

                "Vehicle Breakdown":
                "Mechanic",

                "Fuel Assistance":
                "General Service",

                "Towing":
                "Towing Service"
            }

            service = service_map[emergency]

            providers = find_providers(service)

            if providers:

                st.success(
                    f"Found {len(providers)} available provider(s)."
                )

                for provider in providers:

                    with st.container(
                        border=True
                    ):

                        st.subheader(
                            f"🚗 {provider['name']}"
                        )

                        st.write(
                            f"⭐ {provider['rating']}"
                        )

                        st.write(
                            f"📞 {provider['phone']}"
                        )

                        if st.button(
                            "🚨 Request Help",
                            key=
                            "emergency_"
                            + provider["id"]
                        ):

                            booking = {

                                "id":
                                str(uuid.uuid4()),

                                "customer":
                                user["username"],

                                "customer_name":
                                user["name"],

                                "provider":
                                provider["username"],

                                "provider_name":
                                provider["name"],

                                "service":
                                service,

                                "problem":
                                emergency
                                + " - "
                                + details,

                                "location":
                                location,

                                "status":
                                "Emergency Requested",

                                "date":
                                datetime.now().strftime(
                                    "%Y-%m-%d %H:%M"
                                ),

                                "rating":
                                None
                            }

                            data["bookings"].append(
                                booking
                            )

                            save_data(data)

                            st.success(
                                "🚨 Emergency request sent!"
                            )

            else:

                st.error(
                    "No emergency provider is "
                    "currently available."
                )

    # -----------------------------------------------------

    elif menu == "📋 My Bookings":

        st.header(
            "📋 My Bookings"
        )

        bookings = [

            b for b in data["bookings"]

            if b["customer"] ==
            user["username"]

        ]

        if not bookings:

            st.info(
                "You have no bookings yet."
            )

        for booking in bookings:

            with st.container(
                border=True
            ):

                st.write(
                    f"### {booking['service']}"
                )

                st.write(
                    f"Provider: "
                    f"{booking['provider_name']}"
                )

                st.write(
                    f"Problem: "
                    f"{booking['problem']}"
                )

                st.write(
                    f"Location: "
                    f"{booking['location']}"
                )

                st.write(
                    f"Status: "
                    f"**{booking['status']}**"
                )

                st.write(
                    f"Date: "
                    f"{booking['date']}"
                )

    # -----------------------------------------------------

    elif menu == "⭐ Rate Service":

        st.header(
            "⭐ Rate Completed Service"
        )

        bookings = [

            b for b in data["bookings"]

            if (
                b["customer"] ==
                user["username"]
                and
                b["status"] ==
                "Completed"
                and
                b["rating"] is None
            )
        ]

        if not bookings:

            st.info(
                "No completed services waiting for rating."
            )

        for booking in bookings:

            st.write(
                f"Service: **{booking['service']}**"
            )

            rating = st.slider(
                "Rating",
                1,
                5,
                5,
                key=booking["id"]
            )

            if st.button(
                "Submit Rating",
                key="rate_" + booking["id"]
            ):

                booking["rating"] = rating

                save_data(data)

                st.success(
                    "Thank you for your rating!"
                )


# =========================================================
# PROVIDER DASHBOARD
# =========================================================

def provider_dashboard():

    provider = st.session_state.user

    st.title(
        f"👷 Provider Dashboard — {provider['name']}"
    )

    menu = st.sidebar.radio(
        "Provider Menu",
        [
            "📊 Dashboard",
            "📋 Job Requests",
            "⚙️ Availability",
            "💰 My Work"
        ]
    )

    # -----------------------------------------------------

    if menu == "📊 Dashboard":

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Rating",
                provider["rating"]
            )

        with col2:

            st.metric(
                "Jobs",
                provider["jobs"]
            )

        with col3:

            st.metric(
                "Availability",
                "Available"
                if provider["available"]
                else "Busy"
            )

    # -----------------------------------------------------

    elif menu == "📋 Job Requests":

        st.header(
            "📋 Incoming Requests"
        )

        requests = [

            b for b in data["bookings"]

            if b["provider"] ==
            provider["username"]

        ]

        if not requests:

            st.info(
                "No requests available."
            )

        for booking in requests:

            with st.container(
                border=True
            ):

                st.write(
                    f"### {booking['service']}"
                )

                st.write(
                    f"Customer: "
                    f"{booking['customer_name']}"
                )

                st.write(
                    f"Problem: "
                    f"{booking['problem']}"
                )

                st.write(
                    f"Location: "
                    f"{booking['location']}"
                )

                st.write(
                    f"Status: "
                    f"{booking['status']}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    if booking["status"] in [
                        "Pending",
                        "Emergency Requested"
                    ]:

                        if st.button(
                            "✅ Accept",
                            key=
                            "accept_"
                            + booking["id"]
                        ):

                            booking["status"] = "Accepted"

                            save_data(data)

                            st.success(
                                "Request accepted."
                            )

                with col2:

                    if booking["status"] == "Accepted":

                        if st.button(
                            "🔧 Complete",
                            key=
                            "complete_"
                            + booking["id"]
                        ):

                            booking["status"] = "Completed"

                            provider["jobs"] += 1

                            save_data(data)

                            st.success(
                                "Job completed."
                            )

                with col3:

                    if booking["status"] in [
                        "Pending",
                        "Emergency Requested"
                    ]:

                        if st.button(
                            "❌ Reject",
                            key=
                            "reject_"
                            + booking["id"]
                        ):

                            booking["status"] = "Rejected"

                            save_data(data)

                            st.warning(
                                "Request rejected."
                            )

    # -----------------------------------------------------

    elif menu == "⚙️ Availability":

        st.header(
            "⚙️ Availability"
        )

        status = st.toggle(
            "Available for new jobs",
            value=provider["available"]
        )

        provider["available"] = status

        save_data(data)

        if status:

            st.success(
                "You are currently AVAILABLE."
            )

        else:

            st.warning(
                "You are currently OFFLINE."
            )

    # -----------------------------------------------------

    elif menu == "💰 My Work":

        st.header(
            "💰 Work Summary"
        )

        st.metric(
            "Completed Jobs",
            provider["jobs"]
        )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_dashboard():

    st.title(
        "👨‍💼 Admin Dashboard"
    )

    menu = st.sidebar.radio(
        "Admin Menu",
        [
            "📊 Overview",
            "👥 Users",
            "👷 Providers",
            "📋 Bookings"
        ]
    )

    # -----------------------------------------------------

    if menu == "📊 Overview":

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Customers",
                len(data["users"])
            )

        with col2:

            st.metric(
                "Providers",
                len(data["providers"])
            )

        with col3:

            st.metric(
                "Bookings",
                len(data["bookings"])
            )

        with col4:

            completed = len([
                b for b in data["bookings"]
                if b["status"] == "Completed"
            ])

            st.metric(
                "Completed",
                completed
            )

    # -----------------------------------------------------

    elif menu == "👥 Users":

        st.header(
            "Registered Customers"
        )

        for user in data["users"]:

            st.write(
                f"👤 {user['name']} "
                f"— {user['city']}"
            )

    # -----------------------------------------------------

    elif menu == "👷 Providers":

        st.header(
            "Service Providers"
        )

        for provider in data["providers"]:

            with st.container(
                border=True
            ):

                st.write(
                    f"👷 {provider['name']}"
                )

                st.write(
                    f"Skills: "
                    f"{', '.join(provider['skills'])}"
                )

                st.write(
                    f"Rating: "
                    f"{provider['rating']}"
                )

                st.write(
                    f"Available: "
                    f"{provider['available']}"
                )

    # -----------------------------------------------------

    elif menu == "📋 Bookings":

        st.header(
            "All Bookings"
        )

        for booking in data["bookings"]:

            st.write(
                f"""
                **{booking['service']}**

                Customer: {booking['customer_name']}

                Provider: {booking['provider_name']}

                Status: {booking['status']}

                Date: {booking['date']}
                """
            )

            st.divider()


# =========================================================
# LOGOUT
# =========================================================

def logout():

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None

        st.rerun()


# =========================================================
# MAIN APPLICATION
# =========================================================

if not st.session_state.logged_in:

    authentication()

else:

    logout()

    if st.session_state.role == "Customer":

        customer_dashboard()

    elif st.session_state.role == "Service Provider":

        provider_dashboard()

    elif st.session_state.role == "Admin":

        admin_dashboard()