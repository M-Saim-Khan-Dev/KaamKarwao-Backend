require('dotenv').config({ path: require('path').resolve(__dirname, '..', '..', '.env') });
const express = require('express')
const jwt = require('jsonwebtoken')

function log(level, event, fields = {}) {
    console[level](JSON.stringify({ timestamp: new Date().toISOString(), event, ...fields }));
}

const app = express();

const JWT_SIGNING_KEY = process.env.JWT_SIGNING_KEY;
const USER_SERVICE_URL = process.env.USER_SERVICE_URL || 'http://127.0.0.1:8001/';

const ROLES = {
    1: 'Admin',
    2: 'Customer',
    3: 'Worker'
}


const userStatusCache = new Map();
const USER_STATUS_CACHE_TTL_MS = 30_000;


async function fetchUserStatus(userId, req) {
    const cached = userStatusCache.get(userId);
    const now = Date.now();

    if (cached && now < cached.expiry) {
        return cached.data;
    }

    try {
        const response = await fetch(`${USER_SERVICE_URL}internal/user/${userId}/status/`);
        if (!response.ok) {
            log('warn', 'user_status_fetch_failed', { user_id: userId, status: response.status, path: req.originalUrl });
            return null;
        }
        const data = await response.json();
        userStatusCache.set(userId, { data, expiry: now + USER_STATUS_CACHE_TTL_MS });
        return data;
    } catch (err) {
        log('error', 'user_status_fetch_error', { user_id: userId, error: err.message, path: req.originalUrl });
        return null;
    }
}

async function verifyJWT(req, res, next) {
    const authHeader = req.headers['authorization'];
    let token;

    if (authHeader && authHeader.startsWith('Bearer')) {
        token = authHeader.split(' ')[1];
    } else if (req.query && req.query.token) {
        token = req.query.token;
    }

    if (!token) {
        log('warn', 'authentication_rejected', { reason: 'token_missing', path: req.originalUrl });
        return res.status(401).json({ error: 'Authorization header or token query param missing' });
    }

    let payload;
    try {
        payload = jwt.verify(token, JWT_SIGNING_KEY, { algorithms: ['HS256'] });
    } catch (err) {
        log('warn', 'authentication_rejected', { reason: 'token_invalid', path: req.originalUrl });
        return res.status(401).json({ error: 'Invalid or expired token' });
    }

    if (!payload.user_id) {
        log('warn', 'authentication_rejected', { reason: 'user_id_missing', path: req.originalUrl });
        return res.status(401).json({ error: 'Token missing user_id' });
    }

    const userStatus = await fetchUserStatus(payload.user_id, req);
    if (!userStatus) {
        log('warn', 'authentication_rejected', { reason: 'user_status_unavailable', user_id: payload.user_id, path: req.originalUrl });
        return res.status(401).json({ error: 'Could not verify account status' });
    }

    if (userStatus.deleted_at) {
        log('warn', 'authentication_rejected', { reason: 'account_deleted', user_id: payload.user_id, path: req.originalUrl });
        return res.status(401).json({ error: 'This account has been deleted' });
    }
    if (!userStatus.is_active) {
        log('warn', 'authentication_rejected', { reason: 'account_inactive', user_id: payload.user_id, path: req.originalUrl });
        return res.status(401).json({ error: 'This account is inactive' });
    }
    if (userStatus.usertype_id === null || userStatus.usertype_id === undefined) {
        log('warn', 'authentication_rejected', { reason: 'role_missing', user_id: payload.user_id, path: req.originalUrl });
        return res.status(403).json({ error: 'Account has no assigned role' });
    }
    if (userStatus.is_verified !== true) {
        log('warn', 'authentication_rejected', { reason: 'user_unverified', user_id: payload.user_id, path: req.originalUrl });
        return res.status(403).json({ error: 'Account not verified' });
    }

    req.userId = payload.user_id;
    req.isVerified = userStatus.is_verified;
    req.isStaff = userStatus.is_staff || false;
    req.usertypeId = userStatus.usertype_id;
    req.role = ROLES[userStatus.usertype_id] || null;
    log('info', 'authentication_succeeded', { user_id: req.userId, path: req.originalUrl });
    next();
}

function requireRole(...allowedRoles) {
    return (req, res, next) => {
        if (!req.role || !allowedRoles.includes(req.role)) {
            log('warn', 'authorization_rejected', { user_id: req.userId, role: req.role, path: req.originalUrl });
            return res.status(403).json({ error: `Requires one of the roles: ${allowedRoles.join(',')}` });
        }
        next();
    };
}

function withUserHeaders(target) {
    const { createProxyMiddleware } = require('http-proxy-middleware');
    return createProxyMiddleware({
        target,
        changeOrigin: true,
        pathRewrite: (path, req) => req.originalUrl,
        on: {
            proxyReq: (proxyReq, req) => {
                if (req.userId) {
                    proxyReq.setHeader('X-User-Id', req.userId)
                    proxyReq.setHeader('X-Is-Verified', req.isVerified ? 'true' : 'false');
                    proxyReq.setHeader('X-Is-Staff', req.isStaff ? 'true' : 'false');
                    proxyReq.setHeader('X-Usertype-Id', req.usertypeId != null ? String(req.usertypeId) : '');
                }
            },
        },
    });
}

async function optionalJWT(req, res, next) {
    const authHeader = req.headers['authorization'];
    if (!authHeader || !authHeader.startsWith('Bearer')) {
        return next();
    }
    const token = authHeader.split(' ')[1];
    let payload;
    try {
        payload = jwt.verify(token, JWT_SIGNING_KEY, { algorithms: ['HS256'] });
    } catch (err) {
        log('warn', 'optional_authentication_failed', { path: req.originalUrl });
        return next();
    }

    const userStatus = await fetchUserStatus(payload.user_id, req);
    if (userStatus && !userStatus.deleted_at && userStatus.is_active) {
        req.userId = payload.user_id;
        req.isVerified = userStatus.is_verified === true;
        req.isStaff = userStatus.is_staff || false;
        req.usertypeId = userStatus.usertype_id;
        req.role = ROLES[userStatus.usertype_id] || null;
    }
    next();
}

module.exports = { verifyJWT, withUserHeaders, optionalJWT, requireRole };