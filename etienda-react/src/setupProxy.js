const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:8000',  // Reemplaza con la URL de tu servidor Django
      changeOrigin: true,
    })
  );
};
