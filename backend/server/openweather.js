// ฟังก์ชันสำหรับบันทึกข้อมูล OpenWeather ลง MySQL
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
      weatherData.clouds,  // เพิ่ม clouds ลงใน query
      weatherData.timestamp,
    ], (err, result) => {
      if (err) {
        console.error('Error saving OpenWeather data to MySQL:', err.message);
        return;
      }
      console.log('OpenWeather data saved to MySQL:', result);
    });
  };
  
  // ฟังก์ชันดึงข้อมูลจาก OpenWeather API
  const fetchOpenWeatherData = async (city, apiKey) => {
    const url = `http://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
    try {
      const response = await axios.get(url);
      const data = response.data;
  
      return {
        temperature: data.main.temp,
        feels_like: data.main.feels_like,
        humidity: data.main.humidity,
        wind_speed: data.wind.speed,
        wind_deg: data.wind.deg,
        weather_text: data.weather[0]?.description || 'Unknown',
        clouds: data.clouds.all,  // ดึงข้อมูล clouds
        timestamp: data.dt,
      };
    } catch (error) {
      console.error('Error fetching data from OpenWeather API:', error.message);
      throw new Error(`Error fetching data from OpenWeather API: ${error.message}`);
    }
  };
  