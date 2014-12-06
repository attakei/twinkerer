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

conf.py に次の変数を追加します。

* twitter_consumer_key
* twitter_consumer_secret
* twitter_access_token_key
* twitter_access_token_secret


使い方
------

至極シンプルな使い方

.. code::

   $ twinker -p
   (output result generated rst-file)



参考リンク
----------

* http://tinkerer.me/
