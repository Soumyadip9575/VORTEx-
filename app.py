from flask import Flask, request, jsonify, render_template
from datetime import datetime
import math
import random

app = Flask(__name__)

# --- In-Memory Database ---
account = {
    "main_balance": 10000.0,
    "piggy_bank": 0.0
}
transactions = []

# --- EXTENDED MILESTONES ---
milestones = [
    {"id": 1, "desc": "Spend ₹500 total", "target": 500, "progress": 0, "category": "Any", "done": False},
    {"id": 2, "desc": "Spend ₹300 on Food", "target": 300, "progress": 0, "category": "Food", "done": False},
    {"id": 3, "desc": "Spend ₹1000 on Travel", "target": 1000, "progress": 0, "category": "Travel", "done": False},
    {"id": 4, "desc": "Spend ₹500 on Shopping", "target": 500, "progress": 0, "category": "Shopping", "done": False},
    {"id": 5, "desc": "Spend ₹200 on Recharge", "target": 200, "progress": 0, "category": "Recharge", "done": False},
    {"id": 6, "desc": "Spend ₹2000 total", "target": 2000, "progress": 0, "category": "Any", "done": False},
    {"id": 7, "desc": "Spend ₹800 on Food", "target": 800, "progress": 0, "category": "Food", "done": False}
]

def predict_next_spend(spends):
    n = len(spends)
    if n < 2: return spends[0] if n == 1 else 0.0
    x = list(range(1, n + 1)) 
    y = spends                
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
    if denominator == 0: return mean_y
    m = numerator / denominator
    b = mean_y - m * mean_x
    return max(0.0, (m * (n + 1)) + b) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == 'admin' and data.get('password') == 'password':
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Invalid credentials"}), 401

@app.route('/api/state', methods=['GET'])
def get_state():
    analytics = {}
    for t in transactions:
        if t['type'] == 'Spend':
            analytics[t['category']] = analytics.get(t['category'], 0) + t['amount']
    
    ai_offer = "Keep spending to unlock personalized AI offers!"
    if len(analytics) > 0:
        top_category = max(analytics, key=analytics.get)
        ai_offer = f"✨ AI Insight: You love {top_category}! Spend more here for rewards!"

    spends = [t['amount'] for t in transactions if t['type'] == 'Spend']
    prediction = "Need more data to predict."
    if len(spends) > 1:
        prediction = f"🔮 ML Predicts next spend: ₹{round(predict_next_spend(spends), 2)}"

    active_milestone = next((m for m in milestones if not m['done']), None)

    return jsonify({
        "account": account,
        "transactions": transactions[::-1], # Newest first
        "active_milestone": active_milestone,
        "prediction": prediction,
        "ai_offer": ai_offer
    })

@app.route('/api/add_money', methods=['POST'])
def add_money():
    data = request.json
    amount = float(data.get('amount', 0))
    method = data.get('method', 'Bank Transfer') 
    
    if amount <= 0: return jsonify({"error": "Invalid amount"}), 400
    
    account['main_balance'] += amount
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    transactions.append({"date": now, "type": "Deposit", "amount": amount, "category": method, "receiver": "Main Account"})
    return jsonify({"success": True})

@app.route('/api/spend', methods=['POST'])
def spend_money():
    data = request.json
    amount = float(data.get('amount', 0))
    category = data.get('category', 'Others')
    upi_id = data.get('upi_id', 'Unknown')
    receiver_name = data.get('receiver_name', 'Merchant')
    round_to = int(data.get('round_to', 10))

    if amount <= 0: return jsonify({"error": "Invalid amount"}), 400
    if round_to not in [10, 100]: round_to = 10 

    platform_fee = 1.0 if amount > 50 else 0.0
    rounded_amount = math.ceil(amount / float(round_to)) * round_to
    spare_change = rounded_amount - amount
    
    total_deduction = amount + platform_fee + spare_change

    if account['main_balance'] < total_deduction:
        return jsonify({"error": "Insufficient funds"}), 400

    account['main_balance'] -= total_deduction
    account['piggy_bank'] += spare_change

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    transactions.append({"date": now, "type": "Spend", "amount": amount, "category": category, "receiver": receiver_name, "upi": upi_id})
    
    if platform_fee > 0:
        transactions.append({"date": now, "type": "Fee", "amount": platform_fee, "category": "Platform Fee", "receiver": "FinPay Network"})
    if spare_change > 0:
        transactions.append({"date": now, "type": "Round-Up", "amount": round(spare_change, 2), "category": f"Saved in Piggy Bank (Nearest ₹{round_to})", "receiver": "Piggy Bank"})

    # --- MILESTONE & ADVANCED REWARD LOGIC ---
    active_m = next((m for m in milestones if not m['done']), None)
    if active_m and (active_m['category'] == 'Any' or active_m['category'] == category):
        active_m['progress'] += amount
        if active_m['progress'] >= active_m['target']:
            active_m['done'] = True
            
            # The Reward Pool (Cash has multiple entries to make it more likely to hit)
            reward_pool = ['cash', 'cash', 'food_coupon', 'travel_coupon', 'shopping_coupon', 'movie_ticket', 'recharge_discount']
            reward_type = random.choice(reward_pool)
            
            if reward_type == 'cash':
                # Weighted Randomizer: 75% chance for ₹1-₹5, 25% chance for ₹6-₹9
                if random.random() < 0.75:
                    cash_reward = random.randint(1, 5)
                else:
                    cash_reward = random.randint(6, 9)
                    
                account['piggy_bank'] += cash_reward
                transactions.append({"date": now, "type": "Cashback", "amount": cash_reward, "category": "Reward", "receiver": f"₹{cash_reward} Cash!"})
                
            elif reward_type == 'food_coupon':
                transactions.append({"date": now, "type": "Coupon", "amount": 0, "category": "Reward", "receiver": "50% Off Domino's!"})
            elif reward_type == 'travel_coupon':
                transactions.append({"date": now, "type": "Coupon", "amount": 0, "category": "Reward", "receiver": "₹250 Off Uber!"})
            elif reward_type == 'shopping_coupon':
                transactions.append({"date": now, "type": "Coupon", "amount": 0, "category": "Reward", "receiver": "10% Off Amazon!"})
            elif reward_type == 'movie_ticket':
                transactions.append({"date": now, "type": "Coupon", "amount": 0, "category": "Reward", "receiver": "BOGO Movie Ticket!"})
            elif reward_type == 'recharge_discount':
                transactions.append({"date": now, "type": "Coupon", "amount": 0, "category": "Reward", "receiver": "₹50 Off Jio/Airtel!"})

    return jsonify({"success": True})
@app.route('/api/donate', methods=['POST'])
def donate():
    data = request.json
    amount = float(data.get('amount', 0))
    charity = data.get('charity', 'General Fund')

    if amount <= 0 or account['main_balance'] < amount:
        return jsonify({"error": "Invalid amount or Insufficient funds"}), 400

    account['main_balance'] -= amount
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # Added to transactions feed
    transactions.append({"date": now, "type": "Donation", "amount": amount, "category": "Charity", "receiver": charity})
    return jsonify({"success": True})

@app.route('/api/redeem', methods=['POST'])
def redeem():
    if account['piggy_bank'] > 0:
        amount = account['piggy_bank']
        account['main_balance'] += amount
        account['piggy_bank'] = 0.0
        transactions.append({"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "type": "Redeem", "amount": round(amount, 2), "category": "Piggy Bank to Main", "receiver": "Self"})
        return jsonify({"success": True})
    return jsonify({"error": "Empty"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')