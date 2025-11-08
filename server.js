const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');

const app = express();
const PORT = 3000;

// Serve static files from the React app build directory
app.use(express.static(path.join(__dirname, 'dashboard', 'dist')));

// Proxy API requests to the Flask backend
app.use('/api/v1', createProxyMiddleware({
  target: 'http://localhost:5000',
  changeOrigin: true,
}));

// Serve the React app for all other routes (this handles client-side routing)
app.use((req, res) => {
  res.sendFile(path.join(__dirname, 'dashboard', 'dist', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Dashboard server running on http://localhost:${PORT}`);
});