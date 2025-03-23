from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional

from app.domain.entities.order import Order
from app.domain.entities.order import OrderDb
from app.domain.entities.order import OrderStatus
from app.domain.entities.payment import PaymentStatus


class IOrderRepository(ABC):
    @abstractmethod
    def add_order(self, order: Order, status: OrderStatus) -> OrderDb:
        pass

    @abstractmethod
    def cancel_order(self, order_id: int) -> bool:
        pass

    @abstractmethod
    def get_order(self, order_id: int) -> Optional[OrderDb]:
        pass

    @abstractmethod
    def get_all_orders(self) -> List[OrderDb]:
        pass

    @abstractmethod
    def update_order_status(self, order_id: int, status: OrderStatus) -> Optional[OrderDb]:
        """
        Update order status as Placed > Preparing > Ready > Delivered > Finalized
        """
        pass

    @abstractmethod
    def update_payment_status(
        self, order_id: int, payment_status: PaymentStatus
    ) -> Optional[OrderDb]:
        pass

    @abstractmethod
    def get_filtered_orders(self) -> List[OrderDb]:
        """
        Returns orders excluding 'FINALIZED', sorted by:
          - status order
            - READY > PREPARING > RECEIVED
          - older orders first
        """
        pass
