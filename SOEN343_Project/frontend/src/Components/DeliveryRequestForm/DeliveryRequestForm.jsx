import React, { useState } from 'react';
//this bitch massive, so imma move it here instead - Arnab
// dw i didn't put any checkboxes... or did I?

//not using this currently. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


export const ShippingForm = () => {
  const [formData, setFormData] = useState({
    customer_id: "",
    pick_up_address: {
      street: "",
      house_number: "",
      apartment_number: "",
      postal_code: "",
      city: "",
      country: ""

    },

    drop_off_address: {
      street: "",
      house_number: "",
      apartment_number: "",
      postal_code: "",
      city: "",
      country: ""

    },
    package: {
      unit_system: "imperial", //change in case they chose to switch
      width_in: "",
      length_in: "",
      height_in: "",
      weight_lb: "",
      is_fragile: false, //dynamically change or create new vciable for it below
      package_items: [
        { item_description: "", quantity: "", weight: "" }
      ]
    }
  });

  // Handle form field changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    const keys = name.split('.');
    let newFormData = { ...formData };

    // Navigate through the object to set the value at the correct depth
    let temp = newFormData;
    while (keys.length > 1) {
      temp = temp[keys.shift()];
    }
    temp[keys[0]] = value;

    setFormData(newFormData);
  };

  // Handle checkbox changes
  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setFormData({
      ...formData,
      package: {
        ...formData.package,
        is_fragile: checked
      }
    });
  };

  // Handle package item changes
  const handleItemChange = (index, e) => {
    const { name, value } = e.target;
    const newItems = [...formData.package.package_items];
    newItems[index][name] = value;
    setFormData({
      ...formData,
      package: {
        ...formData.package,
        package_items: newItems
      }
    });
  };

  // Add a new package item
  const addPackageItem = () => {
    setFormData({
      ...formData,
      package: {
        ...formData.package,
        package_items: [
          ...formData.package.package_items,
          { item_description: '', quantity: '', weight: '' }
        ]
      }
    });
  };

  // Remove a package item
  const removePackageItem = (index) => {
    const newItems = formData.package.package_items.filter((_, i) => i !== index);
    setFormData({
      ...formData,
      package: {
        ...formData.package,
        package_items: newItems
      }
    });
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // Example: Send the formData to an API
    console.log('Form Data:', JSON.stringify(formData, null, 2));
    // You can use fetch or axios to submit the formData to a server here
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Shipping Form</h1>

      <label>
        Customer ID:
        <input
          type="text"
          name="customer_id"
          value={formData.customer_id}
          onChange={handleChange}
        />
      </label>

      <h2>Pick Up Address</h2>
      <label>
        Street:
        <input
          type="text"
          name="pick_up_address.street"
          value={formData.pick_up_address.street}
          onChange={handleChange}
        />
      </label>
      <label>
        House Number:
        <input
          type="text"
          name="pick_up_address.house_number"
          value={formData.pick_up_address.house_number}
          onChange={handleChange}
        />
      </label>
      <label>
        Apartment Number:
        <input
          type="text"
          name="pick_up_address.apartment_number"
          value={formData.pick_up_address.apartment_number}
          onChange={handleChange}
        />
      </label>
      <label>
        Postal Code:
        <input
          type="text"
          name="pick_up_address.postal_code"
          value={formData.pick_up_address.postal_code}
          onChange={handleChange}
        />
      </label>
      <label>
        City:
        <input
          type="text"
          name="pick_up_address.city"
          value={formData.pick_up_address.city}
          onChange={handleChange}
        />
      </label>
      <label>
        Country:
        <input
          type="text"
          name="pick_up_address.country"
          value={formData.pick_up_address.country}
          onChange={handleChange}
        />
      </label>

      <h2>Drop Off Address</h2>
      <label>
        Street:
        <input
          type="text"
          name="drop_off_address.street"
          value={formData.drop_off_address.street}
          onChange={handleChange}
        />
      </label>
      <label>
        House Number:
        <input
          type="text"
          name="drop_off_address.house_number"
          value={formData.drop_off_address.house_number}
          onChange={handleChange}
        />
      </label>
      <label>
        Apartment Number:
        <input
          type="text"
          name="drop_off_address.apartment_number"
          value={formData.drop_off_address.apartment_number}
          onChange={handleChange}
        />
      </label>
      <label>
        Postal Code:
        <input
          type="text"
          name="drop_off_address.postal_code"
          value={formData.drop_off_address.postal_code}
          onChange={handleChange}
        />
      </label>
      <label>
        City:
        <input
          type="text"
          name="drop_off_address.city"
          value={formData.drop_off_address.city}
          onChange={handleChange}
        />
      </label>
      <label>
        Country:
        <input
          type="text"
          name="drop_off_address.country"
          value={formData.drop_off_address.country}
          onChange={handleChange}
        />
      </label>

      <h2>Package Details</h2>
      <label>
        Width (inches):
        <input
          type="number"
          name="package.width_in"
          value={formData.package.width_in}
          onChange={handleChange}
        />
      </label>
      <label>
        Length (inches):
        <input
          type="number"
          name="package.length_in"
          value={formData.package.length_in}
          onChange={handleChange}
        />
      </label>
      <label>
        Height (inches):
        <input
          type="number"
          name="package.height_in"
          value={formData.package.height_in}
          onChange={handleChange}
        />
      </label>
      <label>
        Weight (lbs):
        <input
          type="number"
          name="package.weight_lb"
          value={formData.package.weight_lb}
          onChange={handleChange}
        />
      </label>
      <label>
        Is Fragile:
        <input
          type="checkbox"
          name="package.is_fragile"
          checked={formData.package.is_fragile}
          onChange={handleCheckboxChange}
        />
      </label>

      <h2>Package Items</h2>
      {formData.package.package_items.map((item, index) => (
        <div key={index}>
          <label>
            Item Description:
            <input
              type="text"
              name="item_description"
              value={item.item_description}
              onChange={(e) => handleItemChange(index, e)}
            />
          </label>
          <label>
            Quantity:
            <input
              type="number"
              name="quantity"
              value={item.quantity}
              onChange={(e) => handleItemChange(index, e)}
            />
          </label>
          <label>
            Weight:
            <input
              type="number"
              name="weight"
              value={item.weight}
              onChange={(e) => handleItemChange(index, e)}
            />
          </label>
          <button type="button" onClick={() => removePackageItem(index)}>
            Remove Item
          </button>
        </div>
      ))}
      <button type="button" onClick={addPackageItem}>Add Package Item</button>

      <br /><br />
      <button type="submit">Submit</button>
    </form>
  );
}

export default ShippingForm;
