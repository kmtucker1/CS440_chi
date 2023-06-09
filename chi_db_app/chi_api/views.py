from django.db import connections
from django.shortcuts import render, redirect

from django.http import HttpResponse

from chi_api.models import Vehicle, Customer, Employee, VehicleTransaction
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from django.db import connection
from django.http import HttpResponse
from django.template import loader


def home_page(request):
    template = loader.get_template("chi_api/home_page.html")
    return HttpResponse(template.render(request=request))


def vehicle_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM vehicle WHERE active=1')
        rows = cursor.fetchall()
        vehicles = []
        for row in rows:
            vehicle = {
                'vehicle_id': row[0],
                'vin': row[1],
                'make': row[2],
                'model': row[3],
                'year': row[4],
                'trim': row[5],
                'color': row[6],
                'mpg': row[7],
                'country_of_assembly': row[8],
                'mileage': row[9]
            }
            vehicles.append(vehicle)

    template = loader.get_template('chi_api/vehicle_list.html')
    context = {
        'vehicle_list': vehicles,
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def vehicle_form(request):
    if request.method == 'POST':
        vin = request.POST.get('vin', '')
        make = request.POST.get('make', '')
        model = request.POST.get('model', '')
        year = request.POST.get('year', '')
        trim = request.POST.get('trim', '')
        color = request.POST.get('color', '')
        mpg = request.POST.get('mpg', '')
        mileage = request.POST.get('mileage', '')
        country_of_assembly = request.POST.get('country_of_assembly', '')
        active = 1
        cursor = connections['default'].cursor()
        db_response = cursor.execute("INSERT INTO vehicle "
                                     "(vin, make, model, year, trim, color, mpg, mileage, country_of_assembly, active) "
                                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                     [vin, make, model, year, trim, color, mpg, mileage, country_of_assembly, active])
        return redirect('vehicle_list')

    template = loader.get_template('chi_api/vehicle_form.html')
    return HttpResponse(template.render(request=request))

def update_vehicle(request, id):
    vehicle = Vehicle.objects.get(pk=id)

    if request.method == 'POST':
        make = request.POST.get('make', '')
        model = request.POST.get('model', '')
        year = request.POST.get('year', '')
        trim_level = request.POST.get('trim', '')
        color = request.POST.get('color', '')
        mpg = request.POST.get('mpg', '')
        assembly = request.POST.get('country_of_assembly', '')
        mileage = request.POST.get('mileage', '')


        cursor = connections['default'].cursor()
        db_response = cursor.execute(
            "UPDATE vehicle "
            "SET make = %s, model = %s, year = %s, trim = %s, color = %s, mpg = %s, country_of_assembly = %s, mileage = %s "
            "WHERE vehicle_id = %s",
            [make, model, year, trim_level, color, mpg, assembly, mileage, id]
        )

        return redirect('vehicle', id=id)

    context = {'vehicle': vehicle}
    return render(request, 'chi_api/update_vehicle.html', context)


def vehicle(request, id):
    # Fetch the vehicle using raw SQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vehicle WHERE vehicle_id = %s", [id])
        row = cursor.fetchone()
        if not row:
            return HttpResponse("Vehicle not found", status=404)

        vehicle = {
            'vehicle_id': row[0],
            'vin': row[1],
            'make': row[2],
            'model': row[3],
            'year': row[4],
            'trim': row[5],
            'color': row[6],
            'mpg': row[7],
            'country_of_assembly': row[8],
            'mileage': row[9]
        }

    # Fetch the vehicle histories using raw SQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vehicle_history WHERE vehicle_id = %s", [id])
        history_rows = cursor.fetchall()
        histories = []
        for row in history_rows:
            history = {
                'history_id': row[0],
                'history_type': row[1],
                'description': row[2],
                'history_date': row[3],
                'vehicle_id': row[4],
            }
            histories.append(history)

    template = loader.get_template("chi_api/vehicle.html")
    context = {
        "vehicle": vehicle,
        "histories": histories
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def add_vehicle_history(request, id):

    vehicle = Vehicle.objects.get(pk=id)

    if request.method == 'POST':
        history_type = request.POST.get('history_type', '')
        history_date = request.POST.get('history_date', '')
        description = request.POST.get('history_description', '')

        cursor = connections['default'].cursor()
        db_response = cursor.execute("INSERT INTO vehicle_history"
                                     "(history_type, history_date, description, vehicle_id)"
                                     "VALUES (%s, %s, %s, %s)", [history_type, history_date, description, id])

        return redirect('vehicle', id=id)

    context = {
        "vehicle": vehicle
    }
    return render(request, 'chi_api/add_vehicle_history.html', context)

@csrf_exempt
def add_transaction(request, id):

    customer = Customer.objects.get(pk=id)

    if request.method == 'POST':
        transaction_type = request.POST.get('transaction_type', '')
        sale_price = request.POST.get('sale_price', '')
        employee_name = request.POST.get('employee_name', '')
        vehicle_vin = request.POST.get('vehicle_vin', '')

        cursor = connections['default'].cursor()

        vehicle_id_query = "SELECT vehicle_id FROM vehicle WHERE vin = %s"
        cursor.execute(vehicle_id_query, [vehicle_vin])
        vehicle_result = cursor.fetchone()
        vehicle_id = vehicle_result[0] if vehicle_result else None

        employee_id_query = "SELECT employee_id FROM employee WHERE name = %s"
        cursor.execute(employee_id_query, [employee_name])
        employee_result = cursor.fetchone()
        employee_id = employee_result[0] if employee_result else None

        insert_query = "INSERT INTO vehicle_transaction (transaction_type, sale_price, customer_id, employee_id, vehicle_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, [transaction_type, sale_price, id, employee_id, vehicle_id])

        return redirect('customer', id=id)

    context = {
        'customer': customer
    }
    return render(request, 'chi_api/add_transaction.html', context)

def customer_list(request):
    cursor = connections['default'].cursor()

    cursor.execute("SELECT * FROM customer WHERE active = 1")
    customers = cursor.fetchall()
    template = loader.get_template('chi_api/customer_list.html')
    context = {
        "customer_list": customers
    }
    return HttpResponse(template.render(context, request))


def customer(request, id) :
    cursor = connections['default'].cursor()
    cursor.execute("SELECT * FROM customer "
                   "WHERE customer.customer_id = %s", [id])
    customer = cursor.fetchone()
    cursor.execute("SELECT * FROM vehicle_transaction "
                   "LEFT JOIN vehicle "
                   "ON vehicle_transaction.vehicle_id = vehicle.vehicle_id "
                   "LEFT JOIN employee "
                   "ON vehicle_transaction.employee_id = employee.employee_id " 
                   "WHERE customer_id = %s", [id])
    transactions = cursor.fetchall()
    template = loader.get_template('chi_api/customer.html')

    context = {
        "customer": customer,
        "transactions": transactions
    }
    return HttpResponse(template.render(context, request))

def employee_sales_stats(request, id):
    template = loader.get_template('chi_api/employee_sales_stats.html')

    cursor = connections['default'].cursor()

    cursor.execute("SELECT * FROM employee "
                   "WHERE employee_id = %s", [id])
    employee = cursor.fetchone()

    total_sales = cursor.execute("SELECT %s, SUM(sale_price) "
                                 "FROM vehicle_transaction "
                                 "WHERE employee_id = %s "
                                 "GROUP BY %s", [id, id, id])
    total_sales = cursor.fetchone()

    average_sales = cursor.execute("SELECT %s, ROUND(AVG(sale_price)) "
                                   "FROM vehicle_transaction "
                                   "WHERE employee_id = %s "
                                   "GROUP BY %s", [id, id, id])
    average_sales = cursor.fetchone()

    total_transactions = cursor.execute("SELECT %s, COUNT(sale_price) "
                                        "FROM vehicle_transaction "
                                        "WHERE employee_id = %s "
                                        "GROUP BY %s", [id, id, id])
    total_transactions = cursor.fetchone()

    context = {
        'employee': employee,
        'total_sales': total_sales,
        'average_sales': average_sales,
        'total_transactions': total_transactions
    }

    return HttpResponse(template.render(context, request))

def update_customer(request, id):
    customer = Customer.objects.get(pk=id)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        license_number = request.POST.get('license_number', '')
        license_state = request.POST.get('license_state', '')
        insurance_provider = request.POST.get('insurance_provider', '')
        policy_number = request.POST.get('policy_number', '')

        cursor = connections['default'].cursor()
        db_response = cursor.execute(
            "UPDATE customer "
            "SET name = %s, license_number = %s, license_state = %s, insurance_provider = %s, policy_number = %s "
            "WHERE customer_id = %s",
            [name, license_number, license_state, insurance_provider, policy_number, id]
        )

        return redirect('customer', id=id)

    context = {'customer': customer}
    return render(request, 'chi_api/update_customer.html', context)


@csrf_exempt
def customer_form(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        license_number = request.POST.get('license_number', '')
        license_state = request.POST.get('license_state', '')
        insurance_provider = request.POST.get('insurance_provider', '')
        policy_number = request.POST.get('policy_number', '')
        cursor = connections['default'].cursor()
        db_response = cursor.execute("INSERT INTO customer "
                                     "(name, license_number, license_state, insurance_provider, policy_number, active) "
                                     "VALUES (%s, %s, %s, %s, %s, 1)",
                                     [name, license_number, license_state, insurance_provider, policy_number])
        return HttpResponse('successfully submitted')

    template = loader.get_template('chi_api/customer_form.html')
    return HttpResponse(template.render(request=request))

def employee_list(request):
    cursor = connections['default'].cursor()

    cursor.execute("SELECT * FROM employee WHERE active = 1 ")
    employees = cursor.fetchall()
    template = loader.get_template('chi_api/employee_list.html')
    context = {
        "employee_list": employees
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def employee_search(request):
    if request.method == 'POST':
        employee_name = request.POST.get('employee_name', '')

        cursor = connections['default'].cursor()
        cursor.execute("SELECT employee_id FROM employee WHERE name = %s", [employee_name])
        employee_result = cursor.fetchone()

        if employee_result:
            employee_id = employee_result[0]
            return redirect('employee', id=employee_id)
        else:
            # Handle case when employee is not found
            # You can redirect to an appropriate page or display an error message
            return HttpResponse('Employee not found')

    template = loader.get_template('chi_api/employee_search.html')
    return HttpResponse(template.render(request=request))


def employee(request, id):
    cursor = connections['default'].cursor()
    cursor.execute("SELECT * FROM employee "
                   "WHERE employee_id = %s", [id])
    employee = cursor.fetchone()
    cursor.execute("SELECT * FROM vehicle_transaction "
                   "LEFT JOIN vehicle "
                   "ON  vehicle_transaction.vehicle_id = vehicle.vehicle_id "
                   "LEFT JOIN customer "
                   "ON  vehicle_transaction.customer_id = customer.customer_id "
                   "WHERE employee_id = %s", [id])
    transactions = cursor.fetchall()
    template = loader.get_template("chi_api/employee.html")

    context = {
        "employee": employee,
        "transactions": transactions
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def employee_form(request):
    if request.method == 'POST':
        employee_name = request.POST.get('employee_name', '')
        job_title = request.POST.get('job_title', '')
        salary = request.POST.get('salary', '')
        benefits = request.POST.get('benefits', '')
        cursor = connections['default'].cursor()
        db_response = cursor.execute("INSERT INTO employee "
            "(name, job_title, salary, benefits, active) "
            "VALUES (%s, %s, %s, %s, 1)",
            [employee_name, job_title, salary, benefits])
        return redirect("home")

    template = loader.get_template('chi_api/employee_form.html')
    return HttpResponse(template.render(request=request))


def employee_delete(request, employee_id):
    if request.method == 'POST':
        cursor = connections['default'].cursor()
        cursor.execute('UPDATE employee '
                       'SET active = 0 '
                       'WHERE employee_id = %s',
                       [employee_id])

        # Redirect to a home page
        return render(request, 'chi_api/home_page.html')

def update_employee(request, id):
    employee = Employee.objects.get(pk=id)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        job_title = request.POST.get('job_title', '')
        salary = request.POST.get('salary', '')
        benefits = request.POST.get('benefits', '')

        cursor = connections['default'].cursor()
        db_response = cursor.execute(
            "UPDATE Employee "
            "SET name = %s, job_title = %s, salary = %s, benefits = %s "
            "WHERE employee_id = %s",
            [name, job_title, salary, benefits, id]
        )

        return redirect('employee', id=id)

    context = {'employee': employee}
    return render(request, 'chi_api/update_employee.html', context)

def customer_delete(request, customer_id):
    if request.method == 'POST':
        cursor = connections['default'].cursor()
        cursor.execute('UPDATE customer '
                       'SET active = 0 '
                       'WHERE customer_id = %s',
                       [customer_id])

        # Redirect to a home page
        return render(request, 'chi_api/home_page.html')

@csrf_exempt
def delete_vehicle(request, id):
    cursor = connections['default'].cursor()

    # cursor.execute("DELETE FROM vehicles WHERE vin=?", (vehicle_id,))
    # cursor.execute("SELECT * FROM vehicles "
    #                "WHERE employee_id = %s", [id])

    cursor.execute( 'UPDATE vehicle '
    'SET active = 0 '
    'WHERE vehicle_id = %s', [id])


    return redirect('vehicle_list')

