const express = require ('express')
const { createProxyMiddleware } = require ('http-proxy-middleware');

const app = express();

const USER_SERVICE_URL = process.env.USER_SERVICE_URL || 'https://kaamkarwao-backend-production.up.railway.app/';
const LOCATION_SERVICE_URL = process.env.LOCATION_SERVICE_URL || 'https://hopeful-cooperation-production-0c01.up.railway.app/';

app.use('/app', createProxyMiddleware({
    target: USER_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: (path, req) => req.originalUrl,
}))


app.use('/areas', createProxyMiddleware({ target: LOCATION_SERVICE_URL, changeOrigin: true,  pathRewrite: (path, req) => req.originalUrl, }));
app.use('/cities', createProxyMiddleware({ target: LOCATION_SERVICE_URL, changeOrigin: true,  pathRewrite: (path, req) => req.originalUrl, }));
app.use('/countries', createProxyMiddleware({ target: LOCATION_SERVICE_URL, changeOrigin: true,  pathRewrite: (path, req) => req.originalUrl, }));
app.use('/locations', createProxyMiddleware({ target: LOCATION_SERVICE_URL, changeOrigin: true,  pathRewrite: (path, req) => req.originalUrl, }));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`API Gateway running on port ${PORT}`));