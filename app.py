from flask_sqlalchemy import SQLAlchemy  # new
from flask import Flask,request
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow  # new
import datetime
from iteration_utilities import deepflatten



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)  # new
api = Api(app)

#def datetime_sqlalchemy(value):
#    return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')

#datetime_created=datetime_sqlalchemy(str(datetime.datetime.now()))

class Ticket(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    seatNumber = db.Column(db.String(100), nullable=False)
    cost=db.Column(db.Integer)

class TicketSchema(ma.Schema):
    class Meta:
        fields = ("id", "seatNumber", "cost")
        model = Ticket
ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)


class TicketListResource(Resource):
    def get(self):
        posts = Ticket.query.all()
        return (tickets_schema.dump(posts))

    def post(self):
        new_post = Ticket(
            seatNumber=request.json['seatNumber'],
            cost=request.json['cost']
        )
        if Ticket.query.filter_by(seatNumber=request.json['seatNumber'],cost=request.json['cost']).count() == 1:
            return "Ticket Entry already exists!"

        db.session.add(new_post)
        db.session.commit()
        return 'ticket updated!'

class TicketResource(Resource):
    def get(self,id):
        post = Ticket.query.filter_by(id=id)
        res = []
        for x in post:
            res.append(x.seatNumber)
            res.append(x.cost)
        name = ['seatNumber','cost']
        return dict(zip(name,res))

    def put(self, id):
        post = Ticket.query.filter_by(id=id)
        for i in post:
            i.seatNumber = request.json['seatNumber']
            i.cost = request.json['cost']
        db.session.commit()
        return 'ticket updated!'

    def delete(self, id):
        post = Ticket.query.filter_by(id=id)
        for i in post:
            db.session.delete(i)
        db.session.commit()
        return 'Deleted!!'

api.add_resource(TicketResource, '/tickets/<int:id>',endpoint='ticket')
api.add_resource(TicketListResource, '/tickets')

class Flights(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    flightNumber=db.Column(db.String(100),nullable=False)
    date=db.Column(db.DateTime,nullable=False)

class FlightSchema(ma.Schema):
    class Meta:
        fields = ("id", "flightNumber", "date")
        model = Flights

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)

class FlightListResource(Resource):
    def get(self):
        posts = Flights.query.all()
        return (flights_schema.dump(posts))






        '''flightNumber = dict(zip("flightNumber",[z.flight.flightNumber for z in z]))
        occupiedSeats = [z.ticket.seatNumber for z in z]
        res_ls = [flightNumber,occupiedSeats]
        print(res_ls)
        return flightNumber'''



        '''posts = Flights.query.all()
        return flights_schema.dump(posts)'''

    def post(self):
        #current_date_today = date.today()
        #print("curr", current_date_today, type(current_date_today))
        date_str = request.json['date'].split("-")
        print(date_str)
        y = int(date_str[0])
        m = int(date_str[1])
        day = int(date_str[2])
        new_post = Flights(
            flightNumber=request.json['flightNumber'],
            date=datetime.date(y,m,day)
        )
        if Flights.query.filter_by(flightNumber=request.json['flightNumber']).count() == 1:
            return "Flight Entry already exists!"
        db.session.add(new_post)
        db.session.commit()
        return 'Added to flight table!'

class FlightResource(Resource):
    def get(self,id):
        post = Flights.query.filter_by(id=id)
        res = []
        for x in post:
            res.append(x.flightNumber)
            res.append(x.date)
        name = ['flightNumber','date']
        return dict(zip(name,res))

    def put(self, id):
        post = Flights.query.filter_by(id=id)
        for i in post:
            print("flight number: ",i.flightNumber)
            i.date = request.json['date']
            #i.flightNumber = request.json['flightNumber']
        db.session.commit()
        return 'post updated!'

    def delete(self, id):
        post = Flights.query.filter_by(id=id)
        for i in post:
            db.session.delete(i)
        db.session.commit()
        return 'Deleted!'

#api.add_resource(FlightListResource, '/flights',endpoint='flights')
api.add_resource(FlightListResource, '/flights',endpoint='flights')
api.add_resource(FlightResource, '/flights/<int:id>',endpoint='flight')


class FlightsTickets(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    ticket_id=db.Column(db.Integer,db.ForeignKey('ticket.id'))
    ticket=db.relationship('Ticket',backref=db.backref('FlightsTickets'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    flight = db.relationship('Flights', backref=db.backref('FlightsTickets'))

class FlightsTicketsSchema(ma.Schema):
    class Meta:
        model = FlightsTickets
flightticket_schema = FlightsTicketsSchema()
flightstickets_schema = FlightsTicketsSchema(many=True)

class FlightsTicketsListResource(Resource):
    def get(self):
        posts = FlightsTickets.query.all()
        id = []
        for x in posts:
            id.append(x.ticket.id)
        print("id: ",id)

        flight_id = []
        for x in posts:
            flight_id.append(x.flight_id)
        # print(seatnumber)

        seatnumber = []
        for x in posts:
            seatnumber.append(x.ticket.seatNumber)
        #print(seatnumber)

        cost = []
        for x in posts:
            cost.append(x.ticket.cost)
        #print(cost)

        date = []
        for x in posts:
            date.append(str(x.flight.date))
        #print(date)

        flightnumber = []
        for x in posts:
            flightnumber.append(x.flight.flightNumber)
        #print(flightnumber)

        final_ls = list(zip(id,seatnumber,cost,date,flightnumber,flight_id))
        name = ['ticketId','seatNumber', 'cost', 'date', 'flightnumber','flight_id']
        x = []
        for i in final_ls:
            x.append(list(zip(name, i)))
        z = []
        for i in x:
            y = dict(i)
            z.append(y)
        return z



    def post(self):
        new_post = FlightsTickets(
            ticket_id=request.json['ticket_id'],
            flight_id=request.json['flight_id']
        )
        if FlightsTickets.query.filter_by(ticket_id=request.json['ticket_id'],flight_id=request.json['flight_id']).count() >= 1:
            x = FlightsTickets.query.filter_by(flight_id=request.json['flight_id']).first().flight.flightNumber
            return "seat number already taken for flight number " + str(x)
        db.session.add(new_post)
        db.session.commit()
        return 'Flight Ticket Booked!'

class FlightsTicketsResource(Resource):
    def get(self,id):
        post = FlightsTickets.query.filter_by(id=id)
        id = []
        for x in post:
            id.append(x.ticket.id)
        print("id: ", id)

        seatnumber = []
        for x in post:
            seatnumber.append(x.ticket.seatNumber)
        # print(seatnumber)

        cost = []
        for x in post:
            cost.append(x.ticket.cost)
        # print(cost)

        date = []
        for x in post:
            date.append(x.flight.date)
        # print(date)

        flightnumber = []
        for x in post:
            flightnumber.append(x.flight.flightNumber)
        # print(flightnumber)

        final_ls = list(zip(id, seatnumber, cost, date, flightnumber))
        name = ['ticketId', 'seatNumber', 'cost', 'date', 'flightnumber']
        x = []
        for i in final_ls:
            x.append(list(zip(name, i)))
        z = []
        for i in x:
            y = dict(i)
            z.append(y)
        return z

    def delete(self, id):
        post = FlightsTickets.query.filter_by(id=id)
        for i in post:
            db.session.delete(i)
        db.session.commit()
        return 'Deleted!!'

api.add_resource(FlightsTicketsResource, '/api/tickets/<int:id>',endpoint='api/ticket')
api.add_resource(FlightsTicketsListResource, '/api/tickets')


class FlightsQuery(Resource):
    def get(self):
        startDate = request.args.get('startDate')
        enddate = request.args.get('endDate')
        flights_bw_date = Flights.query.filter(Flights.date.between(startDate, enddate)).all()
        flights_multiple_ids = [x.id for x in flights_bw_date]
        FlightsTickets_data = FlightsTickets.query.filter(FlightsTickets.flight_id.in_(flights_multiple_ids)).all()
        #flight_number = [FlightsTickets_data.flight.flightNumber for FlightsTickets_data in FlightsTickets_data]
        #print(flight_number)
        #seat_number = [FlightsTickets_data.flight.flightNumber for FlightsTickets_data in FlightsTickets_data]
        dic = {}
        flight_ticket_dic = {}
        flight = []
        seat = []
        for x in FlightsTickets_data:
            #flight.append(x.flight.flightNumber)
            #flight.append(x.ticket.seatNumber)
            #print(flight)
            #print(seat)
            if x.flight.flightNumber in flight_ticket_dic:
                flight_ticket_dic[x.flight.flightNumber] = x.ticket.seatNumber + flight_ticket_dic[x.flight.flightNumber]
                #seat.append(flight_ticket_dic[x.flight.flightNumber])
                #seat.append(x.ticket.seatNumber)
            else:
                flight_ticket_dic[x.flight.flightNumber] = x.ticket.seatNumber
            print("flight_ticket_dic: ",flight_ticket_dic)
            n = 3
            for i, j in flight_ticket_dic.items():
                print([j[i:i + n] for i in range(0, len(j), n)])
            #flight_ticket_dic[x.flight.flightNumber] =
            #flight_ticket_ls.append(x.flight.flightNumber)
            #flight_ticket_ls.append(x.ticket.seatNumber)
            #print(flight_ticket_ls)
            if x.flight.flightNumber in dic:
                dic[x.flight.flightNumber] = x.ticket.cost + dic[x.flight.flightNumber]
                #dic[x.flight.flightNumber] = x.ticket.seatNumber
            else:
                dic[x.flight.flightNumber] = x.ticket.cost
                #dic[x.flight.flightNumber] = x.ticket.seatNumber
        '''for i in dic:
            values = (dic[i])
            flatten_list = list(deepflatten(values))
            dic[i] = sum(flatten_list)
        print(dic)'''
        return dic

    #{'F01'}


    '''def get(self):
        startDate = request.args.get('startDate')
        enddate = request.args.get('endDate')
        if startDate == "" or enddate == "":
            posts = Flights.query.all()
            return (flights_schema.dump(posts))
        x = Flights.query.filter(Flights.date.between(startDate, enddate)).all()
        y = [x.id for x in x]
        name_ls = ['flightNumber', 'occupiedSeats']
        flightNumber = []
        z = FlightsTickets.query.filter(FlightsTickets.id.in_(y)).all()
        for i in z:
            flightNumber.append(i.flight.flightNumber)
        print(flightNumber)
        # zz=(dict(zip(name_ls,res_ls)))
        # print(zz)
        ticketNumber = []
        for i in z:
            ticketNumber.append(i.ticket.seatNumber)
        print(ticketNumber)

        final_ls = list(zip(flightNumber, ticketNumber))
        x = []
        for i in final_ls:
            x.append(list(zip(name_ls, i)))
        z = []
        for i in x:
            y = (dict(i))
            z.append(y)
        return z'''

api.add_resource(FlightsQuery, '/api/flights')


if __name__ == '__main__':
    app.run(debug=True)







