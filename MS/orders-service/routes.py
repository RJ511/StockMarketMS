from fastapi import APIRouter  # type: ignore
from Controllers.OrderController import create_order

router = APIRouter()

router.add_api_route("/orders", create_order, methods=["POST"])