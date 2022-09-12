import 'leaflet/dist/leaflet.css';
import { useEffect, useState } from 'react';
import { GeoJSON, MapContainer, TileLayer } from 'react-leaflet';
import { fetchData } from '../store/tools';
import countiesDataJson from './../data/counties.json';
import './CovidMap.css';
import LoadingAnimation from './ui/LoadingAnimation';

type DataRecord = {
  county_name: string,
  area: number,
  population: number,
  population_density: number,
  year: number,
  year_total_deaths: number,
  reference_date: string,
  incidence_risk: string,
  incidence: number,
  confirmed_1: number,
  cases_14: number,
}

interface DataRecordMap {
  [k: string]: DataRecord,
}

export default function CovidMap() {

  const emptyData: DataRecordMap = {};
  const [apiData, setData] = useState(emptyData);
  const [isLoading, setIsLoading] = useState(true);

  const countiesData: any = countiesDataJson;
  const counties = countiesData.features;

  async function runCall() {
    const url = `${import.meta.env.VITE_API_URL}county_summary/`;
    const returnedApiData = (await fetchData(url));

    setData(returnedApiData);
    setIsLoading(false);
  }

  useEffect(() => { runCall(); }, [])

  function getDistrictColor(id: number) {
    switch (id) {
      case 1: return '#C7B446'
      case 2: return '#3D642D'
      case 3: return '#734222'
      case 4: return '#1F3A3D'
      case 5: return '#2271B3'
      case 6: return '#4E5452'
      case 7: return '#C51D34'
      case 8: return '#9DA1AA'
      case 9: return '#20214F'
      case 10: return '#49678D'
      case 11: return '#E4A010'
      case 12: return '#991F19'
      case 13: return '#ED760E'
      case 14: return '#6F4F28'
      case 15: return '#2F353B'
      case 16: return '#6C4675'
      case 17: return '#898176'
      case 18: return '#E63244'
      case 19: return '#EE9900'
      default: return '#781F19'
    }
  }

  function districtStyle(feature: any) {
    return {
      fillColor: getDistrictColor(feature.properties.ID_1),
      fillOpacity: 0.5,
      color: getDistrictColor(feature.properties.ID_1),
      weight: 1,
    };
  }

  function countyPopup(districtName: string, countyName: string) {
    return (
      `<div>
        <h3>${districtName} - ${countyName}</h3>
        <p style="margin:0;">County data:</p>
        <li style="margin:0;">Area: ${(apiData[countyName.toUpperCase()].area / 100).toFixed(2)} km&#178;</li>
        <li style="margin:0;">Population: ${apiData[countyName.toUpperCase()].population}</li>
        <li style="margin:0;">Population density: ${apiData[countyName.toUpperCase()].population_density} inhabitant/km&#178;</li>
        <li style="margin:0;">Deaths in ${apiData[countyName.toUpperCase()].year}: ${apiData[countyName.toUpperCase()].year_total_deaths}</li>
        <p style="margin-bottom:0;">COVID-19 data:</p>
        <li style="margin:0;">Reference date: ${apiData[countyName.toUpperCase()].reference_date}</li>
        <li style="margin:0;">Cases last 14 days: ${apiData[countyName.toUpperCase()].cases_14}</li>
        <li style="margin:0;">Incidence: ${apiData[countyName.toUpperCase()].incidence} cases per 100k inhabitants</li>
        <li style="margin:0;">Incidence category: ${apiData[countyName.toUpperCase()].incidence_risk}</li>
      </div>`);
  }


  const onEachCounty = (county: any, layer: any) => {
    const districtName = county.properties.NAME_1;
    const countyName = county.properties.NAME_2;
    layer.bindPopup(countyPopup(districtName, countyName));
    layer.on({
      mouseover: (event: any) => {
        event.target.setStyle({
          fillOpacity: 1,
        });
      },
      mouseout: (event: any) => {
        event.target.setStyle({
          fillOpacity: 0.5,
        });
      },
    });
  };


  return (
    <div className='mapDiv'>
      <h1>Map</h1>

      {isLoading ?
        <div className='loadAnimationWrapper'><LoadingAnimation /></div> :

        <MapContainer
          style={{
            height: '70vh',
            width: '80%',
            left: '10%',
            marginBottom: '2rem',
            marginTop: '2rem',
          }}
          zoom={7}
          center={[39.3999, -8.2245]}
        >
          <TileLayer
            url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
          />
          <GeoJSON
            style={districtStyle}
            data={counties}
            onEachFeature={onEachCounty}
          />
        </MapContainer>
      }

    </div>
  );
}
