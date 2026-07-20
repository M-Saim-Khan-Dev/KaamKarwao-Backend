require('dotenv').config({ path: require('path').resolve(__dirname, '..', '..', '.env') });
console.log("JWT_SIGNING_KEY loaded:", process.env.JWT_SIGNING_KEY ? "yes" : "NO - undefined!");
const express = require('express')
const jwt = require('jsonwebtoken')

const app = express();

const JWT_SIGNING_KEY = process.env.JWT_SIGNING_KEY;

const ROLES = {
    1: 'Admin',
    2: 'Customer',
    3: 'Worker'
}

function verifyJWT(req,res,next){
    const authHeader = req.headers['authorization'];
    let token;

    if (authHeader && authHeader.startsWith('Bearer')) {
        token = authHeader.split(' ')[1];
    } else if (req.query && req.query.token){
        token = req.query.token;
    }

    if (!token){
        return res.status(401).json({ error: 'Authorization header or token query param missing' });
    }

    try{
        const payload = jwt.verify(token, JWT_SIGNING_KEY, {algorithms: ['HS256']});
        if (!payload.user_id) {
            return res.status(401).json({ error: 'Token missing user_id' });
        }
        if(payload.usertype_id === null || payload.usertype_id === undefined){
            return res.status(403).json({error : 'Account has no assigned role'})
        }
        if (payload.is_verified !== true) {
            return res.status(403).json({ error: 'Account not verified' });
        }
        req.userId = payload.user_id;
        req.isVerified = true;
        req.isStaff = payload.is_staff || false;
        req.usertypeId = payload.usertype_id;
        req.role = ROLES[payload.usertype_id] || null;
        next();
    } catch(err){
        return res.status(401).json({error: 'Invalid or expired token'})
    }
}

function requireRole(...allowedRoles){
    return(req,res,next) => {
        if (!req.role || !allowedRoles.includes(req.role)){
            return res.status(403).json({error: `Requires one of the roles: ${allowedRoles.join(',')}`})
        }
        next();
    };
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
                    proxyReq.setHeader('X-Usertype-Id', req.usertypeId != null ? String(req.usertypeId) : '');
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
        req.role = ROLES[payload.usertype_id] || null;
    }catch (err) {

    }
    next();
}

module.exports = { verifyJWT,withUserHeaders, optionalJWT, requireRole  };
