import React from 'react'
import './SearchTracking.css'

export const SearchTracking = () => {
  return (
    <div className='search-tracking'>
        <p>Find your package!</p>
        <div className="search-input-container">
            <input type="text" placeholder='Enter tracking number'/>
            <button>Search</button>
        </div>
    </div>
  )
}
