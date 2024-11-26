import React from 'react'
import { Hero } from '../Components/Hero/Hero'
import { SearchTracking } from '../Components/SearchTracking/SearchTracking'
import { ServiceDescription } from '../Components/ServiceDescription/ServiceDescription'
import { AboutUs } from '../Components/AboutUs/AboutUs'
import { ImageTextSection } from '../Components/ImageTextSection/ImageTextSection'

export const Landing = () => {
  return (
        <div>
            <Hero/>
            <SearchTracking/>
            <ServiceDescription/>
            <AboutUs/>
            <ImageTextSection/>
        </div>
  )
}
