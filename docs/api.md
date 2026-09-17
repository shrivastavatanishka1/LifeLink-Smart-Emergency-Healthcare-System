# API

POST /api/users/register
POST /api/users/login
GET /api/users/me
POST /api/health/readings
GET /api/health/readings
POST /api/alerts
GET /api/alerts
PATCH /api/alerts/<id>/acknowledge
GET /api/blood/compatible/<group>
GET /api/blood/inventory
POST /api/blood/inventory

Protected endpoints use:
Authorization: Bearer <JWT>
