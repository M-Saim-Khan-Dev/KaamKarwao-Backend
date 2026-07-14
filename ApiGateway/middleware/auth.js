require('dotenv').config({ path: require('path').resolve(__dirname, '..', '..', '.env') });
console.log("JWT_SIGNING_KEY loaded:", process.env.JWT_SIGNING_KEY ? "yes" : "NO - undefined!");
const express = require('express')
const jwt = require('jsonwebtoken')

const app = express();

const JWT_SIGNING_KEY = process.env.JWT_SIGNING_KEY;

function verifyJWT(req,res,next){
    const authHeader = req.headers['authorization'];

    if (!authHeader || !authHeader.startsWith('Bearer')) {
        return res.status(401).json({error : 'Authorization header missing or malformed'});
    }

    const token = authHeader.split(' ')[1];

    try{
        const payload = jwt.verify(token, JWT_SIGNING_KEY, {algorithms: ['HS256']});
        if (!payload.user_id) {
            return res.status(401).json({ error: 'Token missing user_id' });
        }
        if (payload.is_verified !== true) {
            return res.status(403).json({ error: 'Account not verified' });
        }
        req.userId = payload.user_id;
        req.isVerified = true;
        req.isStaff = payload.is_staff || false;
        next();
    } catch(err){
        return res.status(401).json({error: 'Invalid or expired token'})
    }
}

function withUserHeaders(target){
    const { createProxyMiddleware } = require('http-proxy-middleware');
    return createProxyMiddleware({
        target,
        changeOrigin: true,
        pathRewrite:(path, req)=>req.originalUrl,
        on:{
            proxyReq: (proxyReq, req)=>{
                if (req.userId){
                    proxyReq.setHeader('X-User-Id', req.userId)
                    proxyReq.setHeader('X-Is-Verified', req.isVerified?'true':'false');
                    proxyReq.setHeader('X-Is-Staff', req.isStaff ? 'true' : 'false');
                }
            },
        },
    });
}

function optionalJWT(req,res,next){
    const authHeader = req.headers['authorization'];
    if (!authHeader || !authHeader.startsWith('Bearer')){
        return next();
    }
    const token = authHeader.split(' ')[1];
    try{
        const payload = jwt.verify(token, JWT_SIGNING_KEY, {algorithms:['HS256']});
        req.userId = payload.user_id;
        req.isVerified = payload.is_verified === true;
        req.isStaff = payload.is_staff || false;
    }catch (err) {

    }
    next();
}

module.exports = { verifyJWT,withUserHeaders, optionalJWT };
