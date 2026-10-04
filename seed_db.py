from models import db, User, Card, Transaction
import random
from datetime import datetime

def seed():
    u = User(username='demo', password='demo123', name='Muhammad')
    db.session.add(u)
    db.session.commit()

    c = Card(user_id=u.id, card_number_masked='**** **** **** 4912', expiry='12/29', status='PROTECTED')
    db.session.add(c)
    db.session.commit()

    txns = [
        ("TXN001", "Today", "09:15", "Amazon", "Shopping", 2499, "Chennai", 8, "Safe", 0, "Normal pattern"),
        ("TXN002", "Today", "11:30", "Swiggy", "Food", 650, "Chennai", 5, "Safe", 0, "Normal pattern"),
        ("TXN003", "Today", "14:45", "Unknown Merchant", "Online", 28900, "Mumbai", 87, "Suspicious", 1, "Unusual amount + unusual location + unusual transaction time"),
        ("TXN004", "Today", "16:10", "BookMyShow", "Entertainment", 850, "Chennai", 7, "Safe", 0, "Normal pattern"),
        ("TXN005", "Yesterday", "10:00", "Starbucks", "Food", 350, "Chennai", 2, "Safe", 0, "Normal pattern"),
        ("TXN006", "Yesterday", "23:45", "Foreign Store", "Shopping", 15000, "Foreign Country", 92, "Fraud", 1, "Unusual amount + unusual location"),
    ]

    for t in txns:
        txn = Transaction(
            txn_id=t[0], date=t[1], time=t[2], merchant=t[3],
            category=t[4], amount=t[5], location=t[6],
            risk_score=t[7], status=t[8], prediction=t[9], reason=t[10]
        )
        db.session.add(txn)
    
    db.session.commit()
