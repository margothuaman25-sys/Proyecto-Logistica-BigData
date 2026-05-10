import pandas as pd
from faker import Faker
import random
from sqlalchemy import create_engine

# --- CONFIGURACIÓN DE DATOS ---
fake = Faker()
Faker.seed(42)

# 1. Generar Conductores (Drivers) - 250 registros
drivers = []
for i in range(1, 251):
    drivers.append({
        "driver_id": i,
        "name": fake.name(),
        "license_number": f"LIC-{fake.bothify(text='??-####')}",
        "phone": fake.phone_number(),
        "status": random.choice(["Active", "Inactive"])
    })

df_drivers = pd.DataFrame(drivers)

# 2. Generar Vehículos (Vehicles) - 150 registros
vehicles = []
for i in range(1, 151):
    vehicles.append({
        "vehicle_id": i,
        "plate": fake.bothify(text='???-####').upper(),
        "model": random.choice(["Volvo FH16", "Scania R500", "Freightliner Cascadia", "Mercedes-Benz Actros"]),
        "capacity_kg": random.randint(5000, 20000),
        "status": random.choice(["Operational", "Maintenance"])
    })

df_vehicles = pd.DataFrame(vehicles)

# --- CONEXIÓN A POSTGRESQL ---
try:
    # Usamos las credenciales: fleetlogix_user y fleetlogix123
    # Asegúrate de que el puerto sea 5432 (el estándar de Postgres)
    engine = create_engine('postgresql://fleetlogix_user:fleetlogix123@localhost:5432/fleetlogix')
    
    # Enviamos los DataFrames a las tablas en PostgreSQL
    df_drivers.to_sql('drivers', engine, if_exists='append', index=False)
    df_vehicles.to_sql('vehicles', engine, if_exists='append', index=False)
    
    print("¡Éxito total, bb! Los datos ya están en PostgreSQL.")
except Exception as e:
    print(f"Error de conexión: {e}")

# Guardar respaldos en archivos CSV
df_drivers.to_csv("drivers.csv", index=False)
df_vehicles.to_csv("vehicles.csv", index=False)