修論実験用リポジトリ
====

グラフ構造を考慮したWord2VecやDock2Vecでの学習

## 機能

### D2Vクラス
* executeメソッド(@staticmethod)
- Doc2Vec学習モデルを生成
- libs/dock2vecs.py

### W2Vクラス
* executeメソッド(@staticmethod)
- Word2Vec学習モデルを生成
- libs/word2vecs.py

### Dockerfileクラス
- Dockerfileをナイーブに解析するオブジェクトを生成
- libs/dockerfiles.py

### Graphクラス
- グラフ構造を表現
- 追加予定機能
    - 命令列の後ろを考慮した構造の表現
- libs/graphs.py

### Primitiveクラス
- Dockerfileをprimitiveに解析
- 既存のインデントを用いて, 命令列ないの単語の重要度を表現
- libs/primitives.py

### Structureクラス
- toStackメソッド(@staticmethod)
-  インデントを考慮して階層構造を表現, 実装
- スタックを利用
- libs/structures.py



## モデル
### libs/delv/default-test-2021-12-05 01:45:27.835636.model
- binnacle-icse202を全て学習させたモデル


## 結果
### naiveなデータでの学習
* Dockerfileにあるレイヤごとの命令を配列として学習
- 入力データが"apt-get"と"install"だった時の結果
    ```bash
        (('+', 0.9916801452636719)
        ('{}', 0.9910140037536621)
        ('-not', 0.9847615957260132)
        ('*tkinter*', 0.9843180179595947)
        ('-executable', 0.9811577200889587)
        ('/usr/local', 0.9765851497650146)
        ('find', 0.9741872549057007)
        ('-exec', 0.9539327621459961)
        ('*.a', 0.9269841909408569)
        ('d', 0.9113402366638184))
    ```

### 前の命令+単語の重要度などを考慮したデータでの学習(少しグラフ構造)
* Dockerfile内のインデントを単語の重要度の尺度として利用
- 入力データが"apt-get"と"install"だった時の結果
    ```bash
        (('update', 0.9994246959686279)
        ('-y', 0.9989630579948425)
        ('--no-install-recommends', 0.9984796047210693)
        ('pkg-config', 0.9965482950210571)
        ('libc6-dev', 0.9931356906890869)
        ('git', 0.9850125312805176)
        ('--no-install-suggests', 0.9848350882530212)
        ('g++', 0.9822943210601807)
        ('build-essential', 0.9681098461151123))
    ```

### 前と後の命令+単語の重要度などを考慮したデータでの学習(少しグラフ構造)
* Dockerfile内のインデントを単語の重要度の尺度として利用
- 入力データが"apt-get"と"install"だった時の結果
    ```bash
        (('update', 0.9975267052650452)
        ('--no-install-recommends', 0.9973561763763428)
        ('-y', 0.9940279722213745)
        ('libc6-dev', 0.9882516264915466)
        ('pkg-config', 0.9873135089874268)  
        ('--no-install-suggests', 0.9772453904151917)
        ('g++', 0.976104736328125)
        ('ca-certificates', 0.961370587348938)
        ('gcc', 0.9584934711456299)
        ('dnf', 0.9575251340866089))
    ```

### インデントを考慮した記述の変換
* スタックを利用, インデントの構造をスタックに積んでいき, POPが行われるタイミングなどでオブジェクトのコピーを行う
- 変換例
    ```bash
        ----------------------------変換前----------------------------
        COPY scripts/sccache.sh /scripts/
        RUN set -ex; \
            \
            find /usr/local -depth \
                \( \
                    \( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
                    -o \
                    \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
                \) -exec rm -rf '{}' +; \
            rm -f get-pip.py
        
        ----------------------------変換後----------------------------
        ["COPY", "scripts/sccache.sh", "/scripts/"],
        ["RUN", "set", "-ex", "AND", "BACK"],
        ["RUN", "find", "/usr/local", "-depth"],
        ["RUN", "find", "/usr/local", "-depth", "-type", "d", "-a", "-name", "test", "-o", "-name", "tests",,,],
        ["RUN", "find", "/usr/local", "-depth", "-type", "d", "-a", "-name", "*.pyc",,,,],
        ["RUN", "rm", "-rf", "get-pip.py"]

    ```

### ファイルパスとレイヤ番号の情報を学習データに付与, Doc2Vecのタグとして利用
* 後で記述
- 付与例
    ```bash
        $FILE_PATH = "./debian-binnacle-icse2020/243133876.Dockerfile"

        FROM debian:buster-slim
        ENV PATH /usr/local/bin:$PATH
        ENV LANG C.UTF-8
        RUN set -eux; \
            apt-get update; \
            apt-get install -y --no-install-recommends \
                ca-certificates \
                netbase \
                tzdata \
            ; \
            rm -rf /var/lib/apt/lists/*
        ENV GPG_KEY E3FF2839C048B25C084DEBE9B26995E310250568
        ENV PYTHON_VERSION 3.9.7

    ```

    ```python
        {
            Hash("./debian-binnacle-icse2020/243133876.Dockerfile/0/0"): 
            [
                "FROM",
                "debian:buster-slim"
            ],
            ...
            Hash("./debian-binnacle-icse2020/243133876.Dockerfile/3/3"):
            [
                "apt-get",
                "install",
                "-y",
                "--no-install-recommends",
                "ca-certificates",
                "AND",
                "BACK"
            ] 
            ...
        }
    ```
### 5月12日用のメモ

* メモ
- コマンド集
    ```bash
    DBOWモデルトDMPVモデルの作成
    $ python3 main.py (ファイル内のD2Vのstaticmethoの引数を直接イジる)

    DBOWモデルを用いた結果, 取得できたコマンドのみメモ
    $ python3 create_res_file_dbow.py [ファイルのキー]
    $ ex. python3 create_res_file_dbow.py 260798842 

    DMPVモデルでも同様
    $ python3 create_res_file_dmpv.py [ファイルのキー]

    内容例:
    {
    "190111884:1:0": {
        "src_command": [
            "git",
            "clone",
            "-b",
            "DULL",
            ...
        ],
        "similar_datas": [
            {
                "sim_commands": [
                    "export",
                    "PATH",
                    "EQUAL",
                    ...
                ],
                "sim_value": 0.76941978931427
            },
            {
                "sim_commands": [
                    "git",
                    "clone",
                    "--depth",
                    "1",
                    ...
            },
            {
                "sim_commands": [
                    "git",
                    "clone",
                    "https",
                    "COLON",
                    "//github.com/datacenter/acitoolkit"
                ],
                "sim_value": 0.7324718832969666
            },
    }

    アソシエーション分析, DMPVでもDBOWでも一緒
    $ python3 apriori_dbow.py [コマンドのキー]
    $ python3 apriori_dbow.py 260798842:0:0
    $ python3 apriori_dmpv.py 260798842:0:0
    DMPV時間かかる.......

    作成されるのは, aprioriの結果とそれに対応するコマンド集

    内容例:
    apriori結果:
    ,support,itemsets
    0,1.0,frozenset({'--depth'})
    1,1.0,"frozenset({'-b', 'DULL', 'git', 'LEFT_BRACKET3', 'clone', 'CLONE_TAG', 'COLON'})"
    2,1.0,"frozenset({'-b', 'DULL', 'LEFT_BRACKET3', 'RIGHT_BRACKET3', 'https', 'clone', 'CLONE_TAG'})"
    3,1.0,"frozenset({'-b', 'DULL', 'git', 'LEFT_BRACKET3', 'RIGHT_BRACKET3', 'clone', 'CLONE_TAG'})"
    4,1.0,"frozenset({'-b', 'git', 'RIGHT_BRACKET3', 'https', 'clone', 'CLONE_TAG', 'COLON'})"
    5,1.0,"frozenset({'-b', 'git', 'LEFT_BRACKET3', 'https', 'clone', 'CLONE_TAG', 'COLON'})"
    6,1.0,"frozenset({'-b', 'git', 'LEFT_BRACKET3', 'RIGHT_BRACKET3', 'https', 'CLONE_TAG', 'COLON'})"
    7,1.0,"frozenset({'-b', 'LEFT_BRACKET3', 'RIGHT_BRACKET3', 'https', 'clone', 'CLONE_TAG', 'COLON'})"

    対応コマンド結果:
    {
    "src_command": [
        "git",
        "clone",
        "-b",
        "DULL",
        "LEFT_BRACKET3",
        "CLONE_TAG",
        "RIGHT_BRACKET3",
        "--depth",
        "1",
        "https",
        "COLON",
        "//github.com/BVLC/caffe.git",
        "."
    ],
    "dist_command": [
        [
            "git",
            "clone",
            "-b",
            "DULL",
            "LEFT_BRACKET3",
            "CLONE_TAG",
            "RIGHT_BRACKET3",
            "--depth",
            "1",
            "https",
            "COLON",
            "//github.com/BVLC/caffe.git",
            "."
        ],
        [
            "git",
            "clone",
            ...

    以上!!!

    ['apt-get', 'install', '-y', '--no-install-recommends', 'apt-transport-https', 'libxml2-dev', 'libcairo2-dev', 'libsqlite-dev', 'libmariadbd-dev', 'libmariadb-client-lgpl-dev', 'libpq-dev', 'libssh2-1-dev', 'libcurl4-openssl-dev', 'locales']
    ['apt-get', 'install', '--no-install-recommends', '-y', 'gcc', 'git', 'openssh-client', 'less', 'libxtst-dev', 'libxext-dev', 'libxrender-dev', 'libfreetype6-dev', 'libfontconfig1', 'libgtk2.0-0', 'libxslt1.1', 'libxxf86vm1']
    ['sudo', 'apt-get', 'install', '-q', '-y', 'cpanminus', 'vim', 'net-tools', 'git-email', 'telnet', 'screen', 'wget', 'less', 'curl', 'htop']
    ['apt-get', 'install', '-y', 'gawk', 'make', 'python', 'gcc', 'gcc-multilib', 'gettext', 'texinfo']
    ['apt-install', 'imagemagick', 'graphicsmagick', 'ghostscript', 'jpegoptim', 'libjpeg-turbo-progs', 'pngcrush', 'optipng', 'apngopt', 'pngnq', 'pngquant', 'libldap-2.4-2', 'libxslt1.1', 'zlibc', 'zlib1g', 'libpq5', 'libpng16-16', 'libmcrypt4', 'libzip4', 'libjpeg62-turbo-dev', 'libfreetype6-dev', 'libbz2-dev', 'libicu-dev', 'libldap2-dev', 'libldb-dev', 'libmcrypt-dev', 'libxml2-dev', 'libxslt1-dev', 'zlib1g-dev', 'libmemcached-dev', 'libpng-dev', 'libpq-dev', 'libzip-dev', 'libc-client-dev', 'libkrb5-dev']
    ['apt-get', 'install', '-y', 'libsnappy-dev', 'zlib1g-dev', 'libbz2-dev', 'libyaml-dev', 'libltdl-dev', 'libtool']
    ['apt-get', 'install', '-y', 'git', 'libyaml-dev', 'libssl-dev', 'libreadline-dev', 'libxml2-dev', 'libxslt1-dev', 'libffi-dev', 'build-essential']
    ['apt-get', 'install', '-y', 'gawk', 'make', 'python', 'gcc', 'gcc-multilib', 'gettext', 'texinfo']
    ['apt-get', 'install', '-y', 'libsnappy-dev', 'zlib1g-dev', 'libbz2-dev', 'libltdl-dev']
    ['apt-install', 'zip', 'unzip', 'bzip2', 'moreutils', 'dnsutils', 'openssh-client', 'rsync', 'git', 'patch']
    ['apt-get', 'install', '-y', 'vim', 'telnet', 'netcat', 'git-core', 'zip']

    ```