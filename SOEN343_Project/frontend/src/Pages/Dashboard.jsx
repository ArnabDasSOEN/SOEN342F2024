import { Link } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import { LoadScript, Autocomplete } from "@react-google-maps/api";
import "./CSS/Dashboard.css";

const libraries = ["places"]; // Load Places library

export const Dashboard = () => {
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

  const [dropOffAddress, setDropOffAddress] = useState({
    street: "",
    house_number: "",
    apartment_number: "",
    postal_code: "",
    city: "",
    country: "",
  });

  const [packageItem, setPackageItem] = useState({
    item_description: "",
    quantity: 0,
    weight: 0,
  });

  const [packageItemArray, setPackageItemArray] = useState([]);

  const [packageInfo, setPackageInfo] = useState({
    unit_system: "imperial",
    length: 0,
    width: 0,
    height: 0,
    weight: 0,
    is_fragile: false,
    package_items: [],
  });

  const [selectedUnit, setSelectedUnit] = useState("imperial");

  // Google Places Autocomplete Handlers
  const onLoadPickup = (autocomplete) => setAutocompletePickup(autocomplete);
  const onPlaceChangedPickup = () => {
    if (autocompletePickup) {
      const place = autocompletePickup.getPlace();
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
      if (place && place.address_components) {
        const address = formatAddressComponents(place.address_components);
        setDropOffAddress((prev) => ({ ...prev, ...address }));
      }
    }
  };

  // Format Address Components
  const formatAddressComponents = (components) => {
    const address = {
      street: "",
      house_number: "",
      apartment_number: "",
      postal_code: "",
      city: "",
      country: "",
    };

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

  const handlePickUpAddressChange = (e) => {
    const { name, value } = e.target;
    setPickUpAddress((prev) => ({ ...prev, [name]: value }));
  };

  const handleDropOffAddressChange = (e) => {
    const { name, value } = e.target;
    setDropOffAddress((prev) => ({ ...prev, [name]: value }));
  };

  const handlePackageItemChange = (e) => {
    const { name, value } = e.target;
    setPackageItem((currItem) => ({
      ...currItem,
      [name]:
        name === "quantity" || name === "weight" ? parseFloat(value) : value,
    }));
  };

  const handleAddPackageItem = () => {
    setPackageItemArray((currItems) => [...currItems, packageItem]);
    setPackageItem({ item_description: "", quantity: 0, weight: 0 });
  };

  const handlePackageChange = (e) => {
    const { name, value } = e.target;
    setPackageInfo((prev) => ({
      ...prev,
      [name]: ["length", "width", "height", "weight"].includes(name)
        ? parseFloat(value)
        : value,
    }));
  };

  const handleChangeUnits = (e) => {
    setSelectedUnit(e.target.value);
    setPackageInfo((prev) => ({
      ...prev,
      unit_system: e.target.value,
    }));
  };

  const handleSubmitForm = async (e) => {
    e.preventDefault();

    const customerId = localStorage.getItem("user_id");

    // Ensure all numeric fields are converted to numbers
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

    const deliveryDataObj = {
      customer_id: parseInt(customerId, 10),
      pick_up_address: pickUpAddress,
      drop_off_address: dropOffAddress,
      package: normalizedPackageInfo,
    };

    console.log("Delivery Request Data:", deliveryDataObj);

    try {
      const response = await axios.post(
        "http://localhost:5000/create_delivery_request",
        deliveryDataObj
      );
      console.log("Response:", response.data);
    } catch (e) {
      console.error("Error submitting delivery request:", e);
    }
  };

  return (
    <main className="dashboard">
      <h1>{localStorage.getItem("username")}'s Dashboard</h1>
      <h2>Make request for delivery</h2>
      <LoadScript
        googleMapsApiKey={process.env.REACT_APP_GOOGLE_MAPS_API_KEY}
        libraries={libraries}
      >
        <form onSubmit={handleSubmitForm}>
          <h3>Pick Up Location</h3>
          <Autocomplete
            onLoad={onLoadPickup}
            onPlaceChanged={onPlaceChangedPickup}
          >
            <input
              type="text"
              name="street"
              placeholder="Enter pickup address"
              value={pickUpAddress.street}
              onChange={handlePickUpAddressChange}
            />
          </Autocomplete>

          <h3>Drop Off Location</h3>
          <Autocomplete
            onLoad={onLoadDropoff}
            onPlaceChanged={onPlaceChangedDropoff}
          >
            <input
              type="text"
              name="street"
              placeholder="Enter drop-off address"
              value={dropOffAddress.street}
              onChange={handleDropOffAddressChange}
            />
          </Autocomplete>

          <h3>Package Information</h3>
          <select value={selectedUnit} onChange={handleChangeUnits}>
            <option value="imperial">Imperial (inches, lbs)</option>
            <option value="metric">Metric (cm, kg)</option>
          </select>
          <label>
            Length:
            <input
              type="number"
              name="length"
              value={packageInfo.length}
              onChange={handlePackageChange}
            />
          </label>
          <label>
            Width:
            <input
              type="number"
              name="width"
              value={packageInfo.width}
              onChange={handlePackageChange}
            />
          </label>
          <label>
            Height:
            <input
              type="number"
              name="height"
              value={packageInfo.height}
              onChange={handlePackageChange}
            />
          </label>
          <label>
            Weight:
            <input
              type="number"
              name="weight"
              value={packageInfo.weight}
              onChange={handlePackageChange}
            />
          </label>

          <h3>Package Items</h3>
          <label>
            Item Description:
            <input
              type="text"
              name="item_description"
              value={packageItem.item_description}
              onChange={handlePackageItemChange}
            />
          </label>
          <label>
            Quantity:
            <input
              type="number"
              name="quantity"
              value={packageItem.quantity}
              onChange={handlePackageItemChange}
            />
          </label>
          <label>
            Weight:
            <input
              type="number"
              name="weight"
              value={packageItem.weight}
              onChange={handlePackageItemChange}
            />
          </label>
          <button type="button" onClick={handleAddPackageItem}>
            Add Package Item
          </button>

          <button type="submit">Submit Delivery Request</button>
        </form>
      </LoadScript>
    </main>
  );
};
