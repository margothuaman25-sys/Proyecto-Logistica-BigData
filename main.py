import psycopg2
from psycopg2.extras import execute_batch
from faker import Faker
import random

fake = Faker()

def cargar_datos_final():
    conn = None
    try:
        # CONEXIÓN
        conn = psycopg2.connect(
            host="localhost", database="fleetlogix", user="postgres", password="hDiosfe7"
        )
        cur = conn.cursor()
        print("🚀 Conexión exitosa. Iniciando carga de precisión de 505k...")

        # A. POBLAR MAESTROS (650 registros)
        print("Cargando Maestros...")
        for _ in range(200):
            cur.execute("INSERT INTO vehicles (license_plate, vehicle_type, capacity_kg) VALUES (%s, %s, %s)",
                        (fake.unique.bothify(text='??-####-##'), random.choice(['Truck', 'Van', 'Motorcycle']), random.randint(500, 15000)))
        
        for _ in range(400):
            cur.execute("INSERT INTO drivers (full_name, license_number, hire_date) VALUES (%s, %s, %s)",
                        (fake.name(), fake.unique.bothify(text='LIC-########'), fake.date_this_decade()))
        
        for _ in range(50):
            cur.execute("INSERT INTO routes (origin, destination, estimated_distance_km) VALUES (%s, %s, %s)",
                        (fake.city(), fake.city(), random.uniform(50, 1200)))
        
        conn.commit()

        # B. POBLAR TRANSACCIONALES (505,000 registros exactos)
        # 1. Trips (100,000)
        print("Insertando 100,000 Trips...")
        sql_trips = "INSERT INTO trips (vehicle_id, driver_id, route_id, start_date, status) VALUES (%s, %s, %s, %s, %s)"
        for i in range(0, 100000, 10000):
            batch = [(random.randint(1, 200), random.randint(1, 400), random.randint(1, 50), 
                      fake.date_time_this_year(), 'Completed') for _ in range(10000)]
            execute_batch(cur, sql_trips, batch)
            print(f"   - Procesados: {i + 10000}/100000")

        # 2. Deliveries (400,000)
        print("Insertando 400,000 Deliveries...")
        sql_del = "INSERT INTO deliveries (trip_id, customer_name, delivery_status) VALUES (%s, %s, %s)"
        for i in range(0, 400000, 20000):
            batch = [(random.randint(1, 100000), fake.name(), 'Delivered') for _ in range(20000)]
            execute_batch(cur, sql_del, batch)
            print(f"   - Procesados: {i + 20000}/400000")

        # 3. Maintenance (5,000)
        print("Insertando 5,000 Maintenance...")
        batch_maint = [(random.randint(1, 200), fake.date_this_year(), random.uniform(50, 2000)) for _ in range(5000)]
        execute_batch(cur, "INSERT INTO maintenance (vehicle_id, maintenance_date, cost) VALUES (%s, %s, %s)", batch_maint)

        conn.commit()
        print("\n✨ ¡TODO CARGADO PERFECTAMENTE MARGOT BB! ✨")

    except Exception as e:
        print(f"❌ Error: {e}")
        if conn: conn.rollback()
    finally:
        if conn: cur.close(); conn.close()

if __name__ == "__main__":
    cargar_datos_final()