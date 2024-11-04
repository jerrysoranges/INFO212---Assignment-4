from flask import flask, request
from neo4j import GraphDatabase


app = Flask(__name__)


# Bilar

@app.route("/new_car", methods=["POST"])
def create_car_data():
    data = request.get_json()
    return create_car((data["car_id"]), data["make"], data["model"], data["year"], data["location"], data["status"])

@app.route("/update_car", methods=["PUT"])
def update_car_data():
    data = request.get_json()
    return update_car((data["car_id"]), data["make"], data["model"], data["year"], data["location"], data["status"])

@app.route("/cars", methods=["GET"])
def find_car():
    data = request.get_json()
    return showAllCars

@app.route("/cars", methods=["DELETE"])
def delete_car_data():
    data = request.get_json()
    print(data)
    delete_car(data["car_id"])
    return showAllCars()


# Kundar

@app.route("/create_customer", methods=["POST"])
def create_customer_data():
    data = request.get_json()
    print(data)
    return create_customer(data["name"], data["age"], data["address"])

@app.route("/update_customer", methods=["PUT"])
def update_customer_data():
    data = request.get_json()
    print(data)
    return update_customer(data["name"], data["age"], data["address"])

@app.route("/delete_customer", methods=["DELETE"])
def delete_customer_data():
    data = request.get_json()
    print(data)
    delete_customer(data["name"])
    return data_customer()


# Ansatte

@app.route("/employee", methods=[POST])
def create_employee_data():
    data = request.get_json()
    print(data)
    return create_employee(data["employee_id"], data["name"], data["address"], data["branch"])

@app.route("/update_employee", methods=["PUT"])
def update_employee_data():
    data = request.get_json()
    print(data)
    return update_employee(data["name"], data["address"], data["branch"])

@app.route("/delete_employee", methods=["DELETE"])
def delete_employee_data():
    data = request.get_json()
    print(data)
    delete_employee(data["name"])
    return listAllEmployees()

@app.route("/show_employee", method=["GET"])
def show_employee_data():
    data = request.get_json()
    print(data)
    return findEmployeeName(data["name"])

@app.route("/cancel_car_order", method=["POST"])
def cancel_car_order(customer_id, car_id):
    cars_rented = showRentedCarsCustomer(Customer.customer_id)
    if booked_cars:
        delete_customer(customer_id)
        delete_car(car_id)
    else: return 0

@app.route("/rent_car", method=["POST"])
def rent_car(customer_id, car_id):
    cars_rented = showRentedCarsCustomer(Customer.customer_id)
    if cars_rented:
        update_car(car_id.make, car_id.model, car_id.reg, car_id.year, car_id.new_CarStatus(rented), car_id.location)
    
    else: return 0

@app.route("/return_car", method=["POST"])
def return_car(customer_id, car_id):
    cars_rented = showRentedCarsCustomer(Customer.customer_id)
    if cars_rented:
        update_car(car_id.make, car_id.model, car_id.reg, car_id_year, car_id.new_CarStatus(available), car_id.location)

    else: return 0

if __name__ == "__main__":
    app.run(debug=True)
