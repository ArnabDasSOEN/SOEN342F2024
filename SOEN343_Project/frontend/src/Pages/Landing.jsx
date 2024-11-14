import React from 'react'
import { Hero } from '../Components/Hero/Hero'
import { SearchTracking } from '../Components/SearchTracking/SearchTracking'
import { ServiceDescription } from '../Components/ServiceDescription/ServiceDescription'

export const Landing = () => {
  return (
        <div>
            <Hero/>
            <SearchTracking/>
            <ServiceDescription/>
        </div>
  )
}
