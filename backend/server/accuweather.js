
// Fetch data from AccuWeather API
const fetchAccuWeatherData = async (locationKey, apiKey) => {
  const url = `http://dataservice.accuweather.com/currentconditions/v1/${locationKey}`;
  const params = { apikey: apiKey };

  try {
    const response = await axios.get(url, { params });

    if (response.data && response.data.length > 0) {
      const weatherData = response.data[0];

      console.log('Response data:', response.data);

      // ตรวจสอบค่าของตัวแปร
      const localObservationDateTime = weatherData.LocalObservationDateTime || 'Unknown';
      const epochTime = weatherData.EpochTime || Math.floor(Date.now() / 1000);
      const weatherText = weatherData.WeatherText || 'Unknown';
      const weatherIcon = weatherData.WeatherIcon || null;
      const hasPrecipitation = weatherData.HasPrecipitation || false;
      const precipitationType = weatherData.PrecipitationType || null;
      const isDayTime = weatherData.IsDayTime || false;

      const temperatureMetricValue = weatherData?.Temperature?.Metric?.Value || null;
      const temperatureMetricUnit = weatherData?.Temperature?.Metric?.Unit || 'C';
      const temperatureImperialValue = weatherData?.Temperature?.Imperial?.Value || null;
      const temperatureImperialUnit = weatherData?.Temperature?.Imperial?.Unit || 'F';

      const mobileLink = weatherData.MobileLink || null;
      const link = weatherData.Link || null;

      // บันทึกข้อมูลลงในฐานข้อมูล
      await saveAccuWeatherData({
        localObservationDateTime,
        epochTime,
        weatherText,
        weatherIcon,
        hasPrecipitation,
        precipitationType,
        isDayTime,
        temperatureMetricValue,
        temperatureMetricUnit,
        temperatureImperialValue,
        temperatureImperialUnit,
        mobileLink,
        link,
      });

      return {
        localObservationDateTime,
        epochTime,
        weatherText,
        weatherIcon,
        hasPrecipitation,
        precipitationType,
        isDayTime,
        temperatureMetricValue,
        temperatureMetricUnit,
        temperatureImperialValue,
        temperatureImperialUnit,
        mobileLink,
        link,
      };
    } else {
      throw new Error('No data returned from AccuWeather API');
    }
  } catch (error) {
    console.error('Error fetching data from AccuWeather API:', error.message);
    throw new Error(`Error fetching data from AccuWeather API: ${error.message}`);
  }
};

// Save AccuWeather data to MySQL
const saveAccuWeatherData = async (weatherData) => {
  const query = `
    INSERT INTO accuweather_data (
      local_observation_datetime,
      epoch_time,
      weather_text,
      weather_icon,
      has_precipitation,
      precipitation_type,
      is_daytime,
      temperature_metric_value,
      temperature_metric_unit,
      temperature_imperial_value,
      temperature_imperial_unit,
      mobile_link,
      link
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `;
  const values = [
    weatherData.localObservationDateTime,
    weatherData.epochTime,
    weatherData.weatherText,
    weatherData.weatherIcon,
    weatherData.hasPrecipitation,
    weatherData.precipitationType,
    weatherData.isDayTime,
    weatherData.temperatureMetricValue,
    weatherData.temperatureMetricUnit,
    weatherData.temperatureImperialValue,
    weatherData.temperatureImperialUnit,
    weatherData.mobileLink,
    weatherData.link,
  ];

  return new Promise((resolve, reject) => {
    db.query(query, values, (err, result) => {
      if (err) {
        console.error('Error saving AccuWeather data to MySQL:', err.message);
        reject(err);
      } else {
        console.log('AccuWeather data saved to MySQL:', result);
        resolve(result);
      }
    });
  });
};
