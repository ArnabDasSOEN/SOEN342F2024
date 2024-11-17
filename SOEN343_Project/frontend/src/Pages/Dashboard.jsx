import { Link } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import './CSS/dashboard.css'

export const Dashboard = () => {

    //how the data should look
    // "customer_id": "{{customerId}}",
    // "pick_up_address": {
    //     "street": "123 Main St",
    //     "house_number": "123",
    //     "apartment_number": "2B",
    //     "postal_code": "12345",
    //     "city": "New York",
    //     "country": "USA"
    // },
    // "drop_off_address": {
    //     "street": "456 Elm St",
    //     "house_number": "456",
    //     "apartment_number": "4A",
    //     "postal_code": "67890",
    //     "city": "Los Angeles",
    //     "country": "USA"
    // },
    // "package": {
    //     "unit_system": "imperial",
    //     "width_in_in": 10,
    //     "length_in": 20,
    //     "height_in": 5,
    //     "weight_lb": 30,
    //     "is_fragile": true,
    //     "package_items": [
    //         {
    //             "item_description": "Glass Vase",
    //             "quantity": 2,
    //             "weight_lb": 1.5
    //         },
    //         {
    //             "item_description": "Fragile Sculpture",
    //             "quantity": 1,
    //             "weight_lb": 2.0
    //         }
    //     ]
    // },

    const [packageItem, setPackageItem] = useState({
        item_description: "",
        quantity: 0,
        weight_lb: 0
    });
    const handlePackageItemChange = (e) => {
        //the value attribute here isn't the same as the one defined in the value={packageItem.item_description}
        //the value tag in the return section is what is being displayed (which is the current value of packageItem)
        //the value attribute below is the value of the input when it has changed. They are not the same
        const {name, value} = e.target;
        setPackageItem( currItem => ({...currItem, [name]: value}))
    }


    const [packageItemArray, setPackageItemArray] = useState([])
    const handleAddPackageItem = () => {
        setPackageItemArray( (currItems) => ([...currItems, packageItem]));
        setPackageItem({
            item_description: "",
            quantity: 0,
            weight_lb: 0
        });
    };


    const [pickUpAddress, setPickUpAddress] = useState({
        street: "",
        house_number: "",
        apartment_number: "",
        postal_code: "",
        city: "",
        country: ""
    });
    const handlePickUpAddressChange = (e) => {
        const { name, value } = e.target;
        //using the queue syntax so that we can use the most up to date/relevant data that we need
        //scatter the previous elements of the object, and just update the new one. This event only gets triggered for when an input changes. This means the target will always be that specific input element that changes.
        //hence, it will always have a name and a value (the name tag we specify and the value it contains)
        setPickUpAddress((prev) => ({ ...prev, [name]: value }));
    }

    const [dropOffAddress, setDropOffAddress] = useState({
        street: "",
        house_number: "",
        apartment_number: "",
        postal_code: "",
        city: "",
        country: ""
    });
    const handleDropOffChange = (e) => {
        const { name, value } = e.target;
        setDropOffAddress((prev) => ({ ...prev, [name]: value }));
    };

    const [selectedUnit, setSelectedUnit] = useState("imperial");
    const handleChangeUnits = (e) => {
        setSelectedUnit(e.target.value);
    }
    const [packageInfo, setPackageInfo] = useState({
        unit_system: selectedUnit,
        length: "",
        width_in: "",
        height_in: "",
        weight_lb: "",
        is_fragile: false,
        package_items: packageItemArray
    });
    
    const handlePackageChange = (e) => {
        const { name, value } = e.target;
        setPackageInfo((prev) => ({ ...prev, [name]: value }));
    };

    //resetting all input values
    const resetAllInputs = () => {
        setPackageItem({
            item_description: "",
            quantity: 0,
            weight_lb: 0
        })

        setPackageItemArray([])

        setPickUpAddress({
            street: "",
            house_number: "",
            apartment_number: "",
            postal_code: "",
            city: "",
            country: ""
        })

        setDropOffAddress({
            street: "",
            house_number: "",
            apartment_number: "",
            postal_code: "",
            city: "",
            country: ""
        })

        setSelectedUnit("imperial")

        setPackageInfo({
            unit_system: selectedUnit,
            length: "",
            width_in: "",
            height_in: "",
            weight_lb: "",
            is_fragile: false,
            package_items: packageItemArray
        })
    }


    const handleSubmitForm = (e) => {
        e.preventDefault();
       
        const clientID = localStorage.getItem("user_id")
        
        const deliveryDataObj = {
            customer_id: {clientID},
            pick_up_address: pickUpAddress,
            drop_off_address: dropOffAddress,
            package: packageInfo
        }
        console.log(deliveryDataObj)
        



            axios.post("http://localhost:5000/create_delivery_request", deliveryDataObj)
                .then( (response) => {
                    console.log("response: ", response);
                    resetAllInputs();
                }).catch( e => {
                    console.log("error making delivery request", e);
                })
    }//end of form submission.



      
    

    return (
        <main className="dashboard">
            <h1>{localStorage.getItem("username")}'s Dashboard</h1>
            <h2>Make request for delivery</h2>
            <form action="/create_delivery_request" method="POST" onSubmit={handleSubmitForm}>
                <h3>Pick Up Location</h3>
                <label>
                    Street:
                    <input type="text" name="street" value={pickUpAddress.street} onChange={handlePickUpAddressChange} ></input>
                </label>
                <label>
                    House Number:
                    <input type="number" name="house_number" value={pickUpAddress.house_number} onChange={handlePickUpAddressChange} ></input>
                </label>
                <label>
                    Apartment Number (if applies):
                    <input type="number" name="apartment_number" value={pickUpAddress.apartment_number} onChange={handlePickUpAddressChange} ></input>
                </label>
                <label>
                    Postal Code:
                    <input type="text" name="postal_code" value={pickUpAddress.postal_code} onChange={handlePickUpAddressChange}></input>
                </label>
                <label>
                    City:
                    <input type="text" name="city" value={pickUpAddress.city} onChange={handlePickUpAddressChange}></input>
                </label>
                <label>
                    Country:
                    <input type="text" name="country" value={pickUpAddress.country} onChange={handlePickUpAddressChange}></input>
                </label>
                <h3>Drop Off Location</h3>
                <label>
                    Street:
                    <input type="text" name="street" value={dropOffAddress.street} onChange={handleDropOffChange} ></input>
                </label>
                <label>
                    House Number:
                    <input type="number" name="house_number" value={dropOffAddress.house_number} onChange={handleDropOffChange}></input>
                </label>
                <label>
                    Apartment Number (if applies):
                    <input type="number" name="apartment_number" value={dropOffAddress.apartment_number} onChange={handleDropOffChange}></input>
                </label>
                <label>
                    Postal Code:
                    <input type="text" name="postal_code" value={dropOffAddress.postal_code} onChange={handleDropOffChange}></input>
                </label>
                <label>
                    City:
                    <input type="text" name="city" value={dropOffAddress.city} onChange={handleDropOffChange}></input>
                </label>
                <label>
                    Country:
                    <input type="text" name="country" value={dropOffAddress.country} onChange={handleDropOffChange}></input>
                </label>
                <h3>Package Information</h3>
                <select value={selectedUnit} onChange={handleChangeUnits}>
                    <option value="imperial">Imperial Units (freedom units - inches and lbs)</option>
                    <option value="metric">Metric Units (non stupid units - cm and kg)</option>
                </select>
                <div>
                    {selectedUnit === 'imperial' ? (
                        <p>You have chosen <b>Imperial units</b>. Measurements are in <b>inches</b> and <b>pounds</b>.</p>
                    ) : (
                        <p>You have chosen <b>Metric units</b>. Measurements are in <b>centimeters</b> and <b>kilograms</b>.</p>
                    )}
                </div>
                <label>
                    Length:
                    <input type="number" name="length" value={packageInfo.length} onChange={handlePackageChange}></input>
                </label>
                <label>
                    width:
                    <input type="number" name="width_in" value={packageInfo.width_in} onChange={handlePackageChange}></input>
                </label>
                <label>
                    height:
                    <input type="number" name="height_in" value={packageInfo.height_in} onChange={handlePackageChange}></input>
                </label>
                <label>
                    weight:
                    <input type="number" name="weight_lb" value={packageInfo.weight_lb} onChange={handlePackageChange}></input>
                </label>
                <h3>Is this item fragile?</h3>
                <div className="fragile-option">
                    <label>
                        Yes
                        <input type="radio" name="is_fragile" value={true} checked={packageInfo.is_fragile === false} onChange={handlePackageChange} />
                    </label>
                    <label>
                        No
                        <input type="radio" name="is_fragile" value={false} checked={packageInfo.is_fragile === false} onChange={handlePackageChange}/>
                    </label>
                </div>
                <h2>Package Items</h2>
                <label>
                    Item Description:
                    <input type="text" name="item_description" value={packageItem.item_description} onChange={handlePackageItemChange}></input>
                </label>
                <label>
                    Quantity:
                    <input type="number" name="quantity" value={packageItem.quantity} onChange={handlePackageItemChange}></input>
                </label>
                <label>
                    weight:
                    <input type="number" name="weight_lb" value={packageItem.weight_lb} onChange={handlePackageItemChange}></input>
                </label>
                <div className="button-container">
                    <button type="button" onClick={handleAddPackageItem}>Add Package Item</button>
                    <button type="submit">Submit Delivery Request</button>
                </div>
            </form>
            {packageItemArray.map( (item) => {
                return(
                    <div>
                        <b>NEW ITEM</b>
                        <p>{item.item_description}</p>
                        <p>{item.quantity}</p>
                        <p>{item.weight_lb}</p>
                    </div>
                )})
            }
            <Link to="/logout" className="logout">Log Out</Link>
        </main>
    )
}