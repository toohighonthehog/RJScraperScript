document.addEventListener('DOMContentLoaded', () => {
    fetch('/records')
      .then(response => response.json())
      .then(data => {
        const recordsDiv = document.getElementById('records');
        data.forEach(record => {
          const recordElement = document.createElement('div');
          recordElement.textContent = `ID: ${record.id}, Name: ${record.name}, Age: ${record.age}`;
          recordsDiv.appendChild(recordElement);
        });
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  });
  