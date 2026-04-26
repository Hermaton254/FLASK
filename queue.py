from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///queue.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------
# Database Model
# -------------------
class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True)
    phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='waiting')  # waiting, served, skipped
    time_joined = db.Column(db.DateTime, default=datetime.utcnow)

# -------------------
# Create DB
# -------------------
with app.app_context():
    db.create_all()

# -------------------
# Generate Queue Number
# -------------------
def generate_number():
    last = Queue.query.order_by(Queue.id.desc()).first()
    if not last:
        return "A1"
    last_num = int(last.number[1:])
    return f"A{last_num + 1}"

# -------------------
# Join Queue
# -------------------
@app.route('/join', methods=['POST'])
def join_queue():
    data = request.get_json()
    phone = data.get("phone")

    # Prevent duplicate active entry
    existing = Queue.query.filter_by(phone=phone, status='waiting').first()
    if existing:
        return jsonify({"message": "Already in queue", "number": existing.number})

    number = generate_number()

    new_entry = Queue(number=number, phone=phone)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({
        "message": "Joined successfully",
        "number": number
    })

# -------------------
# Get Queue
# -------------------
@app.route('/queue', methods=['GET'])
def get_queue():
    queue = Queue.query.filter_by(status='waiting').order_by(Queue.id).all()

    result = []
    for person in queue:
        result.append({
            "number": person.number,
            "time_joined": person.time_joined
        })

    return jsonify(result)

# -------------------
# Call Next
# -------------------
@app.route('/next', methods=['POST'])
def call_next():
    next_person = Queue.query.filter_by(status='waiting').order_by(Queue.id).first()

    if not next_person:
        return jsonify({"message": "No one in queue"})

    next_person.status = 'served'
    db.session.commit()

    return jsonify({
        "message": "Next person",
        "number": next_person.number
    })

# -------------------
# Get Position
# -------------------
@app.route('/position/<phone>', methods=['GET'])
def get_position(phone):
    queue = Queue.query.filter_by(status='waiting').order_by(Queue.id).all()

    for index, person in enumerate(queue):
        if person.phone == phone:
            return jsonify({
                "number": person.number,
                "position": index + 1
            })

    return jsonify({"message": "Not in queue"})

# -------------------
# Run Server
# -------------------
if __name__ == '__main__':
    app.run(debug=True)