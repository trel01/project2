require('dotenv').config();
const express = require('express');
const mysql = require('mysql2');
const WebSocket = require('ws');
const axios = require('axios');
const cors = require('cors');
const util = require('util');

const app = express();
const PORT = 3000;


app.use(express.json());
app.use(cors());


const db = mysql.createConnection({
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '483312',
  database: process.env.DB_NAME || 'weather_data',
});

db.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL:', err.message);
    return;
  }
  console.log('Connected to MySQL successfully!');
});


const fetchDataFromTable = (weather_data, res) => {
  db.query(`SELECT * FROM ${weather_data}`, (err, results) => {
    if (err) {
      console.error(`Error fetching data from ${weather_data}:`, err.message);
      return res.status(500).json({ error: err.message });
    }
    console.log(`Data fetched from ${weather_data}:`, results);
    res.json(results);
  });
};
app.get('/outdoor-data', (req, res) => {
  db.query('SELECT * FROM outdoor_data ORDER BY timestamp DESC LIMIT 1', (err, results) => {
    if (err) {
      console.error('Error fetching outdoor data:', err.message);
      res.status(500).json({ error: 'Error fetching outdoor data' });
    } else {
      console.log('Latest outdoor data:', results);  
      res.json(results[0]); 
    }
  });
});
app.get('/indoor-data', (req, res) => {
  db.query('SELECT * FROM indoor_data ORDER BY timestamp DESC LIMIT 1', (err, results) => {
    if (err) {
      console.error('Error fetching indoor data:', err.message);
      res.status(500).json({ error: 'Error fetching indoor data' });
    } else {
      res.json(results[0]);  
    }
  });
});
app.get('/solar-and-uvi', (req, res) => {
  db.query('SELECT * FROM solar_and_uvi ORDER BY timestamp DESC LIMIT 1', (err, results) => {
    if (err) {
      console.error('Error fetching solar and uvi data:', err.message);
      res.status(500).json({ error: 'Error fetching solar and uvi data' });
    } else {
      console.log('Latest solar and uvi data:', results); 
      res.json(results[0]); 
    }
  });
});
app.get('/rainfall-data', (req, res) => {
  db.query('SELECT * FROM rainfall_data ORDER BY timestamp DESC LIMIT 1', (err, results) => {
    if (err) {
      console.error('Error fetching rainfall data:', err.message);
      res.status(500).json({ error: 'Error fetching rainfall data' });
    } else {
      console.log('Latest rainfall data:', results); 
      res.json(results[0]); 
    }
  });
});




const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  console.log('Client connected to WebSocket');
  ws.send(JSON.stringify({ message: 'Connected to WebSocket Server!' }));

 
  db.query(
    'SELECT * FROM outdoor_data ORDER BY timestamp DESC LIMIT 1',
    (err, results) => {
      if (err) {
        console.error('Error fetching data:', err.message);
        ws.send(JSON.stringify({ error: 'Error fetching data' }));
      } else {
        console.log('Sending data to WebSocket client:', results);
        ws.send(JSON.stringify({ outdoor_data: results }));
      }
    }
  );

  
  ws.on('message', (message) => {
    console.log('Received:', message);

    
    db.query(
      'SELECT * FROM outdoor_data ORDER BY timestamp DESC LIMIT 1',
      (err, results) => {
        if (err) {
          console.error('Error fetching data:', err.message);
          ws.send(JSON.stringify({ error: 'Error fetching data' }));
        } else {
          console.log('Sending updated data to WebSocket client:', results);
          ws.send(JSON.stringify({ outdoor_data: results }));
        }
      }
    );
  });

  
  ws.on('close', () => {
    console.log('Client disconnected');
  });
});


const apiUrl = 'https://api.ecowitt.net/api/v3/device/real_time';
const params = {
  application_key: 'F4EAE399ED0BDAB7E0B03462D641DEB2',
  api_key: '7d76f688-062e-45ae-8ddc-7c9bd9c3598c',
  mac: '08:F9:E0:78:0C:71',
  call_back: 'all',
};


const intervalId = setInterval(async () => {
  try {
    const response = await axios.get(apiUrl, { params });
    const data = response.data.data;

    console.log('Fetched data from Ecowitt API:', data);

    
    wss.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify(data));
      }
    });

    
    saveDataToDatabase(data);

  } catch (error) {
    console.error('Error fetching data from Ecowitt API:', error);
  }
}, 3*60*60*1000); 

setInterval(async () => {
  try {
    const city = 'Maha Sarakham';
    const apiKey = process.env.OPENWEATHER_API_KEY;
    
    const weatherData = await fetchOpenWeatherData(city, apiKey);
    
    if (!weatherData) {
      throw new Error('No weather data returned');
    }
    
    saveOpenWeatherData(db, weatherData);
  } catch (error) {
    console.error('Error in interval fetching data:', error.message);
  }
}, 3*60*60*1000+2000); 
setInterval(async () => {
  try {
    const locationKey = '319122'; 
    const apiKey = process.env.ACCUWEATHER_API_KEY; 

    if (!apiKey) {
      throw new Error('AccuWeather API key is missing. Please set it in the .env file.');
    }

    console.log('Fetching weather data for location:', locationKey);

   
    const weatherData = await fetchAccuWeatherData(locationKey, apiKey);

    if (!weatherData) {
      throw new Error('No weather data returned');
    }

    
    await saveAccuWeatherData(weatherData);

    console.log('Weather data fetched and saved successfully:', weatherData);
  } catch (error) {
    console.error('Error in interval fetching data:', error.message);
  }
},3*60*60 * 1000+1000); 





const queryAsync = util.promisify(db.query).bind(db);

async function saveDataToDatabase(data) {
  try {
    const { outdoor, indoor, wind, rainfall, battery, pressure } = data;

    
    if (!outdoor || !indoor || !wind || !rainfall || !battery || !pressure) {
      throw new Error("Missing required data (outdoor, indoor, wind, rainfall, battery, or pressure)");
    }

    const timestamp = Math.floor(Date.now() / 1000);
    const recordTime = new Date().toISOString().slice(0, 19).replace("T", " ");
  
    
    const weatherRecordQuery = `
      INSERT INTO weather_record (record_time, temperature, humidity, wind_speed, wind_direction) 
      VALUES (?, ?, ?, ?, ?)
    `;

    const weatherRecordResult = await queryAsync(weatherRecordQuery, [
      recordTime,
      outdoor.temperature?.value || 0,
      outdoor.humidity?.value || 0,
      wind.wind_speed?.value || 0,
      wind.wind_direction?.value || 0
    ]);

    const recordId = weatherRecordResult.insertId;  

    console.log('Weather record saved:', recordId);

    
    const outdoorQuery = `
      INSERT INTO outdoor_data (record_id, temperature, feels_like, app_temp, dew_point, humidity, wind_speed, wind_direction, rainfall, timestamp) 
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;

    await queryAsync(outdoorQuery, [
      recordId,  
      outdoor.temperature?.value || 0,
      outdoor.feels_like?.value || 0,
      outdoor.app_temp?.value || 0,
      outdoor.dew_point?.value || 0,
      outdoor.humidity?.value || 0,
      wind.wind_speed?.value || 0,
      wind.wind_direction?.value || 0,
      rainfall.daily?.value || 0,
      timestamp
    ]);

    console.log('Outdoor data saved for record ID:', recordId);

    
    const batteryQuery = `
      INSERT INTO battery_data (record_id, sensor_array) 
      VALUES (?, ?)
    `;

    await queryAsync(batteryQuery, [
      recordId,  
      battery.sensor_array?.value || 0  
    ]);

    console.log('Battery data saved for record ID:', recordId);

    
    const pressureQuery = `
      INSERT INTO pressure_data (record_id, relative, absolute) 
      VALUES (?, ?, ?)
    `;

    await queryAsync(pressureQuery, [
      recordId,  
      pressure.relative?.value || 0,  
      pressure.absolute?.value || 0 
    ]);

    console.log('Pressure data saved for record ID:', recordId);

   
    const windQuery = `
      INSERT INTO wind_data (record_id, wind_speed, wind_gust, wind_direction) 
      VALUES (?, ?, ?, ?)
    `;

    await queryAsync(windQuery, [
      recordId,  
      wind.wind_speed?.value || 0,
      wind.wind_gust?.value || 0,
      wind.wind_direction?.value || 0
    ]);

    console.log('Wind data saved for record ID:', recordId);
  
  } catch (err) {
    console.error('Error saving data to MySQL:', err.message, err);
  }
}





app.get('/accuweather', async (req, res) => {
  try {
    const query = 'SELECT * FROM accuweather_data ORDER BY epoch_time DESC LIMIT 1'; 

    db.query(query, (err, result) => {
      if (err) {
        console.error('Error fetching data from MySQL:', err.message);
        return res.status(500).json({ error: 'Error fetching data from database' });
      }

      if (result.length > 0) {
        const latestWeatherData = result[0]; 
        res.json(latestWeatherData);
      } else {
        res.status(404).json({ error: 'No weather data found' });
      }
    });
  } catch (error) {
    console.error('Error:', error.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});




const fetchAccuWeatherData = async (locationKey, apiKey) => {
  const url = `http://dataservice.accuweather.com/currentconditions/v1/${locationKey}`;
  const params = { apikey: apiKey };

  try {
    const response = await axios.get(url, { params });

    if (response.data && response.data.length > 0) {
      const weatherData = response.data[0];

      
      const data = {
        localObservationDateTime: weatherData.LocalObservationDateTime || 'Unknown',
        epochTime: weatherData.EpochTime || Math.floor(Date.now() / 1000),
        weatherText: weatherData.WeatherText || 'Unknown',
        weatherIcon: weatherData.WeatherIcon || null,
        hasPrecipitation: weatherData.HasPrecipitation || false,
        precipitationType: weatherData.PrecipitationType || 0,
        isDayTime: weatherData.IsDayTime || false,
        temperatureMetricValue: weatherData?.Temperature?.Metric?.Value || null,
        temperatureMetricUnit: weatherData?.Temperature?.Metric?.Unit || 'C',
        temperatureImperialValue: weatherData?.Temperature?.Imperial?.Value || null,
        temperatureImperialUnit: weatherData?.Temperature?.Imperial?.Unit || 'F',
        mobileLink: weatherData.MobileLink || null,
        link: weatherData.Link || null,
      };
      console.log('Processed weather data:', data);
     
      await saveAccuWeatherData(data);
      return data;
    } else {
      throw new Error('No data returned from AccuWeather API');
    }
  } catch (error) {
    console.error('Error fetching data from AccuWeather API:', error.message);
    throw new Error(`Error fetching data from AccuWeather API: ${error.message}`);
  }
};


const saveAccuWeatherData = async (data) => {
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
    data.localObservationDateTime,
    data.epochTime,
    data.weatherText,
    data.weatherIcon,
    data.hasPrecipitation,
    data.precipitationType,
    data.isDayTime,
    data.temperatureMetricValue,
    data.temperatureMetricUnit,
    data.temperatureImperialValue,
    data.temperatureImperialUnit,
    data.mobileLink,
    data.link,
  ];

  return new Promise((resolve, reject) => {
    db.query(query, values, (err, result) => {
      if (err) {
        console.error('Error saving AccuWeather data to MySQL:', err.message);
        return reject(err);
      }

      console.log('AccuWeather data saved to MySQL:', result);
      resolve(result);
    });
  });
};


app.use((err, req, res, next) => {
  console.error('Unexpected error:', err.message);
  res.status(500).json({ error: 'Internal server error' });
});

module.exports = app;

//--------------------------------------------------------------------------------------------------------

const saveOpenWeatherData = (db, weatherData) => {
  const query = `
    INSERT INTO openweather_data
    (temperature, feels_like, humidity, wind_speed, wind_deg, weather_text, clouds, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `;
  db.query(query, [
    weatherData.temperature,
    weatherData.feels_like,
    weatherData.humidity,
    weatherData.wind_speed,
    weatherData.wind_deg,
    weatherData.weather_text,
    weatherData.clouds,
    weatherData.timestamp,
  ], (err, result) => {
    if (err) {
      console.error('Error saving OpenWeather data to MySQL:', err.message);
      return;
    }
    console.log('OpenWeather data saved to MySQL:', result);
  });
};


const fetchOpenWeatherData = async (city, apiKey) => {
  try {
    const response = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`
    );

    if (!response.ok) {
      throw new Error(`API response error: ${response.statusText}`);
    }

    const data = await response.json();
    return {
      temperature: data.main.temp,
      feels_like: data.main.feels_like,
      humidity: data.main.humidity,
      wind_speed: data.wind.speed,
      wind_deg: data.wind.deg,
      weather_text: data.weather[0].description,
      clouds: data.clouds.all,
      timestamp: Math.floor(Date.now() / 1000),
    };
  } catch (error) {
    console.error('Error fetching data from OpenWeather API:', error.message);
    throw error;
  }
};



app.get('/latest-openweather', (req, res) => {
  const query = 'SELECT * FROM openweather_data ORDER BY timestamp DESC LIMIT 1';

  db.query(query, (err, results) => {
    if (err) {
      console.error('Error fetching latest weather data from MySQL:', err.message);
      return res.status(500).json({ error: 'Failed to fetch latest weather data' });
    }

    if (results.length > 0) {
      console.log('Latest weather data:', results[0]);
      res.json(results[0]);  
    } else {
      res.status(404).json({ error: 'No weather data found' });
    }
  });
});




// Fetch data every 10 minutes






// Global error handler for unexpected errors
app.use((err, req, res, next) => {
  console.error('Unexpected error:', err.message);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
