from typing import Literal
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

import easydict
import uuid
import boto3
import os
from werkzeug.utils import secure_filename

from demo import demo
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME


app = Flask(__name__)
CORS(app)

app_route = Blueprint('ocr_route',__name__)


S3_LOCATION = f"http://{BUCKET_NAME}.s3.amazonaws.com/"



@app.route('/')
def home_page():
    return "ocr server"

@app.route('/api/ocr', methods=['POST'])
def ocr_from_image():

    image = request.files['image']
    user_id = request.form['id']

    # s3 업로드
    s3_url = upload_image(image, user_id)

    # 이미지 폴더 저장
    path, ext = os.path.splitext(image.filename)
    image.save('./uploads/ocr' + ext) # 파일명을 보호하기위한 함수, 지정된 경로에 파일 저장

    args = easydict.EasyDict({
        "Transformation" : "TPS",
        "FeatureExtraction" : "ResNet",
        "SequenceModeling" : "BiLSTM",
        "Prediction" : "CTC",
        "image_folder" : "./uploads/",
        "saved_model" : "./best_accuracy.pth",
        "workers" : 0,
        "batch_size" : 192,
        "batch_max_length" : 25,
        "imgH" : 32,
        "imgW" : 100,
        "rgb" : False,
        "character" : '0123456789abcdefghijklmnopqrstuvwxyz가각간갇갈감갑값갓강갖같갚갛개객걀걔거걱건걷걸검겁것겉게겨격겪견결겹경곁계고곡곤곧골곰곱곳공과관광괜괴굉교구국군굳굴굵굶굽궁권귀귓규균귤그극근글긁금급긋긍기긴길김깅깊까깍깎깐깔깜깝깡깥깨꺼꺾껌껍껏껑께껴꼬꼭꼴꼼꼽꽂꽃꽉꽤꾸꾼꿀꿈뀌끄끈끊끌끓끔끗끝끼낌나낙낚난날낡남납낫낭낮낯낱낳내냄냇냉냐냥너넉넌널넓넘넣네넥넷녀녁년념녕노녹논놀놈농높놓놔뇌뇨누눈눕뉘뉴늄느늑는늘늙능늦늬니닐님다닥닦단닫달닭닮담답닷당닿대댁댐댓더덕던덜덟덤덥덧덩덮데델도독돈돌돕돗동돼되된두둑둘둠둡둥뒤뒷드득든듣들듬듭듯등디딩딪따딱딴딸땀땅때땜떠떡떤떨떻떼또똑뚜뚫뚱뛰뜨뜩뜯뜰뜻띄라락란람랍랑랗래랜램랫략량러럭런럴럼럽럿렁렇레렉렌려력련렬렵령례로록론롬롭롯료루룩룹룻뤄류륙률륭르른름릇릎리릭린림립릿링마막만많말맑맘맙맛망맞맡맣매맥맨맵맺머먹먼멀멈멋멍멎메멘멩며면멸명몇모목몬몰몸몹못몽묘무묵묶문묻물뭄뭇뭐뭘뭣므미민믿밀밉밌및밑바박밖반받발밝밟밤밥방밭배백뱀뱃뱉버번벌범법벗베벤벨벼벽변별볍병볕보복볶본볼봄봇봉뵈뵙부북분불붉붐붓붕붙뷰브븐블비빌빔빗빚빛빠빡빨빵빼뺏뺨뻐뻔뻗뼈뼉뽑뿌뿐쁘쁨사삭산살삶삼삿상새색샌생샤서석섞선설섬섭섯성세섹센셈셋셔션소속손솔솜솟송솥쇄쇠쇼수숙순숟술숨숫숭숲쉬쉰쉽슈스슨슬슴습슷승시식신싣실싫심십싯싱싶싸싹싼쌀쌍쌓써썩썰썹쎄쏘쏟쑤쓰쓴쓸씀씌씨씩씬씹씻아악안앉않알앓암압앗앙앞애액앨야약얀얄얇양얕얗얘어억언얹얻얼엄업없엇엉엊엌엎에엔엘여역연열엷염엽엿영옆예옛오옥온올옮옳옷옹와완왕왜왠외왼요욕용우욱운울움웃웅워원월웨웬위윗유육율으윽은을음응의이익인일읽잃임입잇있잊잎자작잔잖잘잠잡잣장잦재쟁쟤저적전절젊점접젓정젖제젠젯져조족존졸좀좁종좋좌죄주죽준줄줌줍중쥐즈즉즌즐즘증지직진질짐집짓징짙짚짜짝짧째쨌쩌쩍쩐쩔쩜쪽쫓쭈쭉찌찍찢차착찬찮찰참찻창찾채책챔챙처척천철첩첫청체쳐초촉촌촛총촬최추축춘출춤춥춧충취츠측츰층치칙친칠침칫칭카칸칼캄캐캠커컨컬컴컵컷케켓켜코콘콜콤콩쾌쿄쿠퀴크큰클큼키킬타탁탄탈탑탓탕태택터턱턴털텅테텍텔템토톤톨톱통퇴투툴툼퉁튀튜트특튼튿틀틈티틱팀팅파팎판팔팝패팩팬퍼퍽페펜펴편펼평폐포폭폰표푸푹풀품풍퓨프플픔피픽필핏핑하학한할함합항해핵핸햄햇행향허헌험헤헬혀현혈협형혜호혹혼홀홈홉홍화확환활황회획횟횡효후훈훌훨휘휴흉흐흑흔흘흙흡흥흩희흰히힘?!.,()\'":;',
        "sensitive" : False,
        "PAD" : False,
        "num_fiducial" : 20,
        "input_channel" : 1,
        "output_channel" : 512,
        "hidden_size" : 256
    })

    result = demo(args)

    # 폴더에서 파일 삭제
    os.remove('./uploads/ocr' + ext)
    
    data = {
        "user_id" : user_id,
        "s3_url" : s3_url,
        "result" : result
    }

    return jsonify(data)


def upload_image(image, user_id):
    try:
        
        # filename = secure_filename(image.filename)
        image.filename = get_unique_imgname(image.filename, user_id)
    
        s3 = s3_connection()
        s3.put_object(Bucket=BUCKET_NAME, Body=image, Key=image.filename)
    except Exception as e:
        return jsonify({'errors' : str(e)})
    
    url = f"{S3_LOCATION}{image.filename}"
    
    # return jsonify({'url': url})
    return url
    

def get_unique_imgname(filename, user_id):
    ext = filename.rsplit(".",1)[1].lower()
    # 이미지 파일명 구조 : {userid}/{uuid}.{확장자} 
    # 이미지의 원래 이름에 s3 파일이름에 들어갈 수 없는 문자가 있을 경우를 고려하여 일단 uuid만 넣었음
    return f"{user_id}/{uuid.uuid4().hex}.{ext}"  


def s3_connection():
    s3 = boto3.client('s3',aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
    return s3



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)