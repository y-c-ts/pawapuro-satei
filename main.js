var avility_list = ['チャンス','対左投手','盗塁','走塁','送球','ケガしにくさ','キャッチャー','アベレージヒッター','パワーヒッター','プルヒッター',
        '広角打法','内野安打○', '流し打ち','固め打ち','粘り打ち','悪球打ち','意外性','バント','初球○','代打○',
        'チャンスメーカー','ヘッドスライディング','ホーム突入','満塁男','サヨナラ男','逆境○','ハイボールヒッター','ローボールヒッター','対エース○','ムード○',
        'レーザービーム','守備職人','高速チャージ','ホーム死守','プレッシャーラン','いぶし銀','ささやき戦術','追い打ち','帳尻合わせ','気分屋',
        'ラッキーボーイ','連打○','リベンジ','インコース○','アウトコース○','ささやき破り','本塁生還','ラッキーセブン','バズーカ','司令塔',
        '競争心','打球ノビ','盗塁アシスト','アイコンタクト','速攻○','上り調子', '窮地◯','読心術','情熱エール','打開', 
        '接戦○','祝福', '鼓舞','かく乱','挑発','一発逆転','一掃', '初撃', '冷静', 'サイン察知', 
        '四番〇', '孤高', '走塁ブースト', '守備移動', '痛打','ファースト○','セカンド○','サード○'];

var is_gold = [1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,0,0,1,0,1,1,
        1,0,1,1,1,1,1,1,1,1,
        1,1,0,1,0,0,1,1,0,0,
        1,1,1,1,1,0,1,0,1,1,
        1,1,0,1,0,1,1,1,1,1,
        0,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1];       
        
var avility_detail = {'チャンス':['チャンス○','チャンス◎','勝負師'], '対左投手':['対左投手○','対左投手◎','左キラー'],
'盗塁':['盗塁○','盗塁◎','電光石火'],'走塁':['走塁○','走塁◎','高速ベースラン'],'送球':['送球○','送球◎','ストライク送球'],
'ケガしにくさ':['ケガしにくさ○','ケガしにくさ◎','鉄人'],'キャッチャー':['キャッチャー○','キャッチャー◎','球界の頭脳'],
'アベレージヒッター':['アベレージヒッター','安打製造機'],'パワーヒッター':['パワーヒッター','アーチスト'],'プルヒッター':['プルヒッター','伝説の引っ張り屋'],
'広角打法':['広角打法','広角砲'],'内野安打○':['内野安打○','内野安打王'],'流し打ち':['流し打ち','芸術的流し打ち'],'固め打ち':['固め打ち','メッタ打ち'],'粘り打ち':['粘り打ち'],
'悪球打ち':['悪球打ち'],'意外性':['意外性','大番狂わせ'],'バント':['バント○','バント職人'],'初球○':['初球○','一球入魂'],'代打○':['代打○','代打の神様'],
'チャンスメーカー':['チャンスメーカー','切り込み隊長'],'ヘッドスライディング':['ヘッドスライディング','気迫ヘッド'],'ホーム突入':['ホーム突入','重戦車'],'満塁男':['満塁男','恐怖の満塁男'],
'サヨナラ男':['サヨナラ男','伝説のサヨナラ男'],'逆境○':['逆境○','火事場の馬鹿力'],'ハイボールヒッター':['ハイボールヒッター','高球必打'],'ローボールヒッター':['ローボールヒッター','低球必打'],
'対エース○':['対エース○','エースキラー'],'ムード○':['ムード○','精神的支柱'],'レーザービーム':['レーザービーム','高速レーザー'],'守備職人':['守備職人','魔術師'],
'高速チャージ':['高速チャージ'],'ホーム死守':['ホーム死守','鉄の壁'],'プレッシャーラン':['プレッシャーラン'],'いぶし銀':['いぶし銀'],'ささやき戦術':['ささやき戦術'],
'追い打ち':['追い打ち','ハゲタカ'],'帳尻合わせ':['帳尻合わせ'],'気分屋':['気分屋'],'ラッキーボーイ':['ラッキーボーイ','超ラッキーボーイ'],'連打○':['連打○','つるべ打ち'],
'リベンジ':['リベンジ','逆襲'],'インコース○':['インコース○','内角必打'],'アウトコース○':['アウトコース○','外角必打'],'ささやき破り':['ささやき破り'],'本塁生還':['本塁生還','帰巣本能'],
'ラッキーセブン':['ラッキーセブン'],'バズーカ':['バズーカ'],'司令塔':['司令塔'],'競争心':['競争心','切磋琢磨'],'打球ノビ':['打球ノビ○','打球ノビ◎','ローリング打法'],
'盗塁アシスト':['盗塁アシスト'],'アイコンタクト':['アイコンタクト'],'速攻○':['速攻○'],'上り調子':['上り調子','昇り龍'],'窮地◯':['窮地◯','ヒートアップ'],'読心術':['読心術'],
'情熱エール':['情熱エール'],'打開':['打開','一番槍'],'接戦○':['接戦○'],'祝福':['祝福'],'鼓舞':['鼓舞','ミラクルボイス'],'かく乱':['かく乱','トリックスター'],
'挑発':['挑発'],'一発逆転':['一発逆転','一発逆転王'],'一掃':['一掃','スイープ'],'初撃':['初撃','洗礼の一撃'],'冷静':['冷静','明鏡止水'],'サイン察知':['サイン察知','看破'],
'四番〇':['四番〇','不動の四番'],'孤高':['孤高','孤軍奮闘'],'走塁ブースト':['走塁ブースト','走塁バースト'],'守備移動':['守備移動','牛若丸'],'痛打':['痛打','大打撃'],
'ファースト○':['ファースト○','至高の一塁手'],'セカンド○':['セカンド○','至高の二塁手'],'サード○':['サード○','至高の三塁手']
}

window.onload = function(){
    var table = document.getElementById('blue-avility')
    for (i=0; i < avility_list.length; i++){
        var one_avility_tr = document.createElement('tr');
        one_avility_tr.className = 'avility';
        one_avility_tr.id = 'avility' + '_' + avility_list[i];
        var td_button = document.createElement('td');
        td_button.className = 'button_td';
        td_button.align = 'center';
        var button = document.createElement('input');
        button.value = avility_list[i];
        button.type = "button";
        button.id = i;
        button.name = 'button-button-button';
        button.onclick = changeColor;
        console.log(avility_detail[avility_list[i]].length);
        console.log(avility_detail[avility_list[i]]);
        if(is_gold[i]==1 && avility_detail[avility_list[i]].length == 1){
            button.className = 'btn btn-outline-warning get_avility';
            add_td = make5RadioBoxes(avility_list[i], 'First5Box', through_flag=true);
        }
        else{
            button.className = 'btn btn-outline-primary get_avility';
            add_td = make5RadioBoxes(avility_list[i], 'First5Box', through_flag=false);
        }
        td_button.appendChild(button);
        one_avility_tr.appendChild(td_button);
        one_avility_tr.appendChild(add_td);
        if(is_gold[i] == 1){
            add_gold_td = make5RadioBoxes('gold_' + avility_list[i], 'gold5Box', through_flag=false); 
            one_avility_tr.appendChild(add_gold_td);
        }
        table.appendChild(one_avility_tr);
    }
}

function get_buttons_content(){
    var avility_str = ''; 
    for(i=0; i < avility_list.length; i++){
        var button_elem = document.getElementById(i);
        if((button_elem.className == 'btn btn-primary get_avility')|| (button_elem.className == 'btn btn-warning get_avility')){
            avility_str += button_elem.value + '_'
        }
    }
    var submit_elm = document.getElementById('get_avility_str');
    submit_elm.value = avility_str;
}
        

function make5RadioBoxes(avilityName, className, through_flag){
    master_div = document.createElement('td');
    master_div.align = 'center';
    master_div.className = className;
    master_div.id = className + '_' + avilityName;
    if(through_flag){
        return master_div
    }
    else{
        var div = document.createElement('div');
        div.className = "form-check form-check-inline custom-radio";
        for(j=0; j<6; j++){
            var input = document.createElement('input');
            input.className = "form-check-input radio-input";
            input.type = "radio";
            input.name = "Radio" + '_' + avilityName;
            input.value = "option" + j;
            input.id = 'inlineRadio' + j + '_' + avilityName;
            var label = document.createElement('label');
            label.className = "form-check-label my-form-label"; 
            label.htmlFor = 'inlineRadio' + j + '_' + avilityName;
            label.innerHTML = j;
            if(j==0){
                input.checked = "checked";
            }
            div.appendChild(input);
            div.appendChild(label);
        master_div.appendChild(div)
        }
        return master_div
    }
}

function addGoldBoxes(avilityName){
    var added_elem = document.getElementById('avility_' + avilityName);
    add_elem = make5RadioBoxes('gold_' + avilityName, 'gold5Box') 
    added_elem.appendChild(add_elem)
}

function changeColor(e){
    var obj = e.srcElement;
    var id = obj.id;
    var name = avility_list[id];
    var gold = is_gold[id];
    var list = avility_detail[name];
    var n_list = list.length;
    if (n_list == 1){
        if(gold == 0){
            if(obj.className == 'btn btn-outline-primary get_avility'){
                obj.className = "btn btn-primary get_avility";
            }
            else{
                obj.className = 'btn btn-outline-primary get_avility';
            }
        }
        else{
            if(obj.className == 'btn btn-outline-warning get_avility'){
                obj.className = "btn btn-warning get_avility";
            }
            else{
                obj.className = 'btn btn-outline-warning get_avility';
            }
        }
    }
    else if(n_list == 2){
        if(gold == 0){
            if(obj.className == 'btn btn-outline-primary get_avility'){
                obj.value = list[0];
                obj.className = "btn btn-primary get_avility";
            }
            else if(obj.value == list[0]){
                obj.value = list[1];
            }
            else{
                obj.value = list[0];
                obj.className = 'btn btn-outline-primary get_avility';
            }
        }
        else{
            if(obj.className == 'btn btn-outline-primary get_avility'){
                obj.value = list[0];
                obj.className = "btn btn-primary get_avility";
            }
            else if(obj.value == list[0]){
                obj.value = list[1];
                obj.className = "btn btn-warning get_avility";
            }
            else{
                obj.value = list[0];
                obj.className = "btn btn-outline-primary get_avility";
            }
        }
    }
    else{
        if(obj.className == 'btn btn-outline-primary get_avility'){
            obj.value = list[0];
            obj.className = "btn btn-primary get_avility";
        }
        else if(obj.value == list[0]){
            obj.value = list[1];
            obj.className = "btn btn-primary get_avility";
        }
        else if(obj.value == list[1]){
            obj.value = list[2];
            obj.className = "btn btn-warning get_avility";
        }
        else{
            obj.value = list[0];
            obj.className = "btn btn-outline-primary get_avility";
        }
    }
}