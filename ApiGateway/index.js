const express = require ('express')
const { createProxyMiddleware } = require ('http-proxy-middleware');
const { verifyJWT, withUserHeaders,optionalJWT   } = require('./middleware/auth');

const app = express();
const cors = require('cors');
app.use(cors());

const USER_SERVICE_URL = process.env.USER_SERVICE_URL || 'http://0.0.0.0:8001/';
const LOCATION_SERVICE_URL = process.env.LOCATION_SERVICE_URL || 'http://0.0.0.0:8002/';
const USER_TYPE_SERVICE_URL = process.env.USERTYPE_SERVICE_URL || 'http://0.0.0.0:8003/';
const CATEGORY_URL = process.env.CATEGORY_URL || 'http://0.0.0.0:8004/';
const PAYMENT_PREFERENCE_URL = process.env.PAYMENT_PREFERENCE_URL || 'http://0.0.0.0:8005/';
const ATTACHMENT_URL = process.env.ATTACHMENT_URL || 'http://0.0.0.0:8006/'
const TASK_URL = process.env.TASK_URL || 'http://0.0.0.0:8007/'
const STATUS_SERVICE_URL = process.env.STATUS_SERVICE_URL || 'http://0.0.0.0:8008/'
const CONFIG_SERVICE_URL = process.env.CONFIG_SERVICE_URL || 'http://0.0.0.0:8009/'

app.use('/app/register', createProxyMiddleware({
    target: USER_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: (path, req) => req.originalUrl,
}))
app.use('/app/user/login', createProxyMiddleware({
    target: USER_SERVICE_URL, changeOrigin: true, pathRewrite: (path, req) => req.originalUrl,
}));
app.use('/app/user/token', createProxyMiddleware({
    target: USER_SERVICE_URL, changeOrigin: true, pathRewrite: (path, req) => req.originalUrl,
}));
app.use('/app/user/token/refresh/', createProxyMiddleware({
    target: USER_SERVICE_URL, changeOrigin: true, pathRewrite: (path, req) => req.originalUrl,
}));

app.use('/app/user/:pk/verify/', createProxyMiddleware({
    target: USER_SERVICE_URL, changeOrigin: true, pathRewrite: (path, req) => req.originalUrl,
}));

app.use('/locations', createProxyMiddleware({
    target: LOCATION_SERVICE_URL, changeOrigin: true, pathRewrite: (path, req) => req.originalUrl,
}));

app.use('/areas', optionalJWT, withUserHeaders(LOCATION_SERVICE_URL));
app.use('/cities', optionalJWT, withUserHeaders(LOCATION_SERVICE_URL));
app.use('/countries', optionalJWT, withUserHeaders(LOCATION_SERVICE_URL));

app.use('/app', verifyJWT, withUserHeaders(USER_SERVICE_URL));
app.use('/usertype', verifyJWT, withUserHeaders(USER_TYPE_SERVICE_URL));
app.use('/category', verifyJWT, withUserHeaders(CATEGORY_URL));
app.use('/paymentpref', verifyJWT, withUserHeaders(PAYMENT_PREFERENCE_URL));
app.use('/attachment', verifyJWT, withUserHeaders(ATTACHMENT_URL));
app.use('/task', verifyJWT, withUserHeaders(TASK_URL));
app.use('/status', verifyJWT, withUserHeaders(STATUS_SERVICE_URL));
app.use('/config', verifyJWT, withUserHeaders(CONFIG_SERVICE_URL));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`API Gateway running on port ${PORT}`));