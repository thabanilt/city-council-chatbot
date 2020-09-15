
import os
import secrets
import datetime
from PIL import Image
from flask import Flask, render_template,request,session,logging,url_for,redirect,flash

from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash,check_password_hash
from forms import RegistrationForm, LoginForm,Schedule
from flask_mongoengine import MongoEngine, Document
from flask_login import login_user, current_user, logout_user, login_required,LoginManager,UserMixin

 
import csv
from pymongo import MongoClient
from bson.objectid import ObjectId  
from flask import Flask ,request,app
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import urllib
import requests
import json
import os




client=MongoClient("mongodb://lex:warumwa@cluster0-shard-00-00-lct7x.mongodb.net:27017,cluster0-shard-00-01-lct7x.mongodb.net:27017,cluster0-shard-00-02-lct7x.mongodb.net:27017/report?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db=client["report"]
collection=db["track"]
collections=db["report"]
collect=db["schedule"]


apbot=Flask(__name__)

apbot.config['MONGODB_SETTINGS'] = {
    'db': 'report',
    'host': 'mongodb://lex:warumwa@cluster0-shard-00-00-lct7x.mongodb.net:27017,cluster0-shard-00-01-lct7x.mongodb.net:27017,cluster0-shard-00-02-lct7x.mongodb.net:27017/report?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority'
}
apbot.config['SECRET_KEY'] = 'warumwa'

db = MongoEngine(apbot)
login_manager = LoginManager()
login_manager.init_app(apbot)
login_manager.login_view = 'login'


class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    email = db.StringField(max_length=30)
    password = db.StringField()
    name= db.StringField()
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


@apbot.route("/")
@login_required
def home():
    return render_template('maps.html',user=current_user)

@apbot.route("/complaints")
@login_required
def complaint():
    comp=collections.find({"status":"pending"})
    return render_template('tables.html',user=current_user,comp=comp)

@apbot.route("/donecomplaints")
@login_required
def rescomplaint():
    comp=collections.find({"status":"responded"})
    return render_template('done.html',user=current_user,comp=comp)

@apbot.route("/allcomplaints")
@login_required
def allcomplaint():
    comp=collections.find()
    return render_template('all.html',user=current_user,comp=comp)

@apbot.route("/allschedules")
@login_required
def allschedules():
    # comp=collections.find()
    return render_template('schedule.html',user=current_user)

@apbot.route("/addschedule",methods=["GET","POST"])
@login_required
def addschedule():
    form = Schedule()
    # comp=collections.find()
    return render_template('addschedule.html',user=current_user)



@apbot.route("/add")
@login_required
def add():
    
    return render_template('addschedule.html',user=current_user)


@apbot.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated == True:
       return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
             
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'],form.password.data):
                       
                    login_user(check_user)
                    return redirect(url_for('home'))
                        
  
                else:  flash('Login Unsuccessful. Please check password', 'danger')
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)
    
   
@apbot.route("/register" , methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
                   
           
        existing_user = User.objects(email=form.email.data).first()

        if existing_user is None:
            hashpass = generate_password_hash(form.password.data, method='sha256')
            al=User(email=form.email.data,password=hashpass,name=form.name.data).save()
            login_user(al)
            return redirect(url_for('home'))
                

        else:
            flash('Register Unsuccessful.Email Already exists', 'danger')
    return render_template('register.html',form=form)


@apbot.route("/api", methods=['POST'])
def api():
    db_data = list(collections.find({"status":"pending"}))
    infornation_dic = {}
    infornation_list = []

    for data in db_data:
        
        infornation_dic['data'] = []
        infornation_dic['Name'] = data["fullname"]
        infornation_dic['Picture'] = "https://www.thepatriot.co.zw/wp-content/uploads/2018/09/11-1.jpg"
        infornation_dic['Color'] = "green"
        infornation_dic['Longitude'] = data["longitude"]
        infornation_dic['Latitude'] = data["latitude"]
        infornation_list.append(infornation_dic)
        infornation_dic = {}
        

    return json.dumps(infornation_list) 

@apbot.route("/complaint/<post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    collections.find_one_and_update({"_id":ObjectId(post_id)},{"$set":{"status":"responded"}})
    flash('Register Unsuccessful.Email Already exists', 'success')
    return redirect(url_for('complaint'))


@apbot.route("/sms",methods=["get","post"])
def reply():
    num_media = int(request.values['NumMedia'])
    num=request.form.get("From")
    num=num.replace("whatsapp:","") 
    msg_text=request.form.get("Body")
    lat=request.form.get("Latitude")
    lng=request.form.get("Longitude")
    dat = datetime.datetime.now()
    med= request.values.get('MediaContentType0', '')
    x=collection.find_one({"NUMBER":num})
    try:
        status=x["status"]
    except:
        pass
        
    if(bool(x)==False):   
     collection.insert_one({"NUMBER":num,"status":"first"})
     msg=MessagingResponse()
     resp=msg.message("Hello 🙋🏽‍♂, \nIm Jane a City Council chatbot,\n For any emergency 👇 \n 📞 Toll-Free Number: 8111 \n\n Please enter one of the following option 👇 \n *A*. Report an *Issue*📝. \n *B*.Report by sending us an *image*📷. \n *C*. Report an issue with an *image*📝📷. \n *D*.View City Council Schedule 🚛? \n *")
     return(str(msg))



     
    elif (status=="first") :
            msg=MessagingResponse()
            if(msg_text.lower()=="b"):
                collection.update_one({"NUMBER":num},{"$set":{"status":"optionB"}})
                resp=msg.message("Enter your full name\n\n")

                return(str(msg))

        
            elif(msg_text.lower()=="c"):
                  
                collection.update_one({"NUMBER":num},{"$set":{"status":"optionC"}})
                resp=msg.message("Enter your full name\n\n")
                return(str(msg))

            elif(msg_text.lower()=="d"):
                  r = requests.get('http://newsapi.org/v2/everything?q=covid19&from=2020-04-09&sortBy=popularity&apiKey=426e591a64e44124bb388e53ef227ff1')
                  if r.status_code == 200:
                    data = r.json()
                    lut=[]
                    text = f'_Covid-19 News Worldwide_\n\n'
                    resp1=msg.message(text)
                    for val in data["articles"]:
                         answ = f'*{val["title"]}* \n\n*{val["description"]}* \n\n*{val["content"]}*\n\n *{val["url"]}*\n\n 👉 Type *A,B, D, E,F* to see other options \n 👉 Type *Menu* to view the Main Menu\n\n'
                         lut=answ
                         resp=msg.message(answ)
                    return(str(msg)) 
                
                  return(str(msg))
            elif(msg_text.lower()=="d"):
                   resp1=msg.message("") 
                   text = f'_Coronavirus spreads from an infected person through_ 👇 \n\n ♦ Small droplets from the nose or mouth which are spread when a person coughs or sneezes \n\n ♦ Touching an object or surface with these droplets on it and then touching your mouth, nose, or eyes before washing your hands \n \n ♦ Close personal contact, such as touching or shaking hands \n Please watch the video for more information 👇 https://youtu.be/TjcoN9Aek24 \n\n👉 Type *A,B, C,E,* to see other options \n  👉 Type *Menu* to view the Main Menu\n\n'
                   resp1.media('https://user-images.githubusercontent.com/34777376/77290801-f2421280-6d02-11ea-8b08-fdb516af3d5a.jpeg')
                   resp=msg.message(text)

                   return(str(msg))
            elif(msg_text.lower()=="e"):
                   resp1=msg.message("") 
                   text = f'_Coronavirus infection can be prevented through the following means_ 👇  \n ✔️ Clean hand with soap and water or alcohol-based hand rub \n https://youtu.be/EJbjyo2xa2o \n\n ✔️ Cover nose and mouth when coughing & sneezing with a tissue or flexed elbow \n https://youtu.be/f2b_hgncFi4 \n\n ✔️ Avoid close contact & maintain 1-meter distance with anyone who is coughing or sneezin \n https://youtu.be/mYyNQZ6IdRk \n\n ✔️ Isolation of persons traveling from affected countries or places for at least 14 day \n https://www.mohfw.gov.in/AdditionalTravelAdvisory1homeisolation.pdf \n\n ✔️ Quarantine if advise \n https://www.mohfw.gov.in/Guidelinesforhomequarantine.pdf \n\n 👉 Type *A,B, C, D, * to see other options \n  👉 Type *Menu* to view the Main Menu\n\n'
                   resp1.media('https://user-images.githubusercontent.com/34777376/77290864-1c93d000-6d03-11ea-96fe-18298535d125.jpeg')
                   resp=msg.message(text)
                   return(str(msg))
            elif(msg_text.lower()=="a"):
                collection.update_one({"NUMBER":num},{"$set":{"status":"optionA"}})
                resp=msg.message("Enter your name and surname\n\n")
                return(str(msg))
            elif(msg_text.lower()=="menu"):
                collection.update_one({"NUMBER":num},{"$set":{"status":"first"}})
                msg=MessagingResponse()
                resp=msg.message("Hello 🙋🏽‍♂, \nIm Lento, Im to provide latest information updates i.e cases in different countries and create awareness to help you and your family stay safe.\n For any emergency 👇 \n 📞 Toll-Free Number: 2 0 1 9 \n\n Please enter one of the following option 👇 \n *A*. Covid-19 statistics *Worldwide*. \n *B*. Covid-19 Statistics in *countries*. \n *C*. Covid-19 News *Worldwide_*. \n *D*. How does it *Spread*? \n *E*. *Preventive measures* to be taken.\n\n*F*. *Report if you Suspect you have covid-19 virus🚑*\n\n*Please be adviced this is a test run.*")
                return(str(msg))
            else: 
               resp=msg.message("Invalid input please try again\n\n")
                
               return(str(msg))
    else :
        
        if (status=="second"):
            if (msg_text.lower()=="menu"):
                collection.update_one({"NUMBER":num},{"$set":{"status":"first"}})
                msg=MessagingResponse()
                resp=msg.message("Hello 🙋🏽‍♂, \nIm Lento, Im to provide latest information updates i.e cases in different countries and create awareness to help you and your family stay safe.\n For any emergency 👇 \n 📞 Toll-Free Number: 2 0 1 9 \n\n Please enter one of the following option 👇 \n *A*. Covid-19 statistics *Worldwide*. \n *B*. Covid-19 Statistics in *countries*. \n *C*. Covid-19 News *Worldwide_*. \n *D*. How does it *Spread*? \n *E*. *Preventive measures* to be taken.\n\n*F*. *Report if you Suspect you have covid-19 virus🚑*\n\n*Please be adviced this is a test run.*")
                return(str(msg))



        elif(status=="optionB"):
            collection.update_one({"NUMBER":num},{"$set":{"status":"image"}})
            msg=MessagingResponse()
            global full
            full=str(msg_text)
            resp=msg.message("*Please share your image*\n\n")
            return(str(msg))
        elif(status=="image"):
            
            msg=MessagingResponse()
            # global imag
            # print(med)
            # imag=save_picture(med)
            if num_media > 0:
                global picture_fn
                filename = request.values.get('MessageSid')+ '.png'
                random_hex = secrets.token_hex(8)
                _, f_ext = os.path.splitext(filename)
                picture_fn = random_hex + f_ext
                picture_path = os.path.join(apbot.root_path, 'pictures' )
                with open('{}/{}'.format(picture_path,picture_fn), 'wb') as f:
                    image_url = request.values['MediaUrl0']
                    f.write(requests.get(image_url).content)
            else:
                resp=msg.message("Try sending a picture message.")
                return(str(msg))

            collection.update_one({"NUMBER":num},{"$set":{"status":"location2"}})
            resp=msg.message("*Please share your location*\n\nTo share your location click on 📎 then select location")
            return(str(msg))
        elif(status=="location2"):
            msg=MessagingResponse()
            collections.insert_one({"NUMBER":num,"fullname":full,"image":picture_fn,"latitude":lat,"longitude":lng,"status":"pending","date":dat})
            collection.update_one({"NUMBER":num},{"$set":{"status":"first"}})
            resp=msg.message("Your report has been received thank you.\n\n")
            return (str(msg))

         



        
        elif(status=="optionA"):
            collection.update_one({"NUMBER":num},{"$set":{"status":"report"}})
            msg=MessagingResponse()
            global fullname
            fullname=str(msg_text)
            resp=msg.message("Please enter your complaint")
            return(str(msg))
        elif(status=="report"):
            collection.update_one({"NUMBER":num},{"$set":{"status":"location"}})
            msg=MessagingResponse()
            global report
            report=str(msg_text)
            resp=msg.message("*Please share your location*\n\nTo share your location click on 📎 then select location")
            return(str(msg))
           
        elif(status=="location"):
            msg=MessagingResponse()
            collections.insert_one({"NUMBER":num,"fullname":fullname,"report":report,"latitude":lat,"longitude":lng,"status":"pending","date":dat})
            collection.update_one({"NUMBER":num},{"$set":{"status":"first"}})
            resp=msg.message("Your report has been received thank you.\n\n")
            return (str(msg))

        

        elif(status=="optionC"):
            collection.update_one({"NUMBER":num},{"$set":{"status":"reportC"}})
            msg=MessagingResponse()
            global nam
            nam=str(msg_text)
            resp=msg.message("*Please Enter your report")
            return(str(msg))
        elif(status=="reportC"):
            collection.update_one({"NUMBER":num},{"$set":{"status":"image2"}})
            msg=MessagingResponse()
            global repo
            repo=str(msg_text)
            resp=msg.message("Please share your image")
            return(str(msg))

        elif(status=="image2"):
           
            msg=MessagingResponse()
            # global imag
            # print(med)
            # imag=save_picture(med)
            if num_media > 0:
                global img
                fname = request.values.get('MessageSid')+ '.png'
                random_hex = secrets.token_hex(8)
                _, f_ext = os.path.splitext(fname)
                img = random_hex + f_ext
                picture_path = os.path.join(apbot.root_path, 'static/img' )
                with open('{}/{}'.format(picture_path,img), 'wb') as f:
                    image_url = request.values['MediaUrl0']
                    f.write(requests.get(image_url).content)
            else:
                resp=msg.message("Try sending a picture message.")
                return(str(msg))
            collection.update_one({"NUMBER":num},{"$set":{"status":"locationC"}})
            resp=msg.message("*Please share your location*\n\nTo share your location click on 📎 then select location")
            return(str(msg))
        elif(status=="locationC"):
            msg=MessagingResponse()
            collections.insert_one({"NUMBER":num,"fullname":nam,"report":repo,"image":img,"latitude":lat,"longitude":lng,"status":"pending","date":dat})
            collection.update_one({"NUMBER":num},{"$set":{"status":"first"}})
            resp=msg.message("Your report has been received thank you.\n\n")
            return (str(msg))

@apbot.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
#endregion

 
if __name__ == '__main__':
  apbot.run(debug=True)