import { useState } from "react"
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { LoadScript, Autocomplete } from "@react-google-maps/api";
import axios from "axios";


export const UpdateDelivery = () => {

    const [deliveryRequestID, setDeliveryRequestID] = useState(null);
    const handleDeliveryIDChange = (e) => {
        setDeliveryRequestID(e.target.value);
    }
    


    const [autocompletePickup, setAutocompletePickup] = useState(null);
    const [autocompleteDropoff, setAutocompleteDropoff] = useState(null);

    const [pickUpAddress, setPickUpAddress] = useState({
        street: "",
        house_number: "",
        apartment_number: "",
        postal_code: "",
        city: "",
        country: "",
    });

    const handlePickUpAddressChange = (e) => {
        const { name, value } = e.target;
        setPickUpAddress((prev) => ({ ...prev, [name]: value }));
    };

    const [dropOffAddress, setDropOffAddress] = useState({
        street: "",
        house_number: "",
        apartment_number: "",
        postal_code: "",
        city: "",
        country: "",
    });

    const handleDropOffAddressChange = (e) => {
        const { name, value } = e.target;
        setDropOffAddress((prev) => ({ ...prev, [name]: value }));
    };

    const [packageItem, setPackageItem] = useState({
        item_description: "",
        quantity: 0,
        weight: 0,
    });

    const handlePackageItemChange = (e) => {
        const { name, value } = e.target;
        setPackageItem((currItem) => ({
            ...currItem, [name]: name === "quantity" || name === "weight" ? parseFloat(value) : value,
        }));
    };

    const [packageItemArray, setPackageItemArray] = useState([]);

    const handleAddPackageItem = () => {
        setPackageItemArray((currItems) => [...currItems, packageItem]);
        setPackageItem({ item_description: "", quantity: 0, weight: 0 });
    };

    const [packageInfo, setPackageInfo] = useState({
        unit_system: "imperial",
        length: 0,
        width: 0,
        height: 0,
        weight: 0,
        is_fragile: false,
        package_items: [],
    });

    const handlePackageChange = (e) => {
        const { name, value } = e.target;
        setPackageInfo((prev) => ({
            ...prev,
            [name]: ["length", "width", "height", "weight"].includes(name)
                ? parseFloat(value)
                : value,
        }));
    };

    const [selectedUnit, setSelectedUnit] = useState("imperial");

    const handleChangeUnits = (e) => {
        setSelectedUnit(e.target.value);
        setPackageInfo((prev) => ({
            ...prev,
            unit_system: e.target.value,
        }));
    };

    // Google Places Autocomplete Handlers
    const onLoadPickup = (autocomplete) => setAutocompletePickup(autocomplete);

    const onPlaceChangedPickup = () => {
        if (autocompletePickup) {
            const place = autocompletePickup.getPlace();
            //console.log(autocompletePickup.getPlace())
            if (place && place.address_components) {
                const address = formatAddressComponents(place.address_components);
                setPickUpAddress((prev) => ({ ...prev, ...address }));
            }
        }
    };

    const onLoadDropoff = (autocomplete) => setAutocompleteDropoff(autocomplete);

    const onPlaceChangedDropoff = () => {
        if (autocompleteDropoff) {
            const place = autocompleteDropoff.getPlace();
            //console.log(place);
            if (place && place.address_components) {
                const address = formatAddressComponents(place.address_components);
                setDropOffAddress((prev) => ({ ...prev, ...address }))
            }
        }
    };

    // Format Address Components
    //components in the address_components array
    const formatAddressComponents = (components) => {
        const address = {
            street: "",
            house_number: "",
            apartment_number: "",
            postal_code: "",
            city: "",
            country: "",
        };
        //console.log(components[0].types);
        components.forEach((component) => {
            if (component.types.includes("street_number")) {
                address.house_number = component.long_name;
            }
            if (component.types.includes("route")) {
                address.street = component.long_name;
            }
            if (component.types.includes("postal_code")) {
                address.postal_code = component.long_name;
            }
            if (
                component.types.includes("locality") ||
                component.types.includes("administrative_area_level_2")
            ) {
                address.city = component.long_name;
            }
            if (component.types.includes("country")) {
                address.country = component.long_name;
            }
        });

        return address;
    };


    const handleSubmitForm = async (e) => {
        e.preventDefault();

        //replace with delivery request id
        //const customerId = localStorage.getItem("user_id");

        // Ensure all numeric fields are converted to numbers
        // const normalizedPackageInfo = {
        //     ...packageInfo,
        //     length: parseFloat(packageInfo.length),
        //     width: parseFloat(packageInfo.width),
        //     height: parseFloat(packageInfo.height),
        //     weight: parseFloat(packageInfo.weight),
        //     package_items: packageItemArray.map((item) => ({
        //         ...item,
        //         quantity: parseInt(item.quantity, 10),
        //         weight: parseFloat(item.weight),
        //     })),
        // };

        let deliveryDataObj = {
            delivery_request_id: deliveryRequestID
        }

        if( !(pickUpAddress.street === "" || pickUpAddress.house_number === "")){
            deliveryDataObj = {...deliveryDataObj, pick_up_address: pickUpAddress}
        }

        if( !(dropOffAddress.street === "" || dropOffAddress.house_number === "")){
            deliveryDataObj = {...deliveryDataObj, drop_off_address: dropOffAddress}
        }



        if( !(packageInfo.length === 0 || packageInfo.width === 0 || packageInfo.height === 0 || packageInfo.weight === 0)){
            const normalizedPackageInfo = {
                ...packageInfo,
                length: parseFloat(packageInfo.length),
                width: parseFloat(packageInfo.width),
                height: parseFloat(packageInfo.height),
                weight: parseFloat(packageInfo.weight),
                package_items: packageItemArray.map((item) => ({
                    ...item,
                    quantity: parseInt(item.quantity, 10),
                    weight: parseFloat(item.weight),
                })),
            };
            deliveryDataObj = {...deliveryDataObj, package: normalizedPackageInfo}
        }



        // const deliveryDataObj = {
        //     customer_id: parseInt(customerId, 10),
        //     pick_up_address: pickUpAddress,
        //     drop_off_address: dropOffAddress,
        //     package: normalizedPackageInfo,
        // };

        console.log("Delivery update request Data:", deliveryDataObj);

        try {
            //change this
            const response = await axios.post("http://localhost:5000/delivery_request/update_delivery_request", deliveryDataObj);
            console.log("Response:", response.data);
            toast.success("succesfully updated delivery request")
            resetInput()

        } catch (e) {
            console.error("Error updating delivery request:", e);
        }
    };



    const resetInput = () => {
        const textInputs = document.querySelectorAll("input[type='text']");
        const numberInputs = document.querySelectorAll("input[type='number']");
        textInputs.forEach(el => {
            el.value = "";
        })

        numberInputs.forEach(el => {
            el.value = 0;
        })
    }

    return (
        <main>
            <h1>Update a delivery Request</h1>
            <label>
                <input type="number" value={deliveryRequestID} onChange={handleDeliveryIDChange} > Delivery request ID</input>
            </label>

        </main>
    )
}