const express = require('express')
const http = require('http')
const { createProxyMiddleware } = require('http-proxy-middleware');
const { verifyJWT, withUserHeaders, optionalJWT, requireRole } = require('./middleware/auth');
const routeMap = require('./routeMap');
const SERVICE_URLS = require('./serviceUrls');

function maskedProxy(target, PublicPath, RealPath) {
    return createProxyMiddleware({
        target,
        changeOrigin: true,
        pathRewrite: (path, req) => {
            let rewritten = req.originalUrl.replace(PublicPath, RealPath);
            rewritten = rewritten.replace(/\/{2,}/g, '/');
            return rewritten;
        },
        on: {
            proxyReq: (proxyReq, req) => {
                if (req.userId) {
                    proxyReq.setHeader('X-User-Id', req.userId);
                    proxyReq.setHeader('X-Is-Verified', req.isVerified ? 'true' : 'false');
                    proxyReq.setHeader('X-Is-Staff', req.isStaff ? 'true' : 'false');
                    proxyReq.setHeader('X-Usertype-Id', req.usertypeId != null ? String(req.usertypeId) : '');
                }
            }
        }
    })
}

const app = express();
const cors = require('cors');
app.use(cors());

for (const route of routeMap) {
    const target = SERVICE_URLS[route.target];
    const middlewares = []

    if (route.auth === 'optional') {
        middlewares.push(optionalJWT);
    } else if (route.auth === 'required') {
        middlewares.push(verifyJWT);
    }
    if (route.roles) {
        middlewares.push(requireRole(...route.roles));
    }
    app.use(route.publicPath, ...middlewares, maskedProxy(target, route.publicPath, route.realPath));
}

const taskWsProxy = createProxyMiddleware({
    target: SERVICE_URLS.TASK_URL,
    changeOrigin: true,
    ws: true,
    pathRewrite: (path, req) => req.originalUrl,
});

app.use('/ws/tasks', verifyJWT, taskWsProxy);

const docsRouter = require('./docs');
app.use('/api-docs', docsRouter);

const PORT = process.env.PORT || 3000;
const server = http.createServer(app);
server.on('upgrade', taskWsProxy.upgrade)
server.listen(PORT, () => console.log(`API Gateway running on port ${PORT}`));