(function () {
  var LAT = 30.69, LON = -88.04;
  var API = 'https://api.open-meteo.com/v1/forecast?latitude=' + LAT + '&longitude=' + LON +
    '&current=temperature_2m,apparent_temperature,weathercode,windspeed_10m' +
    '&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max,windspeed_10m_max' +
    '&temperature_unit=fahrenheit&windspeed_unit=mph&timezone=America%2FChicago&forecast_days=10';

  function wx(code) {
    if (code === 0) return ['Clear', '\u2600\uFE0F'];
    if (code === 1) return ['Mainly clear', '\uD83C\uDF24\uFE0F'];
    if (code === 2) return ['Partly cloudy', '\u26C5'];
    if (code === 3) return ['Overcast', '\u2601\uFE0F'];
    if (code === 45 || code === 48) return ['Fog', '\uD83C\uDF2B\uFE0F'];
    if (code >= 51 && code <= 57) return ['Drizzle', '\uD83C\uDF26\uFE0F'];
    if ((code >= 61 && code <= 67) || (code >= 80 && code <= 82)) return ['Rain', '\uD83C\uDF27\uFE0F'];
    if ((code >= 71 && code <= 77) || code === 85 || code === 86) return ['Snow', '\u2744\uFE0F'];
    if (code >= 95) return ['Thunderstorms', '\u26C8\uFE0F'];
    return ['Cloudy', '\u26C5'];
  }

  function dayName(iso, i) {
    if (i === 0) return 'Today';
    var d = new Date(iso + 'T12:00:00');
    return d.toLocaleDateString('en-US', { weekday: 'short' });
  }

  function esc(n) { return Math.round(n); }

  function render(data) {
    var c = data.current, dl = data.daily;
    var w0 = wx(c.weathercode);
    var out = '';

    out += '<div class="wx-today">';
    out += '<div class="wx-now"><span class="wx-icon">' + w0[1] + '</span>';
    out += '<div><div class="wx-temp">' + esc(c.temperature_2m) + '&deg;</div>';
    out += '<div class="wx-cond">' + w0[0] + ' in Mobile, AL</div></div></div>';
    out += '<div class="wx-meta">';
    out += '<span>High ' + esc(dl.temperature_2m_max[0]) + '&deg; / Low ' + esc(dl.temperature_2m_min[0]) + '&deg;</span>';
    out += '<span>Feels like ' + esc(c.apparent_temperature) + '&deg;</span>';
    out += '<span>Wind ' + esc(c.windspeed_10m) + ' mph</span>';
    out += '<span>Rain ' + (dl.precipitation_probability_max[0] || 0) + '%</span>';
    out += '</div></div>';

    out += '<div class="wx-days">';
    for (var i = 0; i < dl.time.length; i++) {
      var w = wx(dl.weathercode[i]);
      out += '<div class="wx-day" title="' + w[0] + '">';
      out += '<div class="wx-dname">' + dayName(dl.time[i], i) + '</div>';
      out += '<div class="wx-dicon">' + w[1] + '</div>';
      out += '<div class="wx-dtemp">' + esc(dl.temperature_2m_max[i]) + '&deg; <span>' + esc(dl.temperature_2m_min[i]) + '&deg;</span></div>';
      out += '<div class="wx-draw">' + (dl.precipitation_probability_max[i] || 0) + '%</div>';
      out += '</div>';
    }
    out += '</div>';
    out += '<p class="wx-note">Planning outdoor work? <a href="blog/hurricane-preparedness-mobile-al.html">See our storm prep checklist</a>.</p>';

    document.getElementById('wx-body').innerHTML = out;
  }

  function fallback() {
    document.getElementById('wx-body').innerHTML =
      '<p class="wx-note">Live weather is temporarily unavailable. ' +
      'Check <a href="https://www.foxweather.com/local-weather/alabama/mobile" target="_blank" rel="noopener">FOX Weather Mobile</a> ' +
      'or <a href="https://www.nhc.noaa.gov/" target="_blank" rel="noopener">the National Hurricane Center</a>.</p>';
  }

  if (document.getElementById('wx-body')) {
    fetch(API).then(function (r) { return r.json(); }).then(render).catch(fallback);
  }
})();
