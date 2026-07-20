const express = require('express');
const swaggerUi = require('swagger-ui-express');
const routeMap = require('./routeMap');
const SERVICE_URLS = require('./serviceUrls');

const router = express.Router();

const SERVICES = [...new Set(routeMap.map(r => r.service))].map(name => {
    const entry = routeMap.find(r => r.service === name);
    return { name, url: SERVICE_URLS[entry.target] };
});

let cachedSchema = null;
let cacheExpiry = 0;
const CACHE_TTL_MS = 60_000;

function maskPath(realPath, serviceName) {
    const match = routeMap
        .filter(r => r.service === serviceName)
        .find(r => realPath.startsWith(r.realPath.replace(/\/$/, '')));

    if (!match) return null;

    const suffix = realPath.slice(match.realPath.replace(/\/$/, '').length);
    return (match.publicPath.replace(/:pk/, '') + suffix).replace(/\/{2,}/g, '/');
}

function rewriteRefs(node, serviceName) {
    if (Array.isArray(node)) {
        return node.map(item => rewriteRefs(item, serviceName));
    }
    if (node && typeof node === 'object') {
        const result = {};
        for (const [key, value] of Object.entries(node)) {
            if (key === '$ref' && typeof value === 'string' && value.startsWith('#/components/schemas/')) {
                const originalName = value.replace('#/components/schemas/', '');
                result[key] = `#/components/schemas/${serviceName}_${originalName}`;
            } else {
                result[key] = rewriteRefs(value, serviceName);
            }
        }
        return result;
    }
    return node;
}

async function buildMergedSchema() {
    const merged = {
        openapi: '3.0.3',
        info: { title: 'KamKarwao API Gateway', version: '1.0.0' },
        paths: {},
        components: {
            schemas: {},
            securitySchemes: {
                bearerAuth: { type: 'http', scheme: 'bearer', bearerFormat: 'JWT' },
            },
        },
        security: [{ bearerAuth: [] }],
    };

    for (const service of SERVICES) {
        try {
            const response = await fetch(`${service.url}schema/?format=json`);
            if (!response.ok) continue;
            const schema = await response.json();
            const fixedSchema = rewriteRefs(schema, service.name);

            for (const [realPath, methods] of Object.entries(fixedSchema.paths || {})) {
                const masked = maskPath(realPath, service.name);
                if (masked) {
                    merged.paths[masked] = methods;
                }
            }

            for (const [schemaName, def] of Object.entries(fixedSchema.components?.schemas || {})) {
                merged.components.schemas[`${service.name}_${schemaName}`] = def;
            }
        } catch (err) {
            console.error(`Failed to fetch schema for ${service.name}:`, err.message);
        }
    }
    return merged;
}

router.get('/schema.json', async (req, res) => {
    const now = Date.now();
    if (!cachedSchema || now > cacheExpiry) {
        cachedSchema = await buildMergedSchema();
        cacheExpiry = now + CACHE_TTL_MS;
    }
    res.json(cachedSchema);
});

router.use('/docs', swaggerUi.serve, swaggerUi.setup(null, {
    swaggerOptions: { url: '/api-docs/schema.json' },
}));

module.exports = router;