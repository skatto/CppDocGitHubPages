---
layout: default
title: 演習の解答例.
date: 2018-05-22
---

## 1部の11.の演習問題

### 解答例

```c++
#include <iostream>
#include <vector>

using real = long long;

int main()
{
  std::vector<real> a = {1, 1};
  std::cout << "1 : 1" << std::endl << "2 : 1" << std::endl;
  for (int i = 3;; i++) {
    a.push_back(*(std::end(a) - 1) + *(std::end(a) - 2));
    if (a.back() < *(std::end(a) - 2)) {
      break;
    }
    std::cout << i << " : " << a.back() << std::endl;
  }

  return EXIT_SUCCESS;
}
```

## 1部の最後の演習問題

### 解答例

```c++
#include <iostream>
#include <stdexcept>

struct Pos {
  int x, y;
  Pos() {};
  Pos(int xx, int yy) {
    x = xx;
    y = yy;
  }
};

class Mine {
public:

  void init() {
    for (int i = 0; i < getSize(); i++) {
      for (int j = 0; j < getSize(); j++) {
        is_open[i][j] = false;
      }
    }
    for (int i = 0; i < getSize() + 2; i++) {
      for (int j = 0; j < getSize() + 2; j++) {
        bombs[i][j] = false;
      }
    }

    bombs[4][7] = true;
    bombs[3][6] = true;
    bombs[3][5] = true;
    bombs[3][3] = true;
    bombs[2][6] = true;
    bombs[3][9] = true;
    bombs[1][9] = true;
    bombs[7][3] = true;
  }

  void click(Pos appointed) {
    if (appointed.x >= getSize() or appointed.y >= getSize() or
        appointed.x < 0 or appointed.y < 0) {
      throw(std::runtime_error("invalid position."));
    }

    if (bombs[appointed.x + 1][appointed.y + 1]) {
      game_over = true;
    }
    else {
      openWindow(appointed);
    }
  }

  int getSize() { return 10; }

  bool isGameOver() { return game_over; }

  int getStatus(Pos pos) {
    if (is_open[pos.x][pos.y]) {
      return getBombNum(pos);
    }
    return -1;
  }

  bool getAnswer(Pos pos) { return bombs[pos.x + 1][pos.y + 1]; }

  bool isClear() {
    for (int i = 0; i < getSize(); i++) {
      for (int j = 0; j < getSize(); j++) {
        if (is_open[i][j] == bombs[i + 1][j + 1]) {
          return false;
        }
      }
    }
    return true;
  }

private:
  bool bombs[12][12];
  bool game_over;
  bool is_open[10][10];

  void roundPos(Pos pos, Pos out[8] ) {
    for (int i = 0; i < 4; i++){
      out[i].x = pos.x + i / 3 - 1;
      out[i].y = pos.y + i % 3 - 1;
    }
    for (int i = 4; i < 8; i++){
      out[i].x = pos.x + (i + 1) / 3 - 1;
      out[i].y = pos.y + (i + 1) % 3 - 1;
    }
  }

  int getBombNum(Pos pos) {
    Pos round[8];
    roundPos(pos, round);
    int n = 0;
    for (int i = 0; i < 8; i++) {
      n += int(bombs[round[i].x + 1][round[i].y + 1]);
    }
    return n;
  }

  void openWindow(Pos pos) {
    if (pos.x < 0 or pos.x >= getSize() or
        pos.y < 0 or pos.y >= getSize() or is_open[pos.x][pos.y]) {
      return;
    }
    is_open[pos.x][pos.y] = true;
    if (getBombNum(pos) == 0) {
      Pos round[8];
      roundPos(pos, round);
      for (int i = 0; i < 8; i++) {
        openWindow(round[i]);
      }
    }
  }
};

class MineManager {
public:
  void start() {
    mine.init();
    while (true) {
      showCurrent();

      while(true) {
        try {
          Pos appointed = getPos();

          std::cout << "check (" << appointed.x << ", " << appointed.y
                    << ")" << std::endl;

          mine.click(appointed);
          break;
        }
        catch (std::runtime_error e) {
          std::cout << e.what() << " please try again." << std::endl;
        }
      }

      if (mine.isGameOver()) {
        std::cout << "Game Over !" << std::endl;
        showAnswer();
        break;
      }
      if (mine.isClear()){
        std::cout << "Game Clear !" << std::endl;
        showAnswer();
        break;
      }
    }
  }

private:
  Mine mine;

  Pos getPos() {
    Pos input;
    std::cout << "input x coordinate : ";
    std::cin >> input.x;
    std::cout << "input y coordinate : ";
    std::cin >> input.y;
    if (!std::cin) {
      std::cin.clear();
      std::string line;
      std::getline(std::cin, line);
      throw(std::runtime_error("please input number."));
    }
    return input;
  }

  void showCurrent() {
    std::cout << "  ";
    for (int i = 0; i < mine.getSize(); i++) {
      std::cout << ' ' << i;
    }
    std::cout << std::endl;

    for (int i = 0; i < mine.getSize(); i++) {
      std::cout << i << " ";
      for (int j = 0; j < mine.getSize(); j++) {
        int status = mine.getStatus(Pos(j, i));
        if (status == -1) {
          std::cout << " _";
        }
        else {
          std::cout << ' ' << status;
        }
      }
      std::cout << std::endl;
    }
  }

  void showAnswer() {
    for (int i = 0; i < mine.getSize(); i++) {
      for (int j = 0; j < mine.getSize(); j++) {
        if (mine.getAnswer(Pos(j, i))) {
          std::cout << " x";
        }
        else {
          std::cout << " _";
        }
      }
      std::cout << std::endl;
    }
  }
};

int main()
{
  MineManager m;
  m.start();
}
```

二部の知識も多少使っていますが（例外など）, 使わずでもほぼ同じ実装ができます.
出力は実行して確かめてみてください.
