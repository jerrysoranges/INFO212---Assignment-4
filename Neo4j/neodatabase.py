from neo4j import GraphDatabase, Driver
import get_json

URI = "neo4j+s://0c592cb4.databases.neo4j.io"
AUTH = ("neo4j", "tfH_IqGREpH75q71bLA0D8_DAG3fzzKXUeXxASeC41c")

def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver


def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties


# Bil-metodar

def create_car(car_id, make, model, year, location, status):
    with _get_connection().session as session:
        cars = session.run(
            "Merge (a: Car{car_id:$car_id, make:$make, model:$model, year:$year, location:$location, status:$status})RETURN a;",
            car_id=car_id, make=make, model = model, year = year, location=location, status = status
        )

        nodes_json = [node_to_json(record["a"])for record in cars]
        return nodes_json

'''
def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties
'''

def listAllCars():
    with _get_connection().session() as session:
        cars = session.run("MATCH (a: Car) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json


def listRegisteredCar(car_id):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a: Car) where a.car_id=$car_id RETURN a;", car_id=car_id)
        print(cars)
        nodes_json = [node_to_json(record["a"]) for record in cars]
    
    print(nodes_json)


def save_car(make, model, car_id, year, status, location):
    with _get_connection().session() as session:
        cars = session.run(
            "MERGE (a:Car{make:$make, model:$model, year:$year, location:$location, status:$status})RETURN a;",
            make = make, model = model, year = year, location = location, status = status)
    nodes_json = [node_to_json(record["a"] for record in car)]
    return nodes_json


def update_car(make, model, car_id, year, status, location):
    with _get_connection.session() as session:
        cars = session.run("MATCH (a:Car{car_id:$car_id}) set a.make=$make, a.model=$model, a.year=$year, a.status=$status, a.location=$location RETURN a;",
        car_id=car_id, make=make, model=model, year=year, status=status, location = location)

    print(cars)
    nodes_json = [node_to_json(record["a"]) for record in cars]
    print(nodes_json)
    return nodes_json


def delete_car(car_id):
    _get_connection().execute_query("MATCH (a:Car{car_id: $car_id}) delete a;", car_id = car_id)


# Kunde-metodar

def create_customer(customer_id, name, age, address):
    with _get_connection().session() as session:
        customer = session.run(
            "MERGE (a:Customer{customer_id:$customer_id, name:$name, age:$age, address:$address})RETURN a;",
            customer_id=customer_id, name = name, age = age, address = address
        )
        nodes_json = [node_to_json(record["a"]) for record in customer]
        return nodes_json


def list_customers():
    with _get_connection().session() as session:
        customer = session.run("MATCH (a:Customer) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in customers]
        return nodes_json


def update_customer(customer_id, name, age, address):
    with _get_connection().session() as session:
        customers = session.run("MATCH (a:Customer{customer_id:$customer_id}) set a.name=$name, a.age=$age, a.address = $address RETURN a;",
            name = name, age = age, address = address)
        print(customers)
        nodes_json = [node_to_json(record["a"]) for record in customers]
        print(nodes_json)
        return nodes_json


def delete_customer(customer_id):
    _get_connection().execute_query("MATCH (a:Customer{name: $name}) delete a;", customer_id = customer_id)
    return delete_customer




# Ansatte

def create_employee(employee_id, name, address, branch):


    employees = _get_connection().execute_query("MERGE (a:Employee{employee_id:$employee_id, name:$name, address:$address, branch:$branch})RETURN a;",
    employee_id = employee_id, name = name, address = address, branch = branch)
    nodes:json = [node_to_json(record["a"]) for record in employees]
    return nodes_json


def list_employees():
    with _get_connection().session() as session:
        employees = session.run("MATCH (a:Employee) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in employees]
        return nodes_json


def update_employee(employee_id, name, address, branch):
    with _get_connection().session() as session:
        employees = session.run("MATCH (a:Employee{employee_id:$employee_id}) set a.name=$name, a.address=$address, a.branch=$branch RETURN a;",
        employee_id = employee_id, name = name, address = address, branch = branch)
        nodes_json = [node_to_json(record["a"]) for record in employees]
        return nodes_json


def delete_employee(employee_id):
    _get_connection().execute_query("MATCH (a:Employee{employee_id:$employee_id}) delete a;", employee_id=employee_id)


# Order a car

def order_car(customer_id, car_id):
    with _get_connection().session() as session:

        car = session.run(
            "MATCH (a:CAR {car_id: $car_id})"
            "RETURN a.status as status;",
            car_id=car_id).single()



        if car and car["status"] != "available":
            return {"error": "This car isn't available. "}, 400

        
        last_order = session.run(
            "MATCH (c:Customer {customer_id: $customer_id}) - [:ORDERED] -> (a:Car) "
            "RETURN a LIMIT 1;",
            customer_id = customer_id).single()

        if last_order:
            return {"error": "This customer has already ordered a car. "}, 400

        session.run(
            "MATCH (c:Customer {customer_id: $customerid}, (a:Car {car_id: $car_id}) "
            "MERGE (c) - [:ORDERED] -> (a)"
            "SET a.status = 'booked'"
            "RETURN c, a;",
            customer_id=customer_id, car_id=car_id)

        return {"status": "The car has been ordered. Status: Ordered! "}


        # Avbestille

def cancel_car_order(customer_id, car_id):
    with _get_connection().session() as session:
        order = session.run(
            "MATCH (c:Customer {customer_id: $customer_id}) - [r:ORDERED] -> (a:Car {car_id: $car_id}) "
            "RETURN r;",
            customer_id=customer_id, car_id=car_id).single()

        if not order:
            return {"Error ": "No order found. "}, 400


        session.run(
            "MATCH (c:Customer {customer_id: $customer_id}) - [r:ORDERED] -> (a:Car {car_id: $car_id})"
            "DELETE r "
            "SET a.status = 'Available'. "
            "RETURN c, a;",
            customer_id=customer_id, car_id=car_id)

        return {"status": "The order has been cancelled. Car Status: Available. "}

# Leie bil

def rent_car(customer_id, car_id):
    with _get_connection().session() as session:
        
        booking = session.run(
            "MATCH (c:Customer {customer_id: $customer_id}) - [r:ORDERED] -> (a:Car {car_id: $car_id})"
            "RETURN a;",
            customer_id=customer_id, car_id=car_id).single()

        if not booking:
            return {"Error": "The customer has not booked this car. "}, 400

        session.run(
            "MATCH (c:Customer {customer_id: $customer_id}) - [:RENTED] -> (a:Car {car_id: $car_id})"
            "SET a.status = 'rented' "
            "RETURN a;",
            customer_id=customer_id, car_id=car_id)


        return {"Status": "Car has been successfully rented. Status: RENTED! "}


def return_car(customer_id, car_id, return_status):
    with _get_connection().session() as session:
        rental = session.run(
            "MATCH (c:Customer {customer_id: $customer_id} - [ORDERED/RENTED]->(a:Car {car_id: $car_id})"
            "RETURN a;",
            customer_id = customer_id, car_id=car_id).single()

        if not rental:
            return {"error": "This customer has not rented this car. "}, 400

        if return_status == "OK":
            new_status = "Available. "

        elif return_status == "Damaged. ":
            new_status = "Damaged. "
        
        else:
            return {"Error": "Invalid. "}, 400


        session.run(
            "MATCH (c:Customer {customer_id: $customer_id} - [ORDERED/RENTED]->(a:Car {car_id: $car_id})"
            "DELETE r "
            "SET a.status = $new_status "
            "RETURN a;",
            customer_id=customer_id, car_id=car_id, new_status=new_status
        )
        

        return {"Status": f"Car has been successfully returned. Status: {new_status}"}