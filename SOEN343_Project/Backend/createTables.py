import sqlite3

connection = sqlite3.connect("database.db")
print("Connected to Database")

connection.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customerID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    phoneNumber TEXT,
    email TEXT
)
''')
print('Users table created successfully')

connection.execute('''
CREATE TABLE IF NOT EXISTS deliveryAgents (
    agentID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    email TEXT,
    phoneNumber TEXT,
    vehicleType TEXT,
    licensePlate TEXT
)
''')
print('Delivery Agents table created successfully')

connection.execute('''
CREATE TABLE IF NOT EXISTS addresses(
    addressID INTEGER PRIMARY KEY AUTOINCREMENT,
    Street TEXT,
    houseNumber INTEGER,
    apartmentNumber INTEGER,
    postalCode TEXT
)
''')
print('Addresses table successfully created.')

connection.execute('''
CREATE TABLE IF NOT EXISTS orders(
    orderID INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT,
    ETA TEXT,
    addressID INTEGER,
    customerID INTEGER,
    FOREIGN KEY (addressID) REFERENCES addresses(addressID),
    FOREIGN KEY (customerID) REFERENCES customers(customerID)
)
''')
print('Orders table created successfully')

connection.execute('''
CREATE TABLE IF NOT EXISTS packages(
    packageID INTEGER PRIMARY KEY AUTOINCREMENT,
    packageType TEXT,
    weight INTEGER,
    dimensions TEXT,
    state TEXT,
    Eta TEXT,
    orderID INTEGER,
    FOREIGN KEY (orderID) REFERENCES orders(orderID)
)
''')
print('Packages table created successfully')

# Create other tables such as Quotation, Tracker, DeliveryRequest when needed.
# Remember to add them above the orders table so that you can add foreign keys into the orders table.

connection.close()
