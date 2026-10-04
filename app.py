from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from models import db, User, Card, Transaction
import ml_module
import seed_db
import os

app = Flask(__name__)
app.secret_key = 'demo_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.first():
        seed_db.seed()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['name'] = user.name
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid demo credentials. Use demo/demo123")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    card = Card.query.filter_by(user_id=session['user_id']).first()
    recent_txns = Transaction.query.order_by(Transaction.id.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                           name=session['name'], 
                           card=card, 
                           recent_txns=recent_txns,
                           stats={
                               'total_txns': 1248,
                               'total_spending': 48650,
                               'fraud_txns': 18,
                               'detection_rate': 98.7
                           })

@app.route('/security')
def security():
    if 'user_id' not in session: return redirect(url_for('login'))
    card = Card.query.filter_by(user_id=session['user_id']).first()
    return render_template('security.html', card=card, name=session['name'])

@app.route('/transactions')
def transactions():
    if 'user_id' not in session: return redirect(url_for('login'))
    txns = Transaction.query.all()
    return render_template('transactions.html', txns=txns, name=session['name'])

@app.route('/fraud_detection')
def fraud_detection():
    if 'user_id' not in session: return redirect(url_for('login'))
    metrics = ml_module.get_metrics()
    info = ml_module.explain_model()
    return render_template('fraud_detection.html', metrics=metrics, info=info, name=session['name'])

@app.route('/analytics')
def analytics():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('analytics.html', name=session['name'])

@app.route('/daily_spending')
def daily_spending():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('daily_spending.html', name=session['name'])

@app.route('/presentation')
def presentation():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('presentation.html', name=session['name'])

# --- API ENDPOINTS ---
@app.route('/api/card/freeze', methods=['POST'])
def freeze_card():
    card = Card.query.filter_by(user_id=session.get('user_id')).first()
    if card:
        card.status = 'CARD FROZEN'
        db.session.commit()
        return jsonify({"status": "success", "new_status": card.status})
    return jsonify({"status": "error"}), 400

@app.route('/api/card/unfreeze', methods=['POST'])
def unfreeze_card():
    card = Card.query.filter_by(user_id=session.get('user_id')).first()
    if card:
        card.status = 'PROTECTED'
        db.session.commit()
        return jsonify({"status": "success", "new_status": card.status})
    return jsonify({"status": "error"}), 400

@app.route('/api/transaction/<int:id>')
def get_transaction(id):
    t = Transaction.query.get(id)
    if t:
        return jsonify({
            'txn_id': t.txn_id, 'amount': t.amount, 'merchant': t.merchant,
            'date': t.date, 'time': t.time, 'location': t.location,
            'category': t.category, 'risk_score': t.risk_score,
            'prediction': 'FRAUD' if t.prediction == 1 else 'GENUINE',
            'reason': t.reason
        })
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
