You can create market or pending order with the commands.

```python
CtraderFix.buy("GBPUSD", 0.01, 1.18, 1.19)
```

```python
CtraderFix.sell("GBPUSD", 0.01, 1.19, 1.18)
```

# Limit

```python
CtraderFix.buyLimit("GBPUSD", 0.01, 1.17, 1.19, 1.18)
CtraderFix.sellLimit("GBPUSD", 0.01, 1.23, 1.17, 1.22)
```

# Stop

```python
CtraderFix.buyStop("GBPUSD", 0.01, 1.20, 1.24, 1.22)
CtraderFix.sellStop("GBPUSD", 0.01, 1.19, 1.17, 1.18)
```

# Positions

```python
positions = CtraderFix.positions()
print(positions)
for position in positions:
    CtraderFix.positionCloseById(position['pos_id'], position['amount'])

positions = CtraderFix.positions()
print(positions)

```

# Orders

```python
Corders = CtraderFix.orders()
print(orders)
for order in orders:
    CtraderFix.orderCancelById(order['ord_id'])

orders = CtraderFix.orders()
print(orders)

```

# If you want to cancel all Orders

```python
CtraderFix.cancel_all()
```

# if you want to close all positions

```python
CtraderFix.close_all()
```

```

```
