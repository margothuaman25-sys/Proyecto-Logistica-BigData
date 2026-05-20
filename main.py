import psycopg2
from psycopg2.extras import execute_batch
from faker import Faker
import random
from datetime import datetime, timedelta
import numpy as np

fake = Faker('es_CO') # Usamos español para que las direcciones se vean reales

def cargar_datos_fleetlogix_pro():
    conn = None
    try:
        # 1. CONEXIÓN (Asegúrate de que tu password sea la correcta)
        conn = psycopg2.connect(
            host="localhost", 
            database="fleetlogix", 
            user="postgres", 
            password="hDiosfe7" 
        )
        cur = conn.cursor()
        print("🚀 Iniciando carga profesional de 505,000 registros...")

        # 2. LIMPIEZA TOTAL (RESTART IDENTITY para que los IDs empiecen en 1)
        print("🧹 Limpiando tablas...")
        cur.execute("TRUNCATE TABLE deliveries, maintenance, trips, routes, drivers, vehicles RESTART IDENTITY CASCADE;")
        
        # 3. VEHÍCULOS (200)
        print("📦 Insertando 200 Vehículos...")
        vehicles_data = []
        for i in range(1, 201):
            v_type = random.choice(['Truck', 'Heavy Van', 'Trailer', 'Motorcycle'])
            capacity = 15000 if v_type == 'Trailer' else (5000 if v_type == 'Truck' else 1500)
            vehicles_data.append((
                i, fake.unique.bothify(text='??-####').upper(), v_type, 
                capacity, random.choice(['Diesel', 'Electric', 'Gas']), fake.date_this_decade()
            ))
        execute_batch(cur, "INSERT INTO vehicles (vehicle_id, license_plate, vehicle_type, capacity_kg, fuel_type, acquisition_date) VALUES (%s, %s, %s, %s, %s, %s)", vehicles_data)

        # 4. CONDUCTORES (400)
        print("👤 Insertando 400 Conductores...")
        drivers_data = []
        for i in range(1, 401):
            drivers_data.append((
                i, f'EMP-{i:04d}', fake.first_name(), fake.last_name(), 
                fake.unique.bothify(text='LIC-########'), fake.date_this_decade()
            ))
        execute_batch(cur, "INSERT INTO drivers (driver_id, employee_code, first_name, last_name, license_number, hire_date) VALUES (%s, %s, %s, %s, %s, %s)", drivers_data)
            
        # 5. RUTAS (50)
        print("🗺️ Insertando 50 Rutas...")
        routes_data = []
        ciudades = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cusco', 'Lima']
        for i in range(1, 51):
            routes_data.append((
                i, f'RT-{i:03d}', random.choice(ciudades), random.choice(ciudades), random.randint(100, 1200)
            ))
        execute_batch(cur, "INSERT INTO routes (route_id, route_code, origin_city, destination_city, distance_km) VALUES (%s, %s, %s, %s, %s)", routes_data)
        
        conn.commit() 

        # 6. TRIPS (100,000)
        print("✈️ Generando 100,000 Trips...")
        sql_trips = """INSERT INTO trips (trip_id, vehicle_id, driver_id, route_id, departure_datetime, 
                       arrival_datetime, fuel_consumed_liters, total_weight_kg, status) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        for i in range(0, 100000, 10000):
            batch_trips = []
            for j in range(i, i + 10000):
                dep_time = fake.date_time_this_year()
                arr_time = dep_time + timedelta(hours=random.randint(2, 24))
                batch_trips.append((
                    j + 1, random.randint(1, 200), random.randint(1, 400), random.randint(1, 50), 
                    dep_time, arr_time, round(random.uniform(40.0, 350.0), 2), 
                    round(random.uniform(500.0, 8000.0), 2), 'Completed'
                ))
            execute_batch(cur, sql_trips, batch_trips)
            print(f"   ✅ {i + 10000} viajes cargados...")

        # 7. DELIVERIES (400,000)
        print("📦 Generando 400,000 Deliveries (Esto puede tardar un poco)...")
        sql_del = """INSERT INTO deliveries (trip_id, tracking_number, customer_name, delivery_address, package_weight_kg, delivery_status) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
        
        for i in range(0, 400000, 20000):
            batch_del = []
            for _ in range(20000):
                batch_del.append((
                    random.randint(1, 100000), fake.unique.bothify(text='TRK-##########'), 
                    fake.name(), fake.address().replace('\n', ' '), 
                    round(random.uniform(1.0, 50.0), 2), 'Delivered'
                ))
            execute_batch(cur, sql_del, batch_del)
            print(f"   ✅ {i + 20000} entregas cargadas...")

        # 8. MAINTENANCE (5,000)
        print("🛠️ Insertando 5,000 registros de Mantenimiento...")
        sql_maint = """INSERT INTO maintenance (vehicle_id, maintenance_date, maintenance_type, cost) 
                       VALUES (%s, %s, %s, %s)"""
        batch_maint = [
            (random.randint(1, 200), fake.date_this_year(), 
             random.choice(['Oil Change', 'Tires', 'Engine Check', 'Brakes']), 
             round(random.uniform(100.0, 1500.0), 2)) 
            for _ in range(5000)
        ]
        execute_batch(cur, sql_maint, batch_maint)

        conn.commit()
        print("\n✨ ¡CARGA PROFESIONAL EXITOSA! ✨")
        print(f"Total registros: {200+400+50+100000+400000+5000:,}")

    except Exception as e:
        print(f"❌ Error durante la carga: {e}")
        if conn: conn.rollback()
    finally:
        if conn: 
            cur.close()
            conn.close()

if __name__ == "__main__":
    cargar_datos_fleetlogix_pro()