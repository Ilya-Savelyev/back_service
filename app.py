from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql://admin:password@localhost:5432/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Postcard(db.Model):
    __tablename__='postcards'
    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String(100), nullable=False)
    recipient_name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'sender_name': self.sender_name,
            'recipient_name': self.recipient_name,
            'message': self.message,
            'image_url': self.image_url,
            'sent_at': self.sent_at.isoformat()
        }

#Создание\отправка открытки
@app.route('/postcards', method=['POST'])
def create_postcard():
    data = request.json
    try:
        new_postcard = Postcard(
            sender_name = data['sender_name'],
            recipient_name = data['recipient_name'],
            message = data['message'],
            image_url = data.get('image_url')
        )
        db.session.add(new_postcard)
        db.session.commit()
        return jsonify({'status': 'success', 'postcard': new_postcard.to_dict()}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

#Получение всех открыток
@app.route('/postcards', method=['GET'])
def get_postcards():
    postcards = Postcard.query.all()
    return jsonify([p.to_dict() for p in postcards])

#Получение открыток по ID
@app.route('/postcards/<int:postcard_id>', method=['GET'])
def get_postcards(postcard_id):
    postcards = Postcard.query.get_or_404(postcard_id)
    return jsonify(postcard_id.to_dict())

if __name__ == '__main__':
    app.run(debug=True)