from flask import Flask, render_template,request,redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
app = Flask(__name__)
app.secret_key="Çok gizli key "

#veritabanı bağlantısı


client=MongoClient("mongodb+srv://egitim:egitim48@cluster0-a4rqa.mongodb.net/test?retryWrites=true&w=majority")
#tododb veritabanı adı todos:collections...
db = client.tododb.todos
#artık db ile veri tabanında herşeyi yapabilirimi.


@app.route('/')
def index():
    #veritabanından kayıtları çek bir listeye al.
    yapilacaklar=[]
    for yap in db.find():
        yapilacaklar.append({
            "_id":str(yap.get("_id")),
            "isim":yap.get("isim"),
            "durum":yap.get("durum")
        })
    #index.html e bu listeyi gönder.
    return render_template('index.html',yapilacaklar=yapilacaklar)
@app.route('/guncelle/<id>')
def guncelle(id):
    #gelen id değeri ile kaydı bulalım.
    yap=db.find({'_id':ObjectId(id)})
    #durum değeri true ise false false ise true yapalım.
    durum=not yap.get('durum')
    #kaydı güncelle
    db.find_one_and_update({'_id':ObjectId(id)},{'$set':{'durum':durum}})
    #anasayfaya yönlendir.
    return redirect('/')
@app.route('/sil<id>')
def sil(id):
   #gelen id değeri kaydı sil
   db.find_one_and_delete({'_id':ObjectId(id)})
   #anasayfaya gönder
    return redirect('/')
@app.route('/ekle',methods=['POST'])
def ekle():
    #kullanıcıdan sadece isim aldık durumu default olarak false kabul ediyoruz.
    isim=request.form.get('isim')
    db.insert_one({'isim':isim,'durum':'False'})
    #anasayfaya yönlendir.
    return redirect('/')
#hatalı ya da olmayan bir url isteği gelirse 
#hata vermesin anasayfaya yönlendirelim..
@app.errorhandler(404')
def hatali_url():
   return redirect('/')
    
   
@app.route('/kimiz')
def kimiz():
   return render_template('kimiz.html')
@app.route('/user/<isim>')
def user(isim):
    #ismi sayfaya gönder
    return render_template('user.html',isim=isim)
  

if __name__ == '__main__':
  app.run(debug=True)
 