module.exports = {
    USER_SERVICE_URL: process.env.USER_SERVICE_URL || 'http://0.0.0.0:8001/',
    LOCATION_SERVICE_URL: process.env.LOCATION_SERVICE_URL || 'http://0.0.0.0:8002/',
    USER_TYPE_SERVICE_URL: process.env.USERTYPE_SERVICE_URL || 'http://0.0.0.0:8003/',
    CATEGORY_URL: process.env.CATEGORY_URL || 'http://0.0.0.0:8004/',
    PAYMENT_PREFERENCE_URL: process.env.PAYMENT_PREFERENCE_URL || 'http://0.0.0.0:8005/',
    ATTACHMENT_URL: process.env.ATTACHMENT_URL || 'http://0.0.0.0:8006/',
    TASK_URL: process.env.TASK_URL || 'http://0.0.0.0:8007/',
    STATUS_SERVICE_URL: process.env.STATUS_SERVICE_URL || 'http://0.0.0.0:8008/',
    CONFIG_SERVICE_URL: process.env.CONFIG_SERVICE_URL || 'http://0.0.0.0:8009/',
    EARNINGS_SERVICE_URL: process.env.EARNINGS_SERVICE_URL || 'http://0.0.0.0:8010/',
    REVIEW_SERVICE_URL: process.env.REVIEW_SERVICE_URL || 'http://0.0.0.0:8011/',
};