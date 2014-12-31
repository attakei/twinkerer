Tinkerer向けのツイートまとめポストを作ります
============================================

TwinkererはTinkerer上で自分のツイートまとめエントリーの作成をサポートするための拡張コマンドです。


インストール
------------

ソースをダウンロードしてインストールする

.. code::

   $ git clone https://github.com/attakei/twinkerer twinkerer
   $ cd twinkerer
   $ python setup.py install

pipを使用してインストールする

.. code::

   $ pip install tinkerer


設定
----

事前にtinkererのプロジェクトが作成されていることを前提にします。

Twitter Developers にて、事前にアプリケーションの作成を行います。
PermissionsはReadのみで十分です。

aconf.py に次の変数を追加します。

.. code-block:: python

   twitter_consumer_key = 'your_application_consumer_key'
   twitter_consumer_secret = 'your_application_consumer_secret'
   twitter_access_token_key = 'your_access_token'
   twitter_access_token_secret = 'your_access_token_secret'


使い方
------

至極シンプルな使い方

.. code::

   $ twinker -p
   (output result generated rst-file)

他の引数指定がない場合は、 **コマンド実行した日付** に **その前日7日分** のツイートをまとめてファイル出力します。

オプション例

.. code-block:: bash

   $ twinker --help
   usage: twinker [-h] [-f | -p] [--date POST_DATE] [--to TO_DATE] [--days DAYS]
                  [--conf [CONFIG_PATH]]

   optional arguments:
     -h, --help            ヘルプを表示する
     -f, --fetch           ポストの対象となるツイートを表示するだけのモード
     -p, --post            ポストを生成するモード
     --date POST_DATE      投稿予定日時を指定(指定がなければ、コマンド実行日を指定します)
     --to TO_DATE          ツイート取得対象の最終日(指定がなければ、コマンド実行日の前日を指定します)
     --days DAYS           ツイートの取得日数(指定がなければ、7日分を取得します)
     --conf [CONFIG_PATH]  Tinkererの設定ファイルパス(指定がなければ、カレントフォルダのconf.pyを選択します)


コマンド実行パターン
--------------------

.. code-block:: bash

   $ twinker --p --date 2014-01-09
   (2014年1月2日〜8日のまとめを2014年1月9日のポストとして作成)

   $ twinker --p --date 2014-02-01 --days 31
   (2014年1月のまとめを2014年2月1日のポストとして作成)

   $ twinker --p --date 2014-12-31 --to 2014-01-31 --days 31
   (2014年1月のまとめを年末のポストとして作成)

参考リンク
----------

* http://tinkerer.me/
