// App.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
// Bootstrap CSS
import "bootstrap/dist/css/bootstrap.min.css";
// Bootstrap Bundle JS
import "bootstrap/dist/js/bootstrap.bundle.min";

const App = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await axios.post(
        'http://localhost:8000/api/productos/buscar',
        { query: searchTerm }
      );

      setSearchResults(response.data);
    } catch (error) {
      console.error('Error al realizar la búsqueda:', error);
    }
  };

  return (
    <div>
      <h1>Tienda Virtual</h1>
      <input
        type="text"
        placeholder="Buscar productos"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <button onClick={handleSearch}>Buscar</button>

      <ul>
        {searchResults.map((producto) => (
          <li key={producto.id}>{producto.titulo} - {producto.descripcion}</li>
        ))}
      </ul>
    </div>
  );
};

export default App;

