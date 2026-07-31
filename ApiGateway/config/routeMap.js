const { API_PREFIX } = require('../constants/constants');

console.log('API_PREFIX loaded as:', API_PREFIX);

const routes = [
    {
        publicPath: `${API_PREFIX}/register`,
        realPath: `/app/register/user/`,
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'none'
    },
    {
        publicPath: `${API_PREFIX}/login`,
        realPath: '/app/user/login/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'none'
    },
    {
        publicPath: `${API_PREFIX}/token`,
        realPath: '/app/user/token/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'none'
    },
    {
        publicPath: `${API_PREFIX}/token/refresh`,
        realPath: '/app/user/token/refresh/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'none'
    },
    {
        publicPath: `${API_PREFIX}/verify/:pk`,
        realPath: '/app/user/verify/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'none'
    },

    {
        publicPath: `${API_PREFIX}/location`,
        realPath: '/locations/',
        service: 'location',
        target: 'LOCATION_SERVICE_URL',
        auth: 'none'
    },
    {
        publicPath: `${API_PREFIX}/area`,
        realPath: '/areas/',
        service: 'location',
        target: 'LOCATION_SERVICE_URL',
        auth: 'optional'
    },
    {
        publicPath: `${API_PREFIX}/city`,
        realPath: '/cities/',
        service: 'location',
        target: 'LOCATION_SERVICE_URL',
        auth: 'optional'
    },
    {
        publicPath: `${API_PREFIX}/country`,
        realPath: '/countries/',
        service: 'location',
        target: 'LOCATION_SERVICE_URL',
        auth: 'optional'
    },

    {
        publicPath: `${API_PREFIX}/review`,
        realPath: '/review_service/',
        service: 'review',
        target: 'REVIEW_SERVICE_URL',
        auth: 'optional'
    },

    {
        publicPath: `${API_PREFIX}/professional/earning`,
        realPath: '/earnings/',
        service: 'earnings',
        target: 'EARNINGS_SERVICE_URL',
        auth: 'required',
        roles: ['Worker', 'Admin']
    },
    {
        publicPath: `${API_PREFIX}/update/user`,
        realPath: '/app/user/update/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'required',
        roles: ['Customer', 'Admin', 'Worker']
    },
    {
        publicPath: `${API_PREFIX}/user/phone`,
        realPath: '/app/user/check-phone/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'none',
    },
    {
        publicPath: `${API_PREFIX}/delete/user`,
        realPath: '/app/user/delete/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'required',
        roles: ['Customer', 'Admin', 'Worker']
    },
    {
        publicPath: `${API_PREFIX}/update/user/image`,
        realPath: '/app/user/update/image/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'required',
        roles: ['Customer', 'Admin']
    },
    {
        publicPath: `${API_PREFIX}/admin`,
        realPath: '/administrator/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'required',
        roles: ['Admin']
    },
    {
        publicPath: `${API_PREFIX}/wallet`,
        realPath: '/wallet/',
        service: 'wallet',
        target: 'WALLET_SERVICE_URL',
        auth: 'required',
        roles: ['Customer', 'Admin', 'Worker']
    },
    {
        publicPath: `${API_PREFIX}/usertype`,
        realPath: '/usertype_service/',
        service: 'usertype',
        target: 'USER_TYPE_SERVICE_URL',
        auth: 'required',
        roles: ['Admin']
    },
    {
        publicPath: `${API_PREFIX}/category`,
        realPath: '/category_service/',
        service: 'category',
        target: 'CATEGORY_URL',
        auth: 'required',
        roles: ['Customer', 'Admin', 'Worker']
    },
    {
        publicPath: `${API_PREFIX}/sub/category`,
        realPath: '/subcategory_service/',
        service: 'subcategory',
        target: 'CATEGORY_URL',
        auth: 'required',
        roles: ['Customer', 'Admin', 'Worker']
    },
    {
        publicPath: `${API_PREFIX}/paymentpref`,
        realPath: '/paymentpref_service/',
        service: 'paymentpref',
        target: 'PAYMENT_PREFERENCE_URL',
        auth: 'required',
        roles: ['Customer', 'Admin', 'Worker']
    },
    {
        publicPath: `${API_PREFIX}/attachment`,
        realPath: '/attachment_service/',
        service: 'attachment',
        target: 'ATTACHMENT_URL',
        auth: 'required',
        roles: ['Customer', 'Admin','Worker']
    },
    {
        publicPath: `${API_PREFIX}/profile`,
        realPath: '/app/user/info',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'required',
        roles: ['Customer', 'Admin', 'Worker']
    },
    {
        publicPath: `${API_PREFIX}/task`,
        realPath: '/task_service/',
        service: 'task',
        target: 'TASK_URL',
        auth: 'required',
        roles: ['Customer', 'Worker', 'Admin']
    },
    {
        publicPath: `${API_PREFIX}/status`,
        realPath: '/status_service/',
        service: 'status',
        target: 'STATUS_SERVICE_URL',
        auth: 'required',
        roles: ['Customer', 'Worker', 'Admin']
    },
    {
        publicPath: `${API_PREFIX}/config`,
        realPath: '/configuration_service/',
        service: 'config',
        target: 'CONFIG_SERVICE_URL',
        auth: 'required',
        roles: ['Admin']
    },
    {
        publicPath: `${API_PREFIX}/bidding`,
        realPath: '/bidding_service/',
        service: 'bidding',
        target: 'BIDDING_SERVICE_URL',
        auth: 'required',
        roles:['Customer', 'Worker', 'Admin']
    },
    {
    publicPath: `${API_PREFIX}/message`,
    realPath: '/messages/',
    service: 'message',
    target: 'MESSAGE_SERVICE_URL',
    auth: 'required',
    roles: ['Customer', 'Worker', 'Admin']
    },
];
module.exports = [...routes].sort((a, b) => b.publicPath.length - a.publicPath.length);