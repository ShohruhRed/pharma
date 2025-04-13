from fastapi import APIRouter
from . import routes_ml, routes_sanfis, routers_batches, routes_stages, routes_predictions, routers_stage_data, routers_stage_predictions# + routes_batches, routes_stages если добавишь

router = APIRouter()
router.include_router(routes_ml.router)
router.include_router(routes_sanfis.router)
router.include_router(routers_batches.router)
router.include_router(routes_stages.router)
router.include_router(routes_predictions.router)
router.include_router(routers_stage_data.router)
router.include_router(routers_stage_predictions.router)
