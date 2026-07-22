const routes = [
    {
        publicPath: '/app/register',
        realPath: '/app/register/user/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'none'
    },
    {
        publicPath: '/app/login',
        realPath: '/app/user/login/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'none'
    },
    {
        publicPath: '/app/token',
        realPath: '/app/user/token/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'none'
    },
    {
        publicPath: '/app/token/refresh',
        realPath: '/app/user/token/refresh/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'none'
    },
    {
        publicPath: '/app/verify/:pk',
        realPath: '/app/user/verify/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'none'
    },

    {
        publicPath: '/app/location',
        realPath: '/locations/',
        service: 'location',
        target: 'LOCATION_SERVICE_URL',
        auth: 'none'
    },
    {
        publicPath: '/app/area',
        realPath: '/areas/',
        service: 'location',
        target: 'LOCATION_SERVICE_URL',
        auth: 'optional'
    },
    {
        publicPath: '/app/city',
        realPath: '/cities/',
        service: 'location',
        target: 'LOCATION_SERVICE_URL',
        auth: 'optional'
    },
    {
        publicPath: '/app/country',
        realPath: '/countries/',
        service: 'location',
        target: 'LOCATION_SERVICE_URL',
        auth: 'optional'
    },

    {
        publicPath: '/app/review',
        realPath: '/review_service/',
        service: 'review',
        target: 'REVIEW_SERVICE_URL',
        auth: 'optional'
    },

    {
        publicPath: '/app/professional/earning',
        realPath: '/earnings/',
        service: 'earnings',
        target: 'EARNINGS_SERVICE_URL',
        auth: 'required',
        roles: ['Worker', 'Admin']
    },
    {
        publicPath: '/app/update/user',
        realPath: '/app/user/update/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'required',
        roles: ['Customer', 'Admin', 'Worker']
    },
    {
        publicPath: '/app/update/user/image',
        realPath: '/app/user/update/image/',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'required',
        roles: ['Customer', 'Admin']
    },
    {
        publicPath: '/app/usertype',
        realPath: '/usertype_service/',
        service: 'usertype',
        target: 'USER_TYPE_SERVICE_URL',
        auth: 'required',
        roles: ['Admin']
    },
    {
        publicPath: '/app/category',
        realPath: '/category_service/',
        service: 'category',
        target: 'CATEGORY_URL',
        auth: 'required',
        roles: ['Customer', 'Admin', 'Worker']
    },
    {
        publicPath: '/app/paymentpref',
        realPath: '/paymentpref_service/',
        service: 'paymentpref',
        target: 'PAYMENT_PREFERENCE_URL',
        auth: 'required',
        roles: ['Customer', 'Admin']
    },
    {
        publicPath: '/app/attachment',
        realPath: '/attachment_service/',
        service: 'attachment',
        target: 'ATTACHMENT_URL',
        auth: 'required',
        roles: ['Customer', 'Admin']
    },
    {
        publicPath: '/app/profile',
        realPath: '/app/user/info',
        service: 'user',
        target: 'USER_SERVICE_URL',
        auth: 'required',
        roles: ['Customer', 'Admin', 'Worker']
    },
    {
        publicPath: '/app/task',
        realPath: '/task_service/',
        service: 'task',
        target: 'TASK_URL',
        auth: 'required',
        roles: ['Customer', 'Worker', 'Admin']
    },
    {
        publicPath: '/app/status',
        realPath: '/status_service/',
        service: 'status',
        target: 'STATUS_SERVICE_URL',
        auth: 'required',
        roles: ['Customer', 'Worker', 'Admin']
    },
    {
        publicPath: '/app/config',
        realPath: '/configuration_service/',
        service: 'config',
        target: 'CONFIG_SERVICE_URL',
        auth: 'required',
        roles: ['Admin']
    },
    {
        publicPath: '/app/bidding',
        realPath: '/bidding_service/',
        service: 'bidding',
        target: 'BIDDING_SERVICE_URL',
        auth: 'required',
        roles:['Customer', 'Worker', 'Admin']
    },
];
module.exports = [...routes].sort((a, b) => b.publicPath.length - a.publicPath.length);