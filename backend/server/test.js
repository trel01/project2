const axios = require('axios');
const apiKey = 'iDXG5WIkiNgiZwOVEZpAS2USEAecLoiW';
const locationKey = '317566';

const url = `https://dataservice.accuweather.com/currentconditions/v1/${locationKey}?apikey=${apiKey}`;

axios.get(url)
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.error('Error fetching data from AccuWeather API:', error.message);
  });
