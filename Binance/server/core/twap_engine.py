from datetime import datetime, timedelta, timezone
import json
import asyncio

class TWAPEngine:
    def __init__(self, order_book_path: str):
        """
        Initialise le moteur TWAP.
        :param order_book_path: Chemin vers le fichier contenant les données du carnet d'ordres.
        """
        self.order_book_path = order_book_path
        self.executions = []

    async def read_order_book(self):
        """
        Lit les dernières données du carnet d'ordres depuis le fichier.
        """
        try:
            with open(self.order_book_path, "r") as f:
                lines = f.readlines()
                if lines:
                    return json.loads(lines[-1])  # Dernière ligne (dernière donnée)
        except FileNotFoundError:
            print(f"Error: File {self.order_book_path} not found.")
        return None

    async def execute_twap(self, symbol: str, quantity: float, duration: int, limit_price: float, side: str):
        """
        Exécute un ordre TWAP.
        :param symbol: Le symbole de la paire (ex. : BTC/USDT).
        :param quantity: Quantité totale à exécuter.
        :param duration: Durée totale de l'exécution (en secondes).
        :param limit_price: Prix limite pour exécuter.
        :param side: "buy" ou "sell".
        """
        slices = duration  # Une tranche par seconde
        slice_quantity = quantity / slices  # Quantité par tranche

        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(seconds=duration)

        print(f"Starting TWAP execution for {symbol}:")
        print(f"Total Quantity: {quantity}, Slice Quantity: {slice_quantity}, Duration: {duration}s")

        while datetime.now(timezone.utc) < end_time:
            order_book = await self.read_order_book()
            if not order_book:
                print("Order book data not available.")
                await asyncio.sleep(1)
                continue

            # Déterminer le prix à utiliser
            price = None
            if side == "buy":
                price = float(order_book["asks"][0][0])  # Meilleur prix ask
            elif side == "sell":
                price = float(order_book["bids"][0][0])  # Meilleur prix bid

            # Vérifier si le prix respecte la contrainte
            if price is not None and ((side == "buy" and price <= limit_price) or (side == "sell" and price >= limit_price)):
                self.executions.append({"timestamp": datetime.now(timezone.utc).isoformat(), "price": price, "quantity": slice_quantity})
                print(f"Executed slice: {slice_quantity} @ {price}")
            else:
                print(f"Price {price} not suitable for execution. Waiting...")

            await asyncio.sleep(1)  # Attendre la tranche suivante

        # Résumé de l'exécution
        total_executed = sum(exec["quantity"] for exec in self.executions)
        avg_price = sum(exec["price"] * exec["quantity"] for exec in self.executions) / total_executed if total_executed > 0 else 0
        print(f"Execution completed: {total_executed}/{quantity} executed.")
        print(f"Average Execution Price: {avg_price}")
        return {"total_executed": total_executed, "avg_price": avg_price, "details": self.executions}



