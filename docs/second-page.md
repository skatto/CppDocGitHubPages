---
layout: default
title: 第二部・より効率よく, よいプログラムを書こう.
prev: first-page
next: third-page
---

## constによる定数

`const`修飾詞は変数の宣言時に型名の前に書くことで,
その変数を定数として扱うことができます.  
その場合, 宣言と同時に初期化する必要があります.  
`const`は意図しない解釈や, タイプミスによるバグを防ぐことができます.  

ただし, ポインタを扱う際は注意が必要で,

* `const 型名* 変数名`は`const`な変数のポインタ
* `型名* const 変数名`は変数の`const`なポインタ
* `const 型名* const 変数名`は`const`な変数の`const`なポインタ

となります.  

参照の場合は, `const 型名&`と言う様に`const`な参照を書くことができます.  
`const`な参照は書き換えることができず, 読み出しのみ行えます.

### 例文

```c++
int main()
{
    const float pi = 3.14;

    // pi = 3.0  <- これはエラー

    const float* p_pi = &pi;  // OK
    // float* const p_pi = &pi;  <- これはエラー
    const float* const p2_pi = &pi;  // OK

    float e = 2.7;

    p_pi = &e; // OK
    // p2_pi = &e  <- これはエラー, 定数なので書き換えられない.

    const float& r_e = e;

    std::cout << r_e << std::endl;  // 読める.
    // r_e += 1;  <- エラー, 書き込めない.

    return EXIT_SUCCESS;
}
```

大事な文法で, 変更しない変数には積極的に`const`修飾詞をつけるようにしましょう.
意図しない書き換えを防げます.

## const なメンバ関数

`const`修飾詞はクラスのメンバ関数にもつけることができますが,
`const`な変数とは意味は大きく違います.  
`const`なメンバ関数は,
そのクラスのインスタンスが`const`な変数だとしても呼び出せるようになります.  
(逆に言うと`const`なオブジェクトでは普通のメンバ変数は呼び出せません)  
その代わり, 当然`const`なメンバ関数ではメンバ変数を変更することはできません.

### 基本文法

```c++
型名 関数名(引数.. ) const {
    // 内容
}
```

### 例文

```c++
class A {
private:
    int a = 0;

public:
    int get() {
        return a;
    }

    int constGet() const {
        return a;
    }
};

int main()
{
    A not_const_a;

    not_const_a.get();  // OK
    not_const_a.constGet();  // OK

    const A const_a;

    // const_a.get();  <- エラー
    const_a.constGet();  // OK

    return EXIT_SUCCESS;
}
```

上記の通り`const`なオブジェクトでは普通のメンバ関数は使えなくなってしますので
メンバ変数を書き換えない関数ならば, 積極的に`const`をつけるようにしましょう.  

## 自動変数と静的変数

`static`修飾詞をつけることで, 静的変数を宣言することができます.  
静的変数はプログラムを通して消滅することがありません.  

変数の寿命を説明したところでは触れませんでしたが,
これを使うことで, ただの関数に"連続性"を持たせることが可能です.

### 例文

```c++
#include <iostream>

int counter() {
    static int count = 0;  // この初期化が呼び出されるのはプログラムの最初

    count += 1;
    return count;
}

int main()
{
    std::cout << counter() << std::endl;
    std::cout << counter() << std::endl;
    std::cout << counter() << std::endl;
    return EXIT_SUCCESS;
}
```
```:出力
1
2
3
```

一方, `auto`修飾子をつけることで, `static`でない, 普通の変数を宣言できますが,
のちに出てくる型推論の`auto`と混同するので, 省略しましょう.  

## 値渡し, 参照渡し

関数に引数を渡すときには色々な渡し方があります.  
どれがどのように動くかを注意して扱いましょう.

```c++
void function(int a, const int b, int& c, const int& d) {
    // 内容..
}

int main()
{
    int x, y, z, w;
    function(x, y, z, w);
}
```

は以下のように展開されます.

```c++
int main()
{
    int x, y, z, w;
    {
        int a = x;
        const int b = y;
        int& c = z;
        const int& d = w;

        // 内容..
    }
}
```

動きは見た通りなのですが,  
関数の内容の中で`c`を書き換えれば, 元の`z`も書き換わると言う点,  
`a`, `b`の生成にコピーコスト (時間的な話) がかかること,  
を注意しましょう.  

なので, ただの値を見るためだけの引数の場合は
`const`な参照 (上の`d`の方式) を使う様にしましょう.

## namespace

c++には名前空間という仕様があります.  
もし巨大なプログラムを書く場合に関数の名前やグローバル変数の名前が被ったら面倒です.  

パソコンの中のファイル構造を思い浮かべるとわかりやすいです.
同じ名前のファイルも別の場所にあれば違うファイルとして扱いますよね.   

* 基本文法

名前空間の定義

```c++
namespace 空間の名前 { ... }
```

名前空間`A`の中のものにアクセス

```c++
A::名前
```

* 例文

```c++
namespace myname {
  void say() {
    std::cout << "Foo!" << std::endl;
  }
}
void say() {
  std::cout << "Bar!" << std::endl;
}

int main()
{
  say();
  myname::say();
  
  return EXIT_SUCCESS;
}
```
```出力
Bar!
Foo!
```

以上のようにある名前空間が違えば全く別物となります.  
よく書く`std::`というのものも`std`という名前空間の内部にアクセスしているのです.  

## 右辺値, 左辺値

c++のコード中の値は右辺値と左辺値  
具体的に例を見てみましょう.  

## 右辺値参照, ムーブ

## もっとクラス コンストラクタ

## 例外処理

## 便利なマクロ

マクロはコンパイル時に解決（解釈）されるコードです.  


* `#if`
  

## ファイルを分ける

## ファイルの入出力

## 型テンプレート

## 変数テンプレート

## コマンドライン引数

## スマートポインタ

## autoによる型推論

## n. c++の配列

### 基本文型

#### std::array

使う場合はプログラムの冒頭に`#include <array>`と書く必要があります.

* 宣言

```c++
std::array<型名, 配列の長さ> 変数名;
```
配列の長さは自然数.

* 長さnの配列の値を設定しつつの宣言

```c++
std::array<型名, n> 変数名 = {変数1, 変数2, ... 変数n};
std::array<型名, n> 変数名{変数1, 変数2, ... 変数n};
std::array<型名, n> 変数名 = {{変数1, 変数2, ... 変数n}};
std::array<型名, n> 変数名{{変数1, 変数2, ... 変数n}};　// 全て同じ意味.
```

* i番目にアクセス(ただし0から数える)

```c++
変数名[i]
変数名.at(i)  // こちらの方が遅い.
```

#### std::vector

使う場合はプログラムの冒頭に`#include <vector>`と書く必要があります.  
アクセスは上の`std::array`の部分を`std::vector`に置き換える.

* 宣言

```c++
std::vector<型名> 変数名(配列の長さ);
```

* 値を設定しつつの宣言

```c++
std::vector<型名> 変数名 = {変数1, 変数2, ... 変数n};
std::vector<型名> 変数名{変数1, 変数2, ... 変数n};　// 上と同じ意味.
```

* 要素の追加

```c++
変数名.push_back(変数);
```

### 例文

* 16_1.cpp

```c++
#include <iostream>
#include <array>
#include <vector>

int main()
{
    int a[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};  //長さ10の配列を作成!
    // cスタイルの配列. 配列の長さは決め打ちでないといけない.
    std::array<int, 10> b;  // 長さ10の配列を作成!
    // c++スタイルの配列1. arrayの長さは決め打ちでないといけない.
    int length = 6;
    length += 4;
    std::vector<int> c(length - 3);  // 長さ7の配列を作成!
    // c++スタイルの配列2. vectorの長さはプログラムの実行中に決めて良い.

    std::cout << a[5] << std::endl;
    // 配列aの6番目にアクセス (0から数えるので)

    for (int i = 0; i < 10; i++) {
        b[i] = i * i;
    }

    for (int i = 0; i < 7; i++) {
        c[i] = i * i * i;
    }
    c.push_back(7 * 7 * 7);  // 配列に要素(7^3)を追加.
    c.push_back(8 * 8 * 8);  // 配列に要素(8^3)を追加.
    c.push_back(9 * 9 * 9);  // 配列に要素(9^3)を追加.

    return EXIT_SUCCESS;
}
```

## 並列処理

## 数学関数

## chrono

## constexpr

## 主なコンパイラオプション

## イテレータ

## もっとfor文

