// ホストネームに含まれる文字列
host_name = 'pokemon-go-map.tokyo';

// コピーされたときのredirect先
redirect_millisec = 500;

// コピーされたときに表示するメッセージ
deny_message = '<h3 style="color: white">本ページは削除されました。(・ω<) ﾃﾍﾍﾟﾛ </h3>';
redirect_deny_url = $('meta[name=Identifier-URL]').attr("content");


function deny(){
    // ローカルなら動かさない
    if ($(location).attr('hostname') == '' || $(location).attr('hostname') == '127.0.0.1'){
        console.info('is local');
        return null;
    }

    // ホストが異なるなら実行
    if ($(location).attr('hostname').match(host_name)){
        // 正常
        //console.info('my site');
        return null;
    }else{
        // コピーサイト
        //console.info('copy site');
        disable();
    }
}

function disable(){
    console.info('start disable');
    // div.mainを書き換え
    $("div.container").html(deny_message);
    // N秒後にredirect
    setTimeout(function(){
        $(document).ready( function() {
            $(location).attr("href", redirect_deny_url);
        });
    },redirect_millisec);
}

$(deny);