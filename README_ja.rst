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



参考リンク
----------

* http://tinkerer.me/
