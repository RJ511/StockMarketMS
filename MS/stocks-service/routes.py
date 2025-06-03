from fastapi import APIRouter  # type: ignore
from Controllers.StockController import create_stock, get_stock

router = APIRouter()

router.add_api_route("/stocks", create_stock, methods=["POST"])
router.add_api_route("/stocks/{ticker}", get_stock, methods=["GET"])